---
applies_to:
  stack: ga 9.6+
  serverless: ga
navigation_title: Default lifecycle
description: Learn how Elasticsearch manages data streams that have no data stream lifecycle of their own, including automatic rollover and tail merging.
type: overview
products:
  - id: elasticsearch
---

# Default lifecycle for data streams

If you create a data stream without configuring a [lifecycle](/manage-data/lifecycle/data-stream.md), in the following contexts it is automatically provided:

* {applies_to}`serverless: ga` All data streams have a lifecycle by default.
* {applies_to}`stack: ga 9.6+` Any {{tsds}} ({{tsds-init}}) created without a lifecycle gets a minimum lifecycle.

The default and minimum lifecycles include the following operations:

* **Rollover:** Rolls over the write index when the conditions in [`cluster.lifecycle.default.rollover`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#cluster-lifecycle-default-rollover) are met.
  This keeps shards a usable size and allows backwards incompatible mapping changes.
* **Tail merge:** After rollover, merges the long tail of small Lucene segments.
  Those segments usually hold recent, often-queried data.
  Tail merging costs a fraction of a full force merge.

## Requirements

::::{applies-switch}
:::{applies-item} serverless: ga

To configure the lifecycle, you need [`manage_data_stream_lifecycle`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.

:::
:::{applies-item} stack: ga 9.6+

- To configure or turn off the lifecycle, you need [`manage_data_stream_lifecycle`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.
- To inspect whether a default lifecycle manages a stream, you need the [`view_index_metadata`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.
- To change [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) or [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled), you need the [`manage`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) cluster privilege.
:::
::::

## How it works

::::{applies-switch}
:::{applies-item} serverless: ga

When you create a data stream, {{es}} adds a lifecycle and turns it on so rollover, tail merging, and retention run.

To customize the data stream lifecycle, refer to [](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md). For example, you can change the data retention settings.
:::
:::{applies-item} stack: ga 9.6+

When you create a {{tsds}} ({{tsds-init}}) without a data stream lifecycle, {{es}} adds a minimum lifecycle and turns it on so rollover and tail merging can run.

The minimum lifecycle applies when the following are true:

* The data stream is a {{tsds-init}}.
* The data stream has no data stream lifecycle configured.
  A lifecycle that is turned off is still a configuration, so the minimum lifecycle doesn't apply.
* The [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) cluster setting is `true`.
* Backing indices are not managed by {{ilm-init}} policies.
  A backing index with an {{ilm-init}} policy stays managed by {{ilm-init}} unless [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) is `false`.

The minimum lifecycle performs only the operations a data stream needs to stay healthy: rollover and tail merging.
It never changes the data set, so it doesn't downsample, move data to {{search-snaps}}, or delete data.
It doesn't delete data even if you configure a global retention.

Adding a data stream lifecycle to the data stream replaces the minimum lifecycle with your configuration.
Refer to [](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md). For example, you can change the data retention settings and add frozen transitions to {{search-snaps}}.
:::
::::

To leave a classic data stream unmanaged by data stream lifecycle, [turn off the lifecycle](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#delete-lifecycle).

Wired streams cannot be unmanaged.
They inherit lifecycle details from the parent or you can set a period or an {{ilm-init}} policy.
Refer to [](/solutions/observability/streams/configure-retention.md).

## Troubleshooting
```{applies_to}
stack: ga 9.6+
```

To check whether a data stream or an index is managed by a minimum lifecycle, use the following APIs:

* [Get data stream API]({{es-apis}}operation/operation-indices-get-data-stream): returns `"minimum_lifecycle_enabled": true` and `"next_generation_managed_by": "Data stream lifecycle"` for the data stream.
* [Get data stream lifecycle API]({{es-apis}}operation/operation-indices-get-data-lifecycle): returns `"minimum_lifecycle_enabled": true` for the data stream.
* [Explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle): returns `"minimum_lifecycle_enabled": true` for each index the minimum lifecycle manages. For indices that no lifecycle manages, the response includes an `unmanaged_reason` field when {{es}} can determine why. The [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) includes the same field.

::::{important}
Before 9.6, a {{tsds-init}} without a lifecycle or an {{ilm-init}} policy was never rolled over automatically. If an external process rolls over your {{tsds-init}}, you might now see additional backing indices.
If your {{tsds-init}} has an {{ilm-init}} policy, no data stream lifecycle, and [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) is set to `false`, it moves from {{ilm-init}} to the minimum lifecycle.
As a result, {{ilm-init}} phases such as delete or downsample stop running for it.

To restore the previous behavior, set [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) to `false`.
The setting is dynamic, so you don't need to restart {{es}}.
For example:

```console
PUT _cluster/settings
{
  "persistent": {
    "data_streams.lifecycle.minimum.enabled": false
  }
}
```

::::

## Related pages [related-pages]

- [Set up a data stream](/manage-data/data-store/data-streams/set-up-data-stream.md)
- [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md)
- [Configure data lifecycle with Streams](/solutions/observability/streams/configure-retention.md)
