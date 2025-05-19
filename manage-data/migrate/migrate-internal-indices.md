---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-data-internal.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data-internal.html
applies_to:
  stack: ga
  deployment:
    eck: unavailable
    ess: ga
    ece: ga
  serverless: unavailable
---

# Migrate system indices

When you migrate your {{es}} data into a new infrastructure you may also want to migrate your {{es}} system internal indices, specifically the `.kibana` index and the `.security` index.

In {{es}} 8.0 and later versions, the snapshot and restore of [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) is the only way to back up and restore system indices and system data streams.

## Migrate system indices using snapshot and restore

To restore system indices from a snapshot, follow the same procedure described in [](../migrate.md#ec-restore-snapshots) and select the appropriate **feature states** when preparing the restore operation, such as `kibana` or `security`.

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
