---
navigation_title: "Unavailable nodes"
applies: 
  hosted:
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-scenario_why_is_my_node_unavailable.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echscenario_why_is_my_node_unavailable.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-single-node-deployment-disk-used.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-multiple-node-deployment-disk-used.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-jvm-heap-usage-exceed-allowed-threshold.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-cpu-usage-exceed-allowed-threshold.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-nodes-unavailable-missing.html
---

% TODO fix the layout and formatting

# Diagnose unavailable nodes [ec-scenario_why_is_my_node_unavailable]

This section provides a list of common symptoms and possible actions that you can take to resolve issues when one or more nodes become unhealthy or unavailable. This guide is particularly useful if you are not [shipping your logs and metrics](/deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) to a dedicated monitoring cluster.

**What are the symptoms?**

* [Full disk on single-node deployment](/troubleshoot/monitoring/unavailable-nodes.md#ec-single-node-deployment-disk-used)
* [Full disk on multiple-nodes deployment](/troubleshoot/monitoring/unavailable-nodes.md#ec-multiple-node-deployment-disk-used)
* [JVM heap usage exceeds the allowed threshold on master nodes](/troubleshoot/monitoring/unavailable-nodes.md#ec-jvm-heap-usage-exceed-allowed-threshold)
* [CPU usage exceeds the allowed threshold on master nodes](/troubleshoot/monitoring/unavailable-nodes.md#ec-cpu-usage-exceed-allowed-threshold)
* [Some nodes are unavailable and are displayed as missing](/troubleshoot/monitoring/unavailable-nodes.md#ec-nodes-unavailable-missing)

**What is the impact?**

* Only some search results are successful
* Ingesting, updating, and deleting data do not work
* Most {{es}} API requests fail

::::{note}
Some actions described here, such as stopping indexing or Machine Learning jobs, are temporary remediations intended to get your cluster into a state where you can make configuration changes to resolve the issue.
::::


For production deployments, we recommend setting up a dedicated monitoring cluster to collect metrics and logs, troubleshooting views, and cluster alerts.

If your issue is not addressed here, then [contact Elastic support for help](/troubleshoot/index.md).

## Full disk on single-node deployment [ec-single-node-deployment-disk-used]

**Health check**

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Click the **Manage** link corresponding to the deployment that you want to manage.

3. On your deployment page, scroll down to **Instances** and check if the disk allocation for your {{es}} instance is over 90%.

    :::{image} /images/cloud-ec-full-disk-single-node.png
    :alt: Full disk on single-node deployment
    :::


**Possible cause**

* The available storage is insufficient for the amount of ingested data.

**Resolution**

* [Delete unused data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
* Increase the disk size on your Hot data and Content tier (scale up).

::::{note}
If your {{es}} cluster is unhealthy and reports a status of red, then increasing the disk size of your Hot data and Content tier may fail. You might need to delete some data so the configuration can be edited. If you want to increase your disk size without deleting data, then [reach out to Elastic support](/troubleshoot/index.md) and we will assist you with scaling up.
::::


**Preventions**

* Increase the disk size on your Hot data and Content tier (scale up).

    From your deployment menu, go to the **Edit** page and increase the **Size per zone** for your Hot data and Content tiers.

    :::{image} /images/cloud-ec-increase-size-per-zone.png
    :alt: Increase size per zone
    :::

* Enable [autoscaling](/deploy-manage/autoscaling.md) to grow your cluster automatically when it runs out of space.
* Configure [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies to automatically delete unused data.
* Add nodes to your {{es}} cluster and enable [data tiers](/manage-data/lifecycle/data-tiers.md) to move older data that you don’t query often to more cost-effective storage.


## Full disk on multiple-nodes deployment [ec-multiple-node-deployment-disk-used]

**Health check**

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the {{es}} Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} /images/cloud-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. On your deployment page, scroll down to **Instances** and check if the disk allocation for any of your {{es}} instances is over 90%.

    :::{image} /images/cloud-ec-full-disk-multiple-nodes.png
    :alt: Full disk on multiple-nodes deployment
    :::


**Possible cause**

* The available storage is insufficient for the amount of ingested data.

**Resolution**

* [Delete unused data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
* Increase the disk size (scale up).

::::{note}
If your {{es}} cluster is unhealthy and reports a status of red, the scale up configuration change to increasing disk size on the affected data tiers may fail. You might need to delete some data so the configuration can be edited. If you want to increase your disk size without deleting data, then [reach out to Elastic support](/troubleshoot/index.md) and we will assist you with scaling up.
::::


**Preventions**

* Increase the disk size (scale up).

    1. On your deployment page, scroll down to **Instances** and identify the node attribute of the instances that are running out of disk space.

        :::{image} /images/cloud-ec-node-attribute.png
        :alt: Instance node attribute
        :::

    2. Use the node types identified at step 1 to find out the corresponding data tier.

        :::{image} /images/cloud-ec-node-types-data-tiers.png
        :alt: Node type and corresponding attribute
        :::

    3. From your deployment menu, go to the **Edit** page and increase the **Size per zone** for the data tiers identified at step 2.

        :::{image} /images/cloud-ec-increase-size-per-zone.png
        :alt: Increase size per zone
        :::

* Enable [autoscaling](/deploy-manage/autoscaling.md) to grow your cluster automatically when it runs out of space.
* Configure [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies to automatically delete unused data.
* Enable [data tiers](/manage-data/lifecycle/data-tiers.md) to move older data that you don’t query often to more cost-effective storage.


## JVM heap usage exceeds the allowed threshold on master nodes [ec-jvm-heap-usage-exceed-allowed-threshold]

**Health check**

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the {{es}} Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} /images/cloud-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. On your deployment page, scroll down to **Instances** and check if the JVM memory pressure for your {{es}} instances is high.

    :::{image} /images/cloud-ec-deployment-instances-config.png
    :alt: Deployment instances configuration
    :::


**Possible causes**

* The master node is overwhelmed by a large number of snapshots or shards.

    * External tasks initiated by clients

        * Index, search, update
        * Frequent template updates due to the Beats configuration

    * Internal tasks initiated by users

        * Machine Learning jobs, watches, monitoring, ingest pipeline

    * Internal tasks initiated by {{es}}

        * Nodes joining and leaving due to hardware failures
        * Shard allocation due to nodes joining and leaving
        * Configuration of [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies.


**Resolutions**

* If the master node is overwhelmed by external tasks initiated by clients:

    Investigate which clients might be overwhelming the cluster and reduce the request rate or pause ingesting, searching, or updating from the client. If you are using Beats, temporarily stop the Beat that’s overwhelming the cluster to avoid frequent template updates.

* If the master node is overwhelmed by internal tasks initiated by users:

    * Check [cluster-level pending tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-pending-tasks).
    * Reduce the number of Machine Learning jobs or watches.
    * Change the number of ingest pipelines or processors to use less memory.

* If the master node is overwhelmed by internal tasks initiated by {{es}}:

    * For nodes joining and leaving, this should resolve itself. If increasing the master nodes size doesn’t resolve the issue, contact support.
    * For shard allocation, inspect the progress of shards recovery.

        * Make sure `indices.recovery.max_concurrent_operations` is not aggressive, which could cause the master to be unavailable.
        * Make sure `indices.recovery.max_bytes_per_sec` is set adequately to avoid impact on ingest and search workload.

    * Check [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies to avoid index rollover and relocate actions that are concurrent and aggressive.

* If the master node is overwhelmed by a large number of snapshots, reduce the number of snapshots in the repo.
* If the master node is overwhelmed by a large number of shards, delete unneeded indices and shrink read-only indices to fewer shards. For more information, check [Reduce a cluster’s shard count](/deploy-manage/production-guidance/optimize-performance/size-shards.md#reduce-cluster-shard-count).


## CPU usage exceeds the allowed threshold on master nodes [ec-cpu-usage-exceed-allowed-threshold]

**Health check**

By default, the allowed CPU usage threshold is set at 85%.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the {{es}} Service panel, click the **Quick link** icon corresponding to the deployment that you want to manage.

    :::{image} /images/cloud-ec-quick-link-to-deployment.png
    :alt: Quick link to the deployment page
    :::

3. Identify the IDs of your master nodes. On your deployment page, scroll down to **Instances** and filter your instance configuration by master. The IDs of your master nodes are in the title. In this example, the IDs are 21, 26 and 27:

    :::{image} /images/cloud-ec-instances-filtered-by-master-id.png
    :alt: Instances configuration filtered by master nodes ID
    :::

    ::::{note}
    The name of the instance configuration might differ depending on the cloud provider.
    ::::

4. Navigate to the **Performance** page of your deployment. Check if the CPU usage of your master nodes exceeds 85%. Your master node has the format `instance-<ID>``, where `<ID>`` is the ID of the master node.

If you use [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md), open Kibana from your deployment page and select **Stack Monitoring** from the menu or the search bar.

::::{note}
Stack Monitoring comes with out-of-the-box rules, but you need to enable them when prompted.
::::


**Possible causes**

* The master node is overwhelmed by a large number of snapshots or shards.
* The memory available on the master node is overwhelmed by these tasks:

    * External tasks initiated by clients

        * Index, search, update
        * Frequent template updates due to the Beats configuration

    * Internal tasks initiated by users

        * Machine Learning jobs, watches, monitoring, ingest pipelines

    * Internal tasks initiated by {{es}}

        * Nodes joining and leaving due to hardware failures
        * Shard allocation due to nodes joining and leaving
        * Configuration of [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies.


**Resolutions**

* Navigate to the **Edit** page of your deployment and increase the master node size.
* [Upgrade the cluster](/deploy-manage/upgrade/deployment-or-cluster.md) to the latest version.
* If the master node is overwhelmed by external tasks initiated by clients:

    * Reduce the request rate or pause ingesting, searching, or updating from the client.
    * Enable ingest and search-based autoscaling.
    * Stop Beats to avoid frequent template updates.

* If the master node is overwhelmed by internal tasks initiated by users:

    * Check [cluster-level pending tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-pending-tasks).
    * Reduce the number of Machine Learning jobs or watches.
    * Change the number of ingest pipelines or processors to use less memory.

* If the master node is overwhelmed by internal tasks initiated by {{es}}:

    * For nodes joining and leaving, this should resolve itself. If increasing the master nodes size doesn’t resolve the issue, contact support.
    * For shard allocation, inspect the progress of shards recovery. If there’s no progress, contact support.

        * Make sure `indices.recovery.max_concurrent_operations` is not aggressive, which could cause the master to be unavailable.
        * Make sure `indices.recovery.max_bytes_per_sec` is set adequately to avoid impact on ingest and search workload.

    * Check [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies to avoid index rollover and relocate actions that are concurrent and aggressive.

* If the master node is overwhelmed by a large number of snapshots, reduce the number of snapshots in the repo.
* If the master node is overwhelmed by a large number of shards, reduce the number of shards on the node. For more information, check [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md).


## Some nodes are unavailable and are displayed as missing [ec-nodes-unavailable-missing]

**Health check**

* Use the [Metrics inventory](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) to identify unavailable or unhealthy nodes. If the number of minimum master nodes is down, {{es}} is not available.

**Possible causes**

* Hardware issue.
* Routing has stopped because of a previous ES configuration failure.
* Disk/memory/CPU are saturated.
* The network is saturated or disconnected.
* Nodes are unable to join.

**Resolutions**

* Hardware issue: Any unhealthy hardware detected by the platform is automatically vacated within the hour. If this doesn’t happen, contact support.
* Routing stopped: A failed {{es}} configuration might stop the nodes routing. Restart the routing manually to bring the node back to health.
* Disk/memory/CPU saturated:

    * [Delete unused data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).
    * Increase disk size.
    * [Enable autoscaling](/deploy-manage/autoscaling.md).
    * Configuration of [ILM](/manage-data/lifecycle/index-lifecycle-management.md) policies.
    * [Manage data tiers](/manage-data/lifecycle/data-tiers.md).

* Network saturated or disconnected: Contact support.
* Nodes unable to join: Fix the {{es}} configuration.
* Nodes unable to join: Contact support.

