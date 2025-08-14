---
navigation_title: Migrate Elasticsearch data with minimal downtime
applies_to:
  stack: ga
  deployment:
    ess: ga
    ece: ga
    eck: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{es}} data with minimal downtime [migrate-elasticsearch-data-with-minimal-downtime]
When moving your data and services from one {{es}} cluster to another, such as to {{ech}}, {{ece}}, new on-premises hardware, or any other {{es}} environment, you can use incremental snapshots to minimize downtime. 

Migrating with incremental snapshots is useful when you want to:

* Migrate all data in your indices and configurations, such as roles and {{kib}} dashboards, from the old cluster to a new cluster.
* Ensure data ingestion, such as {{ls}} or {{beats}}, and data consumption, such as applications using {{es}} as a backend, seamlessly migrate to the new cluster.
* Maintain data consistency and minimize disruption.  

## How incremental snapshots work [how-incremental-snapshots-work]
Incremental snapshots capture only the data that has changed since the previous snapshot. 

After the initial full snapshot, each subsequent snapshot contains only the differences, which makes the snapshot process faster over time. When you restore snapshots, only the missing data segments are copied from the snapshot repository to the cluster local storage, speeding up restores when the changes between snapshots are small.

When you incrementally create and restore snapshots, you can repeatedly synchronize the new cluster with the old cluster by taking and restoring multiple snapshots before performing the final cutover.

## Recommended migration timeline [recommended-migration-timeline]
Complete the minimal-downtime migration using incremental snapshots. While the exact sequence may differ depending on your infrastructure and operational requirements, you can use the recommended migration timeline as a reliable baseline that you can adapt. Adjust the steps and times to fit your own operational needs.

1. **09:00**: Take the initial full snapshot of the old cluster. You can also take the initial full snapshot the day before.
2. **09:30**: Restore the snapshot to the new cluster.
3. **09:55**: Take another snapshot of the old cluster and restore it to the new cluster. Repeat this process until the snapshot and restore operations take only a few seconds or minutes.
4. **10:15**: Perform the final cutover.
    1. In the old cluster, pause indexing or set indices to ready-only.
    2. Take a final snapshot. 
    3. Restore the snapshot to the new cluster. 
    4. Change ingestion and querying to the new cluster. 
    5. Open the indices in the new cluster. 

## Incremental snapshot limitations [incremental-snapshot-limitations]
While incremental snapshots allow efficient migration with minimal downtime, consider the limitations when planning your migration.

Limitations include the following:
* **Storage requirements** – Sufficient repository storage is required, and usage can grow based on snapshot frequency and data volume.
* **Network overhead** – Transferring snapshots across networks, regions, or providers can be time-consuming and incur costs.
* **Version compatibility** – Old and new clusters must use compatible {{es}} versions. To check if your cluster versions are compatible, check [Snapshot version compatibility](/deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility).
* **Custom integrations** – Some custom integrations that directly use the {{es}} API can require additional handling during the cutover from the old cluster to the new cluster.
* **Resource usage** – Initial and incremental snapshot and restore operations can be resource-intensive, potentially affecting cluster performance.

## Additional topics [additional-incremental-snapshot-topics]
For more information on migrating {{es}} data with minimal downtime using incremental snapshots, review the related resources. 

### Snapshot and restore
* For more information about snapshot and restore concepts, check [Snapshot and Restore](/deploy-manage/tools/snapshot-and-restore.md).
* To learn how to configure snapshot repositories before taking or restoring snapshots, check [Manage snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md).
* To learn how to restore snapshots to clusters other than the source, check [Restore to a different cluster](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster).

### Cluster and index management
* For details on setting indices to read-only to safely pause indexing during migration, check [Index lifecycle actions: Read-only](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-readonly.md).

### Data ingestion
* For information about using {{ls}} for data ingestion, check the [{{ls}} documentation](logstash://reference/index.md).
* For information about using Beats for data ingestion, check the [{{beats}} documentation](beats://reference/index.md).

### Alternative migration methods
* To learn about reindexing from remote clusters as an alternative migration method, check [Reindex documents API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).

### Elastic Cloud environments
* To explore {{ech}} environments for migration targets, check the [{{ech}} documentation](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).
* To explore {{ece}} environments for migration targets, check the [{{ece}} documentation](/deploy-manage/deploy/cloud-enterprise.md).

### Additional support
* To get expert assistance for your {{es}} migrations, go to [Elastic Professional Services](https://www.elastic.co/consulting).
