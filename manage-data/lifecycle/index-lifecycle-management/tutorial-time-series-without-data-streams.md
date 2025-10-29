---
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Manage time series data without data streams [manage-time-series-data-without-data-streams]

Even though [data streams](../../data-store/data-streams.md) are a convenient way to scale and manage time series data, they are designed to be append-only. We recognise there might be use-cases where data needs to be updated or deleted in place and the data streams don’t support delete and update requests directly, so the index APIs would need to be used directly on the data stream’s backing indices. In these cases we still recommend using a data stream.

If you frequently send multiple documents using the same `_id` expecting last-write-wins, you can use an index alias instead of a data stream to manage indices containing the time series data and periodically roll over to a new index.

To automate rollover and management of time series indices with {{ilm-init}} using an index alias, you:

1. [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md#ilm-gs-create-policy) that defines the appropriate phases and actions.
2. [Create an index template](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md#ilm-gs-alias-apply-policy) to apply the policy to each new index.
3. [Bootstrap an index](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md#ilm-gs-alias-bootstrap) as the initial write index.
4. [Verify indices are moving through the lifecycle phases](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-without-data-streams.md#ilm-gs-alias-check-progress) as expected.

## Create a lifecycle policy [ilm-gs-create-policy]

:::{include} /manage-data/_snippets/create-lifecycle-policy.md
:::

## Create an index template to apply the lifecycle policy [ilm-gs-alias-apply-policy]

To automatically apply a lifecycle policy to the new write index on rollover, specify the policy in the index template used to create new indices.

For example, you might create a `timeseries_template` that is applied to new indices whose names match the `timeseries-*` index pattern.

To enable automatic rollover, the template configures two {{ilm-init}} settings:

* `index.lifecycle.name` specifies the name of the lifecycle policy to apply to new indices that match the index pattern.
* `index.lifecycle.rollover_alias` specifies the index alias to be rolled over when the rollover action is triggered for an index.

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To use the {{kib}} **Create template** wizard to add the template:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, click **Create template**.

![Create template page](/manage-data/images/elasticsearch-reference-create-template-wizard.png "")

:::{tip}
For more information about the available index template options that you can specify, refer to [Create an index template to apply the lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#apply-policy-template).
:::
:::

:::{tab-item} API
:sync: api
The create template request for the example template looks like this:

```console
PUT _index_template/timeseries_template
{
  "index_patterns": ["timeseries-*"],                 <1>
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "timeseries_policy",      <2>
      "index.lifecycle.rollover_alias": "timeseries"    <3>
    }
  }
}
```

1. Apply the template to a new index if its name starts with `timeseries-`.
2. The name of the lifecycle policy to apply to each new index.
3. The name of the alias used to reference these indices. Required for policies that use the rollover action.

:::
::::

## Bootstrap the initial time series index with a write index alias [ilm-gs-alias-bootstrap]

To get things started, you need to bootstrap an initial index and designate it as the write index for the rollover alias specified in your index template. The name of this index must match the template’s index pattern and end with a number. On rollover, this value is incremented to generate a name for the new index.

For example, the following request creates an index called `timeseries-000001` and makes it the write index for the `timeseries` alias.

```console
PUT timeseries-000001
{
  "aliases": {
    "timeseries": {
      "is_write_index": true
    }
  }
}
```

When the rollover conditions are met, the `rollover` action:

* Creates a new index called `timeseries-000002`. This matches the `timeseries-*` pattern, so the settings from `timeseries_template` are applied to the new index.
* Designates the new index as the write index and makes the bootstrap index read-only.

This process repeats each time rollover conditions are met. You can search across all of the indices managed by the `timeseries_policy` with the `timeseries` alias. Write operations should be sent towards the alias, which will route them to its current write index.


## Check lifecycle progress [ilm-gs-alias-check-progress]

Retrieving the status information for managed indices is very similar to the case of [managing time series data with data streams](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md) case, the only difference being the indices namespace. Run the following API request to retrieve the lifecycle progress:

```console
GET timeseries-*/_ilm/explain
```

See [Check lifecycle progress](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-check-progress) for more information.