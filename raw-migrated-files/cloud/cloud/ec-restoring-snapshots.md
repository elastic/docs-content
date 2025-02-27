# Work with snapshots [ec-restoring-snapshots]

Snapshots provide a way to restore your Elasticsearch indices. They can be used to copy indices for testing, to recover from failures or accidental deletions, or to migrate data to other deployments.

By default, {{ech}} takes a snapshot of all the indices in your Elasticsearch cluster every 30 minutes. You can set a different snapshot interval, if needed for your environment. You can also take snapshots on demand, without having to wait for the next interval. Taking a snapshot on demand does not affect the retention schedule for existing snapshots, it just adds an additional snapshot to the repository. This might be helpful if you are about to make a deployment change and you don’t have a current snapshot.

Use Kibana to manage your snapshots. In Kibana, you can set up additional repositories where the snapshots are stored, other than the one currently managed by {{ech}}. You can view and delete snapshots, and configure a snapshot lifecycle management (SLM) policy to automate when snapshots are created and deleted. To learn more, check the [Snapshot and Restore](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md) documentation.

::::{important} 
Snapshots back up only open indices. If you close an index, it is not included in snapshots and you will not be able to restore the data.
::::


::::{note} 
A snapshot taken using the default `found-snapshots` repository can only be restored to deployments in the same region. If you need to restore snapshots across regions, create the destination deployment, connect to the [custom repository](../../../deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md), and then [restore from a snapshot](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).
::::


From within {{ech}}, you can [restore a snapshot](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) from a different deployment in the same region.

