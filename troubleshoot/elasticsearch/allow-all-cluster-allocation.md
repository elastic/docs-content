---
navigation_title: Data allocation
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/allow-all-cluster-allocation.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Allow Elasticsearch to allocate the data in the system [allow-all-cluster-allocation]

The allocation of data in an {{es}} deployment can be controlled using the [enable cluster allocation configuration](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable). In certain circumstances users might want to temporarily disable or restrict the allocation of data in the system.

Forgetting to re-allow all data allocations can lead to unassigned shards.

To get the shards assigned we need to change the value of the [configuration](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) that restricts the assignment of the shards to allow all shards to be allocated.

We achieve this by inspecting the system-wide `cluster.routing.allocation.enable` [cluster setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) and changing the configured value to `all`.

To (re)allow all data to be allocated, follow these steps:

:::::::{tab-set}

::::::{tab-item} {{kib}}

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} /troubleshoot/images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :screenshot:
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

5. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the [configuration](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) value to allow all the data in the system to be fully allocated:

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

::::::{tab-item} API

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

2. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) the [configuration](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#cluster-routing-allocation-enable) value to allow all the data in the system to be fully allocated:

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
