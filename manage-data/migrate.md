---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrating-data.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrating-data.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data2.html
applies_to:
  stack: ga
  deployment:
    ess: ga
    ece: ga
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Migrate your {{es}} data

You might have switched to {{ech}} (ECH) or {{ece}} (ECE) for any number of reasons, and you’re likely wondering how to get your existing {{es}} data into your new infrastructure. Along with easily creating as many new deployments with {{es}} clusters that you need, you have several options for moving your data over. Choose the option that works best for you:

* Index your data from the original source, which is the simplest method and provides the greatest flexibility for the {{es}} version and ingestion method.
* Reindex from a remote cluster, which rebuilds the index from scratch.
* Restore from a snapshot, which copies the existing indices.

::::{note}
Although this guide focuses on migrating data from a self-managed cluster to an {{ech}} or {{ece}} deployment, the steps can also be adapted for other scenarios, such as when the source cluster is managed by {{eck}}, or when migrating from {{ece}} to {{ech}}.

If both the source and destination clusters belong to the same {{ech}} or {{ece}} environment, refer to [](/deploy-manage/tools/snapshot-and-restore/ece-restore-across-clusters.md).
::::

## Before you begin [ec_migrate_before_you_begin]

Depending on which option you choose, you might have limitations or need to do some preparation beforehand.

Indexing from the source
:   The new cluster must be the same size as your old one, or larger, to accommodate the data.

Reindex from a remote cluster
:   The new cluster must be the same size as your old one, or larger, to accommodate the data. Depending on your security settings for your old cluster, you might need to temporarily allow TCP traffic on port 9243 for this procedure.

    For {{ech}}, if your cluster is self-managed with a self-signed certificate, you can follow this [step-by-step migration guide](migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md).

Restore from a snapshot
:   The new cluster must be the same size as your old one, or larger, to accommodate the data. The new cluster must also be an Elasticsearch version that is compatible with the old cluster (check [Elasticsearch snapshot version compatibility](/deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility) for details). If you have not already done so, you will need to [set up snapshots for your old cluster](/deploy-manage/tools/snapshot-and-restore/self-managed.md) using a repository that can be accessed from the new cluster.

:::{admonition} Migrating system {{es}} indices
In {{es}} 8.0 and later versions, to back up and restore system indices and system data streams such as `.kibana` or `.security`, you must snapshot and restore the related feature's [feature state](/deploy-manage/tools/snapshot-and-restore.md#feature-state).

Refer to [Migrate system indices](./migrate/migrate-internal-indices.md) to learn how to restore the internal {{es}} system indices from a snapshot.
:::

## Index from the source [ec-index-source]

If you still have access to the original data source, outside of your old {{es}} cluster, you can load the data from there. This might be the simplest option, allowing you to choose the {{es}} version and take advantage of the latest features. You have the option to use any ingestion method that you want—Logstash, Beats, the {{es}} clients, or whatever works best for you.

If the original source isn’t available or has other issues that make it non-viable, there are still two more migration options, getting the data from a remote cluster or restoring from a snapshot.

## Reindex from a remote cluster [ech-reindex-remote]

Through the {{es}} [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex), you can connect your new {{es}} deployment remotely to your old {{es}} cluster. This pulls the data from your old cluster and indexes it into your new one. Reindexing essentially rebuilds the index from scratch and it can be more resource intensive to run than a [snapshot restore](#ec-restore-snapshots).

::::{warning}
Reindex operations do not migrate index mappings, settings, or associated index templates from the source cluster.

Before migrating your {{es}} data, define the necessary [mappings](/manage-data/data-store/mapping.md) and [templates](/manage-data/data-store/templates.md) on the new cluster. The easiest way to do this is to copy the relevant index templates from the old cluster to the new one before starting reindex operations.
::::

Follow these steps to reindex data remotely:

1. Log in to {{ech}} or {{ece}}.
2. Select a deployment or create one.
3. Ensure that the new {{es}} cluster can access the remote source cluster to perform the reindex operation. Access is controlled by the {{es}} `reindex.remote.whitelist` user setting.

    Domains matching the patterns `["*.io:*", "*.com:*"]` are allowed by default, so if your remote host URL matches that pattern you do not need to explicitly define `reindex.remote.whitelist`.

    Otherwise, if your remote endpoint is not covered by the default patterns, adjust the setting to add the remote {{es}} cluster as an allowed host:

    1. From your deployment menu, go to the **Edit** page.
    2. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node type instead.
    3. Add the following `reindex.remote.whitelist: [REMOTE_HOST:PORT]` user setting, where `REMOTE_HOST` is a pattern matching the URL for the remote {{es}} host that you are reindexing from, and PORT is the host port number. Do not include the `https://` prefix.

        Note that if you override the parameter it replaces the defaults: `["*.io:*", "*.com:*"]`. If you still want these patterns to be allowed you need to specify them explicitly in the value.

        For example:

        `reindex.remote.whitelist: ["*.us-east-1.aws.found.io:9243", "*.com:*"]`

    4. Save your changes.

4. Using the **API Console** or within {{kib}}, either create the destination index with the appropriate settings and [mappings](/manage-data/data-store/mapping.md), or ensure that the relevant [index templates](/manage-data/data-store/templates.md) are in place.

5. Using the **API Console** or [{{kib}} DevTools Console](/explore-analyze/query-filter/tools/console.md), reindex the data remotely from the old cluster:

    ```sh
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "https://<REMOTE_ELASTICSEARCH_ENDPOINT>:<PORT>",
          "username": "USER",
          "password": "PASSWORD"
        },
        "index": "INDEX_NAME",
        "query": {
          "match_all": {}
        }
      },
      "dest": {
        "index": "INDEX_NAME"
      }
    }
    ```

    For additional options and details, refer to the [reindex API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).

6. Verify that the new index is present:

    ```sh
    GET INDEX-NAME/_search?pretty
    ```

7. If you are not planning to reindex more data from the remote, you can remove the `reindex.remote.whitelist` user setting that you added previously.

## Restore from a snapshot [ec-restore-snapshots]

Restoring from a snapshot is often the fastest and most reliable way to migrate data between {{es}} clusters. It preserves mappings, settings, and optionally parts of the cluster state such as index templates, component templates, and system indices.

System indices can be restored by including their corresponding [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) in the restore operation, allowing you to retain internal configurations related to security, {{kib}}, or other stack features.

This method is especially useful when:

* You want to fully replicate the source cluster or when remote reindexing is not possible, for example if the source cluster is in a degraded or unreachable state.
* Your old cluster contains mostly static data, allowing you to snapshot the source cluster, restore in the new cluster, and continue operations.

When your source cluster is actively ingesting data, such as logs, metrics, or traces, and you need a seamless migration with minimal downtime, consider using the [minimal downtime migration](migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md).

### Requirements [ec-restore-snapshots-requirements]
* The new cluster must have access to the snapshot repository that contains the data from the old cluster.
* Both clusters must use [compatible versions](/deploy-manage/tools/snapshot-and-restore.md#snapshot-compatibility).

For more information, refer to [Restore into a different cluster](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster).

::::{note}
For {{ece}}, Amazon S3 us the most common snapshot storage, but you can restor from any accesible external storage that contains your {{es}} snapshots.
::::

### Step 1: Set up the repository in the new cluster [migrate-repo-setup]

In this step, you’ll configure a snapshot repository in the new cluster that points to the storage location used by the old cluster. This allows the new cluster to access and restore snapshots created in the original environment.

::::{tip}
If your new {{ech}} or {{ece}} deployment cannot connect to the same repository used by your self-managed cluster, for example if it's a private NFS share, consider one of the following alternatives:

* [Back up your repository](/deploy-manage/tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) to a supported storage system such as AWS S3, Google Cloud Storage, or Azure Blob Storage, and then configure your new cluster to use that location for the data migration.
* Expose the repository contents over `ftp`, `http`, or `https`, and use a [read-only URL repository](/deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md) type in your new deployment to access the snapshots.
::::

1. On your old {{es}} cluster, retrieve the snapshot repository configuration:

    ```sh
    GET /_snapshot/_all
    ```

    Take note of the repository name and type (for example, `s3`, `gcs`, or `azure`), its base path, and any additional settings. Authentication credentials are often stored in the [secure settings](/deploy-manage/security/secure-settings.md) on each node. You’ll need to replicate all this configuration when registering the repository in the new ECH or ECE deployment.

    If your old cluster has multiple repositories configured, identify the repository with the snapshots containing the data that you want to migrate.

2. Add the snapshot repository on the new cluster.

    Considerations:

      * If you’re migrating [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md), the repository name must be identical in the source and destination clusters.
      * If the old cluster still has write access to the repository, register the repository as read-only to avoid data corruption. This can be done using the `readonly: true` option.

    To connect the existing snapshot repository to your new deployment, follow the steps for the storage provider where the repository is hosted:

    * **Amazon Web Services (AWS) Storage**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md#ec-snapshot-secrets-keystore)
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md#ec-create-aws-repository)
    * **Google Cloud Storage (GCS)**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md#ec-configure-gcs-keystore)
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md#ec-create-gcs-repository)
    * **Azure Blob Storage**
        * [Store credentials in the keystore](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md#ec-configure-azure-keystore).
        * [Create the repository](/deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md#ec-create-azure-repository).

    ::::{important}
    Although these instructions are focused on {{ech}}, you should follow the same steps for {{ece}} by configuring the repository directly **at the deployment level**.

    **Do not** configure the repository as an [ECE-managed repository](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), which is intended for automatic snapshots of deployments. In this case, you need to add a custom repository that already contains snapshots from another cluster.
    ::::


### Step 2: Run the snapshot restore [migrate-restore]

After the repository has been registered and verified, you are ready to restore any data from any of its snapshots to your new cluster.

You can run a restore operation using the {{kib}} Management UI, or using the {{es}} API. Refer to [Restore a snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) for more details, including API-based examples.

For details about the contents of a snapshot, refer to [](/deploy-manage/tools/snapshot-and-restore.md#snapshot-contents).

To start the restore process:

1. Open Kibana and go to the **Snapshot and Restore** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Snapshots** tab, you can find the available snapshots from your newly added snapshot repository. Select any snapshot to view its details, and from there you can choose to restore it.
3. Select **Restore**.
4. Select the index or indices you wish to restore.
5. Optionally, configure additional restore options, such as **Restore aliases**, **Restore global state**, or **Restore feature state**.
6. Select **Restore snapshot** to begin the process.

7. Verify that each restored index is available in your deployment. You can do this using {{kib}} **Index Management** UI, or by running this query:

    ```sh
    GET INDEX_NAME/_search?pretty
    ```

    If you have restored many indices you can also run `GET _cat/indices?s=index` to list all indices for verification.
