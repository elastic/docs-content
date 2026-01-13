---
navigation_title: Skip rollover
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/skipping-rollover.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Skip rollover in {{ilm}} ({{ilm-init}}) [skipping-rollover]

You can use {{ilm}} to manage index lifecycle transitions without rolling over your indices. For example, when working with data that isn't continuously ingested, you might prefer to create a new index on a set schedule, such as the first Monday of each month. In this case, you can still use an {{ilm-init}} policy to automatically move indices through [lifecycle phases](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md#ilm-phase-transitions) as they age and control when new indices are created by disabling the rollover action.

You can configure indices to skip rollover either as part of an {{ilm-init}} policy or manually by adjusting the index settings.

## Skip rollover through an {{ilm-init}} policy

When you [create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) in {{kib}}, you can choose to enable or disable rollover.

To update the automatic rollover setting in an {{ilm-init}} policy:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

1. Select a policy to update, and from the **Actions** menu select **Edit**.

1. In the **Hot phase** section, expand the advanced settings.

1. Update the **Enable rollover** option to enable or disable automatic rollover.

    ![Create policy page](/manage-data/images/elasticsearch-reference-create-policy.png "")


## Skip rollover manually

When the [`index.lifecycle.indexing_complete`](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md#_index_level_settings_2) setting is `true`, {{ilm-init}} won’t perform the rollover action on an index, even if it otherwise meets the rollover criteria. This setting is updated to `true` automatically by {{ilm-init}} when the rollover action completes successfully.

You can update this setting manually to skip rollover if, for instance, you need to make an exception to your normal lifecycle policy and update the alias to force a rollover, but you want {{ilm-init}} to continue to manage the index. If you use the rollover API rather than an {{ilm-init}} policy to roll over indices, it is not necessary to configure this setting manually.

If an index’s lifecycle policy is removed, this setting is also removed.

::::{important}
When `index.lifecycle.indexing_complete` is set to `true`, {{ilm-init}} verifies that the index is no longer the write index for the alias specified by `index.lifecycle.rollover_alias`. If the index is still the write index or the rollover alias is not set, the index is moved to the [`ERROR` step](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md).
::::

For example, if you need to change the name of new indices in a series while retaining previously-indexed data in accordance with your configured policy, you can:

1. Create a template for the new index pattern that uses the same policy.
2. Bootstrap the initial index.
3. Change the write index for the alias to the bootstrapped index using the [aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases).
4. Set `index.lifecycle.indexing_complete` to `true` on the old index to indicate that it does not need to be rolled over.

{{ilm-init}} continues to manage the old index in accordance with your existing policy. New indices are named according to the new template and managed according to the same policy without interruption.

