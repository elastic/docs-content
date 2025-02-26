# Restore a snapshot [snapshots-restore-snapshot]

This guide shows you how to restore a snapshot. Snapshots are a convenient way to store a copy of your data outside of a cluster. You can restore a snapshot to recover indices and data streams after deletion or a hardware failure. You can also use snapshots to transfer data between clusters.

In this guide, you’ll learn how to:

* Get a list of available snapshots
* Restore an index or data stream from a snapshot
* Restore a feature state
* Restore an entire cluster
* Monitor the restore operation
* Cancel an ongoing restore

This guide also provides tips for [restoring to another cluster](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster) and [troubleshooting common restore errors](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#troubleshoot-restore).


## Prerequisites [restore-snapshot-prereqs]

* To use {{kib}}'s **Snapshot and Restore** feature, you must have the following permissions:

    * [Cluster privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `all` on the `monitor` index

* You can only restore a snapshot to a running cluster with an elected [master node](../../../deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role). The snapshot’s repository must be [registered](../../../deploy-manage/tools/snapshot-and-restore/self-managed.md) and available to the cluster.
* The snapshot and cluster versions must be compatible. See [Snapshot compatibility](../../../deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility).
* To restore a snapshot, the cluster’s global metadata must be writable. Ensure there aren’t any [cluster blocks](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-read-only) that prevent writes. The restore operation ignores [index blocks](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-block.md).
* Before you restore a data stream, ensure the cluster contains a [matching index template](../../../manage-data/data-store/data-streams/set-up-data-stream.md#create-index-template) with data stream enabled. To check, use {{kib}}'s [**Index Management**](../../../manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md#manage-index-templates) feature or the [get index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-index-template):

    ```console
    GET _index_template/*?filter_path=index_templates.name,index_templates.index_template.index_patterns,index_templates.index_template.data_stream
    ```

    If no such template exists, you can [create one](../../../manage-data/data-store/data-streams/set-up-data-stream.md#create-index-template) or [restore a cluster state](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-entire-cluster) that contains one. Without a matching index template, a data stream can’t roll over or create backing indices.

* If your snapshot contains data from App Search or Workplace Search, ensure you’ve restored the [Enterprise Search encryption key](https://www.elastic.co/guide/en/enterprise-search/current/encryption-keys.html) before restoring the snapshot.
:::{important}
Enterprise Search is not available in {{stack}} 9.0+.
:::


## Considerations [restore-snapshot-considerations]

When restoring data from a snapshot, keep the following in mind:

* If you restore a data stream, you also restore its backing indices.
* You can only restore an existing index if it’s [closed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close) and the index in the snapshot has the same number of primary shards.
* You can’t restore an existing open index. This includes backing indices for a data stream.
* The restore operation automatically opens restored indices, including backing indices.
* You can restore only a specific backing index from a data stream. However, the restore operation doesn’t add the restored backing index to any existing data stream.


## Get a list of available snapshots [get-snapshot-list]

To view a list of available snapshots in {{kib}}, go to the main menu and click **Stack Management > Snapshot and Restore**.

You can also use the [get repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get-repository) and the [get snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-get) to find snapshots that are available to restore. First, use the get repository API to fetch a list of registered snapshot repositories.

```console
GET _snapshot
```

Then use the get snapshot API to get a list of snapshots in a specific repository. This also returns each snapshot’s contents.

```console
GET _snapshot/my_repository/*?verbose=false
```


## Restore an index or data stream [restore-index-data-stream]

You can restore a snapshot using {{kib}}'s **Snapshot and Restore** feature or the [restore snapshot API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore).

By default, a restore request attempts to restore all regular indices and regular data streams in a snapshot. In most cases, you only need to restore a specific index or data stream from a snapshot. However, you can’t restore an existing open index.

If you’re restoring data to a pre-existing cluster, use one of the following methods to avoid conflicts with existing indices and data streams:

* [Delete and restore](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#delete-restore)
* [Rename on restore](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#rename-on-restore)


### Delete and restore [delete-restore]

The simplest way to avoid conflicts is to delete an existing index or data stream before restoring it. To prevent the accidental re-creation of the index or data stream, we recommend you temporarily stop all indexing until the restore operation is complete.

::::{warning}
If the [`action.destructive_requires_name`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/index-management-settings.md#action-destructive-requires-name) cluster setting is `false`, don’t use the [delete index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete) to target the `*` or `.*` wildcard pattern. If you use {{es}}'s security features, this will delete system indices required for authentication. Instead, target the `*,-.*` wildcard pattern to exclude these system indices and other index names that begin with a dot (`.`).
::::


```console
# Delete an index
DELETE my-index

# Delete a data stream
DELETE _data_stream/logs-my_app-default
```

In the restore request, explicitly specify any indices and data streams to restore.

```console
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default"
}
```


### Rename on restore [rename-on-restore]

If you want to avoid deleting existing data, you can instead rename the indices and data streams you restore. You typically use this method to compare existing data to historical data from a snapshot. For example, you can use this method to review documents after an accidental update or deletion.

Before you start, ensure the cluster has enough capacity for both the existing and restored data.

The following restore snapshot API request prepends `restored-` to the name of any restored index or data stream.

```console
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default",
  "rename_pattern": "(.+)",
  "rename_replacement": "restored-$1"
}
```

If the rename options produce two or more indices or data streams with the same name, the restore operation fails.

If you rename a data stream, its backing indices are also renamed. For example, if you rename the `logs-my_app-default` data stream to `restored-logs-my_app-default`, the backing index `.ds-logs-my_app-default-2099.03.09-000005` is renamed to `.ds-restored-logs-my_app-default-2099.03.09-000005`.

When the restore operation is complete, you can compare the original and restored data. If you no longer need an original index or data stream, you can delete it and use a [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) to rename the restored one.

```console
# Delete the original index
DELETE my-index

# Reindex the restored index to rename it
POST _reindex
{
  "source": {
    "index": "restored-my-index"
  },
  "dest": {
    "index": "my-index"
  }
}

# Delete the original data stream
DELETE _data_stream/logs-my_app-default

# Reindex the restored data stream to rename it
POST _reindex
{
  "source": {
    "index": "restored-logs-my_app-default"
  },
  "dest": {
    "index": "logs-my_app-default",
    "op_type": "create"
  }
}
```


## Restore a feature state [restore-feature-state]

You can restore a [feature state](../../../deploy-manage/tools/snapshot-and-restore.md#feature-state) to recover system indices, system data streams, and other configuration data for a feature from a snapshot.

If you restore a snapshot’s cluster state, the operation restores all feature states in the snapshot by default. Similarly, if you don’t restore a snapshot’s cluster state, the operation doesn’t restore any feature states by default. You can also choose to restore only specific feature states from a snapshot, regardless of the cluster state.

To view a snapshot’s feature states, use the get snapshot API.

```console
GET _snapshot/my_repository/my_snapshot_2099.05.06
```

The response’s `feature_states` property contains a list of features in the snapshot as well as each feature’s indices.

To restore a specific feature state from the snapshot, specify the `feature_name` from the response in the restore snapshot API’s [`feature_states`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore) parameter.

::::{note}
When you restore a feature state, {{es}} closes and overwrites the feature’s existing indices.
::::


::::{warning}
Restoring the `security` feature state overwrites system indices used for authentication. If you use {{ech}}, ensure you have access to the {{ecloud}} Console before restoring the `security` feature state. If you run {{es}} on your own hardware, [create a superuser in the file realm](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-create-file-realm-user) to ensure you’ll still be able to access your cluster.
::::


```console
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "feature_states": [ "geoip" ],
  "include_global_state": false,    <1>
  "indices": "-*"                   <2>
}
```

1. Exclude the cluster state from the restore operation.
2. Exclude the other indices and data streams in the snapshot from the restore operation.



## Restore an entire cluster [restore-entire-cluster]

In some cases, you need to restore an entire cluster from a snapshot, including the cluster state and all [feature states](../../../deploy-manage/tools/snapshot-and-restore.md#feature-state). These cases should be rare, such as in the event of a catastrophic failure.

Restoring an entire cluster involves deleting important system indices, including those used for authentication. Consider whether you can restore specific indices or data streams instead.

If you’re restoring to a different cluster, see [Restore to a different cluster](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-different-cluster) before you start.

1. If you [backed up the cluster’s configuration files](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#back-up-config-files), you can restore them to each node. This step is optional and requires a [full cluster restart](../../../deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md).

    After you shut down a node, copy the backed-up configuration files over to the node’s `$ES_PATH_CONF` directory. Before restarting the node, ensure `elasticsearch.yml` contains the appropriate node roles, node name, and other node-specific settings.

    If you choose to perform this step, you must repeat this process on each node in the cluster.

2. Temporarily stop indexing and turn off the following features:

    * GeoIP database downloader and ILM history store

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "ingest.geoip.downloader.enabled": false,
            "indices.lifecycle.history_index_enabled": false
          }
        }
        ```

    * ILM

        ```console
        POST _ilm/stop
        ```


    * Machine Learning

        ```console
        POST _ml/set_upgrade_mode?enabled=true
        ```


    * Monitoring

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": false
          }
        }
        ```

    * Watcher

        ```console
        POST _watcher/_stop
        ```


    * Universal Profiling

        Check if Universal Profiling index template management is enabled:

        ```console
        GET /_cluster/settings?filter_path=**.xpack.profiling.templates.enabled&include_defaults=true
        ```

        If the value is `true`, disable Universal Profiling index template management:

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.profiling.templates.enabled": false
          }
        }
        ```

3. $$$restore-create-file-realm-user$$$If you use {{es}} security features, log in to a node host, navigate to the {{es}} installation directory, and add a user with the `superuser` role to the file realm using the [`elasticsearch-users`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/users-command.md) tool.

    For example, the following command creates a user named `restore_user`.

    ```sh
    ./bin/elasticsearch-users useradd restore_user -p my_password -r superuser
    ```

    Use this file realm user to authenticate requests until the restore operation is complete.

4. Use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to set [`action.destructive_requires_name`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/index-management-settings.md#action-destructive-requires-name) to `false`. This lets you delete data streams and indices using wildcards.

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "action.destructive_requires_name": false
      }
    }
    ```

5. Delete all existing data streams on the cluster.

    ```console
    DELETE _data_stream/*?expand_wildcards=all
    ```

6. Delete all existing indices on the cluster.

    ```console
    DELETE *?expand_wildcards=all
    ```

7. Restore the entire snapshot, including the cluster state. By default, restoring the cluster state also restores any feature states in the snapshot.

    ```console
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "*",
      "include_global_state": true
    }
    ```

8. When the restore operation is complete, resume indexing and restart any features you stopped:

    ::::{note}
    When the snapshot is restored, the license that was in use at the time the snapshot was taken will be restored as well. If your license has expired since the snapshot was taken, you will need to use the [Update License API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-license-post) to install a current license.
    ::::


    * GeoIP database downloader and ILM history store

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "ingest.geoip.downloader.enabled": true,
            "indices.lifecycle.history_index_enabled": true
          }
        }
        ```

    * ILM

        ```console
        POST _ilm/start
        ```

    * Machine Learning

        ```console
        POST _ml/set_upgrade_mode?enabled=false
        ```

    * Monitoring

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }
        ```

    * Watcher

        ```console
        POST _watcher/_start
        ```


    * Universal Profiling

        If the value was `true` initially, enable Universal Profiling index template management again, otherwise skip this step:

        ```console
        PUT _cluster/settings
        {
          "persistent": {
            "xpack.profiling.templates.enabled": true
          }
        }
        ```

9. If wanted, reset the `action.destructive_requires_name` cluster setting.

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "action.destructive_requires_name": null
      }
    }
    ```



## Monitor a restore [monitor-restore]

The restore operation uses the [shard recovery process](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-recovery) to restore an index’s primary shards from a snapshot. While the restore operation recovers primary shards, the cluster will have a `yellow` [health status](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health).

After all primary shards are recovered, the replication process creates and distributes replicas across eligible data nodes. When replication is complete, the cluster health status typically becomes `green`.

Once you start a restore in {{kib}}, you’re navigated to the **Restore Status** page. You can use this page to track the current state for each shard in the snapshot.

You can also monitor snapshot recover using {{es}} APIs. To monitor the cluster health status, use the [cluster health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health).

```console
GET _cluster/health
```

To get detailed information about ongoing shard recoveries, use the [index recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-recovery).

```console
GET my-index/_recovery
```

To view any unassigned shards, use the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards).

```console
GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state
```

Unassigned shards have a `state` of `UNASSIGNED`. The `prirep` value is `p` for primary shards and `r` for replicas. The `unassigned.reason` describes why the shard remains unassigned.

To get a more in-depth explanation of an unassigned shard’s allocation status, use the [cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain).

```console
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 0,
  "primary": false,
  "current_node": "my-node"
}
```


## Cancel a restore [cancel-restore]

You can delete an index or data stream to cancel its ongoing restore. This also deletes any existing data in the cluster for the index or data stream. Deleting an index or data stream doesn’t affect the snapshot or its data.

```console
# Delete an index
DELETE my-index

# Delete a data stream
DELETE _data_stream/logs-my_app-default
```


## Restore to a different cluster [restore-different-cluster]

::::{tip}
{{ech}} can help you restore snapshots from other deployments. See [Work with snapshots](../../../deploy-manage/tools/snapshot-and-restore.md).
::::


Snapshots aren’t tied to a particular cluster or a cluster name. You can create a snapshot in one cluster and restore it in another [compatible cluster](../../../deploy-manage/tools/snapshot-and-restore.md#snapshot-restore-version-compatibility). Any data stream or index you restore from a snapshot must also be compatible with the current cluster’s version. The topology of the clusters doesn’t need to match.

To restore a snapshot, its repository must be [registered](../../../deploy-manage/tools/snapshot-and-restore/self-managed.md) and available to the new cluster. If the original cluster still has write access to the repository, register the repository as read-only. This prevents multiple clusters from writing to the repository at the same time and corrupting the repository’s contents. It also prevents {{es}} from caching the repository’s contents, which means that changes made by other clusters will become visible straight away.

Before you start a restore operation, ensure the new cluster has enough capacity for any data streams or indices you want to restore. If the new cluster has a smaller capacity, you can:

* Add nodes or upgrade your hardware to increase capacity.
* Restore fewer indices and data streams.
* Reduce the [number of replicas](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) for restored indices.

    For example, the following restore snapshot API request uses the `index_settings` option to set `index.number_of_replicas` to `1`.

    ```console
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "my-index,logs-my_app-default",
      "index_settings": {
        "index.number_of_replicas": 1
      }
    }
    ```


If indices or backing indices in the original cluster were assigned to particular nodes using [shard allocation filtering](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md), the same rules will be enforced in the new cluster. If the new cluster does not contain nodes with appropriate attributes that a restored index can be allocated on, the index will not be successfully restored unless these index allocation settings are changed during the restore operation.

The restore operation also checks that restored persistent settings are compatible with the current cluster to avoid accidentally restoring incompatible settings. If you need to restore a snapshot with incompatible persistent settings, try restoring it without the [global cluster state](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-restore).


## Troubleshoot restore errors [troubleshoot-restore]

Here’s how to resolve common errors returned by restore requests.


### Cannot restore index [<index>] because an open index with same name already exists in the cluster [_cannot_restore_index_index_because_an_open_index_with_same_name_already_exists_in_the_cluster]

You can’t restore an open index that already exists. To resolve this error, try one of the methods in [Restore an index or data stream](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-index-data-stream).


### Cannot restore index [<index>] with [x] shards from a snapshot of index [<snapshot-index>] with [y] shards [_cannot_restore_index_index_with_x_shards_from_a_snapshot_of_index_snapshot_index_with_y_shards]

You can only restore an existing index if it’s closed and the index in the snapshot has the same number of primary shards. This error indicates the index in the snapshot has a different number of primary shards.

To resolve this error, try one of the methods in [Restore an index or data stream](../../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md#restore-index-data-stream).
