---
navigation_title: Data stream lifecycle
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-stream-lifecycle.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Data stream lifecycle in {{es}} [data-stream-lifecycle]

A data stream lifecycle in {{es}} is a built-in automation mechanism for managing data retention, performance, and storage optimization.
By configuring rollover, retention, downsampling, and frozen transitions to long-term searchable archives, your [data streams](/manage-data/data-store/data-streams.md) stay efficient as they age.
This page explains how the lifecycle works, its key features, and how to configure it for both new and existing data streams.

Data stream lifecycle manages your data streams according to your retention and storage goals. For example, you can configure the lifecycle to:

* Ensure that data indexed in the data stream is kept at least for the retention time you defined.
* Ensure that data older than the retention period is deleted automatically by {{es}} at a later time.
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` Move older backing indices to low-cost searchable storage. Refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).

To achieve these, data stream lifecycle supports:

* Automatic [rollover](index-lifecycle-management/rollover.md), which chunks your incoming data in smaller pieces to facilitate better performance and backwards incompatible mapping changes.
* Configurable retention, which allows you to configure the time period for which your data is guaranteed to be stored. {{es}} is allowed at a later time to delete data older than this time period. Retention can be configured on the data stream level or on a global level. Read more about the different options in this [tutorial](data-stream/tutorial-data-stream-retention.md).

Data stream lifecycle also supports downsampling the data stream backing indices. Refer to [the downsampling example]({{es-apis}}operation/operation-indices-put-data-lifecycle) for more details.

## Data stream lifecycle availability

Note the availability of data stream lifecycle to ensure that it's applicable for your use case:

* Data stream lifecycle is supported only for data streams and cannot be used with individual indices.

* Data stream lifecycle is supported for all deployment types on the versioned {{stack}} as well as for {{es-serverless}}.

## How does it work? [data-streams-lifecycle-how-it-works]

In intervals configured by [`data_streams.lifecycle.poll_interval`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-poll-interval), {{es}} goes over each data stream and performs the following steps:

1. Checks if the data stream has a data stream lifecycle configured, skipping any indices not part of a managed data stream. {applies_to}`stack: ga 9.6` {applies_to}`serverless: unavailable` A {{tsds}} without a lifecycle is managed by the [minimum data stream lifecycle](#minimum-data-stream-lifecycle), which runs only steps 2 and 3.
2. Rolls over the write index of the data stream, if it fulfills the conditions defined by [`cluster.lifecycle.default.rollover`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#cluster-lifecycle-default-rollover).
3. After an index is not the write index anymore (that is, the data stream has been rolled over), automatically tail merges the index. Data stream lifecycle runs a merge operation that only targets the long tail of small segments instead of the whole shard. As the segments are organised into tiers of exponential sizes, merging the long tail of small segments is only a fraction of the cost of force merging to a single segment. The small segments would usually hold the most recent data so tail merging will focus the merging resources on the higher-value data that is most likely to keep being queried.
4. If [downsampling]({{es-apis}}operation/operation-indices-put-data-lifecycle) is configured it will run all the configured downsampling rounds. {applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` Data stream lifecycle limits concurrent downsampling per data stream using the [`data_streams.lifecycle.downsampling.max_indices_in_progress`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-downsampling-max-indices-in-progress) cluster setting (default `10`). For details, refer to [Downsample with a data stream lifecycle](/manage-data/data-store/data-streams/run-downsampling.md#downsample-with-a-data-stream-lifecycle).
5. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` Transitions eligible backing indices to partially mounted {{search-snaps}}. Refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).
6. Applies retention to the remaining backing indices. This means deleting the backing indices whose `generation_time` is longer than the effective retention period (read more about the [effective retention calculation](data-stream/tutorial-data-stream-retention.md#effective-retention-calculation)). The `generation_time` is only applicable to rolled over backing indices and it is either the time since the backing index got rolled over, or the time optionally configured in the [`index.lifecycle.origination_date`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-data-stream-lifecycle-origination-date) setting. Retention can delete indices even after they have been moved to {{search-snaps}}.

::::{important}
We use the `generation_time` instead of the creation time because this ensures that all data in the backing index have passed the retention period. As a result, the retention period is not the exact time data gets deleted, but the minimum time data will be stored.
::::
::::{note}
Steps `2-5` apply only to backing indices that are not already managed by {{ilm-init}}, meaning that these indices either do not have an {{ilm-init}} policy defined, or if they do, they have [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) set to `false`.
::::

## Configuring data stream lifecycle [data-stream-lifecycle-configuration]

Since the lifecycle is configured on the data stream level, the process to configure a lifecycle on a new data stream and on an existing one differ.

The following tutorials help you set up and manage data streams with data stream lifecycle:

* To create a new data stream with a lifecycle, add the data stream lifecycle as part of the index template that matches the name of your data stream. Refer to [](data-stream/tutorial-create-data-stream-with-lifecycle.md) for the detailed steps. When a write operation with the name of your data stream reaches {{es}} then the data stream is created with the respective data stream lifecycle.
* To update the lifecycle settings for an individual, existing data stream, use the [data stream lifecycle APIs]({{es-apis}}group/endpoint-data-stream). Refer to [](data-stream/tutorial-update-existing-data-stream.md) for details.
* Retention settings for data streams can be configured both individually, at the data stream level, and globally, for all data streams in a cluster. To learn more, refer to [](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md).
* To migrate an existing {{ilm-init}} managed data stream to data stream lifecycle, follow the steps in [](data-stream/tutorial-migrate-ilm-managed-data-stream-to-data-stream-lifecycle.md).
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` To move older backing indices to {{search-snaps}}, refer to [](/manage-data/lifecycle/data-stream/dlm-searchable-snapshots.md).

::::{note}
Updating the data stream lifecycle of an existing data stream is different from updating the settings or the mapping, because it is applied on the data stream level and not on the individual backing indices.
::::

## Minimum data stream lifecycle [minimum-data-stream-lifecycle]

```{applies_to}
stack: ga 9.6
serverless: unavailable
```

{{es}} manages {{tsds}} ({{tsds-init}}) that have no data stream lifecycle of their own with a minimum lifecycle. The minimum lifecycle performs only the operations a data stream needs to stay healthy: [rollover](index-lifecycle-management/rollover.md) and tail merging. It never changes the data set, so it doesn't downsample, move data to {{search-snaps}}, or delete data. It doesn't delete data even if you configure a global retention.

The minimum lifecycle applies to a data stream when all the following are true:

* The data stream is a {{tsds-init}}.
* The data stream has no data stream lifecycle configured. A data stream with a lifecycle that is explicitly disabled keeps that configuration, and the minimum lifecycle doesn't apply.
* The [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) cluster setting is `true`, which is the default.
* No {{ilm-init}} policy manages the backing index. A backing index with an {{ilm-init}} policy stays managed by {{ilm-init}} unless [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) is `false`.

Adding a data stream lifecycle to the data stream replaces the minimum lifecycle with your configuration.

::::{important}
Before 9.6, a {{tsds-init}} without a lifecycle or an {{ilm-init}} policy was never rolled over automatically. If an external process rolls over your {{tsds-init}}, you might now see additional backing indices. A {{tsds-init}} that has an {{ilm-init}} policy, `index.lifecycle.prefer_ilm` set to `false`, and no data stream lifecycle also moves from {{ilm-init}} to the minimum lifecycle. As a result, {{ilm-init}} phases such as delete or downsample stop running for it.

To restore the previous behavior, set `data_streams.lifecycle.minimum.enabled` to `false`. The setting is dynamic, so you don't need to restart {{es}}.

```console
PUT _cluster/settings
{
  "persistent": {
    "data_streams.lifecycle.minimum.enabled": false
  }
}
```
::::

### Default lifecycle for the `metrics` {{ilm-init}} policy [minimum-lifecycle-metrics-policy]

```{applies_to}
stack: ga 9.6
serverless: unavailable
```

{{es}} ships with a pre-installed `metrics` {{ilm-init}} policy. New backing indices of {{tsds-init}} that use this policy default `index.lifecycle.prefer_ilm` to `false`, so data stream lifecycle manages them instead of {{ilm-init}}. If the data stream has no lifecycle of its own, the minimum lifecycle manages them.

This default applies only while the `metrics` policy is unmodified, meaning it is still on version 1 and its only action is a rollover in the hot phase. Data streams with a custom {{ilm-init}} policy, or a modified `metrics` policy, stay under {{ilm-init}}. An explicit `index.lifecycle.prefer_ilm` value in the index template, the data stream settings, or the create index request always takes precedence.

The change affects only backing indices created after the default applies. Existing backing indices stay under {{ilm-init}}. To opt out:

* Set the dynamic cluster setting [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled) to `false`. This doesn't change backing indices that already have `prefer_ilm` set to `false`.
* Set `index.lifecycle.prefer_ilm` to `true` in the component or index template.

To return backing indices that are already managed by data stream lifecycle to {{ilm-init}}, update the data stream settings. The following request will change the `prefer_ilm` value of all the backing indices of the data stream:

```console
PUT _data_stream/my-time-series/_settings
{
  "index.lifecycle.prefer_ilm": true
}
```

### Check what manages a data stream [minimum-lifecycle-check]

To find out whether the minimum lifecycle manages a data stream or an index:

* The [get data stream API]({{es-apis}}operation/operation-indices-get-data-stream) returns `"minimum_lifecycle_enabled": true` and `"next_generation_managed_by": "Data stream lifecycle"` for the data stream.
* The [get data stream lifecycle API]({{es-apis}}operation/operation-indices-get-data-lifecycle) returns `"minimum_lifecycle_enabled": true` for the data stream.
* The [explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) returns `"minimum_lifecycle_enabled": true` for each index the minimum lifecycle manages. For indices that no lifecycle manages, the response includes an `unmanaged_reason` field when {{es}} can determine why. The [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) includes the same field.