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


When a data node is critically low on disk space and has reached the [flood-stage disk usage watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage), the following error is logged: `Error: disk usage exceeded flood-stage watermark, index has read-only-allow-delete block`.

To prevent a full disk, when a node reaches this watermark, {{es}} [blocks writes](elasticsearch://reference/elasticsearch/index-settings/index-block.md) to any index with a shard on the node. If the block affects related system indices, {{kib}} and other {{stack}} features may become unavailable. For example, this could induce {{kib}}'s `Kibana Server is not Ready yet` [error message](/troubleshoot/kibana/error-server-not-ready.md).

{{es}} will automatically remove the write block when the affected node’s disk usage falls below the [high disk watermark](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high). To achieve this, {{es}} attempts to rebalance some of the affected node’s shards to other nodes in the same data tier.

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::


## Context

Elasticsearch uses [disk-based shard allocation watermarks](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cluster.html#disk-based-shard-allocation) to prevent disk overuse and protect against data loss. Until a node reaches the flood-stage watermark, indexing is not blocked and shards can continue to grow on disk. Default watermark thresholds and their effects:  
- **75% (`none`)** – In the Cloud UI (ECE and ECH), the disk bar appears red. Elasticsearch takes no action.  
- **85% (`low`)** – Stops allocating new primary or replica shards to the affected node(s).  
- **90% (`high`)** – Moves shards away from the affected node(s).  
- **95% (`flood-stage`)** – Sets all indices on the affected node(s) to read-only. This is automatically reverted once the node’s usage drops below the high watermark. Indexing on affected nodes stops.  


## Monitor rebalancing [fix-watermark-errors-rebalance]

To verify that shards are moving off the affected node until it falls below high watermark, use the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards) and [cat recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery):

```console
GET _cat/shards?v=true

GET _cat/recovery?v=true&active_only=true
```

If shards remain on the node keeping it about high watermark, use the [cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) to get an explanation for their allocation status.

```console
GET _cluster/allocation/explain
{
  "index": "my-index",
  "shard": 0,
  "primary": false
}
```


## Common causes of watermark errors

Watermark errors occur when a node’s disk usage exceeds the configured thresholds (`low`, `high`, or `flood-stage`). While these thresholds protect cluster stability, they can be triggered by several underlying factors including:  

* Sudden ingestion of large volumes of data, often referred to as large indexing bursts, can quickly consume disk space, especially if the cluster is not sized for peak loads. See [Indexing performance considerations](https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html) for guidance.  
* Inefficient index settings, unnecessary stored fields, and suboptimal document structures can increase disk consumption. See [Tune for disk usage](https://www.elastic.co/docs/deploy-manage/production-guidance/optimize-performance/disk-usage) for guidance on reducing storage requirements.  
* A high number of replicas can quickly multiply storage requirements, as each replica consumes the same disk space as the primary shard. See [Index settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html) for details.  
* Very large shards can make disk usage spikes more likely and slow down recovery or relocation. Learn more in [Size your shards](https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html).  


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


## Resolve [fix-watermark-errors-resolve]

To resolve watermark errors permanently, perform one of the following actions:

* Horizontally scale nodes of the affected [data tiers](../../manage-data/lifecycle/data-tiers.md).
* Vertically scale existing nodes to increase disk space.
* Delete indices using the [delete index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete), either permanently if the index isn’t needed, or temporarily to later [restore](../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md).
* update related [ILM policy](../../manage-data/lifecycle/index-lifecycle-management.md) to push indices through to later [data tiers](../../manage-data/lifecycle/data-tiers.md)


## Preventing watermark errors  

To reduce the likelihood of watermark errors:  

* Implement more restrictive ILM policies to delete or move data sooner, helping keep disk usage under control. See [Index lifecycle management](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html).  
* Enable [Autoscaling](https://www.elastic.co/guide/en/cloud/current/ec-autoscaling.html) to automatically adjust resources based on storage and performance needs.  
* Configure [Stack monitoring](https://www.elastic.co/docs/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring) and/or [disk usage monitoring alerts](https://www.elastic.co/guide/en/observability/current/create-alerts.html) to track disk usage trends and identify increases before watermark thresholds are exceeded.  
* Optimize shard sizes to balance disk usage (and performance), avoiding overly large shards. See [Size your shards](https://www.elastic.co/guide/en/elasticsearch/reference/current/size-your-shards.html).  

::::{tip}
On {{ech}} and {{ece}}, indices may need to be temporarily deleted using the its [{{es}} API Console](cloud://reference/cloud-hosted/ec-api-console.md) to later [snapshot restore](../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) to resolve [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) `status:red` which blocks [attempted changes](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md). If you experience issues with this resolution flow, reach out to [Elastic Support](https://support.elastic.co) for assistance.
::::



