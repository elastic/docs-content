---
navigation_title: Breaking changes
products:
  - id: cloud-serverless
---

# {{serverless-full}} breaking changes [elastic-cloud-serverless-breaking-changes]

## April 15, 2026 [elastic-cloud-serverless-04152026-breaking]

:::{dropdown} Disables sequence numbers for TSDB indices in release builds

For indices in time series mode, {{es}} trims sequence numbers when they are no longer needed for replication. This reduces storage overhead (for example, a substantial share of space for OpenTelemetry Protocol metrics) and lowers the cost of segment merging.

When sequence numbers are disabled for an index, [optimistic concurrency control](elasticsearch://reference/elasticsearch/rest-apis/optimistic-concurrency-control.md) no longer applies. Index, update, and delete requests that use `if_seq_no` and `if_primary_term` return an error, and searches that request `seq_no_primary_term` receive sentinel values for those fields. `update_by_query` and `delete_by_query` proceed without conflict detection, so concurrent modifications can overwrite documents without version conflict errors. For typical metrics workloads, concurrent updates are uncommon, and the storage savings are often an acceptable tradeoff.

To retain full sequence numbers and optimistic concurrency control, set `index.disable_sequence_numbers` to `false` in your time series index templates.

**Impact:**

Workflows that depend on optimistic concurrency control, sequence numbers in search responses, or conflict detection for `update_by_query` and `delete_by_query` on time series indices might need changes, or you can opt out by setting `index.disable_sequence_numbers` to `false`.

For more information, view [#145737]({{es-pull}}145737).
:::

## March 18, 2026 [elastic-cloud-serverless-03182026-breaking]

:::{dropdown} The `_source` field mode is now saved to the template index settings

The index and component template forms in **Index Management** previously saved the `_source` field mode (`stored` and `synthetic`) in the `mappings._source.mode` setting. This path is deprecated and has no effect in {{es}}. The form now uses the correct `settings.index.mapping.source.mode` setting. When you edit a template in the UI, any existing `mappings._source.mode` setting is automatically moved to the index settings and removed from mappings. Other `_source` options (`enabled`, `includes`, and `excludes`) remain in mappings.

**Impact:**

The template's JSON structure has changed: The `_source` mode setting (`stored`/`synthetic`) appears in the index settings, not in mappings. Options that were previously ignored when saved from the UI can now take effect for indices that match the template. Automation that only reads `mappings._source.mode` should read `settings.index.mapping.source.mode` instead. Open and save the template in the UI to automatically migrate the field.

For more information, view [#255122]({{kib-pull}}255122).
:::

## March 2, 2026 [elastic-cloud-serverless-03022026-breaking]

:::{dropdown} Removes serializer and deserializer parameters from the {{elastic-sec}} Lists API

The `serializer` and `deserializer` parameters have been removed from the {{elastic-sec}} Lists API. These parameters previously allowed custom parsing logic for value list items:

- `serializer` — Determined how uploaded list item values were parsed using regex patterns.
- `deserializer` — Determined how retrieved list item values were presented using Handlebars expressions.

**Impact:**

API requests that include `serializer` or `deserializer` parameters (in the Create List API request body or Import List Items API query string) will have those parameters silently ignored, and a warning header will be returned in the response. Users who relied on custom parsing logic will need to pre-process their list data before import, as only default parsing behavior is now supported.

For more information, view [#250111]({{kib-pull}}250111).
:::

## October 27, 2025 [serverless-changelog-10272025-breaking]

:::{dropdown} Implement native synthetic source for normalized keywords

This adds a new mapping parameter `normalizer_skip_store_original_value` to keyword fields. When this parameter is set and `synthetic_source` is enabled, keyword fields with configured normalizers will not store the original non-normalized value in `_ignored_source` and will instead use the normalized value to reconstruct the source.
This parameter enabled by default for the built-in `lowercase` normalizer and is disabled by default for other custom normalizers.

**Impact:**

Keyword fields using the `lowercase` normalizer will return the normalized value in the source when synthetic source is enabled.

For more information, view [#136915](https://github.com/elastic/elasticsearch/pull/136915).
:::



## August 25, 2025 [elastic-cloud-serverless-08252025-breaking]

:::{dropdown} Allows partial results by default in {{esql}}

In earlier versions of {{es}}, {{esql}} would fail the entire query if it encountered any error.
{{esql}} now returns partial results instead of failing when encountering errors.

**Impact:**

Callers should check the `is_partial` flag returned in the response to determine if the result is partial or complete.
If returning partial results is not desired, this option can be overridden per request via an `allow_partial_results` parameter in the query URL or globally via the cluster setting `esql.query.allow_partial_results`.

For more information, view [#125060](https://github.com/elastic/elasticsearch/pull/125060).
:::

:::{dropdown} Enable exclude_source_vectors by default for new indices

The `exclude_source_vectors` setting is now enabled by default for newly created indices.
This means that vector fields (for example, `dense_vector`) are no longer stored in the `_source` field by default, although they remain fully accessible through search and retrieval operations.
Instead of being persisted in `_source`, vectors are now rehydrated on demand from the underlying
index structures when needed.
This reduces index size and improves performance for typical vector search workloads where the original vector values do not need to be part of the `_source`.
If your use case requires vector fields to be stored in `_source`, you can disable this behavior by
setting `exclude_source_vectors: false` at index creation time.
  
**Impact:**

Vector fields will no longer be stored in `_source` by default for new indices.
Applications or tools that expect to see vector fields in `_source` (for raw document inspection)
may need to be updated or configured to explicitly retain vectors using `exclude_source_vectors: false`.
Retrieval of vector fields via search or the `_source` API remains fully supported.

For more information, view [#131907](https://github.com/elastic/elasticsearch/pull/131907).
:::

:::{dropdown} Don't enable norms for fields of type text when the index mode is LogsDB or TSDB

This changes the default behavior for norms on `text` fields in LogsDB and TSDB indices.
Prior to this change, norms were enabled by default, with the option to disable them via manual configurations.
After this change, norms will be disabled by default.
Note, because we dont support enabling norms from a disabled state, users will not be able to enable norms on `text` fields in logsdb and tsdb indices.

**Impact:**

Text fields will no longer be normalized by default in LogsDB and TSDB indicies.
  
For more information, view [#131317](https://github.com/elastic/elasticsearch/pull/131317).
:::

## August 11, 2025 [elastic-cloud-serverless-08112025-breaking]

:::{dropdown} Improves advanced settings management APIs privilege checks

Roles with explicit read access to advanced settings but all access to `SavedObjectManagement` can no longer update settings via the internal advanced settings API.
This update enforces explicit privileges instead of relying on saved object security checks.

For more information, view [#230067]({{kib-pull}}230067).
:::

## June 23, 2025 [serverless-changelog-06232025]

:::{dropdown} Disallows mixed quoted/unquoted patterns in FROM

Previously, the {{esql}} grammar allowed users to individually quote constituent strings in index patterns such as `"remote_cluster":"index_name"`. This would allow users to write complex malformed index patterns that often slip through grammar and the subsequent validation.
This could result in runtime errors that can be misleading.
This change simplifies the grammar to early reject such malformed index patterns at the parsing stage, allowing users to write simpler queries and see more relevant and meaningful errors.

**Impact:**

Users can write queries with simpler index patterns and see more meaningful and relevant errors.
For more information, view [#127636]({{es-pull}}127636).
:::
