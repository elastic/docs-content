---
navigation_title: Timestamp data quality
description: "Detect, investigate, and resolve timestamp data quality issues that can cause unexpected behavior."
type: troubleshooting
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Troubleshoot timestamp data quality issues [fix-date-timestamps]

In {{es}} date fields, you can use any valid past, present, or future date as the value, as long as it matches the field's [date format](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md).

Make sure your stored date fields are valid. When ensuring timestamp accuracy, you might encounter these common client-side data quality issues:

* Operating system timezone setting conflicts
* Incorrectly formatted date values
* Unexpected values for the specific date field, for example:
    * future dates that don't make sense for the data
    * default dates, such as the `1970` [Unix epoch](https://en.wikipedia.org/wiki/Unix_time)
    * negative dates
    * time-bucketed dates
    * truncated strings

This page summarizes the symptoms of these issues and helps you address them, focusing on unexpected future dates in the `@timestamp` field. 

:::{tip}
When possible, make sure to resolve timestamp data quality issues in the data itself, rather than working around them in {{es}}.
:::

## Symptoms [fix-date-timestamps-symptoms]

Timestamp data quality issues can strain resources and cause unexpected search results. They can especially affect the following features:

* [Discover](/explore-analyze/discover.md)
* [Dashboards](/explore-analyze/dashboards.md)
* {{elastic-sec}} [detections and alerts](/solutions/security/detect-and-alert.md)
* {{observability}} [incident management alerts](/solutions/observability/incident-management/alerting.md)
* [{{kib}} alerting](/explore-analyze/alerting/alerts.md)
* [Watchers](/explore-analyze/alerting/watcher.md)

Common symptoms of these issues include:

* Later [data tiers](/manage-data/lifecycle/data-tiers.md) have a [search queue backlog](/troubleshoot/elasticsearch/task-queue-backlog.md#diagnose-task-queue-thread-pool), but not on `data_hot`.
* The `data_frozen` data tier shows ongoing [high CPU usage](/troubleshoot/elasticsearch/high-cpu-usage.md).
* [Slow logs](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) report events for `data_cold` or `data_frozen` on short, periodic intervals.
* In {{kib}}, [Inspect](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load#3.-load-search) reports search results from unexpected indices.
* Indices based on {{ls}} [date math syntax](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-index) or the {{es}} [Date index name processor](elasticsearch://reference/enrich-processor/date-index-name-processor.md) refer to dates far into the past or future.

:::{tip}
You can [reduce the performance impact](#fix-date-timestamps-recommendations) of these issues even when the underlying timestamp data quality problems still exist.
:::

### Example [fix-date-timestamps-example]

Here's an example that illustrates how timestamp data quality issues can affect the search performance of your cluster. Suppose a single on-prem host has a misconfigured system clock, causing its `@timestamp` field to log timestamps one year in the future. In this example:

- Host data ingests into an {{es}} [data stream](/manage-data/data-store/data-streams.md) with five [primary shards](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-number-of-shards). 
- The data stream powers a [dashboard](/explore-analyze/dashboards.md), which uses a [data view](/explore-analyze/find-and-organize/data-views.md) with `@timestamp` as the time field.
- The data stream has an [index lifecycle management (ILM) policy](/manage-data/lifecycle/index-lifecycle-management.md) that guarantees it [rolls over indices](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) at least once a day and [migrates data to the frozen tier](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-actions) after 15 days. 

After 30 days, there are 150 shards, half of them hosted in the frozen tier.

#### Scenario 1: No data ingested by misconfigured host

If the misconfigured host didn't ingest data during the 30-day period, the following issues can occur when a user selects a `now-15m` [time window](/explore-analyze/dashboards/using.md#_set_a_time_range) in the dashboard:

1. The [search pre-filter]({{es-apis}}operation/operation-msearch) shows only the five shards from the latest backing index.
1. Data is [read](/deploy-manage/distributed-architecture/reading-and-writing-documents.md#_basic_read_model) from the latest five shards only, and the remaining search [queries](/explore-analyze/query-filter.md) and [aggregations](/explore-analyze/query-filter/aggregations.md) run on that subset of data.
1. [Inspect](/troubleshoot/observability/inspect.md) reports 5 shards searched and 145 shards `skipped`.

#### Scenario 2: Data ingested by misconfigured host

If the misconfigured host was ingesting data during the 30-day period, the following issues can occur:

1. The pre-filter can't filter out backing indices, so it allows searches against all 150 shards backing this data stream.
1. Half of the shards are in the `data_frozen` data tier, which is intended for [rarely queried data](/manage-data/lifecycle/data-tiers.md). The frozen tier is usually provisioned with low CPU relative to high data volume, so searches run slower. Additionally, in the frozen tier, indices are [partially mounted searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), which slows down searches because data must be fetched from the snapshot repository.
1. The cluster searches all 150 shards for timestamps within the desired window. This resource usage can happen even if no documents end up matching the selected time range.
1. [Inspect](/troubleshoot/observability/inspect.md) reports 150 shards searched and 0 `skipped`.

In both scenarios, search is more computationally expensive and can return incorrect results because of the host's misconfigured timestamps. The next section explains how to investigate the scope of a timestamp data quality issue.

## Investigate timestamp data quality [fix-date-timestamps-investigate]

Timestamp data quality issues can be difficult to notice if they're not actively causing performance strain. For best results, make sure you're familiar with the typical patterns and expected trends in your data (also referred to as "seasonal patterns"), so you can spot anomalies.

To check for date values far into the past or future, you can use the following options:

* To review [partially mounted searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md#searchable-snapshot-mount-storage-options) and their `@timestamp` date field only, use a [cluster state request]({{es-apis}}operation/operation-cluster-state):

    ```console
    GET _cluster/state?filter_path=metadata.indices.*.timestamp_range
    ```

    To filter and format the results, you can use third-party tools such as [jq](https://jqlang.github.io/jq/manual/). For example, to see a list of indices with a maximum timestamp in the future:

    ```sh
    cat cluster_state.json | jq -cMr '.metadata.indices| to_entries| sort_by(.key)| .[]| .value.timestamp_range as $ts| select($ts.min)| {min:($ts.min/1000.0 | todate),max:($ts.max/1000.0 | todate), index:.key}' | jq -r --arg now "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" 'select(.max > $now)'
    ```

* To list the top 200 [aggregated](/explore-analyze/query-filter/aggregations.md) indices by the number of documents whose timestamps are in the future, use a search request:

    ```console
    GET */_search
    { "size": 0,
      "aggs": { "0": {
        "terms": {
          "field": "_index",
          "order": { "_count": "desc" },
          "size": 200
        }}
      },
      "query": {
        "bool": {
          "filter": [ { "range": { "@timestamp": { "gte": "now" }}}]
        }
      }
    }
    ```

* To list individual indices' minimum and maximum timestamps, use a search request.

    ::::{warning}
    This search can be resource-intensive, depending on your search target scope and the hardware profiles of nodes hosting related shards.
    ::::

    ```console
    GET my_datastream/_search
    { "size": 0,
      "aggs": { "2": {
        "aggs": {
          "min": {"min": {"field": "@timestamp"} },
          "max": {"max": {"field": "@timestamp"} }
        },
        "terms": {
          "field": "_index",
          "order": {"_key": "asc"},
          "size": 200
        }
      }}
    }
    ```

If you find future dates, check for patterns in the data distribution:

```console
GET my_datastream/_search?filter_path=aggregations
{ "size": 0,
  "query": {
    "bool": {
      "filter": [ { "range": { "@timestamp": { "gte": "now" }}}]
    }
  },
  "aggs": {
    "time_buckets": {
      "auto_date_histogram": {
        "field": "@timestamp",
        "buckets": 30,
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

The rest of this page explains how to [reduce the performance impact](#fix-date-timestamps-recommendations) of these issues and [clean up](#fix-date-timestamps-cleanup) problematic data.

## Reduce performance impact [fix-date-timestamps-recommendations]

Even when timestamp data quality issues remain in your data, you can reduce their performance impact by adjusting how scheduled tasks and searches run.

### Default date field [fix-date-timestamps-defaults]

[Time series data](/manage-data/lifecycle.md) is frequently searched by date field, and the most common date field is [`@timestamp`](ecs://reference/ecs-base.md). By default, this field's value reflects when the event **originated,** as reported by the source. This is the default date field when creating a [data view](/explore-analyze/find-and-organize/data-views.md). Discover and Dashboard objects use data views to [resolve]({{es-apis}}operation/operation-indices-resolve-index) and search data.

For scheduled tasks that run without user interaction, consider searching on the [`event.ingested`](ecs://reference/ecs-event.md) date field instead of `@timestamp`. By default, this field's value reflects when the event was **ingested** into the cluster. If `event.ingested` isn't already populated, refer to [Troubleshoot ingest pipelines](/troubleshoot/elasticsearch/troubleshoot-ingest-pipelines.md) to add the field to your data with a custom [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md).

These common scheduled tasks benefit from using `event.ingested`:

* [Transforms](/explore-analyze/transforms.md)
* [Machine Learning](/explore-analyze/machine-learning.md)
* [{{kib}} alerting](/explore-analyze/alerting/alerts.md)
* [Watchers](/explore-analyze/alerting/watcher.md)

The `event.ingested` approach is recommended for [{{elastic-sec}} data sources](/solutions/security/detect-and-alert/set-rule-data-sources.md#best-practices) and is commonly used in [{{observability}} rules](/solutions/observability/incident-management/create-manage-rules.md#observability-create-manage-rules-observability-rules).

For {{elastic-sec}} [detection rules](/solutions/security/detect-and-alert.md), also consider enabling the advanced setting that ensures `@timestamp` is not used as a [fallback for timestamp overrides](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params).

### {{kib}} data source settings [fix-date-timestamps-flags]

You can use these {{kib}} [advanced settings](kibana://reference/advanced-settings.md) to exclude the `data_cold` and `data_frozen` [data tiers](/manage-data/lifecycle/data-tiers.md) from searches:

* `data_views:fields_excluded_data_tiers` for all [data views](/explore-analyze/find-and-organize/data-views.md)
* `observability:searchExcludedDataTiers` for [{{observability}}](/solutions/observability.md)
* For [Security](/solutions/security.md):
    * `securitySolution:excludedDataTiersForRuleExecution`
    * `securitySolution:excludeColdAndFrozenTiersInPrevalence`
    * `securitySolution:excludeColdAndFrozenTiersInAnalyzer`

    :::{tip}
    For guidance specific to {{elastic-sec}}, refer to [Exclude cold and frozen tiers from rule execution](/solutions/security/detect-and-alert/set-rule-data-sources.md#exclude-cold-frozen-tier).
    :::

### Data tier filters [fix-date-timestamps-tier]

You can also use a Query DSL [boolean query](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) filter out specific [data tiers](/manage-data/lifecycle/data-tiers.md). Filtering with a [query string query](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md) is insufficient.

For example, you can filter out `data_cold` and `data_frozen` with the following boolean query:

```json
{
   "bool":{
      "must_not":{
         "terms":{
            "_tier":[ "data_cold", "data_frozen" ]
         }
      }
   }
}
```

## Clean up timestamp data [fix-date-timestamps-cleanup]

After investigating timestamp data quality and reviewing best practices, clean up any issues by deleting or modifying the problematic data.

### Delete problematic data [fix-date-timestamps-cleanup-delete]

To remove invalid data, use one of these methods:

* [Delete the index]({{es-apis}}operation/operation-indices-delete) or [delete the data stream]({{es-apis}}operation/operation-indices-delete-data-stream). For [searchable snapshot indices](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), consider whether to also [delete their associated snapshots]({{es-apis}}operation/operation-snapshot-delete).

* Use an index [delete by query]({{es-apis}}operation/operation-delete-by-query) request. For example, to remove documents with future dates:

    ```console
    POST my_index/_delete_by_query
    {
      "query": {
        "range": {
          "@timestamp": {
            "gt": "now"
          }
        }
      }
    }
    ```

### Modify problematic data [fix-date-timestamps-cleanup-modify]

The following example steps modify invalid data by updating the `@timestamp` field to the current time:

1. Create an [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) that sets the `@timestamp` date field to the current timestamp:

    ```console
    PUT _ingest/pipeline/update_date
    {
      "processors": [
        {
          "rename": {
            "description": "(Optional) Cache the previous timestamp in a new field",
            "field": "@timestamp",
            "target_field": "old_timestamp"
          }
          ,
          "set": {
            "description": "Override the @timestamp value to the ingested time",
            "field": "_source.@timestamp",
            "value": "{{_ingest.timestamp}}"
          }
        }
      ]
    }
    ```

1. Run the data through the new pipeline to modify the value, using one of these approaches:

    * To modify the value across the entire index, [reindex]({{es-apis}}operation/operation-reindex) to a new index.

        ```console
        POST _reindex
        {
          "source": {
            "index": ["my-index-000001", "my-index-000002"]
          },
          "dest": {
            "index": "my-new-index-000001",
            "pipeline": "update_date"
          }
        }
        ```

    * To target specific documents, use an [update by query]({{es-apis}}operation/operation-update-by-query) request within the existing index.

        ```console
        POST my_index/_update_by_query?pipeline=update_date
        {
          "query": {
            "range": {
              "@timestamp": {
                "gt": "now"
              }
            }
          }
        }
        ```
        
:::{tip}
To modify documents in a [searchable snapshot index](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), you must first [restore it to a regular index](/manage-data/lifecycle/data-tiers/manage-data-tiers-ech-ece.md#searchable-snapshot-data-tier).
:::
