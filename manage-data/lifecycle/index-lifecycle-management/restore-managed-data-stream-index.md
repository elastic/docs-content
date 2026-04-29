---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-and-snapshots.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Restore managed indices and manage {{ilm-init}} actions [index-lifecycle-and-snapshots]

When restoring a managed {{es}} index or data stream, {{ilm}} ({{ilm-init}}) resumes running the associated policies automatically. You can temporarily stop {{ilm-init}} to control the running of lifecycle actions, ensuring restored indices progress through phases according to your operational needs.

To [restore](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) managed indices, ensure that the {{ilm-init}} policies referenced by the indices exist. If necessary, you can restore {{ilm-init}} policies by setting [`include_global_state`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) to `true`.

A restored index’s `min_age` is relative to when it was originally created or rolled over, not its restoration time. Policy actions are performed on the same schedule irrespective of whether an index has been restored from a snapshot. If you restore an index that was accidentally deleted half way through its month long lifecycle, it proceeds normally through the last two weeks of its lifecycle.

You might want to prevent {{ilm-init}} from immediately executing its policy on a restored index. For example, if you are restoring an older snapshot you might want to prevent it from rapidly progressing through all its lifecycle phases. You might want to add or update documents before it’s marked read-only or shrunk, or prevent the index from being immediately deleted.

To prevent {{ilm-init}} from executing a restored index’s policy:

1. In {{kib}}, go to **Data management** and select **Snapshot and Restore**.
1. From the **Snapshots** page, select the snapshot you wish to restore and then select the **Restore** action.
1. On the **Index settings** restore page, enable **Reset index settings** and add the `index.lifecycle.name` and `index.lifecycle.rollover_alias` index settings.
1. Select **Next** and then select **Restore snapshot**.

Alternatively, you can use the [Restore a snapshot](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) API with the `ignore_index_settings` option. If you need to re-add the {{ilm-init}} policy, refer to [](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md) for details.

