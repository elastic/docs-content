---
navigation_title: Preferred data tier
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/add-tier.html
---

% marciw move this page to a new index allocation subsection
% or just move it down in the ToC
% and this page really really needs rewriting

# Add a preferred data tier to a deployment [add-tier]

The allocation of indices in an {{es}} deployment can be allocated on [data tiers](../../manage-data/lifecycle/data-tiers.md).

In order to allow indices to be allocated, follow these steps to add the [data tier](../../manage-data/lifecycle/data-tiers.md) the indices expect to be allocated on to your deployment:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to get the shards assigned we need enable a new tier in the deployment.

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

4. Determine which tier an index expects for assignment. [Retrieve](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) the configured value for the `index.routing.allocation.include._tier_preference` setting:

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

    1. Represents a comma-separated list of data tier node roles this index is allowed to be allocated on, the first one in the list being the one with the higher priority i.e. the tier the index is targeting. e.g. in this example the tier preference is `data_warm,data_hot` so the index is targeting the `warm` tier and more nodes with the `data_warm` role are needed in the {{es}} cluster.

5. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Manage this deployment**.
6. From the right hand side, click to expand the **Manage** dropdown button and select **Edit deployment** from the list of options.
7. On the **Edit** page, click on **+ Add Capacity** for the tier you identified you need to enable in your deployment. Choose the desired size and availability zones for the new tier.
8. Navigate to the bottom of the page and click the **Save** button.
::::::

::::::{tab-item} Self-managed
In order to get the shards assigned you can add more nodes to your {{es}} cluster and assign the index’s target tier [node role](../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md#assign-data-tier) to the new nodes.

To determine which tier an index requires for assignment, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

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

1. Represents a comma-separated list of data tier node roles this index is allowed to be allocated on, the first one in the list being the one with the higher priority i.e. the tier the index is targeting. e.g. in this example the tier preference is `data_warm,data_hot` so the index is targeting the `warm` tier and more nodes with the `data_warm` role are needed in the {{es}} cluster.
::::::

:::::::
