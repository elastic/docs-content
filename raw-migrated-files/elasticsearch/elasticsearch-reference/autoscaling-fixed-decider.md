# Fixed decider [autoscaling-fixed-decider]

::::{warning} 
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


::::{warning} 
The fixed decider is intended for testing only. Do not use this decider in production.
::::


The [autoscaling](../../../deploy-manage/autoscaling.md) `fixed` decider responds with a fixed required capacity. It is not enabled by default but can be enabled for any policy by explicitly configuring it.

## Configuration settings [_configuration_settings]

`storage`
:   (Optional, [byte value](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#byte-units)) Required amount of node-level storage. Defaults to `-1` (disabled).

`memory`
:   (Optional, [byte value](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#byte-units)) Required amount of node-level memory. Defaults to `-1` (disabled).

`processors`
:   (Optional, float) Required number of processors. Defaults to disabled.

`nodes`
:   (Optional, integer) Number of nodes to use when calculating capacity. Defaults to `1`.


## {{api-examples-title}} [autoscaling-fixed-decider-examples]

This example puts an autoscaling policy named `my_autoscaling_policy`, enabling and configuring the fixed decider.

```console
PUT /_autoscaling/policy/my_autoscaling_policy
{
  "roles" : [ "data_hot" ],
  "deciders": {
    "fixed": {
      "storage": "1tb",
      "memory": "32gb",
      "processors": 2.3,
      "nodes": 8
    }
  }
}
```

The API returns the following result:

```console-result
{
  "acknowledged": true
}
```


