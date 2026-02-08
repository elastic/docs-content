---
navigation_title: Watermark errors
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-watermark-errors.html
applies_to:
  stack:
products:
  - id: elasticsearch
---



# Watermark errors [fix-watermark-errors]

When a data node reaches critical disk space usage, its [disk-based shard allocation watermark settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) trigger to protect the node's disk. The default watermark percentage thresholds, the summary of {{es}}'s response, and their corresponding {{es}} log are:

* 75% `none`: The Cloud Deployment's {{es}} node's disk bar turns red, but {{es}} takes no action. {applies_to}`ece: ga` {applies_to}`ess: ga`
* 85% [`low`](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-low): {{es}} stops allocating replica shards and primary shards unless from newly-created indices to the affected node(s).
    ```
    low disk watermark [85%] exceeded on [NODE_ID][NODE_NAME] free: Xgb[X%], replicas will not be assigned to this node
    ```
* 90% [`high`](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high): {{es}} rebalances shards away from the affected node(s).
    ```
    high disk watermark [90%] exceeded on [NODE_ID][NODE_NAME] free: Xgb[X%], shards will be relocated away from this node
    ```
* 95% [`flood-stage`](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage): {{es}} sets all indices on the affected node(s) to read-only. The write block is automatically removed once disk usage on the affected node falls below the high watermark. 
    ```
    flood-stage watermark [95%] exceeded on [NODE_ID][NODE_NAME], all indices on this node will be marked read-only
    ```

To prevent a full disk, when a node reaches `flood-stage` watermark, {{es}} [blocks writes](elasticsearch://reference/elasticsearch/index-settings/index-block.md) to any index with a shard on the affected node(s). If the block affects related system indices, {{kib}} and other {{stack}} features can become unavailable. For example, `flood-stage` can induce errors like:

* {{kib}}'s `Kibana Server is not Ready yet` [error message](/troubleshoot/kibana/error-server-not-ready.md).
* {{es}}'s ingest API's [reject the request](/troubleshoot/elasticsearch/rejected-requests.md) with HTTP 429 error bodies like:
    ```json
    {
      "reason": "index [INDEX_NAME] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block];",
      "type": "cluster_block_exception"
    }
    ```

The following are some common setup issues leading to watermark errors:

* Sudden ingestion of large volumes of data that consumes disk above peak load testing expectations. Refer to [Indexing performance considerations](/deploy-manage/production-guidance/optimize-performance/indexing-speed.md) for guidance.
* Inefficient index settings, unnecessary stored fields, and suboptimal document structures can increase disk consumption. Refer to [Tune for disk usage](/deploy-manage/production-guidance/optimize-performance/disk-usage.md) for guidance.
* A high number of replicas can quickly multiply storage requirements, as each replica consumes the same disk space as the primary shard. Refer to [Index settings](elasticsearch://reference/elasticsearch/index-settings/index-modules.md) for details.
* Oversized shards can make disk usage spikes more likely and slow down recovery and rebalancing. Refer to [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md#shard-size-recommendation) for guidance.

## Monitor disk usage [fix-watermark-errors-monitor]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

To track disk usage over time, enable monitoring using one of the following options, depending on your deployment type:

:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }
* (Recommended) Enable [AutoOps](/deploy-manage/monitor/autoops.md).
* Enable [logs and metrics](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page. You can also enable the [Disk usage threshold alert](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues.
* From your deployment menu, view the [**Performance**](../../deploy-manage/monitor/access-performance-metrics-on-elastic-cloud.md) page's disk usage chart.
::::::

::::::{applies-item} { self:, eck: }
* (Recommended) Enable [AutoOps](/deploy-manage/monitor/autoops.md).
* Enable [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md). When logs and metrics are enabled, monitoring information is visible on {{kib}}'s [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) page. You can also enable the [Disk usage threshold alert](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) to be notified about potential issues.
::::::

:::::::


## Monitor rebalancing [fix-watermark-errors-rebalance]

To verify that shards are moving off the affected node until it falls below high watermark, use the following {{es}} APIs:

* [Cluster health status API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) to check `relocating_shards`.

    ```console
    GET _cluster/health
    ```
    
* [CAT recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery) to check the count of recovering shards and their migrated `bp` bytes percent of `tb` total bytes.

    ```console
    GET _cat/recovery?v=true&expand_wildcards=all&active_only=true&h=time,tb,bp,top,ty,st,snode,tnode,idx,sh&s=time:desc
    ```

If shards remain on the node keeping it above high watermark, use the following {{es}} APIs:

* [CAT shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards) to determine which shards are hosted on the node.

    ```console
    GET _cat/shards?v=true
    ```

* [Cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) to get an explanation for the chosen shard's allocation status.

    ```console
    GET _cluster/allocation/explain
    {
      "index": "my-index-000001",
      "shard": 0,
      "primary": false
    }
    ```

    Refer to [Using the cluster allocation API for troubleshooting](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md) for guidance on interpreting this output.

You should normally wait for {{es}} to balance itself. If advanced users determine shards which should migrate off node faster, whether due to forecasted ingestion rate or existing disk usage, they might consider using the [Reroute the cluster API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute) to push their chosen shard to immediately rebalance to their determined target node.

## Temporary relief [fix-watermark-errors-temporary]

To immediately restore write operations, you can temporarily increase [disk watermarks](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) and remove the [write block](elasticsearch://reference/elasticsearch/index-settings/index-block.md).

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.disk.watermark.low": "90%",
    "cluster.routing.allocation.disk.watermark.low.max_headroom": "100GB",
    "cluster.routing.allocation.disk.watermark.high": "95%",
    "cluster.routing.allocation.disk.watermark.high.max_headroom": "20GB",
    "cluster.routing.allocation.disk.watermark.flood_stage": "97%",
    "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": "5GB",
    "cluster.routing.allocation.disk.watermark.flood_stage.frozen": "97%",
    "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": "5GB"
  }
}

PUT */_settings?expand_wildcards=all
{
  "index.blocks.read_only_allow_delete": null
}
```

When a long-term solution is in place, to reset or reconfigure the disk watermarks:

```console
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.disk.watermark.low": null,
    "cluster.routing.allocation.disk.watermark.low.max_headroom": null,
    "cluster.routing.allocation.disk.watermark.high": null,
    "cluster.routing.allocation.disk.watermark.high.max_headroom": null,
    "cluster.routing.allocation.disk.watermark.flood_stage": null,
    "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": null,
    "cluster.routing.allocation.disk.watermark.flood_stage.frozen": null,
    "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": null
  }
}
```

::::{note}
{{es}} recommends using default watermark settings. Advanced users can override [the watermark thresholds and headroom](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) but risk not giving enough disk for background processes such as force merge, not being right-sized to data ingestion rates vs {{ilm}} settings, and possibly `disk is full` errors if 100% disk is reached.
::::

## Resolve [fix-watermark-errors-resolve]

To resolve watermark errors permanently, perform one of the following actions:

* Horizontally scale nodes of the affected [data tiers](/manage-data/lifecycle/data-tiers.md).
* Vertically scale existing nodes to increase disk space. Ensure nodes within a [data tier](/manage-data/lifecycle/data-tiers.md) are scaled to matching hardware profiles to avoid [hot spotting](/troubleshoot/elasticsearch/hotspotting.md).
* Delete indices using the [delete index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete), either permanently if the index isn’t needed, or temporarily to later [restore from snapshot](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).

::::{tip}
On {{ech}} and {{ece}}, you might need to temporarily delete indices using the [{{es}} API Console](cloud://reference/cloud-hosted/ec-api-console.md). This can resolve a `status: red` [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) status, which blocks [deployment changes](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md). After resolving the issue, you can [restore](/deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) the indices from a snapshot. If you experience issues with this resolution flow, reach out to [Elastic Support](/troubleshoot/index.md#troubleshoot-work-with-support) for assistance.
::::

## Preventing watermark errors  

To reduce the likelihood of watermark errors:  

* Enable [Autoscaling](/deploy-manage/autoscaling.md) to automatically adjust resources based on storage and performance needs. {applies_to}`ece: ga` {applies_to}`ess: ga` {applies_to}`eck: ga`
* Implement more restrictive [{{ilm}} policies](/manage-data/lifecycle/index-lifecycle-management.md) to move data through [data tiers](/manage-data/lifecycle/data-tiers.md) sooner to help keep higher tiers' disk usage under control.
* Avoid a mix of overly large and small indices which can cause an [unbalanced cluster](/troubleshoot/elasticsearch/troubleshooting-unbalanced-cluster.md). Refer to [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md#shard-size-recommendation).
