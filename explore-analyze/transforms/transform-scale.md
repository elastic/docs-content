---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "{{transforms-cap}} at scale"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-scale.html
---

# Transforms at scale [transform-scale]

{{transforms-cap}} convert existing {{es}} indices into summarized indices, which provide opportunities for new insights and analytics. The search and index operations performed by {{transforms}} use standard {{es}} features so similar considerations for working with {{es}} at scale are often applicable to {{transforms}}. If you experience performance issues, start by identifying the bottleneck areas (search, indexing, processing, or storage) then review the relevant considerations in this guide to improve performance. It also helps to understand how {{transforms}} work as different considerations apply depending on whether or not your transform is running in continuous mode or in batch.

In this guide, you’ll learn how to:

* Understand the impact of configuration options on the performance of {{transforms}}.

**Prerequisites:**

These guildelines assume you have a {{transform}} you want to tune, and you’re already familiar with:

* [How {{transforms}} work](transform-overview.md).
* [How to set up {{transforms}}](transform-setup.md).
* [How {{transform}} checkpoints work in continuous mode](transform-checkpoints.md).

The following considerations are not sequential – the numbers help to navigate between the list items; you can take action on one or more of them in any order. Most of the recommendations apply to both continuous and batch {{transforms}}. If a list item only applies to one {{transform}} type, this exception is highlighted in the description.

The keywords in parenthesis at the end of each recommendation title indicates the bottleneck area that may be improved by following the given recommendation.

## Measure {{transforms}} performance [measure-performance]

In order to optimize {{transform}} performance, start by identifying the areas where most work is being done. The **Stats** interface of the **{{transforms-cap}}** page in {{kib}} contains information that covers three main areas: indexing, searching, and processing time (alternatively, you can use the [{{transforms}} stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-get-transform-stats)). If, for example, the results show that the highest proportion of time is spent on search, then prioritize efforts on optimizing the search query of the {{transform}}. {{transforms-cap}} also has [Rally support](https://esrally.readthedocs.io) that makes it possible to run performance checks on {{transforms}} configurations if it is required. If you optimized the crucial factors and you still experience performance issues, you may also want to consider improving your hardware.

## 1. Optimize `frequency` (index) [frequency]

In a {{ctransform}}, the `frequency` configuration option sets the interval between checks for changes in the source indices. If changes are detected, then the source data is searched and the changes are applied to the destination index. Depending on your use case, you may wish to reduce the frequency at which changes are applied. By setting `frequency` to a higher value (maximum is one hour), the workload can be spread over time at the cost of less up-to-date data.

## 2. Increase the number of shards of the destination index (index) [increase-shards-dest-index]

Depending on the size of the destination index, you may consider increasing its shard count. {{transforms-cap}} use one shard by default when creating the destination index. To override the index settings, create the destination index before starting the {{transform}}. For more information about how the number of shards affects scalability and resilience, refer to [Get ready for production](../../deploy-manage/index.md)

::::{tip}
Use the [Preview {{transform}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-preview-transform) to check the settings that the {{transform}} would use to create the destination index. You can copy and adjust these in order to create the destination index prior to starting the {{transform}}.
::::

## 3. Profile and optimize your search queries (search) [search-queries]

If you have defined a {{transform}} source index `query`, ensure it is as efficient as possible. Use the **Search Profiler** under **Dev Tools** in {{kib}} to get detailed timing information about the execution of individual components in the search request. Alternatively, you can use the [Profile](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-profile.html). The results give you insight into how search requests are executed at a low level so that you can understand why certain requests are slow, and take steps to improve them.

{{transforms-cap}} execute standard {{es}} search requests. There are different ways to write {{es}} queries, and some of them are more efficient than others. Consult [*Tune for search speed*](../../deploy-manage/production-guidance/optimize-performance/search-speed.md) to learn more about {{es}} performance tuning.

## 4. Limit the scope of the source query (search) [limit-source-query]

Imagine your {{ctransform}} is configured to group by `IP` and calculate the sum of `bytes_sent`. For each checkpoint, a {{ctransform}} detects changes in the source data since the previous checkpoint, identifying the IPs for which new data has been ingested. Then it performs a second search, filtered for this group of IPs, in order to calculate the total `bytes_sent`. If this second search matches many shards, then this could be resource intensive. Consider limiting the scope that the source index pattern and query will match.

To limit which historical indices are accessed, exclude certain tiers (for example `"must_not": { "terms": { "_tier": [ "data_frozen", "data_cold" ] } }` and/or use an absolute time value as a date range filter in your source query (for example, greater than 2024-01-01T00:00:00). If you use a relative time value (for example, gte now-30d/d) then ensure date rounding is applied to take advantage of query caching and ensure that the relative time is much larger than the largest of `frequency` or `time.sync.delay` or the date histogram bucket, otherwise data may be missed. Do not use date filters which are less than a date value (for example, `lt`: less than  or `lte`: less than or equal to) as this conflicts with the logic applied at each checkpoint execution and data may be missed.

Consider using [date math](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#api-date-math-index-names) in your index names to reduce the number of indices to resolve in your queries. Add a date pattern - for example, `yyyy-MM-dd` - to your index names and use it to limit your query to a specific date. The example below queries indices only from yesterday and today:

```js
  "source": {
    "index": [
        "<mydata-{now/d-1d{yyyy-MM-dd}}*>",
        "<mydata-{now/d{yyyy-MM-dd}}*>"
    ]
  },
```
%  NOTCONSOLE

## 5. Optimize the sharding strategy for the source index (search) [optimize-shading-strategy]

There is no one-size-fits-all sharding strategy. A strategy that works in one environment may not scale in another. A good sharding strategy must account for your infrastructure, use case, and performance expectations.

Too few shards may mean that the benefits of distributing the workload cannot be realised; however too many shards may impact your cluster health. To learn more about sizing your shards, read this [guide](../../deploy-manage/production-guidance/optimize-performance/size-shards.md).

## 6. Tune `max_page_search_size` (search) [tune-max-page-search-size]

The `max_page_search_size` {{transform}} configuration option defines the number of buckets that are returned for each search request. The default value is 500. If you increase this value, you get better throughput at the cost of higher latency and memory usage.

The ideal value of this parameter is highly dependent on your use case. If your {{transform}} executes memory-intensive aggregations – for example, cardinality or percentiles – then increasing `max_page_search_size` requires more available memory. If memory limits are exceeded, a circuit breaker exception occurs.

## 7. Use indexed fields in your source indices (search) [indexed-fields-in-source]

Runtime fields and scripted fields are not indexed fields; their values are only extracted or computed at search time. While these fields provide flexibility in how you access your data, they increase performance costs at search time. If {{transform}} performance using runtime fields or scripted fields is a concern, you may wish to consider using indexed fields instead. For performance reasons, we do not recommend using a runtime field as the time field that synchronizes a {{ctransform}}.

## 8. Use index sorting (search, process) [index-sorting-group-by-ordering]

Index sorting enables you to store documents on disk in a specific order which can improve query efficiency. The ideal sorting logic depends on your use case, but the rule of thumb may be to sort the fields in descending order (high to low cardinality) starting with the time-based fields. Index sorting can be defined only once at index creation. If you don’t already have index sorting on the index that you want to use as a source, consider reindexing it to a new, sorted index.

## 9. Disable the `_source` field on the destination index (storage) [disable-source-dest]

The [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) contains the original JSON document body that was passed at index time. The `_source` field itself is not indexed (and thus is not searchable), but it is still stored in the index and incurs a storage overhead. Consider disabling `_source` to save storage space if you have a large destination index. Disabling `_source` is only possible during index creation.

::::{note}
When the `_source` field is disabled, a number of features are not supported. Consult [Disabling the `_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#disable-source-field) to understand the consequences before disabling it.
::::

## Further reading [_further_reading]

* [*Tune for search speed*](../../deploy-manage/production-guidance/optimize-performance/search-speed.md)
* [*Tune for indexing speed*](../../deploy-manage/production-guidance/optimize-performance/indexing-speed.md)
* [*Size your shards*](../../deploy-manage/production-guidance/optimize-performance/size-shards.md)
* [Index lifecycle](../../manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md)
