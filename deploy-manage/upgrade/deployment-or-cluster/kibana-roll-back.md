---
navigation_title: Roll back to a previous version
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/upgrade-migrations-rolling-back.html
applies_to:
  deployment:
    self: ga
products:
  - id: kibana
---

# Roll back to a previous version of {{kib}} [upgrade-migrations-rolling-back]

If you’ve followed [preparing for migration](/deploy-manage/upgrade/deployment-or-cluster/kibana.md#preventing-migration-failures) and [resolving migration failures](../../../troubleshoot/kibana/migration-failures.md), and {{kib}} is still unable to successfully upgrade, roll back {{kib}} until you identify and fix the root cause.

::::{warning}
Before you roll back {{kib}}, ensure that the version you want to roll back to is compatible with your {{es}} cluster. If the version you want to roll back to is not compatible, you must also roll back {{es}}. Any changes made after an upgrade are lost when you roll back to a previous version.
::::


To roll back after a failed upgrade migration, you must also roll back the {{kib}} feature state to be compatible with the previous {{kib}} version.


## Roll back by restoring the {{kib}} feature state from a snapshot [_roll_back_by_restoring_the_kib_feature_state_from_a_snapshot]

1. Before proceeding, [take a snapshot](../../tools/snapshot-and-restore/create-snapshots.md) that contains the `kibana` feature state. By default, snapshots include the `kibana` feature state.
2. To make sure no {{kib}} instances are performing an upgrade migration, shut down all {{kib}} instances.
3. [Restore](../../tools/snapshot-and-restore/restore-snapshot.md) the `kibana` feature state from a snapshot taken before the failed {{kib}} upgrade. The following {{es}} request will only restore the {{kib}} feature state:

    ```console
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "-*", <1>
      "feature_states": ["kibana"]
    }
    ```

    1. Exclude all indices and data streams from the restore operation to ensure that only the {{kib}} system indices included in the {{kib}} feature state are restored.

4. Start all {{kib}} instances on the older version you want to roll back to.

