In this step, you’ll configure a read-only snapshot repository in the new cluster that points to the storage location used by the old cluster. This allows the new cluster to access and restore snapshots created in the original environment.

1. On your old {{es}} cluster, choose an option to get the name and details of your snapshot repository bucket:

    ```sh
    GET /_snapshot
    GET /_snapshot/_all
    ```
<!--
% Commenting this out because we don't need the snapshot name at this stage, only the repository
2. Get the snapshot name:

    ```sh
    GET /_snapshot/NEW-REPOSITORY-NAME/_all
    ```

    The output for each entry provides a `"snapshot":` value which is the snapshot name.

    ```json
    {
      "snapshots": [
        {
          "snapshot": "scheduled-1527616008-instance-0000000004",
          ...
        },
        ...
      ]
    }
    ```
-->

2. Add the snapshot repository on the new cluster:

    If the original cluster still has write access to the repository, register the repository as read-only.

    ::::{tab-set}

    :::{tab-item} {{ech}}

    From the [console](https://cloud.elastic.co?page=docs&placement=docs-body) of the **new** {{es}} cluster, add the snapshot repository.

    For details, check our guidelines for:
    * [Amazon Web Services (AWS) Storage](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md)
    * [Google Cloud Storage (GCS)](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md)
    * [Azure Blob Storage](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md).

    If you’re migrating [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), the repository name must be identical in the source and destination clusters.

    If the source cluster is still writing to the repository, you need to set the destination cluster’s repository connection to `readonly:true` to avoid data corruption. Refer to [backup a repository](../deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) for details.
    :::

    :::{tab-item} {{ece}}

    From the Cloud UI of the **new** {{es}} cluster add the snapshot repository.

    For details about configuring snapshot repositories on Amazon Web Services (AWS), Google Cloud Storage (GCS), or Azure Blob Storage, check [manage Snapshot Repositories](../deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md).

    If you’re migrating [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), the repository name must be identical in the source and     destination clusters.
    :::

    ::::
