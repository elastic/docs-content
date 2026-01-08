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
[Add more nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) to your {{es}} cluster and assign the index’s target tier [node role](/manage-data/lifecycle/data-tiers.md#configure-data-tiers-on-premise) to the new nodes, by adjusting the configuration in `elasticsearch.yml`.

::::::

::::::{applies-item} { eck: }
To increase the disk capacity of data nodes in your {{eck}} cluster, you can either add more data nodes or increase the storage size of existing nodes.

**Option 1: Add more data nodes**

1. Update the `count` field in your data node NodeSet to add more nodes:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 5  # Increase from previous count
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 100Gi
    ```

1. Apply the changes:

    ```sh
    kubectl apply -f your-elasticsearch-manifest.yaml
    ```

    ECK automatically creates the new nodes and {{es}} will relocate shards to balance the load. You can monitor the progress using:

    ```console
    GET /_cat/shards?v&h=state,node&s=state
    ```

**Option 2: Increase storage size of existing nodes**

1. If your storage class supports [volume expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims), you can increase the storage size in the `volumeClaimTemplates`:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 3
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 200Gi  # Increased from previous size
    ```

1. Apply the changes. If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem will be resized online without restarting {{es}}. Otherwise, you may need to manually delete the Pods after the resize so they can be recreated with the expanded filesystem.

For more information, refer to [](/deploy-manage/deploy/cloud-on-k8s/update-deployments.md) and [](/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md).
::::::


:::::::
:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::