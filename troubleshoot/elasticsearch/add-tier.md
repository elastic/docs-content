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

The allocation of indices in an {{es}} deployment can be allocated on [data tiers](../../manage-data/lifecycle/data-tiers.md).

To allow indices to be allocated, follow these steps.

You can run the following steps using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [Elasticsearch API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

To get the shards assigned, you can add more nodes to your {{es}} cluster and assign the index’s target tier [node role](../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md#assign-data-tier) to the new nodes.

To determine which tier an index requires for assignment, use the [get index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

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

