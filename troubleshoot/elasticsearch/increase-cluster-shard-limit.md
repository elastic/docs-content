---
navigation_title: Total number of shards per node reached
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-cluster-shard-limit.html
---

% marciw move to a new Unassigned shards subsection

# Total number of shards per node has been reached [increase-cluster-shard-limit]

Elasticsearch tries to take advantage of all the available resources by distributing data (index shards) amongst the cluster nodes.

Users might want to influence this data distribution by configuring the [`cluster.routing.allocation.total_shards_per_node`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/total-shards-per-node.md#cluster-total-shards-per-node) system setting to restrict the number of shards that can be hosted on a single node in the system, regardless of the index. Various configurations limiting how many shards can be hosted on a single node can lead to shards being unassigned due to the cluster not having enough nodes to satisfy the configuration.

In order to fix this follow the next steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to get the shards assigned we’ll need to increase the number of shards that can be collocated on a node in the cluster. We’ll achieve this by inspecting the system-wide `cluster.routing.allocation.total_shards_per_node` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) and increasing the configured value.

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. Inspect the `cluster.routing.allocation.total_shards_per_node` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings):

    ```console
    GET /_cluster/settings?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "persistent": {
        "cluster.routing.allocation.total_shards_per_node": "300" <1>
      },
      "transient": {}
    }
    ```

    1. Represents the current configured value for the total number of shards that can reside on one node in the system.

5. [Increase](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the value for the total number of shards that can be assigned on one node to a higher value:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.total_shards_per_node" : 400 <1>
      }
    }
    ```

    1. The new value for the system-wide `total_shards_per_node` configuration is increased from the previous value of `300` to `400`. The `total_shards_per_node` configuration can also be set to `null`, which represents no upper bound with regards to how many shards can be collocated on one node in the system.
::::::

::::::{tab-item} Self-managed
In order to get the shards assigned you can add more nodes to your {{es}} cluster and assign the index’s target tier [node role](../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md#assign-data-tier) to the new nodes.

To inspect which tier is an index targeting for assignment, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

```console
GET /my-index-000001/_settings/index.routing.allocation.include._tier_preference?flat_settings
```

The response will look like this:

```console-result
{
  "my-index-000001": {
    "settings": {
      "index.routing.allocation.include._tier_preference": "data_warm,data_hot" <1>
    }
  }
}
```

1. Represents a comma separated list of data tier node roles this index is allowed to be allocated on, the first one in the list being the one with the higher priority i.e. the tier the index is targeting. e.g. in this example the tier preference is `data_warm,data_hot` so the index is targeting the `warm` tier and more nodes with the `data_warm` role are needed in the {{es}} cluster.


Alternatively, if adding more nodes to the {{es}} cluster is not desired, inspecting the system-wide `cluster.routing.allocation.total_shards_per_node` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) and increasing the configured value:

1. Inspect the `cluster.routing.allocation.total_shards_per_node` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) for the index with unassigned shards:

    ```console
    GET /_cluster/settings?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "persistent": {
        "cluster.routing.allocation.total_shards_per_node": "300" <1>
      },
      "transient": {}
    }
    ```

    1. Represents the current configured value for the total number of shards that can reside on one node in the system.

2. [Increase](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the value for the total number of shards that can be assigned on one node to a higher value:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.total_shards_per_node" : 400 <1>
      }
    }
    ```

    1. The new value for the system-wide `total_shards_per_node` configuration is increased from the previous value of `300` to `400`. The `total_shards_per_node` configuration can also be set to `null`, which represents no upper bound with regards to how many shards can be collocated on one node in the system.
::::::

:::::::
::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::
