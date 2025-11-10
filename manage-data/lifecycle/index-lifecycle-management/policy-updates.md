---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Update or switch a lifecycle policy

You can change how the lifecycle of an index or collection of rolling indices is managed by modifying the current policy or switching to a different policy.

To ensure that policy updates don’t put an index into a state where it can’t exit the current phase, the phase definition is cached in the index metadata when it enters the phase. If changes can be safely applied, {{ilm-init}} updates the cached phase definition. If they cannot, phase execution continues using the cached definition.

When the index advances to the next phase, it uses the phase definition from the updated policy.

To configure an index not currently managed by {{ilm-init}} to be governed by an lifecycle policy, refer to [Manually apply a policy to an index](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md).

## How changes are applied [ilm-apply-changes]

When a policy is initially applied to an index, the index gets the latest version of the policy. If you update the policy, the policy version is bumped and {{ilm-init}} can detect that the index is using an earlier version that needs to be updated.

Changes to `min_age` are not propagated to the cached definition. Changing a phase’s `min_age` does not affect indices that are currently executing that phase.

For example, if you create a policy that has a hot phase that does not specify a `min_age`, indices immediately enter the hot phase when the policy is applied. If you then update the policy to specify a `min_age` of 1 day for the hot phase, that has no effect on indices that are already in the hot phase. Indices created *after* the policy update won’t enter the hot phase until they are a day old.


## How new policies are applied [ilm-apply-new-policy]

When you apply a different policy to a managed index, the index completes the current phase using the cached definition from the previous policy. The index starts using the new policy when it moves to the next phase.


## Update an existing lifecycle policy [update-lifecycle-policy]

You can update a lifecycle policy that is currently associated with one or more indices.

:::{warning}
Avoid changing any managed policies that are shipped with {{es}}, such as `logs@lifecycle` or `metrics@lifecycle`. Instead, create a new, [custom ILM policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md) and associate it with the intended index template or indices.
:::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To update a lifecycle policy:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Use the search tool to find the lifecycle policy that you want to update.

   You can deselect the **Include managed system policies** option to filter out managed policies from the list, since it's strongly recommended not to update these.

1. Check the links in the **Linked index templates** and **Linked indices** columns to confirm that your updates will apply only to templates or indices that you want to affect with a new policy.

1. For the policy that you want to update, select the `edit` icon in the **Actions** menu.

    Note that from the **Actions** menu you can also choose to add the ILM policy to any existing index templates.

1. On the **Edit policy** page, enable any {{ilm-init}} phases as needed, and expand **Advanced settings** to adjust the [index lifecycle actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md) configured for that phase.
:::



:::{tab-item} API
:sync: api
Use the [Create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API to update an existing ILM policy:

```console
PUT _ilm/policy/my_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "25GB" <1>
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {} <2>
        }
      }
    }
  }
}
```

1. Roll over the index when one or more of its shards reach 25GB in size.
2. Delete the index 30 days after rollover.


The specified policy will be replaced and the policy version is incremented.
:::
::::


## Switch to a different lifecycle policy [switch-lifecycle-policies]

You can change an index to be managed by a different {{ilm-init}} policy.

:::::{warning}
When you remove an ILM policy, all {{ilm-init}} metadata is removed from the managed index without consideration of the index’s lifecycle status. This can leave indices in an undesired state.

For example, in certain cases the [`forcemerge`](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) action temporarily closes an index before reopening it. Removing an index’s {{ilm-init}} policy during a `forcemerge` can leave the index closed until it is manually reopened.
:::::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To switch an index’s lifecycle policy:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Indices** tab, search for and select the index that you that you want to switch to a new policy. You can use the **Lifecycle status** filter to narrow the list.

1. From the **Manage index** dropdown menu, select **Remove lifecycle policy**. Confirm your choice before the ILM policy is removed.

1. From the **Manage index** dropdown menu, select **Add lifecycle policy**, and then select a new policy to apply.
:::

:::{tab-item} API
:sync: api
Use the {{es}} [remove policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy) and [update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) APIs to switch an index’s lifecycle policy:

1. Remove the existing policy using the [remove policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy). Target a data stream or alias to remove the policies of all its indices.

    ```console
    POST logs-my_app-default/_ilm/remove
    ```

2. Use the [get index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get) to check an index’s state. Target a data stream or alias to get the state of all its indices.

    ```console
    GET logs-my_app-default
    ```

    You can then change the index as needed. For example, you can re-open any closed indices using the [open index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open).

    ```console
    POST logs-my_app-default/_open
    ```

3. Assign a new policy using the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings). Target a data stream or alias to assign a policy to all its indices.

    ::::::{warning}
    * Don’t assign a new policy without first removing the existing policy. This can cause [phase execution](index-lifecycle.md#ilm-phase-execution) to silently fail.
    ::::::

    ```console
    PUT logs-my_app-default/_settings
    {
      "index": {
        "lifecycle": {
          "name": "new-lifecycle-policy"
        }
      }
    }
    ```

:::
::::