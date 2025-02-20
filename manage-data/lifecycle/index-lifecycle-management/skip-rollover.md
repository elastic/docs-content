---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/skipping-rollover.html
applies_to:
  stack: ga
  serverless: ga
---

# Skip rollover [skipping-rollover]

When `index.lifecycle.indexing_complete` is set to `true`, {{ilm-init}} won’t perform the rollover action on an index, even if it otherwise meets the rollover criteria. It’s set automatically by {{ilm-init}} when the rollover action completes successfully.

You can set it manually to skip rollover if you need to make an exception to your normal lifecycle policy and update the alias to force a roll over, but want {{ilm-init}} to continue to manage the index. If you use the rollover API, it is not necessary to configure this setting manually.

If an index’s lifecycle policy is removed, this setting is also removed.

::::{important} 
When `index.lifecycle.indexing_complete` is `true`, {{ilm-init}} verifies that the index is no longer the write index for the alias specified by `index.lifecycle.rollover_alias`. If the index is still the write index or the rollover alias is not set, the index is moved to the [`ERROR` step](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md).
::::


For example, if you need to change the name of new indices in a series while retaining previously-indexed data in accordance with your configured policy, you can:

1. Create a template for the new index pattern that uses the same policy.
2. Bootstrap the initial index.
3. Change the write index for the alias to the bootstrapped index using the [aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases).
4. Set `index.lifecycle.indexing_complete` to `true` on the old index to indicate that it does not need to be rolled over.

{{ilm-init}} continues to manage the old index in accordance with your existing policy. New indices are named according to the new template and managed according to the same policy without interruption.

