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
