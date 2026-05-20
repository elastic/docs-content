---
navigation_title: Manage data tiers in self-managed and ECK
description: "Assign Elasticsearch data tier roles on self-managed hosts (elasticsearch.yml) or on Elastic Cloud on Kubernetes (ECK node set config)."
applies_to:
  deployment:
    self: ga
    eck: ga
products:
  - id: elasticsearch
  - id: cloud-kubernetes
---

# Configure data tiers for self-managed and {{eck}} deployments

Whether you operate {{es}} on your own infrastructure or on {{k8s}} with {{eck}}, data tiers are expressed through each node’s [data role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-node-role). You choose which tiers the cluster offers by assigning the corresponding `data_*` roles to nodes or to ECK node sets.

## Before you begin

- Review [{{es}} data tiers](/manage-data/lifecycle/data-tiers.md) so you match tiers to your workload.
- Understand how [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) map to hardware and allocation for each tier.

## Assign data tier roles on self-managed hosts [configure-data-tier-self-managed]
```{applies_to}
deployment:
  self: ga
```

1. For each node, decide which data tier or tiers it should participate in (for example `data_hot`, `data_warm`, `data_cold`, `data_frozen`, or `data_content`).
2. Set `node.roles` in that node’s [`elasticsearch.yml`](/deploy-manage/stack-settings.md) to include the corresponding `data_*` roles (and any other roles the node should have, such as `ingest` or `master`).
3. Restart the node or apply your configuration rollout process so the new roles take effect.

For example, the highest-performance nodes in a cluster might be assigned to both the hot and content tiers:

```yaml
node.roles: ["data_hot", "data_content"]
```

::::{note}
We recommend you use [dedicated nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#data-frozen-node) in the frozen tier.
::::

## Assign data tier roles in {{eck}}
```{applies_to}
deployment:
  eck: ga
```

{{es}} settings that you would normally put in `elasticsearch.yml` are set per node set under `spec.nodeSets[?].config` in the {{es}} resource manifest. Assign `node.roles` there to define each group of pods’ tiers. For example, you can assign the following tiers:

```yaml
spec:
  nodeSets:
  - name: hot-content
    count: 3
    config:
      node.roles: ["data_hot", "data_content", "ingest"]
```

Some settings are [managed by {{eck}}](/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck.md); avoid overriding those. For the full mapping between manifest structure and {{es}} configuration, see [Node configuration](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md).


:::{note}
 On {{eck}}, node set and scaling changes try to relocate shards from nodes that are removed, subject to allocation rules, capacity, and [disk watermarks](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) on the destination nodes. For more information, refer to the [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) documentation.
:::

## Related pages

* [Configure data tiers](/manage-data/lifecycle/data-tiers.md#configure-data-tiers)
* [Data tier index allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation)
* [Add or remove {{es}} nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md)
