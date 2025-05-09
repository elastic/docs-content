---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-restore-snapshots-containing-searchable-snapshots-indices-across-clusters.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restore-snapshots-containing-searchable-snapshots-indices-across-clusters.html
applies_to:
  deployment:
    ess:
    ece:
---

# Restore snapshots containing searchable snapshots indices across clusters [ece-restore-snapshots-containing-searchable-snapshots-indices-across-clusters]

If you are restoring a snapshot from one cluster to another, and that snapshot contains indices that are backed by searchable snapshots, there are a few more requirements to be aware of.

The first versions of {{es}} that supported searchable snapshots required that the repository name in the destination cluster, where the snapshot is to be restored from, match the repository name in the source cluster, where the snapshot was taken. Beginning with {{es}} version 7.12 this requirement is no longer present, but there are other prerequisites that need to be met.

Pre-requisites for restoring snapshots containing searchable snapshot indices across clusters:

* The source cluster must have been created as version 7.12.0 or higher.

    To be more precise the requirement is on the `found-snapshots` repository settings at the time the snapshots were taken. The repository must have a `uuid` field, which is supported only in {{es}} versions 7.12.0 and higher. If the cluster was created with a previous version and later upgraded to 7.12.0 or higher, the repository may not have the required `uuid` field and therefore cannot be used to restore onto another cluster.

    To be sure, you can send a `GET /_snapshot/found-snapshots` request to your {{es}} cluster and check if the `uuid` field is present.

* The destination cluster must be version 7.13.2 or higher.

    Previous versions had issues restoring the snapshot or recovering searchable snapshot indices in case of, for example, node failure.


::::{important}
The snapshot in the source cluster MUST NOT be deleted even after being successfully restored in the destination cluster. In fact, that’s also the case for the searchable snapshots in the source cluster for which there were indices backed by the restored snapshot. These snapshots are required for recovery of the searchable snapshot indices in case of, for example, node failure.

This means that until you delete the searchable snapshot indices in the destination cluster, you must not delete your source deployment, delete the restored snapshot, or delete any of the searchable snapshots used by the searchable snapshot indices.

Read [Back up and restore searchable snapshots](searchable-snapshots.md#back-up-restore-searchable-snapshots) for more guidance.

::::


