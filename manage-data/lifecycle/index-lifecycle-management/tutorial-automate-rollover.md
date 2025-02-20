---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-index-lifecycle-management.html
---

# Tutorial: Automate rollover [getting-started-index-lifecycle-management]

When you continuously index timestamped documents into {{es}}, you typically use a [data stream](../../data-store/data-streams.md) so you can periodically [roll over](rollover.md) to a new index. This enables you to implement a [hot-warm-cold architecture](../data-tiers.md) to meet your performance requirements for your newest data, control costs over time, enforce retention policies, and still get the most out of your data.

::::{tip}
[Data streams](../../data-store/data-streams.md) are best suited for [append-only](../../data-store/data-streams.md#data-streams-append-only) use cases. If you need to update or delete existing time series data, you can perform update or delete operations directly on the data stream backing index. If you frequently send multiple documents using the same `_id` expecting last-write-wins, you may want to use an index alias with a write index instead. You can still use [ILM](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md) to manage and [roll over](rollover.md) the alias’s indices. Skip to [Manage time series data without data streams](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#manage-time-series-data-without-data-streams).
::::

## Manage time series data with data streams [manage-time-series-data-with-data-streams]

To automate rollover and management of a data stream with {{ilm-init}}, you:

1. [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-create-policy) that defines the appropriate [phases](index-lifecycle.md) and [actions](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-actions.html).
2. [Create an index template](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-apply-policy) to [create the data stream](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-create-the-data-stream) and apply the ILM policy and the indices settings and mappings configurations for the backing indices.
3. [Verify indices are moving through the lifecycle phases](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-check-progress) as expected.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, lifecycle policies are set up automatically. You do not need to take any other actions. You can modify the default policies through [{{kib}} Management](tutorial-customize-built-in-policies.md) or the {{ilm-init}} APIs.
::::



### Create a lifecycle policy [ilm-gs-create-policy]

A lifecycle policy specifies the phases in the index lifecycle and the actions to perform in each phase. A lifecycle can have up to five phases: `hot`, `warm`, `cold`, `frozen`, and `delete`.

For example, you might define a `timeseries_policy` that has two phases:

* A `hot` phase that defines a rollover action to specify that an index rolls over when it reaches either a `max_primary_shard_size` of 50 gigabytes or a `max_age` of 30 days.
* A `delete` phase that sets `min_age` to remove the index 90 days after rollover.

::::{note}
The `min_age` value is relative to the rollover time, not the index creation time. [Learn more](../../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).

::::


You can create the policy through {{kib}} or with the [create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API. To create the policy from {{kib}}, open the menu and go to **Stack Management > Index Lifecycle Policies**. Click **Create policy**.

:::{image} ../../../images/elasticsearch-reference-create-policy.png
:alt: Create policy page
:class: screenshot
:::

::::{dropdown} API example
```console
PUT _ilm/policy/timeseries_policy
{
  "policy": {
    "phases": {
      "hot": {                                <1>
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50GB", <2>
            "max_age": "30d"
          }
        }
      },
      "delete": {
        "min_age": "90d",                     <3>
        "actions": {
          "delete": {}                        <4>
        }
      }
    }
  }
}
```

1. The `min_age` defaults to `0ms`, so new indices enter the `hot` phase immediately.
2. Trigger the `rollover` action when either of the conditions are met.
3. Move the index into the `delete` phase 90 days after rollover.
4. Trigger the `delete` action when the index enters the delete phase.


::::



### Create an index template to create the data stream and apply the lifecycle policy [ilm-gs-apply-policy]

To set up a data stream, first create an index template to specify the lifecycle policy. Because the template is for a data stream, it must also include a `data_stream` definition.

For example, you might create a `timeseries_template` to use for a future data stream named `timeseries`.

To enable the {{ilm-init}} to manage the data stream, the template configures one {{ilm-init}} setting:

* `index.lifecycle.name` specifies the name of the lifecycle policy to apply to the data stream.

You can use the {{kib}} Create template wizard to add the template. From Kibana, open the menu and go to **Stack Management > Index Management**. In the **Index Templates** tab, click **Create template**.

:::{image} ../../../images/elasticsearch-reference-create-index-template.png
:alt: Create template page
:::

This wizard invokes the [create or update index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) to create the index template with the options you specify.

::::{dropdown} API example
```console
PUT _index_template/timeseries_template
{
  "index_patterns": ["timeseries"],                   <1>
  "data_stream": { },
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1,
      "index.lifecycle.name": "timeseries_policy"     <2>
    }
  }
}
```

1. Apply the template when a document is indexed into the `timeseries` target.
2. The name of the {{ilm-init}} policy used to manage the data stream.


::::



### Create the data stream [ilm-gs-create-the-data-stream]

To get things started, index a document into the name or wildcard pattern defined in the `index_patterns` of the [index template](../../data-store/templates.md). As long as an existing data stream, index, or index alias does not already use the name, the index request automatically creates a corresponding data stream with a single backing index. {{es}} automatically indexes the request’s documents into this backing index, which also acts as the stream’s [write index](../../data-store/data-streams.md#data-stream-write-index).

For example, the following request creates the `timeseries` data stream and the first generation backing index called `.ds-timeseries-2099.03.08-000001`.

```console
POST timeseries/_doc
{
  "message": "logged the request",
  "@timestamp": "1591890611"
}
```

When a rollover condition in the lifecycle policy is met, the `rollover` action:

* Creates the second generation backing index, named `.ds-timeseries-2099.03.08-000002`. Because it is a backing index of the `timeseries` data stream, the configuration from the `timeseries_template` index template is applied to the new index.
* As it is the latest generation index of the `timeseries` data stream, the newly created backing index `.ds-timeseries-2099.03.08-000002` becomes the data stream’s write index.

This process repeats each time a rollover condition is met. You can search across all of the data stream’s backing indices, managed by the `timeseries_policy`, with the `timeseries` data stream name. Write operations should be sent to the data stream name, which will route them to its current write index. Read operations against the data stream will be handled by all its backing indices.


### Check lifecycle progress [ilm-gs-check-progress]

To get status information for managed indices, you use the {{ilm-init}} explain API. This lets you find out things like:

* What phase an index is in and when it entered that phase.
* The current action and what step is being performed.
* If any errors have occurred or progress is blocked.

For example, the following request gets information about the `timeseries` data stream’s backing indices:

```console
GET .ds-timeseries-*/_ilm/explain
```

The following response shows the data stream’s first generation backing index is waiting for the `hot` phase’s `rollover` action. It remains in this state and {{ilm-init}} continues to call `check-rollover-ready` until a rollover condition is met.

```console-result
{
  "indices": {
    ".ds-timeseries-2099.03.07-000001": {
      "index": ".ds-timeseries-2099.03.07-000001",
      "index_creation_date_millis": 1538475653281,
      "time_since_index_creation": "30s",        <1>
      "managed": true,
      "policy": "timeseries_policy",             <2>
      "lifecycle_date_millis": 1538475653281,
      "age": "30s",                              <3>
      "phase": "hot",
      "phase_time_millis": 1538475653317,
      "action": "rollover",
      "action_time_millis": 1538475653317,
      "step": "check-rollover-ready",            <4>
      "step_time_millis": 1538475653317,
      "phase_execution": {
        "policy": "timeseries_policy",
        "phase_definition": {                    <5>
          "min_age": "0ms",
          "actions": {
            "rollover": {
              "max_primary_shard_size": "50gb",
              "max_age": "30d"
            }
          }
        },
        "version": 1,
        "modified_date_in_millis": 1539609701576
      }
    }
  }
}
```

1. The age of the index used for calculating when to rollover the index via the `max_age`
2. The policy used to manage the index
3. The age of the indexed used to transition to the next phase (in this case it is the same with the age of the index).
4. The step {{ilm-init}} is performing on the index
5. The definition of the current phase (the `hot` phase)



## Manage time series data without data streams [manage-time-series-data-without-data-streams]

Even though [data streams](../../data-store/data-streams.md) are a convenient way to scale and manage time series data, they are designed to be append-only. We recognise there might be use-cases where data needs to be updated or deleted in place and the data streams don’t support delete and update requests directly, so the index APIs would need to be used directly on the data stream’s backing indices. In these cases we still recommend using a data stream.

If you frequently send multiple documents using the same `_id` expecting last-write-wins, you can use an index alias instead of a data stream to manage indices containing the time series data and periodically roll over to a new index.

To automate rollover and management of time series indices with {{ilm-init}} using an index alias, you:

1. Create a lifecycle policy that defines the appropriate phases and actions. See [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-create-policy) above.
2. [Create an index template](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-alias-apply-policy) to apply the policy to each new index.
3. [Bootstrap an index](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-alias-bootstrap) as the initial write index.
4. [Verify indices are moving through the lifecycle phases](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-alias-check-progress) as expected.


### Create an index template to apply the lifecycle policy [ilm-gs-alias-apply-policy]

To automatically apply a lifecycle policy to the new write index on rollover, specify the policy in the index template used to create new indices.

For example, you might create a `timeseries_template` that is applied to new indices whose names match the `timeseries-*` index pattern.

To enable automatic rollover, the template configures two {{ilm-init}} settings:

* `index.lifecycle.name` specifies the name of the lifecycle policy to apply to new indices that match the index pattern.
* `index.lifecycle.rollover_alias` specifies the index alias to be rolled over when the rollover action is triggered for an index.

You can use the {{kib}} Create template wizard to add the template. To access the wizard, open the menu and go to **Stack Management > Index Management**. In the **Index Templates** tab, click **Create template**.

![Create template page](../../../images/elasticsearch-reference-create-template-wizard.png "")

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



### Bootstrap the initial time series index with a write index alias [ilm-gs-alias-bootstrap]

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


### Check lifecycle progress [ilm-gs-alias-check-progress]

Retrieving the status information for managed indices is very similar to the data stream case. See the data stream [check progress section](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md#ilm-gs-check-progress) for more information. The only difference is the indices namespace, so retrieving the progress will entail the following api call:

```console
GET timeseries-*/_ilm/explain
```

