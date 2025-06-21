---
navigation_title: Configure a policy
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Configure a lifecycle policy [set-up-lifecycle-policy]

A {{ilm}} policy defines how your indices are managed over time, automating when and how they transition as they reach a certain age, size, or number of documents.

There a few things to note about how an {{ilm-init}} policy works:

* For {{ilm-init}} to manage an index, you need to specify a valid policy in the `index.lifecycle.name` index setting.

* To configure a lifecycle policy for [rolling indices](rollover.md), you create the policy and add it to the [index template](../../data-store/templates.md).

* To use a policy to manage an index that doesn’t roll over, you can specify a lifecycle policy when you create the index, or apply a policy directly to an existing index.

* {{ilm-init}} policies are stored in the global cluster state and can be included in snapshots by setting `include_global_state` to `true` when you [take the snapshot](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md). When the snapshot is restored, all of the policies in the global state are restored and any local policies with the same names are overwritten.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, the necessary policies and configuration changes are applied automatically. You can modify the default policies, but you do not need to explicitly configure a policy or bootstrap an initial index.
::::

## Create a lifecycle policy [ilm-create-policy]

Create a lifecycle policy to define the index lifecycle phases and the actions to perform in each phase. Use these phases to move your data, as it ages, from your most performant hardware, providing the fastest indexing and search capability, to progressively lower cost options.

You can use the {{kib}} **Create policy** page or the [Create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API to add an ILM policy to an {{es}} cluster.

::::{dropdown} {{kib}} steps
1. In {{kib}} go to **Stack Management > Index Lifecycle Policies**, and select **Create policy**.

    ![Create policy page](/manage-data/images/elasticsearch-reference-create-policy.png "")

1. Specify a name for the lifecycle policy. Later on, when you create an index template to define how indices are created, you'll use this name to assign the lifecycle policy to each index.

1. In the **Hot phase**, by default an ILM-managed index [rolls over](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover) when either:
    * It reaches 30 days of age.
     * The primary shard reaches 50 gigabytes in size.
  
    Disaable **Use recommended defaults** to adjust these values or to roll over based on the size of the primary shard, the number of documents in the primary shard, or the total number of documents in the index.

    ::::{important}
    The rollover action implicitly always rolls over a data stream or alias if one or more shards contain 200000000 or more     documents. Normally a shard will reach 25GB long before it reaches 200M documents, but this isn’t the case for space efficient     data sets. Search performance will very likely suffer if a shard contains more than 200M documents. This is the reason for the     built-in limit.
    ::::


1. By default, only the "hot" index lifecycle phase is enabled. Enable each additional lifecycle phase that you'd like, and for each choose the [index lifecycle actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/) to perform on indices when they enter that phase.

    Note that for each phase after the "hot" phase you have the option to move the data into the phase after a certain duration of time. This duration is calculated from the time of the index rollover and not from the time the index is created.



1. For the final phase that's enabled, choose to either keep data in the phase forever or delete the data after a specified period of time.
::::

::::{dropdown} API steps
Use the [create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API to add an ILM policy to the {{es}} cluster.

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

1. Roll over the index when it reaches 25GB in size
2. Delete the index 30 days after rollover

::::{important}
The rollover action implicitly always rolls over a data stream or alias if one or more shards contain 200000000 or more documents. Normally a shard will reach 25GB long before it reaches 200M documents, but this isn’t the case for space efficient data sets. Search performance will very likely suffer if a shard contains more than 200M documents. This is the reason for the built-in limit.
::::
::::

## Create an index template to apply the lifecycle policy [apply-policy-template]

To use a lifecycle policy that triggers a rollover action, you need to configure the policy in the index template used to create each new index. You specify the name of the policy and the alias used to reference the rolling indices.

You can use the {{kib}} **Create template** wizard or the [Create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to add an index template to a cluster and apply the lifecycle policy to indices matching the template.

::::{dropdown} {{kib}} steps

1. In {{kib}} go to **Stack Management > Index Management**. In the **Index Templates** tab, select **Create template** to open the wizard.

    ![Create template page](/manage-data/images/elasticsearch-reference-create-template-wizard-my_template.png "")

1. On the **Logistics** page: 
    1. Specify a name for the template.
    1. Specify a pattern to match the indices you want to manage with the lifecycle policy. For example, `my-index-*`.
    1. If you're storing continuously generated, append-only data, you can opt to create [data streams](/manage-data/data-store/data-streams.md) instead of indices for more efficient storage. If you enable this option, you can also enable **Data retention** to configure how long your indexed data is kept.

        :::{important}
        When the **Data retention** option is set, data is guaranteed to be stored for the specified retention duration. Elasticsearch is allowed at a later time to delete data older than this duration. This setting replaces any data retention settings that may be defined in an ILM policy. Refer to the [Data stream retention](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md) tutorial to learn more.
        :::

    1. Configure any other options you'd like, including:
        * The [Index mode](elasticsearch://reference/elasticsearch/index-settings/time-series) to use for the created indices.
        * The template priority, version, and any metadata.
        * Whether or not to overwrite the `action.auto_create_index` cluster setting.
        
        Refer to the [Create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) documentation for details about these options.

1. On the **Component templates** page, use the search and filter tools to select any [component templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) to include in the index template. The index template will inherit the settings, mappings, or aliases defined in the component templates and apply them to indices when they're created.

1. On the **Index settings** page:
    1. Configure ILM by specifying the [ILM settings](https://www.elastic.co/docs/api/doc/elasticsearch/configuration-reference/index-lifecycle-management-settings#_index_level_settings_2) to apply to the indices:
        * `index.lifecycle.name` - The lifecycle policy that will manage the created indices.
        * `index.lifecycle.rollover_alias` - The index [alias](/manage-data/data-store/aliases.md) used to query and manage the set of indices associated with a lifecycle policy that contains a rollover action.

            :::{tip}
            The `index.lifecycle.rollover_alias` setting is required only if you're using {{ilm}} with an alias. It is unnecessary when using [Data Streams](../../data-store/data-streams.md).
            :::

    1. Add any additional [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md), that should be applied to the indices as they're created.

    For example:

    ```json
    {
      "index.lifecycle.name": "my_policy",
      "index.lifecycle.rollover_alias": "test-alias",
      "number_of_shards": 1,
      "number_of_replicas": 1
    }
    ```

1. On the **Mappings** page, you can customize the fields and data types used when documents are indexed into {{es}}. Refer to [Mapping](/manage-data/data-store/) for details.

1. On the **Aliases** page, you can specify an [alias](/manage-data/data-store/aliases.md), which is used as a single named entity to query or manage the set of indices. This isn't required when configuring ILM.

1. On the **Review** page, confirm your selections. You can also check both the format of the index template that will be created and the associated API request.

The newly created index template will be used for all new indices whose name matches the specified pattern, and for each of these the specified ILM policy will be applied.

::::

::::{dropdown} API steps
Run the following API request:

```console
PUT _index_template/my_template
{
  "index_patterns": ["test-*"], <1>
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "my_policy", <2>
      "index.lifecycle.rollover_alias": "test-alias" <3>
    }
  }
}
```

1. Use this template for all new indices whose name begin with `test-`
2. Apply `my_policy` to new indices created with this template
3. Define an index alias for referencing indices managed by `my_policy`

    :::{tip}
    The `index.lifecycle.rollover_alias` setting is required only if you're using {{ilm}} with an alias. It is unnecessary when using [Data Streams](../../data-store/data-streams.md).
    :::
::::


## Create an initial managed index [create-initial-index]

When you set up policies for your own rolling indices, if you are not using the recommended [data streams](../../data-store/data-streams.md), you need to manually create the first index managed by a policy and designate it as the write index.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, the necessary policies and configuration changes are applied automatically. You can modify the default policies, but you do not need to explicitly configure a policy or bootstrap an initial index.
::::

The name of the index must match the pattern defined in the index template and end with a number. This number is incremented to generate the name of indices created by the rollover action.

You can use the {{kib}} **Create index** UI or the [Create an index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) to create the initial managed index.

::::{dropdown} {{kib}} steps
1. In {{kib}} go to **Stack Management > Index Management**. In the **Indices** tab, select **Create index**.
1. Specify a name for the index that matches the index template pattern and that ends with a number. For example, `test-00001`.
1. Since this is for the backing index of a datastream, leave the **Index mode** set to the default **Standard**.

<!--- QUESTION: How do I set the alias for this initial index? I gather it has to match `index.lifecycle.rollover_alias` in the index tempate. --->

Now you can start indexing data to the rollover alias specified in the lifecycle policy. With the sample `my_policy` policy, the rollover action is triggered once the initial index exceeds 25GB. {{ilm-init}} then creates a new index that becomes the write index for the `test-alias`.
::::

::::{dropdown} API steps
The following request creates the `test-00001` index. Because it matches the index pattern specified in `my_template`, {{es}} automatically applies the settings from that template.

```console
PUT test-000001
{
  "aliases": {
    "test-alias":{
      "is_write_index": true <1>
    }
  }
}
```

1. Set this initial index to be the write index for this alias.

Now you can start indexing data to the rollover alias specified in the lifecycle policy. With the sample `my_policy` policy, the rollover action is triggered once the initial index exceeds 25GB. {{ilm-init}} then creates a new index that becomes the write index for the `test-alias`.
::::

## Apply a lifecycle policy manually [apply-policy-manually]

You can specify a policy when you create an index, or use the {{kib}} **Index management** UI or the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) to apply a lifecycle policy to an existing index.

::::{important}
Do not manually apply a policy that uses the rollover action. Policies that use rollover must be applied by the [index template](#apply-policy-template). Otherwise, the policy is not carried forward when the rollover action creates a new index.
::::

::::{dropdown} {{kib}} steps
1. In {{kib}} go to **Stack Management > Index Management**. In the **Indices** tab, search for and select the index that you created, for example `test-00001`. Note that to view system indices you need to enable **Include hidden indices**.

1. From the **Manage index** dropdown menu select **Add lifecycle policy**.

1. Choose a lifecycle policy and confirm your changes.

Once the policy is applied, {{ilm-init}} starts managing the index immediately.


<!--- QUESTION: Is there a UI way to add a policy to multiple indices? I wasn't able to do so. --->

::::

::::{dropdown} API steps

### Apply an policy to a single index [apply-policy-single]

In the following request, the `index.lifecycle.name` setting specifies an index’s policy.

```console
PUT test-index
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

### Apply a policy to multiple indices [apply-policy-multiple]

You can apply the same policy to multiple indices by using wildcards in the index name when you call the API.

:::{warning}
Be careful that you don’t inadvertently match indices that you don’t want to modify.
:::

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

::::





## Switch lifecycle policies [switch-lifecycle-policies]

To switch an index’s lifecycle policy you can use the {{kib}} index management tools or the {{es}} [remove policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy) and [update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) APIs.

::::{dropdown} {{kib}} steps

1. In {{kib}} go to **Stack Management > Index Management**. In the **Indices** tab, search for and select the index that you that you want to switch to a new policy. You can use the **Lifecycle status** filter to narrow the list.

1. From the **Manage index** dropdown menu select **Remove lifecycle policy**. Confirm your choice and then the ILM policy is removed.

1. From the **Manage index** dropdown menu select **Add lifecycle policy**, and then select a new policy to apply.

::::

::::{dropdown} API steps

1. Remove the existing policy using the [remove policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy). Target a data stream or alias to remove the policies of all its indices.

    ```console
    POST logs-my_app-default/_ilm/remove
    ```

2. The remove policy API removes all {{ilm-init}} metadata from the index and doesn’t consider the index’s lifecycle status. This can leave indices in an undesired state.

    For example, the [`forcemerge`](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) action temporarily closes an index before reopening it. Removing an index’s {{ilm-init}} policy during a `forcemerge` can leave the index closed indefinitely.

    After policy removal, use the [get index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get) to check an index’s state. Target a data stream or alias to get the state of all its indices.

    ```console
    GET logs-my_app-default
    ```

    You can then change the index as needed. For example, you can re-open any closed indices using the [open index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open).

    ```console
    POST logs-my_app-default/_open
    ```

3. Assign a new policy using the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings). Target a data stream or alias to assign a policy to all its indices.

    ::::{warning}
    Don’t assign a new policy without first removing the existing policy. This can cause [phase execution](index-lifecycle.md#ilm-phase-execution) to silently fail.
    ::::


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

::::
