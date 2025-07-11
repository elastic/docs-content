---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logs-data-stream.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Logs data stream [logs-data-stream]

::::{important}
The {{es}} `logsdb` index mode is generally available in Elastic Cloud Hosted and self-managed Elasticsearch as of version 8.17, and is enabled by default for logs in [{{serverless-full}}](https://www.elastic.co/elasticsearch/serverless).
::::


A logs data stream is a data stream type that stores log data more efficiently.

In benchmarks, log data stored in a logs data stream used ~2.5 times less disk space than a regular data stream, at a small (10-20%) penalty in indexing performance. The exact impact varies by data set and Elasticsearch version.


## Create a logs data stream [how-to-use-logsds]

::::{important}
Fleet integrations use [index templates](../templates.md) managed by Elastic. To modify these backing templates, update their [composite `custom` templates](/solutions/observability/logs/logs-index-template-reference.md##custom-logs-template-edit).
::::

To create a logs data stream, set your [template](../templates.md) `index.mode` to `logsdb`:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-datastream-*"],
  "data_stream": { },
  "template": {
     "settings": {
        "index.mode": "logsdb" <1>
     }
  },
  "priority": 101 <2>
}
```

1. The index mode setting.
2. The index template priority. By default, Elasticsearch ships with a `logs-*-*` index template with a priority of 100. To make sure your index template takes priority over the default `logs-*-*` template, set its `priority` to a number higher than 100. For more information, see [Avoid index pattern collisions](../templates.md#avoid-index-pattern-collisions).


After the index template is created, new indices that use the template will be configured as a logs data stream. You can start indexing data and [using the data stream](use-data-stream.md).

You can also set the index mode and adjust other template settings in [the Elastic UI](/manage-data/data-store/index-basics.md#index-management-manage-index-templates).


## Synthetic source [logsdb-synthetic-source]

If you have the required [subscription](https://www.elastic.co/subscriptions), `logsdb` index mode uses [synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source), which omits storing the original `_source` field. Instead, the document source is synthesized from doc values or stored fields upon document retrieval.

If you don’t have the required [subscription](https://www.elastic.co/subscriptions), `logsdb` mode uses the original `_source` field.

Before using synthetic source, make sure to review the [restrictions](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source-restrictions).

When working with multi-value fields, the `index.mapping.synthetic_source_keep` setting controls how field values are preserved for [synthetic source](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source) reconstruction. In `logsdb`, the default value is `arrays`, which retains both duplicate values and the order of entries. However, the exact structure of array elements and objects is not necessarily retained. Preserving duplicates and ordering can be critical for some log fields, such as DNS A records, HTTP headers, and log entries that represent sequential or repeated events.


## Index sort settings [logsdb-sort-settings]

In `logsdb` index mode, indices are sorted by the fields `host.name` and `@timestamp` by default.

* If the `@timestamp` field is not present, it is automatically injected.
* If the `host.name` field is not present, it is automatically injected as a `keyword` field, if possible.

    * If `host.name` can’t be injected (for example, `host` is a keyword field) or can’t be used for sorting (for example, its value is an IP address), only the `@timestamp` is used for sorting.
    * If `host.name` is injected and `subobjects` is set to `true` (default), the `host` field is mapped as an object field named `host` with a `name` child field of type `keyword`. If `subobjects` is set to `false`, a single `host.name` field is mapped as a `keyword` field.

* To prioritize the latest data, `host.name` is sorted in ascending order and `@timestamp` is sorted in descending order.

You can override the default sort settings by manually configuring `index.sort.field` and `index.sort.order`. For more details, see [*Index Sorting*](elasticsearch://reference/elasticsearch/index-settings/sorting.md).

To modify the sort configuration of an existing data stream, update the data stream’s component templates, and then perform or wait for a [rollover](../data-streams.md#data-streams-rollover).

::::{note}
If you apply custom sort settings, the `@timestamp` field is injected into the mappings but is not automatically added to the list of sort fields. For best results, include it manually as the last sort field, with `desc` ordering.
::::



### Existing data streams [logsdb-host-name]

If you’re enabling `logsdb` index mode on a data stream that already exists, make sure to check mappings and sorting. The `logsdb` mode automatically maps `host.name` as a keyword if it’s included in the sort settings. If a `host.name` field already exists but has a different type, mapping errors might occur, preventing `logsdb` mode from being fully applied.

To avoid mapping conflicts, consider these options:

* **Adjust mappings:** Check your existing mappings to ensure that `host.name` is mapped as a keyword.
* **Change sorting:** If needed, you can remove `host.name` from the sort settings and use a different set of fields. Sorting by `@timestamp` can be a good fallback.
* **Switch to a different [index mode](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting)**: If resolving `host.name` mapping conflicts is not feasible, you can choose not to use `logsdb` mode.

::::{important}
On existing data streams, `logsdb` mode is applied on [rollover](../data-streams.md#data-streams-rollover) (automatic or manual).
::::



### Optimized routing on sort fields [logsdb-sort-routing]

If you have the required [subscription](https://www.elastic.co/subscriptions), you can enable routing optimizations to reduce the storage footprint of `logsdb` indexes. A routing optimization uses the fields in the sort configuration (except for `@timestamp`) to route documents to shards.

In benchmarks, routing optimizations reduced storage requirements by 20% compared to the default `logsdb` configuration, with a negligible penalty to ingestion performance (1-4%). Routing optimizations can benefit data streams that are expected to grow substantially over time. Exact results depend on the sort configuration and the nature of the logged data.

To configure a routing optimization:

* Include the index setting `[index.logsdb.route_on_sort_fields:true]` in the data stream configuration.
* [Configure index sorting](elasticsearch://reference/elasticsearch/index-settings/sorting.md) with two or more fields, in addition to `@timestamp`.
* Make sure the [`_id`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-id-field.md) field is not populated in ingested documents. It should be auto-generated instead.

A custom sort configuration is required, to improve storage efficiency and to minimize hotspots from logging spikes that may route documents to a single shard. For best results, use a few sort fields that have a relatively low cardinality and don’t co-vary (for example, `host.name` and `host.id` are not optimal).


## Specialized codecs [logsdb-specialized-codecs]

By default, `logsdb` index mode uses the `best_compression` [codec](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-codec), which applies [ZSTD](https://en.wikipedia.org/wiki/Zstd) compression to stored fields. You can switch to the `default` codec for faster compression with a slightly larger storage footprint.

The `logsdb` index mode also automatically applies specialized codecs for numeric doc values, in order to optimize storage usage. Numeric fields are encoded using the following sequence of codecs:

* **Delta encoding**: Stores the difference between consecutive values instead of the actual values.
* **Offset encoding**: Stores the difference from a base value rather than between consecutive values.
* **Greatest Common Divisor (GCD) encoding**: Finds the greatest common divisor of a set of values and stores the differences as multiples of the GCD.
* **Frame Of Reference (FOR) encoding**: Determines the smallest number of bits required to encode a block of values and uses bit-packing to fit such values into larger 64-bit blocks.

Each encoding is evaluated according to heuristics determined by the data distribution. For example, the algorithm checks whether the data is monotonically non-decreasing or non-increasing. If so, delta encoding is applied; otherwise, the process continues with the next encoding method (offset).

Encoding is specific to each Lucene segment and is reapplied when segments are merged. The merged Lucene segment might use a different encoding than the original segments, depending on the characteristics of the merged data.

For keyword fields, **Run Length Encoding (RLE)** is applied to the ordinals, which represent positions in the Lucene segment-level keyword dictionary. This compression is used when multiple consecutive documents share the same keyword.


## `ignore` settings [logsdb-ignored-settings]

The `logsdb` index mode uses the following `ignore` settings. You can override these settings as needed.


### `ignore_malformed` [logsdb-ignore-malformed]

By default, `logsdb` index mode sets `ignore_malformed` to `true`. With this setting, documents with malformed fields can be indexed without causing ingestion failures.


### `ignore_above` [logs-db-ignore-above]

In `logsdb` index mode, the `index.mapping.ignore_above` setting is applied by default at the index level to ensure efficient storage and indexing of large keyword fields. This applies to all members of the keyword type family (keyword, constant_keyword, and wildcard). The index-level default for `ignore_above` is 8191 *characters.* Using UTF-8 encoding, this results in a limit of 32764 bytes, depending on character encoding.

The mapping-level `ignore_above` setting takes precedence. If a specific field has an `ignore_above` value defined in its mapping, that value overrides the index-level `index.mapping.ignore_above` value. This default behavior helps to optimize indexing performance by preventing excessively large string values from being indexed.

If you need to customize the limit, you can override it at the mapping level or change the index level default.


### `ignore_dynamic_beyond_limit` [logs-db-ignore-limit]

In `logsdb` index mode, the setting `index.mapping.total_fields.ignore_dynamic_beyond_limit` is set to `true` by default. This setting allows dynamically mapped fields to be added on top of statically defined fields, even when the total number of fields exceeds the `index.mapping.total_fields.limit`. Instead of triggering an index failure, additional dynamically mapped fields are ignored so that ingestion can continue.

::::{note}
When automatically injected, `host.name` and `@timestamp` count toward the limit of mapped fields. If `host.name` is mapped with `subobjects: true`, it has two fields. When mapped with `subobjects: false`, `host.name` has only one field.
::::



## Fields without `doc_values` [logsdb-nodocvalue-fields]

When the `logsdb` index mode uses synthetic `_source` and `doc_values` are disabled for a field in the mapping, {{es}} might set the `store` setting to `true` for that field. This ensures that the field’s data remains accessible for reconstructing the document’s source when using [synthetic source](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source).

For example, this adjustment occurs with text fields when `store` is `false` and no suitable multi-field is available for reconstructing the original value.


## Settings reference [logsdb-settings-summary]

The `logsdb` index mode uses the following settings:

* **`index.mode`**: `"logsdb"`
* **`index.mapping.synthetic_source_keep`**: `"arrays"`
* **`index.sort.field`**: `["host.name", "@timestamp"]`
* **`index.sort.order`**: `["desc", "desc"]`
* **`index.sort.mode`**: `["min", "min"]`
* **`index.sort.missing`**: `["_first", "_first"]`
* **`index.codec`**: `"best_compression"`
* **`index.mapping.ignore_malformed`**: `true`
* **`index.mapping.ignore_above`**: `8191`
* **`index.mapping.total_fields.ignore_dynamic_beyond_limit`**: `true`


## Upgrade to logsdb [upgrade-to-logsdb]

Starting with version `9.0`, `logsdb` index mode is automatically applied to data streams with names matching the pattern `logs-*-*`. This default applies to Elasticsearch instances created in version `9.0` or later, as well as older instances that had no data streams matching the pattern `logs-*-*`. For the latter, you can still [configure `logsdb` index mode manually](#how-to-use-logsds).
