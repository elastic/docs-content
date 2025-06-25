---
navigation_title: Apply a policy to an index
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Apply a lifecycle policy to an index [apply-policy-manually]

When you create new {{es}} index you can use an index template to apply the lifecycle policy by which the index will be managed. This process is described in [Configure a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md).

You can also manually apply a lifecycle policy to an existing index, as described here. You can do this in {{kib}} or using the {{es}} API.

::::{important}
Do not manually apply a policy that uses the rollover action. Policies that use rollover must be applied by the index template. Otherwise, the policy is not carried forward when the rollover action creates a new index.
::::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To apply a lifecycle policy to an existing index:

1. Go to **Stack Management > Index Management**. In the **Indices** tab, search for and select the index that you created, for example `test-00001`. Note that to view system indices you need to enable **Include hidden indices**.

1. From the **Manage index** dropdown menu select **Add lifecycle policy**.

1. Choose a lifecycle policy and confirm your changes.

Once the policy is applied, {{ilm-init}} starts managing the index immediately.
:::

:::{tab-item} API
:sync: api
Use the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) to apply a lifecycle policy to one or more indices.

## Apply a policy to a single index [apply-policy-single]

In the following request, the `index.lifecycle.name` setting specifies an index’s policy.

```console
PUT my-index
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1,
    "index.lifecycle.name": "my_policy" <1>
  }
}
```

1. Sets the lifecycle policy for the index.

Once the policy is applied, {{ilm-init}} starts managing the index immediately.

## Apply a policy to multiple indices [apply-policy-multiple]

You can apply the same policy to multiple indices by using wildcards in the index name when you call the API.

```console
PUT mylogs-pre-ilm*/_settings <1>
{
  "index": {
    "lifecycle": {
      "name": "mylogs_policy_existing"
    }
  }
}
```

1. Updates all indices with names that start with `mylogs-pre-ilm`.

::::::{warning}
Be careful not to inadvertently match indices that you don’t want to modify.
::::::
:::
::::
