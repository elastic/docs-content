# Migrate internal indices [ech-migrate-data-internal]

When you migrate your Elasticsearch data into a new infrastructure you may also want to migrate your Elasticsearch internal indices, specifically the `.kibana` index and the `.security` index.

There are two ways to migrate the internal Elasticsearch indices:

1. Reindex the indices from a remote cluster.
2. Restore the indices from a snapshot.

To reindex internal indices from a remote cluster, you can follow the same steps that you use to reindex regular indices when you [migrate your Elasticsearch data indices](../../../manage-data/migrate.md#ech-reindex-remote).

To restore internal indices from a snapshot, the procedure is a bit different from migrating Elasticsearch data indices. Use these steps to restore internal indices from a snapshot:

1. On your old Elasticsearch cluster, choose an option to get the name of your snapshot repository bucket:

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

3. To restore internal Elasticsearch indices, you need to register the snapshot repository in `read-only` mode. To do so, first add the authentication information for the repository to the Elasticsearch Add-On for Heroku keystore, following the steps for [AWS S3](../../../deploy-manage/tools/snapshot-and-restore/ech-aws-custom-repository.md#ech-snapshot-secrets-keystore), [Google Cloud Storage](../../../deploy-manage/tools/snapshot-and-restore/ech-gcs-snapshotting.md#ech-configure-gcs-keystore), or [Azure Blog storage](../../../deploy-manage/tools/snapshot-and-restore/ech-azure-snapshotting.md#ech-configure-azure-keystore).
4. To register a read-only repository, open the Elasticsearch [API console](../../../deploy-manage/deploy/elastic-cloud/ech-api-console.md) or the Kibana [Dev Tools page](../../../explore-analyze/query-filter/tools.md) and run the [Read-only URL repository](../../../deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md) API call.
5. Once the repository has been registered and verified, you are ready to restore the internal indices to your new cluster, either all at once or individually.

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


Your internal Elasticsearch index or indices should now be available in your new Elasticsearch cluster. Once verified, the `restored_*` indices are safe to delete.
