---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-data-internal.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data-internal.html
applies_to:
  stack: ga
products:
  - id: cloud-hosted
---

# Migrate system indices

When you migrate your {{es}} data into a new infrastructure, you might also want to migrate system-level indices and data streams, such as those used by {{kib}} or security features (for example, `.kibana` and `.security`).

Starting in {{es}} 8.0, you can use [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) to back up and restore all system indices and system data streams. This is the only available method for migrating this type of data.

However, using snapshot and restore for system indices does not mean you must use it for everything. You can still migrate other data by re-indexing from the source or a remote cluster.

## Migrate system indices using snapshot and restore

To restore system indices from a snapshot, follow the same procedure described in [](../migrate.md#ec-restore-snapshots) and select the appropriate feature states when preparing the restore operation, such as `kibana` or `security`.

For more details about restoring feature states, or the entire cluster state, refer to [](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-feature-state).

The following example describes how to restore the `security` feature using the [restore snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore):

```sh
POST _snapshot/REPOSITORY/SNAPSHOT_NAME/_restore
{
  "indices": "-*",
  "ignore_unavailable": true,
  "include_global_state": false,
  "include_aliases": false,
  "feature_states": [
    "security"
  ]
}
```
