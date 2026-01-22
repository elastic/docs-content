---
navigation_title: Not enough nodes to allocate shard replicas
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-tier-capacity.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Warning: Not enough nodes to allocate all shard replicas [increase-tier-capacity]

Distributing copies of the data (index shard replicas) on different nodes can parallelize processing requests, speeding up search queries. To achieve this, increase the number of replica shards up to the maximum value (total number of nodes minus one), which also protects against hardware failure. If the index has a preferred tier, {{es}} will only place the copies of the data for that index on nodes in the target tier.

If a warning is encountered with not enough nodes to allocate all shard replicas, you can influence this behavior by adding more nodes to the cluster (or tier), or by reducing the [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting.

To accomplish this, complete the following steps:

1. [Determine which data tier needs more capacity](#determine-data-tier) to identify the tier where shards need to be allocated.
1. [Resize your deployment](#resize-deployment) to add capacity and accommodate all shard replicas.
1. [Check and adjust the index replicas limit](#adjust-index-replica-limit) to determine the current value and reduce it if needed.

## Determine which data tier needs more capacity [determine-data-tier]

You can run the following step using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [Elasticsearch API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

To determine which tiers an index's shards can be allocated to, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

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

You can either increase the size per zone to increase the number of nodes in the availability zone(s) you were already using, or increase the number of availability zones. 

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


## Check and adjust the index replicas limit [adjust-index-replica-limit]


If it is not possible to increase capacity by resizing your deployment, you can reduce the number of replicas of your index data. You achieve this by inspecting the [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting index setting and decreasing the configured value.


1. Use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.number_of_replicas` index setting.

    ```console
    GET /my-index-000001/_settings/index.number_of_replicas
    ```

    The response looks like this:

    ```console-result
    {
      "my-index-000001" : {
        "settings" : {
          "index" : {
            "number_of_replicas" : "2" <1>
          }
        }
      }
    }
    ```

    1. Represents the currently configured value for the number of replica shards required for the index

1. Use the [`_cat/nodes`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) API to find the number of nodes in the target tier:

    ```console
    GET /_cat/nodes?h=node.role
    ```

    The response looks like this, containing one row per node:

    ```console-result
    himrst
    mv
    himrst
    ```

    You can count the rows containing the letter representing the target tier to know how many nodes you have. See [Query parameters](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) for details. The example above has two rows containing `h`, so there are two nodes in the hot tier.

1. Use the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) API to decrease the value for the total number of replica shards required for this index. As replica shards cannot reside on the same node as primary shards for [high availability](../../deploy-manage/production-guidance/availability-and-resilience.md), the new value needs to be less than or equal to the number of nodes found above minus one. Since the example above found 2 nodes in the hot tier, the maximum value for `index.number_of_replicas` is 1.

    ```console
    PUT /my-index-000001/_settings
    {
      "index" : {
        "number_of_replicas" : 1 <1>
      }
    }
    ```

    1. The new value for the `index.number_of_replicas` index configuration is decreased from the previous value of `2` to `1`. It can be set as low as 0 but configuring it to 0 for indices other than [searchable snapshot indices](../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) may lead to temporary availability loss during node restarts or permanent data loss in case of data corruption.


Reduce the `index.number_of_replicas` index setting.



:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::
