---
navigation_title: Index allocation
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/allow-all-index-allocation.html
---

% Need to retitle to be about the problem, not the solution
% New subsection about unassigned shards?

# Allow Elasticsearch to allocate the index [allow-all-index-allocation]

The allocation of data can be controlled using the [enable allocation configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-routing-allocation-enable-setting). In certain circumstances users might want to temporarily disable or restrict the allocation of data.

Forgetting to re-allow all data allocation can lead to unassigned shards.

In order to (re)allow all data to be allocated follow these steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to get the shards assigned we’ll need to change the value of the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-routing-allocation-enable-setting) that restricts the assignemnt of the shards to `all`.

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

4. Inspect the `index.routing.allocation.enable` [index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) for the index with unassigned shards:

    ```console
    GET /my-index-000001/_settings/index.routing.allocation.enable?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.enable": "none" <1>
        }
      }
    }
    ```

    1. Represents the current configured value that controls if the index is allowed to be partially or totally allocated.

5. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-routing-allocation-enable-setting) value to allow the index to be fully allocated:

    ```console
    PUT /my-index-000001/_settings
    {
      "index" : {
        "routing.allocation.enable" : "all" <1>
      }
    }
    ```

    1. The new value for the `allocation.enable` configuration for the `my-index-000001` index is changed to allow all the shards to be allocated.
::::::

::::::{tab-item} Self-managed
In order to get the shards assigned we’ll need to change the value of the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-routing-allocation-enable-setting) that restricts the assignemnt of the shards to `all`.

1. Inspect the `index.routing.allocation.enable` [index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) for the index with unassigned shards:

    ```console
    GET /my-index-000001/_settings/index.routing.allocation.enable?flat_settings
    ```

    The response will look like this:

    ```console-result
    {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.enable": "none" <1>
        }
      }
    }
    ```

    1. Represents the current configured value that controls if the index is allowed to be partially or totally allocated.

2. [Change](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) the [configuration](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index-modules.md#index-routing-allocation-enable-setting) value to allow the index to be fully allocated:

    ```console
    PUT /my-index-000001/_settings
    {
      "index" : {
        "routing.allocation.enable" : "all" <1>
      }
    }
    ```

    1. The new value for the `allocation.enable` configuration for the `my-index-000001` index is changed to allow all the shards to be allocated.
::::::

:::::::
