---
navigation_title: Minimal-downtime migration using snapshots
applies_to:
  stack: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{es}} data with minimal downtime using snapshots [migrate-elasticsearch-data-with-minimal-downtime]

When moving your data and services from one {{es}} cluster to another, such as to {{ech}}, {{ece}}, new on-premises hardware, or any other {{es}} environment, you can migrate with minimal downtime using incremental snapshots. 

Migrating with incremental snapshots is useful when you want to:

* Migrate all data in your indices and configurations, such as roles and {{kib}} dashboards, from the old cluster to a new cluster.
* Ensure data ingestion, such as {{ls}} or {{beats}}, and data consumption, such as applications using {{es}} as a backend, seamlessly migrate to the new cluster.
* Maintain data consistency and minimize disruption.  

## How incremental snapshots work [how-incremental-snapshots-work]
Incremental snapshots save only the data that has changed since the last snapshot. The first snapshot is a full copy of the data. Each subsequent snapshot contains only the differences, which makes creating and restoring snapshots faster and more efficient over time. 

When restoring, {{es}} copies only the missing data segments from the snapshot repository to the new cluster local storage. When the changes between snapshots are small, the restore process is significantly faster. 

By taking and restoring incremental snapshots in sequence, you can keep a new cluster closely synchronized with the old cluster, allowing you to migrate most of your data ahead of time and minimize downtime during the final cutover. 

For more information about migrating your data with snapshot and restore, check [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md).

## Before you begin [incremental-snapshots-before-you-begin]
Before you migrate, review the prerequisites and requirements.

### Prerequisites
* Learn how to [set up and manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md). 
* If restoring to a different cluster, review [Restore to a different cluster](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster).
* As an alternative migration method, you can [reindex from a remote cluster](/manage-data/migrate.md#ech-reindex-remote).

### Requirements
* **Cluster size** – The new cluster must be the same size or larger than the old cluster. 
* **Version compatibility** – Both clusters must use compatible {{es}} versions. To check if your cluster versions are compatible, check [Snapshot version compatibility](/deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility).
* **Storage requirements** - Ensure sufficient repository storage. Usage grows with snapshot frequency and data volume. 
* **Network overhead** – Transferring snapshots across networks, regions, or providers can be time consuming and incur costs.
* **Resource usage** – Snapshot and restore operations can be resource intensive and affect cluster performance.
* **Custom integrations** – Some integrations that use the {{es}} API directly, such as the [Elasticsearch Java Client library](elasticsearch-java://reference/index.md), can require additional handling during cutover.

## Recommended migration timeline [recommended-migration-timeline]
Tp complete the migration with minimal downtime, use incremental snapshots. While the exact sequence may differ depending on your infrastructure and operational requirements, you can use the recommended migration timeline as a reliable baseline that you can adapt. Adjust the steps and times to fit your own operational needs.

1. **09:00**: Take the initial full snapshot of the old cluster. You can also take the initial full snapshot the day before.
2. **09:30**: Restore the snapshot to the new cluster.
3. **09:55**: Take another snapshot of the old cluster and restore it to the new cluster. Repeat this process until the snapshot and restore operations take only a few seconds or minutes. Remember that when restoring indices that _already_ exist in the new cluster (for example, to pull in recently copied data), they first need to be [closed](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#considerations). Also, remember that the restore operation automatically opens indices, so you will likely need to close the actively written ones after restoring them.
4. **10:15**: Perform the final cutover.
    1. In the old cluster, pause indexing or set indices to read-only. For details on setting indices to read-only to safely pause indexing during migration, check [Index lifecycle actions: Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md).
    2. Take a final snapshot. 
    3. Restore the snapshot to the new cluster. Again, remember that to restore indices that already exist, they first need to be closed.
    4. Change ingestion and querying to the new cluster. 
    5. Open the indices in the new cluster. 

## Additional support [incremental-snapshots-additional-support]
To get expert assistance for your {{es}} migrations, go to [Elastic Professional Services](https://www.elastic.co/consulting).
