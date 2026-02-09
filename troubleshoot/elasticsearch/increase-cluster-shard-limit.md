---
navigation_title: Total number of shards per node reached
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-cluster-shard-limit.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move to a new Unassigned shards subsection

# Total number of shards per node has been reached [increase-cluster-shard-limit]

{{es}} takes advantage of all available resources by distributing data (index shards) among the cluster nodes.

You can influence the data distribution by configuring the [`cluster.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#cluster-total-shards-per-node) dynamic cluster setting to restrict the number of shards that can be hosted on a single node in the cluster. 

In earlier {{es}} versions, `cluster.routing.allocation.total_shards_per_node` is set to `1000`. Reaching that limit causes the following error: `Total number of shards per node has been reached` and requires adjusting this setting or reducing the number of shards. In {{es}} 9.x, this setting is not configured by default, which means there is no upper bound on the number of shards per node unless the setting is explicitly defined.

Various configurations limiting how many shards can be hosted on a single node can lead to shards being unassigned, because the cluster does not have enough nodes to satisfy the configuration.
To ensure that each node carries a reasonable shard load, you might need to resize your deployment.

Follow these steps to resolve this issue:

1. [Check and adjust the cluster shard limit](#adjust-cluster-shard-limit) to determine the current value and increase it if needed.
1. [Determine which data tier needs more capacity](#determine-data-tier) to identify the tier where shards need to be allocated.
1. [Resize your deployment](#resize-deployment) to add capacity and accommodate additional shards.


## Check and adjust the cluster shard limit [adjust-cluster-shard-limit]

The `cluster.routing.allocation.total_shards_per_node` setting controls the maximum number of shards that can be allocated to each node in a cluster. When this limit is reached, {{es}} cannot assign new shards to that node, leading to unassigned shards in your cluster.

By checking the current value and increasing it, you allow more shards to be collocated on each node, which might resolve the allocation issue without adding more capacity to your cluster.

You can run the following steps using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

### Check the current setting [check-the-shard-limiting-setting]

Use the [get cluster-wide settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) API to inspect the current value of `cluster.routing.allocation.total_shards_per_node`:

```console
GET /_cluster/settings?flat_settings
```

The response looks like this:

```console-result
{
  "persistent": {
    "cluster.routing.allocation.total_shards_per_node": "300" <1>
  },
  "transient": {}
}
```

1. Represents the current configured value for the total number of shards that can reside on one node in the cluster. If the value is null or absent, no explicit limit is configured.

### Increase the setting

Use the [update the cluster settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) API to increase the value to a higher number that accommodates your workload:

```console
PUT _cluster/settings
{
  "persistent" : {
    "cluster.routing.allocation.total_shards_per_node" : 400 <1>
  }
}
```

1. The new value for the system-wide `total_shards_per_node` configuration is increased from the previous value of `300` to `400`. The `total_shards_per_node` configuration can also be set to `null`, which represents no upper bound with regards to how many shards can be collocated on one node in the system.



## Determine which data tier needs more capacity [determine-data-tier]

If increasing the cluster shard limit alone doesn't resolve the issue, or if you want to distribute shards more evenly, you need to identify which [data tier](/manage-data/lifecycle/data-tiers.md) requires additional capacity.

:::{include} /troubleshoot/elasticsearch/_snippets/determine-data-tier-that-needs-capacity.md
:::



## Resize your deployment [resize-deployment]

After you've identified the tier that needs more capacity, you can resize your deployment to distribute the shard load and allow previously unassigned shards to be allocated.

:::{include} /troubleshoot/elasticsearch/_snippets/resize-your-deployment.md
:::



:::::::
:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::
