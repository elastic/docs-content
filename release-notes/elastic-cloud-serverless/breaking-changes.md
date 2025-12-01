---
navigation_title: Breaking changes
products:
  - id: cloud-serverless
---

# {{serverless-full}} breaking changes [elastic-cloud-serverless-breaking-changes]

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
