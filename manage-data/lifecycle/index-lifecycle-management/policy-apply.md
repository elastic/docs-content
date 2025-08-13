---
navigation_title: Manually apply a policy to an index
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Manually apply a lifecycle policy to an index [apply-policy-manually]

When you create a new {{es}} index, if the index name matches an index pattern configured in an [index template](/manage-data/data-store/templates.md#index-templates), the new index automatically inherits any settings, mappings, and aliases that are defined in the index template or in any component templates that the index template references. If the template specifies a lifecycle policy, that policy is applied automatically to the newly created index. This process is described in detail in [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

You can also apply a lifecycle policy manually to existing indices, as described on this page. This is useful if you want to:
 * Configure the indices to move through different [data tiers](/manage-data/lifecycle/data-tiers.md) as they age.
 * Perform [lifecycle actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md) such as downsampling or shrinking.
 * Delete the indices when they reach a certain age.

If an index is currently managed by an ILM policy you must first remove that policy before applying a new one. Refer to [Switch to a different lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/policy-updates.md#switch-lifecycle-policies) for details.

You can do this procedure in {{kib}} or using the {{es}} API.

::::{warning}
Do not manually apply a policy that uses the rollover action. Policies that use rollover must be applied by the [index template](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#apply-policy-template). Otherwise, the policy is not carried forward when the rollover action creates a new index.
::::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To apply a lifecycle policy to an existing index:

1. Go to **Stack Management > Index Management**. In the **Indices** tab, search for and select an index. Enable **Include hidden indices** to see the full list of indices.

1. From the **Manage index** dropdown menu select **Add lifecycle policy**.

1. Choose a lifecycle policy and confirm your changes.

:::

:::{tab-item} API
:sync: api
Use the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) to apply a lifecycle policy to an index.

```console
PUT my-index/_settings
{
  "index": {
    "lifecycle": {
      "name": "my_ilm_policy"
    }
  }
}
```

You can apply the same policy to multiple indices by using wildcards in the index name when you call the API.

```console
PUT my-indices*/_settings
{
  "index": {
    "lifecycle": {
      "name": "my_ilm_policy"
    }
  }
}
```

::::::{warning}
Be careful not to inadvertently match indices that you don’t want to modify.
::::::

Once the policy is applied, {{ilm-init}} starts managing the index immediately.

:::
::::
