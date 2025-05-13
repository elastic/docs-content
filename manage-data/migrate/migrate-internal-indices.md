---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-data-internal.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data-internal.html
applies_to:
  stack: ga
  deployment:
    eck: unavailable
    ess: ga
    ece: unavailable
  serverless: unavailable
products:
  - id: cloud-hosted
---

# Migrate internal indices

When you migrate your {{es}} data into a new infrastructure you may also want to migrate your {{es}} internal indices, specifically the `.kibana` index and the `.security` index.

There are two ways to migrate the internal {{es}} indices:

1. Reindex the indices from a remote cluster.
2. Restore the indices from a snapshot.

To reindex internal indices from a remote cluster, you can follow the same steps that you use to reindex regular indices when you [migrate your {{es}} data indices](../migrate.md#ech-reindex-remote).

To restore internal indices from a snapshot, the procedure is a bit different from migrating {{es}} data indices. Use these steps to restore internal indices from a snapshot:

1. On your old {{es}} cluster, choose an option to get the name of your snapshot repository bucket:

    ```sh
    GET /_snapshot
    GET /_snapshot/_all
    ```

2. Get the snapshot name:

    ```sh
    GET /_snapshot/NEW-REPOSITORY-NAME/_all
    ```

    The output for each entry provides a `"snapshot":` value which is the snapshot name.

    ```
      {
      "snapshots": [
        {
          "snapshot": "scheduled-1527616008-instance-0000000004",
    ```



3. To restore internal {{es}} indices, you need to register the snapshot repository in `read-only` mode.

    First, add the authentication information for the repository to the {{ech}} keystore, following the steps for your cloud provider:
    * [AWS S3](../../deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md#ec-snapshot-secrets-keystore)
    * [Google Cloud Storage](../../deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md#ec-configure-gcs-keystore)
    * [Azure Blog storage](../../deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md#ec-configure-azure-keystore)

    Next, register a read-only repository. Open an {{es}} [API console](../../explore-analyze/query-filter/tools/console.md) and run the [Read-only URL repository](../../deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md) API call.

4. Once the repository has been registered and verified, you are ready to restore the internal indices to your new cluster, either all at once or individually.

    * **Restore all internal indices**

        Run the following API call to restore all internal indices from a snapshot to the cluster:

        ```sh
        POST /_snapshot/repo/snapshot/_restore
        {
          "indices": ".*",
          "ignore_unavailable": true,
          "include_global_state": false,
          "include_aliases": false,
          "rename_pattern": ".(.+)",
          "rename_replacement": "restored_security_$1"
        }
        ```

    * **Restore an individual internal index**

        ::::{warning}
        When restoring internal indices, ensure that the `include_aliases` parameter is set to `false`. Not doing so will make Kibana inaccessible. If you do run the restore without `include_aliases`, the restored index can be deleted or the alias reference to it can be removed. This will have to be done from either the API console or a curl command as Kibana will not be accessible.
        ::::

        Run the following API call to restore one internal index from a snapshot to the cluster:

        ```sh
        POST /_snapshot/repo/snapshot/_restore
        {
          "indices": ".kibana",
          "ignore_unavailable": true,
          "include_global_state": false,
          "include_aliases": false,
          "rename_pattern": ".(.+)",
          "rename_replacement": "restored_security_$1"
        }
        ```

        Next, the restored index needs to be reindexed into the internal index, as shown:

        ```sh
        POST _reindex
        {
          "source": {
            "index": "restored_kibana"
          },
          "dest": {
            "index": ".kibana"
          }
        }
        ```


Your internal {{es}} index or indices should now be available in your new {{es}} cluster. Once verified, the `restored_*` indices are safe to delete.
