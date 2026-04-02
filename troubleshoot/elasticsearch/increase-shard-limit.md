---
navigation_title: Total number of shards for an index exceeded
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-shard-limit.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw retitle; move to a new Unassigned shards subsection

# Total number of shards for an index on a single node exceeded [increase-shard-limit]

{{es}} takes advantage of all available resources by distributing data (index shards) among the cluster nodes.

You can influence this data distribution by configuring the [index.routing.allocation.total_shards_per_node](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) dynamic index setting to restrict the maximum number of shards from a single index that can be allocated to a node.
For example, in case of a highly trafficked index, the value can be set to `1`. 

Various configurations limiting how many shards an index can have located on one node can lead to shards being unassigned, because the cluster does not have enough nodes to satisfy the index configuration.
To fix this issue, complete the following steps:

1. [Check and adjust the index allocation settings](#adjust-index-allocation-settings) to determine the current value and increase it if needed.
1. [Determine which data tier needs more capacity](#determine-data-tier) to identify the tier where shards need to be allocated.
1. [Resize your deployment](#resize-deployment) to add capacity and accommodate additional shards.



## Check and adjust the index allocation settings [adjust-index-allocation-settings]

The `index.routing.allocation.total_shards_per_node` setting controls the maximum number of shards that can be collocated on a node in your cluster. When this limit is reached, {{es}} cannot assign new shards to that node, leading to unassigned shards in your cluster.

By checking the current value and increasing it, you allow more shards to be collocated on each node, which might resolve the allocation issue without adding more capacity to your cluster.

You can run the following steps using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [{{es}} API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

### Check the current index setting [check-the-index-setting]

Use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to inspect the `index.routing.allocation.total_shards_per_node` value for the index with unassigned shards:

```console
GET /my-index-000001/_settings/index.routing.allocation.total_shards_per_node?flat_settings
```

The response looks like this:

```console-result
{
  "my-index-000001": {
    "settings": {
      "index.routing.allocation.total_shards_per_node": "1" <1>
    }
  }
}
```

1. Represents the current configured value for the total number of shards that can reside on one node for the `my-index-000001` index.

### Increase the setting

Use the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) API to increase the value for the total number of shards that can be assigned on a node to a higher value that accommodates your workload:

```console
PUT /my-index-000001/_settings
{
  "index" : {
    "routing.allocation.total_shards_per_node" : "2" <1>
  }
}
```

1. The new value for the `total_shards_per_node` configuration for the `my-index-000001` index is increased from the previous value of `1` to `2`. The `total_shards_per_node` configuration can also be set to `-1`, which represents no upper bound with regards to how many shards of the same index can reside on one node.


## Determine which data tier needs more capacity [determine-data-tier]

If increasing the index shard limit alone doesn't resolve the issue, or if you want to distribute shards more evenly, you need to identify which [data tier](/manage-data/lifecycle/data-tiers.md) requires additional capacity.

:::{include} /troubleshoot/elasticsearch/_snippets/determine-data-tier-that-needs-capacity.md
:::

## Resize your deployment [resize-deployment]

After you've identified the tier that needs more capacity, you can resize your deployment to distribute the shard load and allow previously unassigned shards to be allocated.

:::{include} /troubleshoot/elasticsearch/_snippets/resize-your-deployment.md
:::



:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::