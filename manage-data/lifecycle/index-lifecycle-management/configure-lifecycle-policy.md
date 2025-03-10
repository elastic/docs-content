---
navigation_title: Configure a policy
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html
applies_to:
  stack: ga
  serverless: ga
---

# Configure a lifecycle policy [set-up-lifecycle-policy]

For {{ilm-init}} to manage an index, a valid policy must be specified in the `index.lifecycle.name` index setting.

To configure a lifecycle policy for [rolling indices](rollover.md), you create the policy and add it to the [index template](../../data-store/templates.md).

To use a policy to manage an index that doesn’t roll over, you can specify a lifecycle policy when you create the index, or apply a policy directly to an existing index.

{{ilm-init}} policies are stored in the global cluster state and can be included in snapshots by setting `include_global_state` to `true` when you [take the snapshot](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md). When the snapshot is restored, all of the policies in the global state are restored and any local policies with the same names are overwritten.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, the necessary policies and configuration changes are applied automatically. You can modify the default policies, but you do not need to explicitly configure a policy or bootstrap an initial index.
::::


## Create lifecycle policy [ilm-create-policy]

To create a lifecycle policy from {{kib}}, open the menu and go to **Stack Management > Index Lifecycle Policies**. Click **Create policy**.

![Create policy page](../../../images/elasticsearch-reference-create-policy.png "")

You specify the lifecycle phases for the policy and the actions to perform in each phase.

The [create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API is invoked to add the policy to the {{es}} cluster.

::::{dropdown} API example
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


::::


::::{important}
The rollover action implicitly always rolls over a data stream or alias if one or more shards contain 200000000 or more documents. Normally a shard will reach 25GB long before it reaches 200M documents, but this isn’t the case for space efficient data sets. Search performance will very likely suffer if a shard contains more than 200M documents. This is the reason of the builtin limit.
::::



## Apply lifecycle policy with an index template [apply-policy-template]

To use a policy that triggers the rollover action, you need to configure the policy in the index template used to create each new index. You specify the name of the policy and the alias used to reference the rolling indices.

::::{tip}
An `index.lifecycle.rollover_alias` setting is only required if using {{ilm}} with an alias. It is unnecessary when using [Data Streams](../../data-store/data-streams.md).
::::


You can use the {{kib}} Create template wizard to create a template. To access the wizard, open the menu and go to **Stack Management > Index Management**. In the **Index Templates** tab, click **Create template**.

![Create template page](../../../images/elasticsearch-reference-create-template-wizard-my_template.png "")

The wizard invokes the [create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to add templates to a cluster.

::::{dropdown} API example
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

1. Use this template for all new indices whose names begin with `test-`
2. Apply `my_policy` to new indices created with this template
3. Define an index alias for referencing indices managed by `my_policy`


::::



### Create an initial managed index [create-initial-index]

When you set up policies for your own rolling indices, if you are not using the recommended [data streams](../../data-store/data-streams.md), you need to manually create the first index managed by a policy and designate it as the write index.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, the necessary policies and configuration changes are applied automatically. You can modify the default policies, but you do not need to explicitly configure a policy or bootstrap an initial index.
::::


The name of the index must match the pattern defined in the index template and end with a number. This number is incremented to generate the name of indices created by the rollover action.

For example, the following request creates the `test-00001` index. Because it matches the index pattern specified in `my_template`, {{es}} automatically applies the settings from that template.

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


## Apply lifecycle policy manually [apply-policy-manually]

You can specify a policy when you create an index or apply a policy to an existing index through {{kib}} Management or the [update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings). When you apply a policy, {{ilm-init}} immediately starts managing the index.

::::{important}
Do not manually apply a policy that uses the rollover action. Policies that use rollover must be applied by the [index template](#apply-policy-template). Otherwise, the policy is not carried forward when the rollover action creates a new index.
::::


The `index.lifecycle.name` setting specifies an index’s policy.

::::{dropdown} API example
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


::::



### Apply a policy to multiple indices [apply-policy-multiple]

You can apply the same policy to multiple indices by using wildcards in the index name when you call the [update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) API.

::::{warning}
Be careful that you don’t inadvertently match indices that you don’t want to modify.
::::


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

1. Updates all indices with names that start with `mylogs-pre-ilm`
%  TEST[continued]


### Switch lifecycle policies [switch-lifecycle-policies]

To switch an index’s lifecycle policy, follow these steps:

1. Remove the existing policy using the [remove policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-remove-policy). Target a data stream or alias to remove the policies of all its indices.

    ```console
    POST logs-my_app-default/_ilm/remove
    ```

2. The remove policy API removes all {{ilm-init}} metadata from the index and doesn’t consider the index’s lifecycle status. This can leave indices in an undesired state.

    For example, the [`forcemerge`](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-forcemerge.md) action temporarily closes an index before reopening it. Removing an index’s {{ilm-init}} policy during a `forcemerge` can leave the index closed indefinitely.

    After policy removal, use the [get index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get) to check an index’s state . Target a data stream or alias to get the state of all its indices.

    ```console
    GET logs-my_app-default
    ```
    %  TEST[continued]

    You can then change the index as needed. For example, you can re-open any closed indices using the [open index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-open).

    ```console
    POST logs-my_app-default/_open
    ```
    %  TEST[continued]

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


