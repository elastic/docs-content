A lifecycle policy specifies the phases in the index lifecycle and the actions to perform in each phase. A lifecycle can have up to five phases: `hot`, `warm`, `cold`, `frozen`, and `delete`.

For example, you might define a policy named `timeseries_policy` that has the following two phases:

* A `hot` phase that defines a rollover action to specify that an index rolls over when it reaches either a `max_primary_shard_size` of 50 gigabytes or a `max_age` of 30 days.
* A `delete` phase that sets `min_age` to remove the index 90 days after rollover.

::::{note}
The `min_age` value is relative to the rollover time, not the index creation time. [Learn more](../../troubleshoot/elasticsearch/index-lifecycle-management-errors.md#min-age-calculation).
::::


You can create the policy in {{kib}} or with the [create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API.

::::{tab-set}
:group: kibana-api
:::{tab-item} {{kib}}
:sync: kibana

To create the policy from {{kib}}:

1. Go to the **Index Lifecycle Policies** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Click **Create policy**.

By default, only the hot index lifecycle phase is enabled. Enable each additional lifecycle phase that you'd like.


:::{image} /manage-data/images/elasticsearch-reference-create-policy.png
:alt: Create policy page
:screenshot:
:::
:::

:::{tab-item} API
:sync: api
Use the [Create or update policy](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) API to add an ILM policy to the {{es}} cluster:

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

:::
::::

Note that for each phase after the hot phase, you have the option to move the data into the next phase after a certain duration of time. This duration is calculated from the time of the index rollover and not from the time the index is created.

:::{tip}
For more details about default {{ilm-init}} policy settings, refer to [Create a lifecycle policy](/manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md#ilm-create-policy).
:::