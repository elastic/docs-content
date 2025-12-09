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

You might want to prevent {{ilm-init}} from immediately executing its policy on a restored index. For example, if you are restoring an older snapshot you might want to prevent it from rapidly progressing through all of its lifecycle phases. You might want to add or update documents before it’s marked read-only or shrunk, or prevent the index from being immediately deleted.

To prevent {{ilm-init}} from executing a restored index’s policy:

1. Temporarily [stop {{ilm-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-stop). This pauses execution of *all* {{ilm-init}} policies.
2. Restore the snapshot.
3. [Remove the policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy) from the index or perform whatever actions you need to before {{ilm-init}} resumes policy execution.
4. [Restart {{ilm-init}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-start) to resume policy execution.

