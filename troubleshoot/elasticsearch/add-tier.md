---
navigation_title: Preferred data tier
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/add-tier.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move this page to a new index allocation subsection
% or just move it down in the ToC
% and this page really really needs rewriting

# Add a preferred data tier to a deployment [add-tier]

In an {{es}} deployment, an index and its shards can be allocated to [data tiers](../../manage-data/lifecycle/data-tiers.md) using routing and allocation settings.

To allow indices to be allocated, follow these steps:

1. [Determine which tiers](#determine-target-tier) an index's shards can be allocated to.
1. [Resize your deployment](#resize-your-deployment).


## Determine the target tier [determine-target-tier]

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

1. Represents a comma-separated list of data tier node roles this index is allowed to be allocated on, the first one in the list being the one with the higher priority i.e. the tier the index is targeting. e.g. in this example the tier preference is `data_warm,data_hot` so the index is targeting the `warm` tier and more nodes with the `data_warm` role are needed in the {{es}} cluster.

## Resize your deployment [resize-your-deployment]



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