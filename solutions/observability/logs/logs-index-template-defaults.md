---
navigation_title: Default `logs` index template
description: Learn what the default component templates and ingest pipeline hooks for logs do.
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
---

# Default `logs` index template

Elastic applies a managed index template to data streams that follow the `logs-*-*` index pattern. This index template references a set of reusable component templates and an optional `@custom` ingest pipeline that standardizes how log data streams are mapped, indexed, and preprocessed.

The managed `logs` index template has a priority of `100` and is automatically applied to any data stream following the `logs-*-*` index pattern, unless you override it with your own higher-priority index template.

By default, this index template also enables [LogsDB index mode](../../..//manage-data/data-store/data-streams/logs-data-stream.md), which optimizes storage and query performance for log data streams.

Depending on your deployment, the `logs` index template applies one of the following data retention policies by default:

* In {{stack}} (self-managed and {{ecloud}}): lifecycle is managed by [Index Lifecycle Management (ILM)](../../../manage-data/lifecycle/index-lifecycle-management.md). By default, rollover occurs when the primary shard reaches 50 GB or the index age reaches 30 days.
* In {{serverless-full}}: lifecycle is managed by [Data Stream Lifecycle (DSL)](../../../manage-data/lifecycle/data-stream.md). By default, logs are retained for 30 days. 

Refer to [Logs index template reference](logs-index-template-reference.md) for instructions on how to view or edit the logs index template in {{kib}}.

## Component templates

The managed `logs` index template is composed of the following component templates:

### `logs@mappings`

Provides general mappings for logs data streams:

* Disables automatic date detection for string fields to avoid mis-parsing.  
* Defines ECS `data_stream.*` fields:
  * [`data_stream.type`](ecs://reference/ecs-data_stream.md#field-data-stream-type): constant_keyword, value `logs`  
  * [`data_stream.dataset`](ecs://reference/ecs-data_stream.md#field-data-stream-dataset): constant_keyword, for example `nginx.access` (must be ≤ 100 characters, no `-`)
  * [`data_stream.namespace`](ecs://reference/ecs-data_stream.md#field-data-stream-namespace): constant_keyword, for example `production` (must be ≤ 100 characters, no `-`)

### `logs@settings`

Configures default index settings for logs data streams: 

  * References the managed ingest pipeline `logs@default-pipeline`, which:
    * Sets `@timestamp` to the ingest time if it is missing.  
    * Contains a hook to the optional [`logs@custom`](#customize-preprocessing-with-logscustom) pipeline.   
  * Sets `ignore_malformed` to `true` globally. With this setting, documents with malformed fields can be indexed without causing ingestion failures. Refer to [ignore_malformed](elasticsearch://reference/elasticsearch/mapping-reference/ignore-malformed.md) for a list of supported fields.
  * Sets `ignore_dynamic_beyond_limit` to `true`, which allows dynamically mapped fields to be added even when the total field limit is exceeded. Extra fields are ignored instead of causing ingestion to fail. Refer to [Mapping limit settings](elasticsearch://reference/elasticsearch/index-settings/mapping-limit.md) for more information.

### `ecs@mappings`

* Adds dynamic templates that automatically align fields with [Elastic Common Schema (ECS)](ecs://reference/index.md).  

Alignment with ECS helps ensure that dashboards, queries, and ML jobs can work consistently across different log sources.


## Customize preprocessing with `logs@custom`

Each logs data stream runs through the default ingest pipeline. However, you can use the `logs@custom` component template to customize your {{es}} indices. The `logs@custom` component template is not installed by default, but you can create a component template named `logs@custom` to override and extend default mappings or settings. Refer to [Edit the `logs` index template](../logs/logs-index-template-reference.md#custom-logs-template-edit) for more information.



## Using logs templates without naming conventions

If your logs data streams do not follow the `logs-*-*` naming scheme, the managed logs index template will not apply automatically.

You can still use the default component templates by adding them to your own index template. For example:

```json
PUT _index_template/my-logs-template
{
  "index_patterns": ["my-logs-template"],
  "composed_of": ["ecs@mappings", "logs@mappings", "logs@settings"],
  "priority": 200
}
```

::::{warning}
Avoid bypassing the `logs-*-*` naming scheme unless you have a specific need. Many {{kib}} features (such as Discover views and Logs ML jobs) expect the managed logs template.
::::