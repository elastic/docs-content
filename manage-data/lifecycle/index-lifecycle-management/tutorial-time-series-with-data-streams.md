---
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Manage time series data with data streams [manage-time-series-data-with-data-streams]

To automate rollover and management of a data stream with {{ilm-init}}, you:

1. [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-create-policy) that defines the appropriate [phases](index-lifecycle.md) and [actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/index.md).
2. [Create an index template](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-apply-policy) to [create the data stream](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-create-the-data-stream) and apply the ILM policy and the indices settings and mappings configurations for the backing indices.
3. [Verify that indices are moving through the lifecycle phases](/manage-data/lifecycle/index-lifecycle-management/tutorial-time-series-with-data-streams.md#ilm-gs-check-progress) as expected.

::::{important}
When you enable {{ilm}} for {{beats}} or the {{ls}} {{es}} output plugin, lifecycle policies are set up automatically. You do not need to take any other actions. You can modify the default policies through [{{kib}} Management](tutorial-customize-built-in-policies.md) or the {{ilm-init}} APIs.
::::



## Create a lifecycle policy [ilm-gs-create-policy]

:::{include} /manage-data/_snippets/create-lifecycle-policy.md
:::


## Create an index template to create the data stream and apply the lifecycle policy [ilm-gs-apply-policy]

To set up a data stream, first create an index template to specify the lifecycle policy. Because the template is for a data stream, it must also include a `data_stream` definition.

For example, you might create a template named `timeseries_template` and use it for a future data stream named `timeseries`.
To configure {{ilm-init}} to manage the data stream, you specify the name of the lifecycle policy that you want to apply to the data stream with the `index.lifecycle.name` setting.

Use the {{kib}} **Create template** wizard to add a template or the [Create or update index template](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) API to add a template and apply the lifecycle policy to indices matching the template.

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana
To add an index template to a cluster using the wizard:

1. Go to the **Index Management** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Index Templates** tab, click **Create template** and follow the instructions.

![Create template page](/manage-data/images/elasticsearch-reference-create-index-template.png "")

You specify the name of the lifecycle policy that you want to apply to the data stream on the **Index settings** page.

![Create template page](/manage-data/images/elasticsearch-reference-tutorial-ilm-datastreams-tutorial-create-index-template.png "")

:::{tip}
To learn about which index template options you can specify, refer to [Create an index template to apply the lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#apply-policy-template).
:::
:::

:::{tab-item} API
:sync: api
Use the API to add an index template to your cluster:

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

:::
::::



## Create the data stream [ilm-gs-create-the-data-stream]

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


## Check lifecycle progress [ilm-gs-check-progress]

Use {{kib}} to [view the current status of your managed indices](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md) and details about the ILM policy, or the {{ilm-init}} explain API. Find out things like:

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

1. The age of the index used for calculating when to rollover the index using the `max_age`
2. The policy used to manage the index
3. The age of the indexed used to transition to the next phase (in this case it is the same with the age of the index).
4. The step {{ilm-init}} is performing on the index
5. The definition of the current phase (the `hot` phase)
