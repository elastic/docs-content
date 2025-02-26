# Machine learning decider [autoscaling-machine-learning-decider]

The [autoscaling](../../../deploy-manage/autoscaling.md) {{ml}} decider (`ml`) calculates the memory and CPU requirements to run {{ml}} jobs and trained models.

The {{ml}} decider is enabled for policies governing `ml` nodes.

::::{note} 
For {{ml}} jobs to open when the cluster is not appropriately scaled, set `xpack.ml.max_lazy_ml_nodes` to the largest number of possible {{ml}} nodes (refer to [Advanced machine learning settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/machine-learning-settings.md#advanced-ml-settings) for more information). In {{ech}}, this is automatically set.
::::


## Configuration settings [autoscaling-machine-learning-decider-settings]

Both `num_anomaly_jobs_in_queue` and `num_analytics_jobs_in_queue` are designed to delay a scale-up event. If the cluster is too small, these settings indicate how many jobs of each type can be unassigned from a node. Both settings are only considered for jobs that can be opened given the current scale. If a job is too large for any node size or if a job can’t be assigned without user intervention (for example, a user calling `_stop` against a real-time {{anomaly-job}}), the numbers are ignored for that particular job.

`num_anomaly_jobs_in_queue`
:   (Optional, integer) Specifies the number of queued {{anomaly-jobs}} to allow. Defaults to `0`.

`num_analytics_jobs_in_queue`
:   (Optional, integer) Specifies the number of queued {{dfanalytics-jobs}} to allow. Defaults to `0`.

`down_scale_delay`
:   (Optional, [time value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#time-units)) Specifies the time to delay before scaling down. Defaults to 1 hour. If a scale down is possible for the entire time window, then a scale down is requested. If the cluster requires a scale up during the window, the window is reset.


## {{api-examples-title}} [autoscaling-machine-learning-decider-examples]

This example creates an autoscaling policy named `my_autoscaling_policy` that overrides the default configuration of the {{ml}} decider.

```console
PUT /_autoscaling/policy/my_autoscaling_policy
{
  "roles" : [ "ml" ],
  "deciders": {
    "ml": {
      "num_anomaly_jobs_in_queue": 5,
      "num_analytics_jobs_in_queue": 3,
      "down_scale_delay": "30m"
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


