---
navigation_title: Data allocation
mapped_pages: 
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/allow-all-cluster-allocation.html
---

# Allow Elasticsearch to allocate the data in the system [allow-all-cluster-allocation]

The allocation of data in an {{es}} deployment can be controlled using the [enable cluster allocation configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable). In certain circumstances users might want to temporarily disable or restrict the allocation of data in the system.

Forgetting to re-allow all data allocations can lead to unassigned shards.

In order to (re)allow all data to be allocated follow these steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to get the shards assigned we’ll need to change the value of the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) that restricts the assignemnt of the shards to allow all shards to be allocated.

We’ll achieve this by inspecting the system-wide `cluster.routing.allocation.enable` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) and changing the configured value to `all`.

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

4. Inspect the `cluster.routing.allocation.enable` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings):

    ```console
    GET /_cluster/settings?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "persistent": {
        "cluster.routing.allocation.enable": "none" <1>
      },
      "transient": {}
    }
    ```

    1. Represents the current configured value that controls if data is partially or fully allowed to be allocated in the system.

5. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) value to allow all the data in the system to be fully allocated:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.enable" : "all" <1>
      }
    }
    ```

    1. The new value for the `allocation.enable` system-wide configuration is changed to allow all the shards to be allocated.
::::::

::::::{tab-item} Self-managed
In order to get the shards assigned we’ll need to change the value of the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) that restricts the assignemnt of the shards to allow all shards to be allocated.

We’ll achieve this by inspecting the system-wide `cluster.routing.allocation.enable` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) and changing the configured value to `all`.

1. Inspect the `cluster.routing.allocation.enable` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings):

    ```console
    GET /_cluster/settings?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "persistent": {
        "cluster.routing.allocation.enable": "none" <1>
      },
      "transient": {}
    }
    ```

    1. Represents the current configured value that controls if data is partially or fully allowed to be allocated in the system.

2. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) value to allow all the data in the system to be fully allocated:

    ```console
    PUT _cluster/settings
    {
      "persistent" : {
        "cluster.routing.allocation.enable" : "all" <1>
      }
    }
    ```

    1. The new value for the `allocation.enable` system-wide configuration is changed to allow all the shards to be allocated.
::::::

:::::::
