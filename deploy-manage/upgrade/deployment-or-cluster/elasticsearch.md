---
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Upgrade {{es}} [upgrading-elasticsearch]

This document provides the detailed steps for performing a rolling upgrade of a self-managed {{es}} cluster. A rolling upgrade allows you to upgrade your cluster one node at a time without interrupting service. Running multiple versions of {{es}} in the same cluster beyond the duration of an upgrade is not supported, as shards cannot be replicated from upgraded nodes to nodes running the older version.

:::{note}
Upgrading from a release candidate build, such as 9.0.0-rc1, is unsupported. Use pre-releases only for testing in a temporary environment.
:::

Before you start the rolling upgrade procedure, [plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md) and [take the upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md).

## {{es}} nodes upgrade order

When performing a [rolling upgrade](#rolling-upgrades):

1. Upgrade the data nodes first, tier-by-tier, in the following order: 
    1. The frozen tier
    2. The cold tier
    3. The warm tier
    4. The hot tier
    5. Any other data nodes which are not in a tier.
    
    Complete the upgrade for all nodes in each data tier before moving to the next. This ensures {{ilm-init}} can continue to move data through the tiers during the upgrade. You can get the list of nodes in a specific tier with a `GET /_nodes` request, for example: `GET /_nodes/data_frozen:true/_none`.
2. Upgrade all remaining nodes that are neither master-eligible nor data nodes. This includes dedicated ML nodes, dedicated ingest nodes, and dedicated coordinating nodes.
3. Upgrade the master-eligible nodes last. You can retrieve a list of these nodes with `GET /_nodes/master:true/_none`.

This order ensures that all nodes can join the cluster during the upgrade. Upgraded nodes can join a cluster with an older master, but older nodes cannot always join a cluster with a upgraded master.

## Upgrade process

To upgrade a cluster:

1. **Disable shard allocation**.

    When you shut down a data node, the allocation process waits for `index.unassigned.node_left.delayed_timeout` (by default, one minute) before starting to replicate the shards on that node to other nodes in the cluster, which can involve a lot of I/O. Since the node is shortly going to be restarted, this I/O is unnecessary. You can avoid racing the clock by [disabling allocation](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) of replicas before shutting down [data nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#data-node):

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": "primaries"
      }
    }
    ```

2. **Stop non-essential indexing and perform a flush.** (Optional)

    While you can continue indexing during the upgrade, shard recovery is much faster if you temporarily stop non-essential indexing and perform a [flush](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush).

    ```console
    POST /_flush
    ```

3. **Temporarily stop the tasks associated with active {{ml}} jobs and {{dfeeds}}.** (Optional)

    It is possible to leave your {{ml}} jobs running during the upgrade, but it puts increased load on the cluster. When you shut down a {{ml}} node, its jobs automatically move to another node and restore the model states.

    ::::{note}
    Any {{ml}} indices created before 8.x must be reindexed before upgrading, which you can initiate from the **Upgrade Assistant** in 8.19. For more information, refer to [Anomaly detection results migration]
    ::::

    * Temporarily halt the tasks associated with your {{ml}} jobs and {{dfeeds}} and prevent new jobs from opening by using the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode):

        ```console
        POST _ml/set_upgrade_mode?enabled=true
        ```

        When you disable upgrade mode, the jobs resume using the last model state that was automatically saved. This option avoids the overhead of managing active jobs during the upgrade and is faster than explicitly stopping {{dfeeds}} and closing jobs.

    * [Stop all {{dfeeds}} and close all jobs](../../../explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-close-job). This option saves the model state at the time of closure. When you reopen the jobs after the upgrade, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states.

4. $$$upgrade-node$$$ **Shut down a single node**.

    To shut down a single node depends on what is currently used to run {{es}}. For example, if using `systemd` or SysV `init` run the commands below.

    * If you are running {{es}} with `systemd`:

        ```sh
        sudo systemctl stop elasticsearch.service
        ```

    * If you are running {{es}} with SysV `init`:

        ```sh
        sudo -i service elasticsearch stop
        ```

5. **Upgrade the node you shut down.**

    To upgrade using a [Debian](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md) or [RPM](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md) package:

    * Use `rpm` or `dpkg` to install the new package. All files are installed in the appropriate location for the operating system and {{es}} config files are not overwritten.

    To upgrade using a zip or compressed tarball:

    1. Extract the zip or tarball to a **new** directory. This is critical if you are not using external `config` and `data` directories.
    2. Set the `ES_PATH_CONF` environment variable to specify the location of your external `config` directory and `jvm.options` file. If you are not using an external `config` directory, copy your old configuration over to the new installation.
    3. Set `path.data` in `config/elasticsearch.yml` to point to your external data directory. If you are not using an external `data` directory, copy your old data directory over to the new installation.<br>

        ::::{important}
        If you use {{monitor-features}}, re-use the data directory when you upgrade {{es}}. Monitoring identifies unique {{es}} nodes by using the persistent UUID, which is stored in the data directory.
        ::::

    4. Set `path.logs` in `config/elasticsearch.yml` to point to the location where you want to store your logs. If you do not specify this setting, logs are stored in the directory you extracted the archive to.

    ::::{tip}
    When you extract the zip or tarball packages, the `elasticsearch-{{bare_version}}` directory contains the {{es}} `config`, `data`, and `logs` directories.

    We recommend moving these directories out of the {{es}} directory so that there is no chance of deleting them when you upgrade {{es}}. To specify the new locations, use the `ES_PATH_CONF` environment variable and the `path.data` and `path.logs` settings. For more information, refer to [Important {{es}} configuration](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md).

    The Debian and RPM packages place these directories in the appropriate place for each operating system. In production, we recommend using the deb or rpm package.

    ::::


    $$$rolling-upgrades-bootstrapping$$$
    Leave `cluster.initial_master_nodes` unset when performing a rolling upgrade. Each upgraded node is joining an existing cluster so there is no need for [cluster bootstrapping](../../../deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md). You must configure [either `discovery.seed_hosts` or `discovery.seed_providers`](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md#discovery-settings) on every node.

6. **Upgrade any plugins.**

    Use the `elasticsearch-plugin` script to install the upgraded version of each installed {{es}} plugin. All plugins must be upgraded when you upgrade a node.

7. **Start the upgraded node.**

    Start the newly-upgraded node and confirm that it joins the cluster by checking the log file or by submitting a `_cat/nodes` request:

    ```console
    GET _cat/nodes
    ```

8. **Reenable shard allocation.**

    For data nodes, once the node has joined the cluster, remove the `cluster.routing.allocation.enable` setting to enable shard allocation and start using the node:

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": null
      }
    }
    ```

9. **Wait for the node to recover.**

    Before upgrading the next node, wait for the cluster to finish shard allocation. You can check progress by submitting a `_cat/health` request:

    ```console
    GET _cat/health?v=true
    ```

    Wait for the `status` column to switch to `green`. Once the node is `green`, all primary and replica shards have been allocated.

    ::::{important}
    During a rolling upgrade, primary shards assigned to a node running the new version cannot have their replicas assigned to a node with the old version. The new version might have a different data format that is not understood by the old version.

    If it is not possible to assign the replica shards to another node (there is only one upgraded node in the cluster), the replica shards remain unassigned and status stays `yellow`.

    In this case, you can proceed once there are no initializing or relocating shards (check the `init` and `relo` columns).

    As soon as another node is upgraded, the replicas can be assigned and the status will change to `green`.

    ::::


    Shards that were not flushed might take longer to recover. You can monitor the recovery status of individual shards by submitting a `_cat/recovery` request:

    ```console
    GET _cat/recovery
    ```

    If you stopped indexing, it is safe to resume indexing as soon as recovery completes.

10. **Repeat**.

    When the node has recovered and the cluster is stable, repeat these steps for each node that needs to be updated. You can monitor the health of the cluster with a `_cat/health` request:

    ```console
    GET /_cat/health?v=true
    ```

    And check which nodes have been upgraded with a `_cat/nodes` request:

    ```console
    GET /_cat/nodes?h=ip,name,version&v=true
    ```

11. **Restart machine learning jobs.**

    If you temporarily halted the tasks associated with your {{ml}} jobs, use the set upgrade mode API to return them to active states:

    ```console
    POST _ml/set_upgrade_mode?enabled=false
    ```

    If you closed all {{ml}} jobs before the upgrade, open the jobs and start the datafeeds from {{kib}} or with the [open jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-open-job) and [start datafeed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-datafeed) APIs.



## Rolling upgrades considerations [rolling-upgrades]

During a rolling upgrade, the cluster continues to operate normally. However, any new functionality is disabled or operates in a backward compatible mode until all nodes in the cluster are upgraded. New functionality becomes operational once the upgrade is complete and all nodes are running the new version. Once that has happened, there’s no way to return to operating in a backward compatible mode. Nodes running the previous version will not be allowed to join the fully-updated cluster.

In the unlikely case of a network malfunction during the upgrade process that isolates all remaining old nodes from the cluster, you must take the old nodes offline and upgrade them to enable them to join the cluster.

If you stop half or more of the master-eligible nodes all at once during the upgrade the cluster will become unavailable. You must upgrade and restart all of the stopped master-eligible nodes to allow the cluster to re-form. It might also be necessary to upgrade all other nodes running the old version to enable them to join the re-formed cluster.

Similarly, if you run a testing/development environment with a single master node it should be upgraded last. Restarting a single master node forces the cluster to be reformed. The new cluster will initially only have the upgraded master node and will thus reject the older nodes when they re-join the cluster. Nodes that have already been upgraded will successfully re-join the upgraded master.


## Archived settings [archived-settings]

If you upgrade an {{es}} cluster that uses deprecated cluster or index settings that are not used in the target version, they are archived. We recommend you remove any archived settings after upgrading. For more information, refer to [Archived settings](../../../deploy-manage/upgrade/deployment-or-cluster/archived-settings.md).

## Next steps

Once you've successfully upgraded {{es}}, continue upgrading the remaining {{stack}} components:
* [{{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana.md)
* [Elastic APM](/solutions/observability/apm/upgrade.md)
* [Ingest components](/deploy-manage/upgrade/ingest-components.md)