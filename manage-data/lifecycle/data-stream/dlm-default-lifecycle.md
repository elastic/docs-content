---
applies_to:
  stack: ga 9.6+
  serverless: ga
navigation_title: Default lifecycle
description: Learn how {{es}} manages data streams that have no data stream lifecycle of their own, with a minimum lifecycle on {{stack}} and a default data stream lifecycle on {{serverless-short}}.
type: overview
products:
  - id: elasticsearch
---

# Default lifecycle for data streams

A data stream with no lifecycle of its own is still managed.
How {{es}} does that depends on the deployment:

* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: unavailable` A {{tsds}} ({{tsds-init}}) gets a [minimum lifecycle](#minimum-data-stream-lifecycle), which rolls over and tail merges the stream.
* {applies_to}`serverless: ga` {applies_to}`stack: unavailable` Any data stream created without a lifecycle gets a [default data stream lifecycle](#default-lifecycle-serverless).

To leave a classic data stream unmanaged by data stream lifecycle, [turn off the lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#turn-off-lifecycle). Removing the lifecycle isn't enough: {{es}} then treats the stream as having no configuration, so the default or minimum lifecycle can apply.

Wired streams have no option to leave a stream unmanaged. They inherit lifecycle from the parent, or you set a period or an {{ilm-init}} policy. Refer to [Configure data lifecycle with Streams](/solutions/observability/streams/configure-retention.md).

## Default lifecycle [default-lifecycle-serverless]
```{applies_to}
serverless: ga
stack: unavailable
```

On {{serverless-short}}, {{es}} does not use the minimum lifecycle.
When you create a data stream and the matching index template has no lifecycle, {{es}} writes an enabled [data stream lifecycle](/manage-data/lifecycle/data-stream.md) onto the stream.

That default applies to every new data stream, not only a {{tsds-init}}.
The stream is managed by ordinary data stream lifecycle: rollover, tail merging, and retention, including [global retention](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md) if you configure it.

The [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) cluster setting is not available on {{serverless-short}}.

To leave a classic stream unmanaged, [turn off the lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#turn-off-lifecycle) instead of omitting it from the template.
For wired streams, refer to [Configure data lifecycle with Streams](/solutions/observability/streams/configure-retention.md).

## Minimum data stream lifecycle [minimum-data-stream-lifecycle]
```{applies_to}
stack: ga 9.6+
serverless: unavailable
```

{{es}} manages {{tsds}} ({{tsds-init}}) that have no data stream lifecycle of their own with a minimum lifecycle.
The minimum lifecycle currently applies only to a {{tsds-init}}.
It performs only the operations a data stream needs to stay healthy: [rollover](/manage-data/lifecycle/index-lifecycle-management/rollover.md) and tail merging.
It never changes the data set, so it doesn't downsample, move data to {{search-snaps}}, or delete data.
It doesn't delete data even if you configure a global retention.

The minimum lifecycle applies to a data stream when all the following are true:

* The data stream is a {{tsds-init}}.
* The data stream has no data stream lifecycle configured. A data stream with a lifecycle that is explicitly disabled keeps that configuration, and the minimum lifecycle doesn't apply.
* The [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) cluster setting is `true`, which is the default.
* No {{ilm-init}} policy manages the backing index. A backing index with an {{ilm-init}} policy stays managed by {{ilm-init}} unless [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) is `false`.

Adding a data stream lifecycle to the data stream replaces the minimum lifecycle with your configuration.
To apply the minimum lifecycle to an existing {{tsds-init}} that already has a data stream lifecycle, use the [delete lifecycle API]({{es-apis}}operation/operation-indices-delete-data-lifecycle).

::::{important}
Before {applies_to}`stack: ga 9.6`, a {{tsds-init}} without a lifecycle or an {{ilm-init}} policy was never rolled over automatically. If an external process rolls over your {{tsds-init}}, you might now see additional backing indices. A {{tsds-init}} that has an {{ilm-init}} policy, `index.lifecycle.prefer_ilm` set to `false`, and no data stream lifecycle also moves from {{ilm-init}} to the minimum lifecycle. As a result, {{ilm-init}} phases such as delete or downsample stop running for it.

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

### Pre-installed lifecycle management for `metrics` moves to the minimum lifecycle [minimum-lifecycle-metrics-policy]

{{es}} migrates {{tsds}} that use the pre-installed `metrics` {{ilm-init}} policy from {{ilm-init}} to the minimum lifecycle.

#### How it works

For new backing indices of a {{tsds-init}} that uses the **pre-installed and unmodified** `metrics` policy, {{es}} defaults [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) to `false`. The policy stays attached to the index, but {{ilm-init}} no longer manages it. If the data stream has its own data stream lifecycle, that lifecycle manages the index. Otherwise, the minimum lifecycle does.

#### When it applies

The new default for [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) applies to a backing index only when all the following are true:

* The index is created in {applies_to}`stack: ga 9.6`. Existing backing indices stay under {{ilm-init}} until they are deleted or you change them manually.
* The data stream is a {{tsds-init}} that uses the `metrics` policy, and the policy is unmodified. Data streams that use a custom policy or a modified `metrics` policy remain unaffected.
* No `index.lifecycle.prefer_ilm` value is set in the index template, the data stream settings, or the create index request. An explicit value always takes precedence.
* The [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled) cluster setting is `true`, which is the default.

#### Revert to {{ilm-init}}

Choose the option that matches the scope you need:

* **All new backing indices in the cluster:** Set the dynamic cluster setting `data_streams.lifecycle.prefer_by_default.metrics_enabled` to `false`. This doesn't change backing indices that already have `prefer_ilm` set to `false`.
* **New backing indices of specific data streams:** Set `index.lifecycle.prefer_ilm` to `true` in the component or index template.
* **Existing backing indices of a data stream:** Update the data stream settings. The following request changes `prefer_ilm` on all backing indices of the data stream:

  ```console
  PUT _data_stream/my-time-series/_settings
  {
    "index.lifecycle.prefer_ilm": true
  }
  ```

### Check what manages a data stream [minimum-lifecycle-check]

To check whether the minimum lifecycle manages a data stream or an index, use the following APIs:

* [Get data stream API]({{es-apis}}operation/operation-indices-get-data-stream): returns `"minimum_lifecycle_enabled": true` and `"next_generation_managed_by": "Data stream lifecycle"` for the data stream.
* [Get data stream lifecycle API]({{es-apis}}operation/operation-indices-get-data-lifecycle): returns `"minimum_lifecycle_enabled": true` for the data stream.
* [Explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle): returns `"minimum_lifecycle_enabled": true` for each index the minimum lifecycle manages. For indices that no lifecycle manages, the response includes an `unmanaged_reason` field when {{es}} can determine why. The [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) includes the same field.

## Related pages [related-pages]

- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
- [Set up a {{tsds-init}}](/manage-data/data-store/data-streams/set-up-tsds.md)
- [Time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
- [Load historical data into a {{tsds-init}}](/manage-data/data-store/data-streams/load-historical-tsds.md)
- [Set up a data stream](/manage-data/data-store/data-streams/set-up-data-stream.md)
- [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md)
- [Configure data lifecycle with Streams](/solutions/observability/streams/configure-retention.md)
