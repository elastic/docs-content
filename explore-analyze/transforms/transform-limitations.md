---
navigation_title: Limitations
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-limitations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# {{transforms-cap}} limitations [transform-limitations]

The following limitations and known problems apply to the {{version.stack}} release of the Elastic {{transform}} feature. The limitations are grouped into the following categories:

* [Configuration limitations](#transform-config-limitations) apply to the configuration process of the {{transforms}}.
* [Operational limitations](#transform-operational-limitations) affect the behavior of the {{transforms}} that are running.
* [Limitations in {{kib}}](#transform-ui-limitations) only apply to {{transforms}} managed via the user interface.

## Configuration limitations [transform-config-limitations]

### Field names prefixed with underscores are omitted from latest {{transforms}} [transforms-underscore-limitation]

If you use the `latest` type of {{transform}} and the source index has field names that start with an underscore (_) character, they are assumed to be internal fields. Those fields are omitted from the documents in the destination index.

### {{transforms-cap}} support {{ccs}} if the remote cluster is configured properly [transforms-ccs-limitation]

If you use [{{ccs}}](../../solutions/search/cross-cluster-search.md), the remote cluster must support the search and aggregations you use in your {{transforms}}. {{transforms-cap}} validate their configuration; if you use {{ccs}} and the validation fails, make sure that the remote cluster supports the query and aggregations you use.

### Using scripts in {{transforms}} [transform-painless-limitation]

{{transforms-cap}} support scripting in every case when aggregations support them. However, there are certain factors you might want to consider when using scripts in {{transforms}}:

* {{transforms-cap}} cannot deduce index mappings for output fields when the fields are created by a script. In this case, you might want to create the mappings of the destination index yourself prior to creating the transform.
* Scripted fields may increase the runtime of the {{transform}}.
* {{transforms-cap}} cannot optimize queries when you use scripts for all the groupings defined in `group_by`, you will receive a warning message when you use scripts this way.

### Deprecation warnings for Painless scripts in {{transforms}} [transform-painless-warning-limitation]

If a {{transform}} contains Painless scripts that use deprecated syntax, deprecation warnings are displayed when the {{transform}} is previewed or started. However, it is not possible to check for deprecation warnings across all {{transforms}} as a bulk action because running the required queries might be a resource intensive process. Therefore any deprecation warnings due to deprecated Painless syntax are not available in the Upgrade Assistant.

### {{transforms-cap}} perform better on indexed fields [transform-runtime-field-limitation]

{{transforms-cap}} sort data by a user-defined time field, which is frequently accessed. If the time field is a [runtime field](../../manage-data/data-store/mapping/runtime-fields.md), the performance impact of calculating field values at query time can significantly slow the {{transform}}. Use an indexed field as a time field when using {{transforms}}.

### {{ctransform-cap}} scheduling limitations [transform-scheduling-limitations]

A {{ctransform}} periodically checks for changes to source data. The functionality of the scheduler is currently limited to a basic periodic timer which can be within the `frequency` range from 1s to 1h. The default is 1m. This is designed to run little and often. When choosing a `frequency` for this timer consider your ingest rate along with the impact that the {{transform}} search/index operations has other users in your cluster. Also note that retries occur at `frequency` interval.

## Operational limitations [transform-operational-limitations]

### Aggregation responses may be incompatible with destination index mappings [transform-aggresponse-limitations]

When a pivot {{transform}} is first started, it will deduce the mappings required for the destination index. This process is based on the field types of the source index and the aggregations used. If the fields are derived from [`scripted_metrics`](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md) or [`bucket_scripts`](elasticsearch://reference/aggregations/search-aggregations-pipeline-bucket-script-aggregation.md), [dynamic mappings](../../manage-data/data-store/mapping/dynamic-mapping.md) will be used. In some instances the deduced mappings may be incompatible with the actual data. For example, numeric overflows might occur or dynamically mapped fields might contain both numbers and strings. Check {{es}} logs if you think this may have occurred.

You can view the deduced mappings by using the [preview transform API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-preview-transform). See the `generated_dest_index` object in the API response.

If it’s required, you may define custom mappings prior to starting the {{transform}} by creating a custom destination index using the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create). As deduced mappings cannot be overwritten by an index template, use the create index API to define custom mappings. The index templates only apply to fields derived from scripts that use dynamic mappings.

### Batch {{transforms}} may not account for changed documents [transform-batch-limitations]

A batch {{transform}} uses a [composite aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-composite-aggregation.md) which allows efficient pagination through all buckets. Composite aggregations do not yet support a search context, therefore if the source data is changed (deleted, updated, added) while the batch {{dataframe}} is in progress, then the results may not include these changes.

### {{ctransform-cap}} consistency does not account for deleted or updated documents [transform-consistency-limitations]

While the process for {{transforms}} allows the continual recalculation of the {{transform}} as new data is being ingested, it does also have some limitations.

Changed entities will only be identified if their time field has also been updated and falls within the range of the action to check for changes. This has been designed in principle for, and is suited to, the use case where new data is given a timestamp for the time of ingest.

If the indices that fall within the scope of the source index pattern are removed, for example when deleting historical time-based indices, then the composite aggregation performed in consecutive checkpoint processing will search over different source data, and entities that only existed in the deleted index will not be removed from the {{dataframe}} destination index.

Depending on your use case, you may wish to recreate the {{transform}} entirely after deletions. Alternatively, if your use case is tolerant to historical archiving, you may wish to include a max ingest timestamp in your aggregation. This will allow you to exclude results that have not been recently updated when viewing the destination index.

### Deleting a {{transform}} does not delete the destination index or {{kib}} index pattern [transform-deletion-limitations]

When deleting a {{transform}} using `DELETE _transform/index` neither the destination index nor the {{kib}} index pattern, should one have been created, are deleted. These objects must be deleted separately.

### Handling dynamic adjustment of aggregation page size [transform-aggregation-page-limitations]

During the development of {{transforms}}, control was favoured over performance. In the design considerations, it is preferred for the {{transform}} to take longer to complete quietly in the background rather than to finish quickly and take precedence in resource consumption.

Composite aggregations are well suited for high cardinality data enabling pagination through results. If a [circuit breaker](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md) memory exception occurs when performing the composite aggregated search then we try again reducing the number of buckets requested. This circuit breaker is calculated based upon all activity within the cluster, not just activity from {{transforms}}, so it therefore may only be a temporary resource availability issue.

For a batch {{transform}}, the number of buckets requested is only ever adjusted downwards. The lowering of value may result in a longer duration for the {{transform}} checkpoint to complete. For {{ctransforms}}, the number of buckets requested is reset back to its default at the start of every checkpoint and it is possible for circuit breaker exceptions to occur repeatedly in the {{es}} logs.

The {{transform}} retrieves data in batches which means it calculates several buckets at once. Per default this is 500 buckets per search/index operation. The default can be changed using `max_page_search_size` and the minimum value is 10. If failures still occur once the number of buckets requested has been reduced to its minimum, then the {{transform}} will be set to a failed state.

### Handling dynamic adjustments for many terms [transform-dynamic-adjustments-limitations]

For each checkpoint, entities are identified that have changed since the last time the check was performed. This list of changed entities is supplied as a [terms query](elasticsearch://reference/query-languages/query-dsl/query-dsl-terms-query.md) to the {{transform}} composite aggregation, one page at a time. Then updates are applied to the destination index for each page of entities.

The page `size` is defined by `max_page_search_size` which is also used to define the number of buckets returned by the composite aggregation search. The default value is 500, the minimum is 10.

The index setting [`index.max_terms_count`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-settings) defines the maximum number of terms that can be used in a terms query. The default value is 65536. If `max_page_search_size` exceeds `index.max_terms_count` the {{transform}} will fail.

Using smaller values for `max_page_search_size` may result in a longer duration for the {{transform}} checkpoint to complete.

### Handling of failed {{transforms}} [transform-failed-limitations]

Failed {{transforms}} remain as a persistent task and should be handled appropriately, either by deleting it or by resolving the root cause of the failure and re-starting.

When using the API to delete a failed {{transform}}, first stop it using `_stop?force=true`, then delete it.

### {{ctransforms-cap}} may give incorrect results if documents are not yet available to search [transform-availability-limitations]

After a document is indexed, there is a very small delay until it is available to search.

A {{ctransform}} periodically checks for changed entities between the time since it last checked and `now` minus `sync.time.delay`. This time window moves without overlapping. If the timestamp of a recently indexed document falls within this time window but this document is not yet available to search then this entity will not be updated.

If using a `sync.time.field` that represents the data ingest time and using a zero second or very small `sync.time.delay`, then it is more likely that this issue will occur.

### Support for date nanoseconds data type [transform-date-nanos]

If your data uses the [date nanosecond data type](elasticsearch://reference/elasticsearch/mapping-reference/date_nanos.md), aggregations are nonetheless on millisecond resolution. This limitation also affects the aggregations in your {{transforms}}.

### Data streams as destination indices are not supported [transform-data-streams-destination]

{{transforms-cap}} update data in the destination index which requires writing into the destination. [Data streams](../../manage-data/data-store/data-streams.md) are designed to be append-only, which means you cannot send update or delete requests directly to a data stream. For this reason, data streams are not supported as destination indices for {{transforms}}.

### ILM as destination index may cause duplicated documents [transform-ilm-destination]

[ILM](../../manage-data/lifecycle/index-lifecycle-management.md) is not recommended to use as a {{transform}} destination index. {{transforms-cap}} update documents in the current destination, and cannot delete documents in the indices previously used by ILM. This may lead to duplicated documents when you use {{transforms}} combined with ILM in case of a rollover.

If you use ILM to have time-based indices, consider using the [Date index name](elasticsearch://reference/enrich-processor/date-index-name-processor.md) instead. The processor works without duplicated documents if your {{transform}} contains a `group_by` based on `date_histogram`.

### SLO transforms at scale may misreport state and increase PIT activity

When running a large number of SLO {{transforms}}, two types of limitations can appear:

- {{transforms-cap}} may [misreport](#transforms-inaccurate-errors) their state and suggest deletion even though they are still valid
- Point-in-time (PIT) requests may [accumulate](#transforms-pit-overloads), creating extra activity on the cluster and slowing down operations

#### {{transforms-cap}} can return inaccurate errors that suggest deletion [transforms-inaccurate-errors]

The {{transforms-cap}} API and the {{transforms-cap}} management page in {{kib}} may display misleading error messages for {{transforms}} created by service level objectives (SLOs).

The message typically reads:

```console
Found task for transform [...], but no configuration for it. To delete this transform use DELETE with force=true.
```
Although the error suggests that the {{transform}} is broken and should be deleted, this is usually not the case. The error occurs because of a limitation in how the {{transforms}} are queried and presented by the API and UI. Deleting the {{transform}} can break related SLOs.

If you encounter this error, do not delete the {{transform}}. If a {{transform}} was already deleted, you can restore it by resetting the SLO, either in the {{kib}} or with the API:

- In {{kib}}, go to the **Observability** > **SLOs application**, open the menu for the affected SLO, and click **Reset**. 

- If you use the API, run the following request:

  ```console
  POST kbn:/api/observability/slos/<SLO_ID>/_reset
  ```

#### Large numbers of {{transform}} can cause PIT overloads [transforms-pit-overloads]

{{transforms-cap}} rely on point-in-time (PIT) searches to ensure that queries remain consistent during data changes. Each {{transform}} can open and close multiple PITs during its lifetime. 

When many {{transforms}} run concurrently, especially in environments with large numbers of SLOs (hundreds to more than a thousand transforms), PITs can be opened and closed in quick succession. Because PITs are closed asynchronously, the close operation does not wait for the previous request to complete. This can create a backlog of PIT close requests, known as a PIT overload.

A PIT overload increases the memory pressure on hot nodes. This may result in rising memory usage and long garbage collection cycles. In practice, searches and writes may slow down or queue until the node recovers, and in severe cases a restart may be required.

As a workaround, you can disable PIT for a specific {{transform}}:

```console
POST _transform/<transform_id>/_update
{
  "settings": {
    "use_point_in_time": false
  }
}
```

To fix this issue permanently, upgrade to the following versions or later: 8.18.8, 8.19.5, 9.0.8, 9.1.5, or 9.2.0.

## Limitations in {{kib}} [transform-ui-limitations]

### {{transforms-cap}} are visible in all {{kib}} spaces [transform-space-limitations]

[Spaces](../../deploy-manage/manage-spaces.md) enable you to organize your source and destination indices and other saved objects in {{kib}} and to see only the objects that belong to your space. However, a {{transform}} is a long running task which is managed on cluster level and therefore not limited in scope to certain spaces. Space awareness can be implemented for a {{data-source}} under **Stack Management > Kibana** which allows privileges to the {{transform}} destination index.

### Up to 1,000 {{transforms}} are listed in {{kib}} [transform-kibana-limitations]

The {{transforms}} management page in {{kib}} lists up to 1000 {{transforms}}.

### {{kib}} might not support every {{transform}} configuration option [transform-ui-support]

There might be configuration options available via the {{transform}} APIs that are not supported in {{kib}}. For an exhaustive list of configuration options, refer to the [documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-transform).
