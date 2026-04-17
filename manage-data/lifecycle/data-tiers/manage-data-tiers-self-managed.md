---
navigation_title:  Manage data tiers in self-managed clusters
description: "Assign Elasticsearch data tier roles to nodes in self-managed clusters by configuring node.roles in elasticsearch.yml."
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Configure data tiers in self-managed deployments [configure-data-tiers-on-premise]

On self-managed clusters, data tiers are expressed through each node’s [data role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role). You enable the tiers your cluster should offer by setting `node.roles` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) on each node.

## Before you begin

- Review [{{es}} data tiers](/manage-data/lifecycle/data-tiers.md) so you match tiers to your workload.
- Understand how [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) map to hardware and allocation for each tier.

## Assign data tier roles to nodes

1. For each node, decide which data tier or tiers it should participate in (for example `data_hot`, `data_warm`, `data_cold`, `data_frozen`, or `data_content`).
2. Set `node.roles` in that node’s `elasticsearch.yml` to include the corresponding `data_*` roles (and any other roles the node should have, such as `ingest` or `master`).
3. Restart the node or apply your configuration rollout process so the new roles take effect.

For example, the highest-performance nodes in a cluster might be assigned to both the hot and content tiers:

```yaml
node.roles: ["data_hot", "data_content"]
```

::::{note}
We recommend you use [dedicated nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier.
::::

## Related pages

- [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
- [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
- [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md)
