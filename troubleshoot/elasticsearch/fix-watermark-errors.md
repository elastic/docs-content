---
navigation_title: "Watermark errors"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fix-watermark-errors.html
---



# Watermark errors [fix-watermark-errors]


When a data node is critically low on disk space and has reached the [flood-stage disk usage watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-flood-stage), the following error is logged: `Error: disk usage exceeded flood-stage watermark, index has read-only-allow-delete block`.

To prevent a full disk, when a node reaches this watermark, {{es}} [blocks writes](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-block.md) to any index with a shard on the node. If the block affects related system indices, {{kib}} and other {{stack}} features may become unavailable. For example, this could induce {{kib}}'s `Kibana Server is not Ready yet` [error message](/troubleshoot/kibana/error-server-not-ready.md).

{{es}} will automatically remove the write block when the affected node’s disk usage falls below the [high disk watermark](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-watermark-high). To achieve this, {{es}} attempts to rebalance some of the affected node’s shards to other nodes in the same data tier.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::


## Monitor rebalancing [fix-watermark-errors-rebalance]

To verify that shards are moving off the affected node until it falls below high watermark., use the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards) and [cat recovery API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery):

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


## Temporary Relief [fix-watermark-errors-temporary]

To immediately restore write operations, you can temporarily increase [disk watermarks](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) and remove the [write block](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-block.md).

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

::::{tip}
On {{ech}} and {{ece}}, indices may need to be temporarily deleted via its [Elasticsearch API Console](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-console.md) to later [snapshot restore](../../deploy-manage/tools/snapshot-and-restore/restore-snapshot.md) in order to resolve [cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) `status:red` which will block [attempted changes](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md). If you experience issues with this resolution flow on {{ech}}, kindly reach out to [Elastic Support](https://support.elastic.co) for assistance.
::::



