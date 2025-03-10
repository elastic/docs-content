---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-deciders.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-reactive-storage-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-proactive-storage-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-frozen-shards-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-frozen-storage-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-frozen-existence-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-machine-learning-decider.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-fixed-decider.html
applies_to:
  ece:
  eck:
  ess:
---

# Autoscaling deciders [autoscaling-deciders]

[Autoscaling](/deploy-manage/autoscaling.md) in Elasticsearch enables dynamic resource allocation based on predefined policies. A key component of this mechanism is autoscaling deciders, which independently assess resource requirements and determine when scaling actions are necessary. Deciders analyze various factors, such as storage usage, indexing rates, and machine learning workloads, to ensure clusters maintain optimal performance without manual intervention.

::::{admonition} Indirect use only 
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::

[Reactive storage decider](#autoscaling-reactive-storage-decider)
:   Estimates required storage capacity of current data set. Available for policies governing data nodes.

[Proactive storage decider](#autoscaling-proactive-storage-decider)
:   Estimates required storage capacity based on current ingestion into hot nodes. Available for policies governing hot data nodes.

[Frozen shards decider](#autoscaling-frozen-shards-decider)
:   Estimates required memory capacity based on the number of partially mounted shards. Available for policies governing frozen data nodes.

[Frozen storage decider](#autoscaling-frozen-storage-decider)
:   Estimates required storage capacity as a percentage of the total data set of partially mounted indices. Available for policies governing frozen data nodes.

[Frozen existence decider](#autoscaling-frozen-existence-decider)
:   Estimates a minimum require frozen memory and storage capacity when any index is in the frozen [ILM](../../manage-data/lifecycle/index-lifecycle-management.md) phase.

[Machine learning decider](#autoscaling-machine-learning-decider)
:   Estimates required memory capacity based on machine learning jobs. Available for policies governing machine learning nodes.

[Fixed decider](#autoscaling-fixed-decider)
:   Responds with a fixed required capacity. This decider is intended for testing only.

## Reactive storage decider [autoscaling-reactive-storage-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) reactive storage decider (`reactive_storage`) calculates the storage required to contain the current data set. It signals that additional storage capacity is necessary when existing capacity has been exceeded (reactively).

The reactive storage decider is enabled for all policies governing data nodes and has no configuration options.

The decider relies partially on using [data tier preference](../../manage-data/lifecycle/data-tiers.md#data-tier-allocation) allocation rather than node attributes. In particular, scaling a data tier into existence (starting the first node in a tier) will result in starting a node in any data tier that is empty if not using allocation based on data tier preference. Using the [ILM migrate](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md) action to migrate between tiers is the preferred way of allocating to tiers and fully supports scaling a tier into existence.

## Proactive storage decider [autoscaling-proactive-storage-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) proactive storage decider (`proactive_storage`) calculates the storage required to contain the current data set plus an estimated amount of expected additional data.

The proactive storage decider is enabled for all policies governing nodes with the `data_hot` role.

The estimation of expected additional data is based on past indexing that occurred within the `forecast_window`. Only indexing into data streams contributes to the estimate.

### Configuration settings [autoscaling-proactive-storage-decider-settings]

`forecast_window`
:   (Optional, [time value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#time-units)) The window of time to use for forecasting. Defaults to 30 minutes.


### {{api-examples-title}} [autoscaling-proactive-storage-decider-examples]

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
%  TEST

The API returns the following result:

```console-result
{
  "acknowledged": true
}
```

## Frozen shards decider [autoscaling-frozen-shards-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) frozen shards decider (`frozen_shards`) calculates the memory required to search the current set of partially mounted indices in the frozen tier. Based on a required memory amount per shard, it calculates the necessary memory in the frozen tier.

### Configuration settings [autoscaling-frozen-shards-decider-settings]

`memory_per_shard`
:   (Optional, [byte value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) The memory needed per shard, in bytes. Defaults to 2000 shards per 64 GB node (roughly 32 MB per shard). Notice that this is total memory, not heap, assuming that the Elasticsearch default heap sizing mechanism is used and that nodes are not bigger than 64 GB.

## Frozen storage decider [autoscaling-frozen-storage-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) frozen storage decider (`frozen_storage`) calculates the local storage required to search the current set of partially mounted indices based on a percentage of the total data set size of such indices. It signals that additional storage capacity is necessary when existing capacity is less than the percentage multiplied by total data set size.

The frozen storage decider is enabled for all policies governing frozen data nodes and has no configuration options.

### Configuration settings [autoscaling-frozen-storage-decider-settings]

`percentage`
:   (Optional, number value) Percentage of local storage relative to the data set size. Defaults to 5.

## Frozen existence decider [autoscaling-frozen-existence-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) frozen existence decider (`frozen_existence`) ensures that once the first index enters the frozen ILM phase, the frozen tier is scaled into existence.

The frozen existence decider is enabled for all policies governing frozen data nodes and has no configuration options.

## Machine learning decider [autoscaling-machine-learning-decider]

The [autoscaling](../../deploy-manage/autoscaling.md) {{ml}} decider (`ml`) calculates the memory and CPU requirements to run {{ml}} jobs and trained models.

The {{ml}} decider is enabled for policies governing `ml` nodes.

::::{note} 
For {{ml}} jobs to open when the cluster is not appropriately scaled, set `xpack.ml.max_lazy_ml_nodes` to the largest number of possible {{ml}} nodes (refer to [Advanced machine learning settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/machine-learning-settings.md#advanced-ml-settings) for more information). In {{ess}}, this is automatically set.
::::


### Configuration settings [autoscaling-machine-learning-decider-settings]

Both `num_anomaly_jobs_in_queue` and `num_analytics_jobs_in_queue` are designed to delay a scale-up event. If the cluster is too small, these settings indicate how many jobs of each type can be unassigned from a node. Both settings are only considered for jobs that can be opened given the current scale. If a job is too large for any node size or if a job can’t be assigned without user intervention (for example, a user calling `_stop` against a real-time {{anomaly-job}}), the numbers are ignored for that particular job.

`num_anomaly_jobs_in_queue`
:   (Optional, integer) Specifies the number of queued {{anomaly-jobs}} to allow. Defaults to `0`.

`num_analytics_jobs_in_queue`
:   (Optional, integer) Specifies the number of queued {{dfanalytics-jobs}} to allow. Defaults to `0`.

`down_scale_delay`
:   (Optional, [time value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#time-units)) Specifies the time to delay before scaling down. Defaults to 1 hour. If a scale down is possible for the entire time window, then a scale down is requested. If the cluster requires a scale up during the window, the window is reset.


### {{api-examples-title}} [autoscaling-machine-learning-decider-examples]

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
%  TEST

The API returns the following result:

```console-result
{
  "acknowledged": true
}
```

## Fixed decider [autoscaling-fixed-decider]

::::{warning} 
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


::::{warning} 
The fixed decider is intended for testing only. Do not use this decider in production.
::::


The [autoscaling](../../deploy-manage/autoscaling.md) `fixed` decider responds with a fixed required capacity. It is not enabled by default but can be enabled for any policy by explicitly configuring it.

### Configuration settings [_configuration_settings]

`storage`
:   (Optional, [byte value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Required amount of node-level storage. Defaults to `-1` (disabled).

`memory`
:   (Optional, [byte value](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Required amount of node-level memory. Defaults to `-1` (disabled).

`processors`
:   (Optional, float) Required number of processors. Defaults to disabled.

`nodes`
:   (Optional, integer) Number of nodes to use when calculating capacity. Defaults to `1`.


### {{api-examples-title}} [autoscaling-fixed-decider-examples]

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
%  TEST

The API returns the following result:

```console-result
{
  "acknowledged": true
}
```