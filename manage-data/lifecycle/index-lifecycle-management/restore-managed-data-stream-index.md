---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-and-snapshots.html
---

# Restore a managed data stream or index [index-lifecycle-and-snapshots]

To [restore](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) managed indices, ensure that the {{ilm-init}} policies referenced by the indices exist. If necessary, you can restore {{ilm-init}} policies by setting [`include_global_state`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) to `true`.

When you restore a managed index or a data stream with managed backing indices, {{ilm-init}} automatically resumes executing the restored indices' policies. A restored index’s `min_age` is relative to when it was originally created or rolled over, not its restoration time. Policy actions are performed on the same schedule whether or not an index has been restored from a snapshot. If you restore an index that was accidentally deleted half way through its month long lifecycle, it proceeds normally through the last two weeks of its lifecycle.

In some cases, you might want to prevent {{ilm-init}} from immediately executing its policy on a restored index. For example, if you are restoring an older snapshot you might want to prevent it from rapidly progressing through all of its lifecycle phases. You might want to add or update documents before it’s marked read-only or shrunk, or prevent the index from being immediately deleted.

To prevent {{ilm-init}} from executing a restored index’s policy:

1. Temporarily [stop {{ilm-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop). This pauses execution of *all* {{ilm-init}} policies.
2. Restore the snapshot.
3. [Remove the policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy) from the index or perform whatever actions you need to before {{ilm-init}} resumes policy execution.
4. [Restart {{ilm-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start) to resume policy execution.

