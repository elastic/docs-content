# Snapshot and restore with custom repositories [ec-custom-repository]

Specify your own repositories to snapshot to and restore from. This can be useful, for example, to do long-term archiving of old indexes, restore snapshots across Elastic Cloud accounts, or to be certain you have an exit strategy, should you need to move away from our service.

{{ech}} supports these repositories:

* [Amazon Web Services (AWS)](../../../deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md)
* [Google Cloud Storage (GCS)](../../../deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md)
* [Azure Blob Storage](../../../deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md)

::::{note} 
Automated snapshots are only available in the *found snapshots* repository. You are responsible for the execution and maintenance of the snapshots that you store in custom repositories. Note that the automated snapshot frequency might conflict with manual snapshots. You can enable SLM to automate snapshot management in a custom repository.
::::


::::{tip} 
By using a custom repository, you can restore snapshots across regions.
::::





