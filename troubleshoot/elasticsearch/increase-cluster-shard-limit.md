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

Use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

```console
GET /my-index-000001/_settings/index.routing.allocation.include._tier_preference?flat_settings
```

The response looks like this:

```console-result
{
  "my-index-000001": {
    "settings": {
      "index.routing.allocation.include._tier_preference": "data_warm,data_hot" <1>
    }
  }
}
```

1. Represents a comma-separated list of data tier node roles this index is allowed to be allocated on. The first tier in the list has the highest priority and is the tier the index is targeting. In this example, the tier preference is `data_warm,data_hot`, so the index is targeting the `warm` tier. If the warm tier lacks capacity, the index will fall back to the `data_hot` tier.




## Resize your deployment [resize-deployment]

After you've identified the tier that needs more capacity, you can resize your deployment to distribute the shard load and allow previously unassigned shards to be allocated.

:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }
To enable a new tier in your {{ech}} deployment, you edit the deployment topology to add a new data tier.

1. In {{kib}}, open your deployment’s navigation menu (placed under the Elastic logo in the upper left corner) and go to **Manage this deployment**.
1. From the right hand side, click to expand the **Manage** dropdown button and select **Edit deployment** from the list of options.
1. On the **Edit** page, click on **+ Add Capacity** for the tier you identified you need to enable in your deployment. Choose the desired size and availability zones for the new tier.
1. Navigate to the bottom of the page and click the **Save** button.

::::::

::::::{applies-item} { self: }
Add more nodes to your {{es}} cluster and assign the index’s target tier [node role](/manage-data/lifecycle/data-tiers.md#configure-data-tiers-on-premise) to the new nodes, by adjusting the configuration in `elasticsearch.yml`.

::::::

::::::{applies-item} { eck: }
Add more nodes to your {{es}} cluster and assign the index’s target tier [node role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#change-node-role) to the new nodes, by adjusting the [node configuration](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md) in the `spec` section of your {{es}} resource manifest.
::::::

:::::::
:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::
