# Work with snapshots [ece-snapshots]

Snapshots provide backups of your Elasticsearch indices. You can use snapshots to recover from a failure when not enough availability zones are used to provide high availability or to recover from accidental deletion.

To enable snapshots for your Elasticsearch clusters and to work with them, you must [have configured a repository](../../../deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md). After you have configured a snapshot repository, a snapshot is taken every 30 minutes or at the interval that you specify.

Use Kibana to manage your snapshots. In Kibana, you can set up additional repositories where the snapshots are stored, other than the one currently managed by Elastic Cloud Enterprise. You can view and delete snapshots, and configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted. To learn more, check the [Snapshot and Restore](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md) documentation.

From within Elastic Cloud Enterprise you can [restore a snapshot](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) from a different deployment in the same region.

::::{important} 
Snapshots back up only open indices. If you close an index, it is not included in snapshots and you will not be able to restore the data.
::::


