# Proactive storage decider [autoscaling-proactive-storage-decider]

The [autoscaling](../../../deploy-manage/autoscaling.md) proactive storage decider (`proactive_storage`) calculates the storage required to contain the current data set plus an estimated amount of expected additional data.

The proactive storage decider is enabled for all policies governing nodes with the `data_hot` role.

The estimation of expected additional data is based on past indexing that occurred within the `forecast_window`. Only indexing into data streams contributes to the estimate.

## Configuration settings [autoscaling-proactive-storage-decider-settings]

`forecast_window`
:   (Optional, [time value](https://www.elastic.co/guide/en/elasticsearch/reference/current/api-conventions.html#time-units)) The window of time to use for forecasting. Defaults to 30 minutes.


## {{api-examples-title}} [autoscaling-proactive-storage-decider-examples]

This example puts an autoscaling policy named `my_autoscaling_policy`, overriding the proactive decider’s `forecast_window` to be 10 minutes.

```console
PUT /_autoscaling/policy/my_autoscaling_policy
{
  "roles" : [ "data_hot" ],
  "deciders": {
    "proactive_storage": {
      "forecast_window": "10m"
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


