---
navigation_title: Not enough nodes to allocate shard replicas
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/increase-tier-capacity.html
---

# Warning: Not enough nodes to allocate all shard replicas [increase-tier-capacity]

Distributing copies of the data (index shard replicas) on different nodes can parallelize processing requests thus speeding up search queries. This can be achieved by increasing the number of replica shards up to the maximum value (total number of nodes minus one) which also serves the purpose to protect against hardware failure. If the index has a preferred tier, Elasticsearch will only place the copies of the data for that index on nodes in the target tier.

If a warning is encountered with not enough nodes to allocate all shard replicas, you can influence this behavior by adding more nodes to the cluster (or tier if tiers are in use), or by reducing the [`index.number_of_replicas`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting.

In order to fix this follow the next steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
One way to get the replica shards assigned is to add an availability zone. This will increase the number of data nodes in the {{es}} cluster so that the replica shards can be assigned. This can be done by editing your deployment. But first you need to discover which tier an index is targeting for assignment. Do this using {{kib}}.

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


To inspect which tier an index is targeting for assignment, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

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


Now that you know the tier, you want to increase the number of nodes in that tier so that the replicas can be allocated. To do this you can either increase the size per zone to increase the number of nodes in the availability zone(s) you were already using, or increase the number of availability zones. Go back to the deployment’s landing page by clicking on the three horizontal bars on the top left of the screen and choosing **Manage this deployment**. On that page click the **Manage** button, and choose **Edit deployment**. Note that you must be logged in to [https://cloud.elastic.co/](https://cloud.elastic.co/) in order to do this. In the {{es}} section, find the tier where the replica shards could not be assigned.

:::{image} ../../images/elasticsearch-reference-ess-advanced-config-data-tiers.png
:alt: {{kib}} Console
:class: screenshot
:::

* Option 1: Increase the size per zone

    * Look at the values in the **Size per zone** drop down. One node is created in each zone for every 64 GB of RAM you select here. If you currently have 64 GB RAM or less selected, you have one node in each zone. If you select 128 GB RAM, you will get 2 nodes per zone. If you select 192 GB RAM, you will get 3 nodes per zone, and so on. If the value is less than the maximum possible, you can choose a higher value for that tier to add more nodes.

* Option 2: Increase the number of availability zones

    * Find the **Availability zones** selection. If it is less than 3, you can select a higher number of availability zones for that tier.


If it is not possible to increase the size per zone or the number of availability zones, you can reduce the number of replicas of your index data. We’ll achieve this by inspecting the [`index.number_of_replicas`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting index setting and decreasing the configured value.

1. Access {{kib}} as described above.
2. Inspect the [`index.number_of_replicas`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting.

    ```console
    GET /my-index-000001/_settings/index.number_of_replicas
    ```

    The response will look like this:

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

3. Use the `_cat/nodes` API to find the number of nodes in the target tier:

    ```console
    GET /_cat/nodes?h=node.role
    ```

    The response will look like this, containing one row per node:

    ```console-result
    himrst
    mv
    himrst
    ```

    You can count the rows containing the letter representing the target tier to know how many nodes you have. See [{{api-query-parms-title}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) for details. The example above has two rows containing `h`, so there are two nodes in the hot tier.

4. [Decrease](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) the value for the total number of replica shards required for this index. As replica shards cannot reside on the same node as primary shards for [high availability](../../deploy-manage/production-guidance/availability-and-resilience.md), the new value needs to be less than or equal to the number of nodes found above minus one. Since the example above found 2 nodes in the hot tier, the maximum value for `index.number_of_replicas` is 1.

    ```console
    PUT /my-index-000001/_settings
    {
      "index" : {
        "number_of_replicas" : 1 <1>
      }
    }
    ```

    1. The new value for the `index.number_of_replicas` index configuration is decreased from the previous value of `2` to `1`. It can be set as low as 0 but configuring it to 0 for indices other than [searchable snapshot indices](../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) may lead to temporary availability loss during node restarts or permanent data loss in case of data corruption.
::::::

::::::{tab-item} Self-managed
In order to get the replica shards assigned you can add more nodes to your {{es}} cluster and assign the index’s target tier [node role](../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md#assign-data-tier) to the new nodes.

To inspect which tier an index is targeting for assignment, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

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


Alternatively, if adding more nodes to the {{es}} cluster is not desired, inspect the [`index.number_of_replicas`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting and decrease the configured value:

1. Inspect the [`index.number_of_replicas`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) index setting for the index with unassigned replica shards:

    ```console
    GET /my-index-000001/_settings/index.number_of_replicas
    ```

    The response will look like this:

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

2. Use the `_cat/nodes` API to find the number of nodes in the target tier:

    ```console
    GET /_cat/nodes?h=node.role
    ```

    The response will look like this, containing one row per node:

    ```console-result
    himrst
    mv
    himrst
    ```

    You can count the rows containing the letter representing the target tier to know how many nodes you have. See [{{api-query-parms-title}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) for details. The example above has two rows containing `h`, so there are two nodes in the hot tier.

3. [Decrease](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) the value for the total number of replica shards required for this index. As replica shards cannot reside on the same node as primary shards for [high availability](../../deploy-manage/production-guidance/availability-and-resilience.md), the new value needs to be less than or equal to the number of nodes found above minus one. Since the example above found 2 nodes in the hot tier, the maximum value for `index.number_of_replicas` is 1.

    ```console
    PUT /my-index-000001/_settings
    {
      "index" : {
        "number_of_replicas" : 1 <1>
      }
    }
    ```

    1. The new value for the `index.number_of_replicas` index configuration is decreased from the previous value of `2` to `1`. It can be set as low as 0 but configuring it to 0 for indices other than [searchable snapshot indices](../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) may lead to temporary availability loss during node restarts or permanent data loss in case of data corruption.
::::::

:::::::
::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::
