---
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Upgrade {{es}} [upgrading-elasticsearch]

This guide outlines the detailed steps for performing an upgrade of a self-managed {{es}} cluster from an earlier to a later version.

:::{tip}
The Elastic Cloud platform handles cluster management and upgrades automatically, so you don't need to follow the steps in this guide on cloud deployments such as {{ECK}}, {{ECH}}, {{ECE}}, or {{serverless-full}}.

If you want to use these automated platform features, consider deploying your {{es}} cluster using one of the available [cloud deployment methods](/deploy-manage/deploy.md#choosing-your-deployment-type). Refer to [migrating your data](/manage-data/migrate.md) to port existing self-managed clusters to Elastic-managed.
:::

Before you start the rolling upgrade procedure, [plan your upgrade](/deploy-manage/upgrade/plan-upgrade.md) and [take the upgrade preparation steps](/deploy-manage/upgrade/prepare-to-upgrade.md). 

Upgrading from a release candidate build such as `9.0.0-rc1` is not supported. Use pre-releases only for testing in a temporary environment.

{{es}} does not support downgrading to an earlier version. A mixed-version cluster is only valid during a rolling upgrade. After at least one node runs the target version, the cluster may perform updates that you can't roll back, so you must run the same upgrade through to the last node.
 
Do not start an upgrade unless you can finish the rolling upgrade for every node. 
If you have to stop mid-upgrade, you cannot return the existing cluster to the earlier version. Instead, you can rebuild an empty cluster of the earlier version and [restore from a snapshot](/deploy-manage/upgrade/prepare-to-upgrade.md#create-a-snapshot-for-backup).

Cluster upgrades can be performed as:

* _(Recommended)_ **A rolling restart**

    This option allows you to upgrade your cluster one node at a time without interrupting service. Running multiple versions of {{es}} in the same cluster beyond the duration of an upgrade is not supported, as shards cannot be replicated from upgraded nodes to nodes running the earlier version. Running more than two versions of {{es}} in the same cluster is not supported.

* **A full restart**

    This option requires that you upgrade every node in a coordinated way by taking your cluster offline: all nodes are stopped, upgraded, and started together. Without [high availability](/deploy-manage/production-guidance/availability-and-resilience.md) during the downtime, data loss is possible if the upgrade process is insufficiently managed.

The following guide describes rolling restarts as the main upgrade path, which is the  default method for production environments. You can use the same workflow for full restart upgrades, except you upgrade all nodes simultaneously.

## Nodes upgrade order [upgrade-order]

When performing a rolling upgrade, upgrade one node at a time in the order of the  [node role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) groupings below. If a node is assigned multiple node roles, it belongs in the first applicable group in the list. This ensures that:

* Built-in plugins, such as {{ilm-init}} and transforms, can continue to process data without errors.
* All nodes can join the cluster during the upgrade. Upgraded nodes can join a cluster with an earlier version master, but earlier version nodes cannot always join a cluster with an upgraded master.

The recommended upgrade order for {{es}} nodes is the following:

1. Upgrade the [`data` nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role) first, tier-by-tier, in the following order:

    1. The [`data_frozen` tier](/manage-data/lifecycle/data-tiers.md#frozen-tier).
    2. The [`data_cold` tier](/manage-data/lifecycle/data-tiers.md#cold-tier).
    3. The [`data_warm` tier](/manage-data/lifecycle/data-tiers.md#warm-tier).
    4. The [`data_hot` tier](/manage-data/lifecycle/data-tiers.md#hot-tier).
    5. Any other `data` nodes, such as [`data_content` tier](/manage-data/lifecycle/data-tiers.md#content-tier), which are not in a data tier.

2. Upgrade all remaining nodes that are neither master-eligible nor data nodes. The order within this grouping does not matter. This includes nodes with the following roles:

    * The [`ml` machine learning role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role).
    * The [`ingest` role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#node-ingest-node).
    * Any [dedicated coordinating nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#coordinating-only-node-role).
    * The [`transform` role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#transform-node-role).
    * The [`remote_cluster_client` role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#remote-node).

3. Upgrade the [`master` and `voting_only` master-eligible nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role) last.


You can get the list of nodes in a specific node role using the [get node information](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-info) API. For example, use the following request for `data_frozen`:

```console
GET /_nodes/data_frozen:true/_none
```

:::{tip}
If you accidentally upgrade a node before its designated grouping order, you might encounter various errors which you can expect to continue until the rolling upgrade is completed for all nodes. 

Within `data` node sub-groupings, you might encounter various [shard allocation errors](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md) which you can expect to continue until more nodes within the sub-grouping are upgraded. For example, these can display as follows:

```
cannot allocate replica shard to a node with version [x.x.x] since this is older than the primary version [y.y.y]
```
:::



## Upgrade process [upgrade-process]

To upgrade a cluster, complete these steps for every node:

:::::{stepper}

::::{step} (Optional) Disable shard allocation
When you shut down a data node, the allocation process waits for `index.unassigned.node_left.delayed_timeout` (by default, one minute) before starting to replicate the shards on that node to other nodes in the cluster, which can involve a lot of I/O. Because the node is shortly going to be restarted, this I/O is unnecessary. You can avoid racing the clock by [disabling allocation](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) of replicas before shutting down [data nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#data-node):

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "primaries"
  }
}
```

::::
::::{step} (Optional) Stop non-essential indexing and perform a flush
While you can continue indexing during the upgrade, shard recovery is much faster if you temporarily stop non-essential indexing and perform a [flush](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-flush).

```console
POST /_flush
```

::::

::::{step} (Optional) Temporarily stop the tasks associated with active {{ml}} jobs and {{dfeeds}}
It is possible to leave your {{ml}} jobs running during the upgrade, but it puts increased load on the cluster. When you shut down a {{ml}} node, its jobs automatically move to another node and restore the model states.

:::{note}
Any {{ml}} indices created before 8.x must be reindexed before upgrading, which you can initiate from the **Upgrade Assistant** in 8.19.
:::

* Temporarily halt the tasks associated with your {{ml}} jobs and {{dfeeds}} and prevent new jobs from opening by using the [set upgrade mode API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-set-upgrade-mode):

    ```console
    POST _ml/set_upgrade_mode?enabled=true
    ```

    When you disable upgrade mode, the jobs resume using the last model state that was automatically saved. This option avoids the overhead of managing active jobs during the upgrade and is faster than explicitly stopping {{dfeeds}} and closing jobs.

* [Stop all {{dfeeds}} and close all jobs](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-close-job). This option saves the model state at the time of closure. When you reopen the jobs after the upgrade, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states.

::::

::::{step} Shut down a single node
To shut down a single node depends on what is currently used to run {{es}}. For example, if using `systemd` or SysV `init` run the commands below.

* If you are running {{es}} with `systemd`:

    ```sh
    sudo systemctl stop elasticsearch.service
    ```

* If you are running {{es}} with SysV `init`:

    ```sh
    sudo -i service elasticsearch stop
    ```

::::

::::{step} Upgrade the version of the node you shut down
To upgrade using a [Debian](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md) or [RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md) package:

* Use `rpm` or `dpkg` to install the new package. All files are installed in the appropriate location for the operating system and {{es}} config files are not overwritten.

To upgrade using a zip or compressed tarball:

1. Extract the zip or tarball to a **new** directory. This is critical if you are not using external `config` and `data` directories.
2. Set the `ES_PATH_CONF` environment variable to specify the location of your external `config` directory and `jvm.options` file. If you are not using an external `config` directory, copy your old configuration over to the new installation.
3. Set `path.data` in `config/elasticsearch.yml` to point to your external data directory. If you are not using an external `data` directory, copy your old data directory over to the new installation.<br>

    :::{important}
    If you use {{monitor-features}}, reuse the data directory when you upgrade {{es}}. Monitoring identifies unique {{es}} nodes by using the persistent UUID, which is stored in the data directory.
    :::

4. Set `path.logs` in `config/elasticsearch.yml` to point to the location where you want to store your logs. If you do not specify this setting, logs are stored in the directory you extracted the archive to.

:::{tip}
When you extract the zip or tarball packages, the `elasticsearch-{{bare_version}}` directory contains the {{es}} `config`, `data`, and `logs` directories.

We recommend moving these directories out of the {{es}} directory so that there is no chance of deleting them when you upgrade {{es}}. To specify the new locations, use the `ES_PATH_CONF` environment variable and the `path.data` and `path.logs` settings. For more information, refer to [Important {{es}} configuration](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md).

The Debian and RPM packages place these directories in the appropriate place for each operating system. In production, we recommend using the deb or rpm package.
:::

::::

::::{step} Merge the config overrides of the shut down node
Apply any required [{{es}} configuration changes](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) to align your configuration with the version you are upgrading to. The most common settings to review include:

* Leave `cluster.initial_master_nodes` unset inside your `elasticsearch.yml` when performing a rolling upgrade. Each upgraded node is joining an existing cluster so there is no need for [cluster bootstrapping](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md). You must configure [either `discovery.seed_hosts` or `discovery.seed_providers`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#discovery-settings) on every node.
* {{es}} ships its recommended [JVM settings](elasticsearch://reference/elasticsearch/jvm-settings.md) inside `jvm.options` which can change across versions. Ensure any overrides are copied into the updated version's `jvm.options.d` files to avoid drift.
* {{es}} ships its recommended [logging settings](/deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md) inside `log4j2.properties` which can change across versions. Ensure any overrides are copied into the updated version's files to avoid drift. 
* Avoid drift in [OS-level system settings](/deploy-manage/deploy/self-managed/important-system-configuration.md) between nodes. That is most likely when you add or rebuild a node and the OS is not a copy of the previous one. For common settings and how to apply them, refer to [System settings configuration methods](/deploy-manage/deploy/self-managed/setting-system-settings.md).

::::

::::{step} Upgrade any plugins on the shut down node
Use the `elasticsearch-plugin` script to install the upgraded version of each installed {{es}} plugin. All plugins must be upgraded when you upgrade a node.

::::

::::{step} Start the upgraded node
Start the newly-upgraded node and confirm that it joins the cluster by checking the log file or by submitting a `_cat/nodes` request:

```console
GET _cat/nodes
```

::::

::::{step} Re-enable shard allocation
For data nodes, once the node has joined the cluster, remove the `cluster.routing.allocation.enable` setting to enable shard allocation and start using the node:

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": null
  }
}
```

::::

::::{step} Wait for the node to recover

Before upgrading the next node, wait for the cluster to finish shard allocations by reporting `status: green`. You can check progress by submitting a [Cluster health status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health):

```console
GET _cluster/health
```

Shards that were not flushed might take longer to recover. You can monitor the recovery status of individual shards using the [CAT recovery](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery) API:

```console
GET _cat/recovery?v=true&expand_wildcards=all&active_only=true
```

If you stopped indexing, it is safe to resume indexing as soon as recovery completes.

::::

::::{step} Restart machine learning jobs
If you temporarily halted the tasks associated with your {{ml}} jobs, use the set upgrade mode API to return them to active states:

```console
POST _ml/set_upgrade_mode?enabled=false
```

If you closed all {{ml}} jobs before the upgrade, open the jobs and start the datafeeds from {{kib}} or with the [open jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-open-job) and [start datafeed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-datafeed) APIs.

:::::

If you plan to upgrade nodes in quick succession, you might choose to leave indexing stopped and machine learning jobs and feeds paused throughout the entire upgrade process. You will still want to re-enable shard allocation after each node's restart.

To monitor which nodes have been upgraded, use the [CAT nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) API:

```console
GET _cat/nodes?v=true&h=name,ip,role,master,version,uptime&s=uptime
```

:::{tip}
If you encounter issues during a rolling upgrade, refer to [](/troubleshoot/elasticsearch/troubleshooting-upgrades.md).
:::

## Archived settings [archived-settings]

:::{include} _snippets/archived-settings-post.md
:::

## Next steps

Once you've successfully upgraded {{es}}, continue upgrading the remaining {{stack}} components:
* [{{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana.md)
* [Elastic APM](/solutions/observability/apm/upgrade.md)
* [Ingest components](/deploy-manage/upgrade/ingest-components.md)