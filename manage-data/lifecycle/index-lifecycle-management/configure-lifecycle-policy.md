---
navigation_title: Create an {{ilm-init}} policy
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Create an index lifecycle management policy in {{es}} [set-up-lifecycle-policy]

An [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) policy defines how indices transition through different phases over time. This guide explains how to create a new {{ilm-init}} policy with configurable rollover, retention, and deletion rules, and then apply the policy using an index template. 

You can use {{ilm-init}} to manage both indices and [data streams](/manage-data/data-store/data-streams.md). There are fewer configuration steps required to set up ILM with data streams. In comparison, configuring ILM with indices requires you to create an initial managed index and alias in addition to defining a policy and creating a template to apply it. This page describes the steps to configure an {{ilm-init}} lifecycle policy for both scenarios.

:::{note}
This page is specifically about using {{ilm-init}} with indices or data streams. If you're looking for a simpler data streams lifecycle management option that focuses on a data retention period, refer to [Data stream lifecycle](/manage-data/lifecycle/data-stream.md). Check [Data lifecycle](/manage-data/lifecycle.md) to compare these lifecycle management options.
:::

**Consider these aspects when creating an {{ilm-init}} policy:**

* To manage an index or data stream with {{ilm-init}}, you need to specify a valid policy in the `index.lifecycle.name` index setting.

* To configure a lifecycle policy for [rolling indices](rollover.md) or data streams, you create the policy and add it to the [index template](../../data-store/templates.md). Data streams are generally recommended in favor of rolling indices due to the lesser amount of manual configuration required. When you use {{ilm-init}} with rolling indices, you must, additionally, create an initial managed index (ensuring that it is named appropriately) and assign an alias to it. This additional process is described in [Step 3](#create-initial-index) on this page.

* To use a policy to manage a single index, you can specify a lifecycle policy when you create the index, or apply a policy directly to an existing index.

* {{ilm-init}} policies are stored in the global cluster state and can be included in snapshots by setting `include_global_state` to `true` when you [take the snapshot](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md). When the snapshot is restored, all of the policies in the global state are restored and any local policies with the same names are overwritten.

## Overview [ilm-configure-overview]

To set up ILM to manage one or more indices, the general procedure is as follows:

1. [Create a lifecycle policy](#ilm-create-policy)
2. [Create an index template to apply the lifecycle policy](#apply-policy-template)

If you're configuring ILM for rolling indices and not using [data streams](../../data-store/data-streams.md), you additionally need to:

3. [Create an initial managed index and alias](#create-initial-index)

You can perform these actions in {{kib}} or using the {{es}} API.

## Create a lifecycle policy [ilm-create-policy]

A lifecycle policy defines a set of index lifecycle phases and the actions to perform on the managed indices in each phase.

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To add an ILM policy to an {{es}} cluster:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Create policy**.

    ![Create policy page](/manage-data/images/elasticsearch-reference-create-policy.png "")

1. Specify a name for the lifecycle policy. Later on, when you create an index template to define how indices are created, you'll use this name to assign the lifecycle policy to each index.

1. In the **Hot phase**, a [rollover index lifecycle action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) is executed by default when either:
    * The index reaches 30 days of age.
    * One or more primary shards reach 50 GB in size.

    Disable **Use recommended defaults** to adjust these values or to roll over based on the size of the primary shard, the number of documents in the primary shard, or the total number of documents in the index.

    ::::{important}
    The rollover action implicitly rolls over a data stream or alias if one or more shards contain 200,000,000 or more documents. Typically, a shard will reach 50GB before it reaches 200M documents, however, this isn’t the case for space efficient data sets. This built-in limit exists to avoid Search performance loss if a shard contains more than 200M documents. For more information about recommended limits, refer to [](/deploy-manage/production-guidance/optimize-performance/size-shards.md).
    ::::

1. By default, only the hot index lifecycle phase is enabled. Enable each additional lifecycle phase that you'd like, and for each choose any [index lifecycle actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md) to perform on indices when they enter that phase.

    For example, you could choose the action to [downsample](/manage-data/data-store/data-streams/downsampling-time-series-data-stream.md) the index, which aggregates the time series data into statistical summaries, reducing the data storage size.

    ![Create policy page](/manage-data/images/elasticsearch-reference-create-policy-downsample.png "")

    ::::{note}
    For each phase after the hot phase, you have the option to move the data into the next phase after a certain duration of time. This duration is calculated from the time of the index rollover and not from the time the index is created.
    ::::


1. For the final phase that's enabled, choose to either keep the data in the phase forever or delete the data after a specified period of time.
:::

:::{tab-item} API
:sync: api
Use the [Create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API to add an ILM policy to the {{es}} cluster:

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

1. Roll over the index when one or more primary shards reach 25GB in size.
2. Delete the index 30 days after rollover

::::{important}
The rollover action implicitly rolls over a data stream or alias if one or more shards contain 200,000,000 or more documents. Typically, a shard will reach 50GB before it reaches 200M documents, however, this isn’t the case for space efficient data sets. This built-in limit exists to avoid Search performance loss if a shard contains more than 200M documents.
:::
::::

## Create an index template to apply the lifecycle policy [apply-policy-template]

To use a lifecycle policy that triggers a rollover action, you need to configure the policy in the index template used to create each new index. You specify the name of the policy and the alias used to reference the rolling indices.

:::{tip}
If you already have an index template to which you'd like to add an {{ilm-init}} policy, you can do this from the **Index Lifecycle Policies** management page. Search for and select the policy you want, and from the **Actions** menu, select **Add to index template**.
:::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To add an index template to a cluster and apply the lifecycle policy to indices matching the template:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, select **Create template**.

    ![Create template page](/manage-data/images/elasticsearch-reference-create-template-wizard-my_template.png "")

1. On the **Logistics** page:
    1. Specify a name for the template.
    1. Specify a pattern to match the indices you want to manage with the lifecycle policy. For example, `my-index-*`.
    1. If you're storing continuously generated, append-only data, you can opt to create [data streams](/manage-data/data-store/data-streams.md) instead of indices for more efficient storage.

        :::{note}
        When you enable the data stream option, an option to set **Data retention** also becomes available. Since you're creating an index lifecycle policy to manage indices, the  **Data retention** option must remain disabled. Data retention is applicable only if you're using a data stream lifecycle, which is an alternative to ILM. Refer to the [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) to learn more.
        :::


    1. Configure any other options you'd like, including:
        * The [index mode](elasticsearch://reference/elasticsearch/index-settings/time-series.md) to use for the created indices.
        * The template priority, version, and any metadata.
        * Whether or not to overwrite the `action.auto_create_index` cluster setting.

        Refer to the [Create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) documentation for details about these options.

1. On the **Component templates** page, use the search and filter tools to select any [component templates](/manage-data/data-store/templates.md#component-templates) to include in the index template. The index template will inherit the settings, mappings, and aliases defined in the component templates and apply them to indices when they're created.

1. On the **Index settings** page:
    1. Configure ILM by specifying the [ILM settings](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md) to apply to the indices:
        * `index.lifecycle.name` - The lifecycle policy to manage the created indices.
        * `index.lifecycle.rollover_alias` - The index [alias](/manage-data/data-store/aliases.md) used for querying and managing the set of indices associated with a lifecycle policy that contains a rollover action.

            :::{tip}
            The `index.lifecycle.rollover_alias` setting is required only if you're using {{ilm}} with an alias. It is unnecessary when using [Data Streams](../../data-store/data-streams.md).
            :::

    1. Optional: Add any additional [index settings](elasticsearch://reference/elasticsearch/index-settings/index.md), that should be applied to the indices as they're created. For example, you can set the number of shards and replicas for each index:

        ```json
        {
          "index.lifecycle.name": "my_policy",
          "index.lifecycle.rollover_alias": "test-alias",
          "number_of_shards": 1,
          "number_of_replicas": 1
        }
        ```

1. Optional: On the **Mappings** page, customize the fields and data types used when documents are indexed into {{es}}. Refer to [Mapping](/manage-data/data-store/mapping.md) for details.

1. Optional: On the **Aliases** page, specify an [alias](/manage-data/data-store/aliases.md) for each created index. This isn't required when configuring ILM, which instead uses the `index.lifecycle.rollover_alias` setting to access rolling indices.

1. On the **Review** page, confirm your selections. You can check your selected options, as well as both the format of the index template that will be created and the associated API request.

The newly created index template will be used for all new indices with names that match the specified pattern, and for each of these, the specified ILM policy will be applied.
:::

:::{tab-item} API
:sync: api
Use the [Create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to add an index template to a cluster and apply the lifecycle policy to indices matching the template:

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

1. Use this template for all new indices with names that begin with `test-`.
2. Apply `my_policy` to new indices created with this template.
3. Define an index alias for referencing indices managed by `my_policy`.

    :::{tip}
    The `index.lifecycle.rollover_alias` setting is required only if you're using {{ilm}} with an alias. It is unnecessary when using [Data Streams](../../data-store/data-streams.md).
    :::
:::
::::

## Create an initial managed index and alias [create-initial-index]

When you set up policies for your own rolling indices and are not using the recommended [data streams](../../data-store/data-streams.md), you must manually create the first index managed by a policy and designate it as the write index.

The name of the index must match the pattern defined in the index template and end with a number. This number is incremented to generate the name of indices created by the rollover action.

This step is required only when you're planning to use {{ilm-init}} with rolling indices. It is not required when you're using data streams, where the initial managed index is created automatically.

::::{important}
When you enable {{ilm}} for {{beats}}, {{agent}}, or for the {{agent}} or {{ls}} {{es}} output plugins, the necessary policies and configuration changes are applied automatically. If you'd like to create a specialized ILM policy for any data stream, refer to our tutorial [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).
::::

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To create the initial managed index:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Indices** tab, select **Create index**.
1. Specify a name for the index that matches the index template pattern and that ends with a number. For example, `test-000001`.
1. Leave the **Index mode** set to the default **Standard**.

Create an alias for the index:

1. Open **Dev tools**.
2. Send the following request:

```console
POST /_aliases
{
  "actions" : [
    { "add" : { "index" : "my-index", "alias" : "my-alias" } } <1>
  ]
}
```

1. Replace `my-index` with the name of the initial managed index that you created previously and set `my-alias` to the rollover alias specified by `index.lifecycle.rollover_alias` in the index template.

Now you can start indexing data to the rollover alias specified in the lifecycle policy. With the sample `my_policy` policy, the rollover action is triggered once the initial index exceeds 50GB. {{ilm-init}} then creates a new index that becomes the write index for the `test-alias`.
:::

:::{tab-item} API
:sync: api
Use the [Create an index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) to create the initial managed index.

The following request creates the `test-000001` index, with the alias `test-alias`. Because the index name matches the index pattern specified in `my_template`, {{es}} automatically applies the settings from that template.

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
:::
::::

