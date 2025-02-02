---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data2.html
---

# Migrate your Elasticsearch data [ech-migrate-data2]

You might have switched to Elasticsearch Add-On for Heroku for any number of reasons and you’re likely wondering how to get your existing Elasticsearch data into your new infrastructure. Along with easily creating as many new deployments with Elasticsearch clusters that you need, you have several options for moving your data over. Choose the option that works best for you:

* Index your data from the original source, which is the simplest method and provides the greatest flexibility for the Elasticsearch version and ingestion method.
* Reindex from a remote cluster, which rebuilds the index from scratch.
* Restore from a snapshot, which copies the existing indices.

One of the many advantages of Elasticsearch Add-On for Heroku is that you can spin up a deployment quickly, try out something, and then delete it if you don’t like it. This flexibility provides the freedom to experiment while your existing production cluster continues to work.


## Before you begin [echbefore_you_begin_3]

Depending on which option that you choose, you might have limitations or need to do some preparation beforehand.

Indexing from the source
:   The new cluster must be the same size as your old one, or larger, to accommodate the data.

Reindex from a remote cluster
:   The new cluster must be the same size as your old one, or larger, to accommodate the data. Depending on your security settings for your old cluster, you might need to temporarily allow TCP traffic on port 9243 for this procedure.

Restore from a snapshot
:   The new cluster must be the same size as your old one, or larger, to accommodate the data. The new cluster must also be an Elasticsearch version that is compatible with the old cluster (check [Elasticsearch snapshot version compatibility](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html#snapshot-restore-version-compatibility) for details). If you have not already done so, you will need to [set up snapshots for your old cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html) using a repository that can be accessed from the new cluster.

Migrating internal Elasticsearch indices
:   If you are migrating internal Elasticsearch indices from another cluster, specifically the `.kibana` index or the `.security` index, there are two options:

    * Use the steps on this page to reindex the internal indices from a remote cluster. The steps for reindexing internal indices and regular, data indices are the same.
    * Check [Migrating internal indices](../../../manage-data/migrate/migrate-internal-indices.md) to restore the internal Elasticsearch indices from a snapshot.


::::{warning}
Before you migrate your Elasticsearch data, [define your index mappings](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) on the new cluster. Index mappings are unable to migrate during reindex operations.
::::



## Index from the source [ech-index-source]

If you still have access to the original data source, outside of your old Elasticsearch cluster, you can load the data from there. This might be the simplest option, allowing you to choose the Elasticsearch version and take advantage of the latest features. You have the option to use any ingestion method that you want—​Logstash, Beats, the Elasticsearch clients, or whatever works best for you.

If the original source isn’t available or has other issues that make it non-viable, there are still two more migration options, getting the data from a remote cluster or restoring from a snapshot.


## Reindex from a remote cluster [ech-reindex-remote]

Through the Elasticsearch reindex API, you can connect your new Elasticsearch Add-On for Heroku deployment remotely to your old Elasticsearch cluster. This pulls the data from your old cluster and indexes it into your new one. Reindexing essentially rebuilds the index from scratch and it can be more resource intensive to run.

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Select a deployment or create one.
3. If the old Elasticsearch cluster is on a remote host (any type of host accessible over the internet), you need to make sure that the host can be accessed. Access is determined by the Elasticsearch `reindex.remote.whitelist` user setting.

    Domains matching the pattern `["*.io:*", "*.com:*"]` are allowed by default, so if your remote host URL matches that pattern you do not need to explicitly define `reindex.remote.whitelist`.

    Otherwise, if your remote endpoint is not covered by the default settings, adjust the setting to add the remote Elasticsearch cluster as an allowed host:

    1. From your deployment menu, go to the **Edit** page.
    2. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node type instead.
    3. Add the following `reindex.remote.whitelist: [REMOTE_HOST:PORT]` user setting, where `REMOTE_HOST` is a pattern matching the URL for the remote Elasticsearch host that you are reindexing from, and PORT is the host port number. Do not include the `https://` prefix.

        Note that if you override the parameter it replaces the defaults: `["*.io:*", "*.com:*"]`. If you still want these patterns to be allowed you need to specify them explicitly in the value.

        For example:

        `reindex.remote.whitelist: ["*.us-east-1.aws.found.io:9243", "*.com:*"]`

    4. Save your changes.

4. From the **API Console** or in the Kibana Console app, create the destination index on Elasticsearch Add-On for Heroku.
5. Copy the index from the remote cluster:

    ```sh
    POST _reindex
    {
      "source": {
        "remote": {
          "host": "https://REMOTE_ELASTICSEARCH_ENDPOINT:PORT",
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

6. Verify that the new index is present:

    ```sh
    GET INDEX-NAME/_search?pretty
    ```

7. You can remove the reindex.remote.whitelist user setting that you added previously.


## Restore from a snapshot [ech-restore-snapshots]

If you cannot connect to a remote index for whatever reason, such as if it’s in a non-working state, you can try restoring from the most recent working snapshot.

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

3. From the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body) of the **new** Elasticsearch cluster, add the snapshot repository. For details, check our guidelines for [Amazon Web Services (AWS) Storage](../../tools/snapshot-and-restore/ech-aws-custom-repository.md), [Google Cloud Storage (GCS)](../../tools/snapshot-and-restore/ech-gcs-snapshotting.md), or [Azure Blob Storage](../../tools/snapshot-and-restore/ech-azure-snapshotting.md).

    ::::{important}
    If you’re migrating [searchable snapshots](../../tools/snapshot-and-restore/searchable-snapshots.md), the repository name must be identical in the source and destination clusters.
    ::::


    ::::{important}
    If source cluster is still writing to the repository, you need to set the destination cluster’s repository connection to `readonly:true` to avoid data corruption. Refer to [backup a repository](../../tools/snapshot-and-restore/self-managed.md#snapshots-repository-backup) for details.
    ::::

4. Start the Restore process.

    1. Open Kibana and go to **Management** > **Snapshot and Restore**.
    2. Under the **Snapshots** tab, you can find the available snapshots from your newly added snapshot repository. Select any snapshot to view its details, and from there you can choose to restore it.
    3. Select **Restore**.
    4. Select the indices you wish to restore.
    5. Configure any additional index settings.
    6. Select **Restore snapshot** to begin the process.

5. Verify that the new index is restored in your Elasticsearch Add-On for Heroku deployment with this query:

    ```sh
    GET INDEX_NAME/_search?pretty
    ```



