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

Data streams without a [lifecycle](/manage-data/lifecycle/data-stream.md) can still be managed by default.

* {applies_to}`serverless: ga` Any data stream created without a lifecycle gets a default lifecycle. That lifecycle supports all operations, including [global retention](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md) if you configure it.
* {applies_to}`stack: ga 9.6+` Any {{tsds}} ({{tsds-init}}) created without a lifecycle get a minimal default lifecycle. It performs only the operations a stream needs to stay healthy: roll over and tail merging. It doesn't downsample, move data to {{search-snaps}}, or delete data, even when a global retention is set.

## Requirements

::::{applies-switch}
:::{applies-item} serverless: ga

To configure or turn off the lifecycle, you need [`manage_data_stream_lifecycle`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.

:::

:::{applies-item} stack: ga 9.6+

- To configure or turn off the lifecycle, you need [`manage_data_stream_lifecycle`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.
- To inspect whether a default lifecycle manages a stream, you need the [`view_index_metadata`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) indices privilege.
- To change [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) or [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled), you need the [`manage`](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) cluster privilege.
:::
::::

## How it works

{{es}} keeps a stream operational without you configuring a policy.
It rolls the write index over so shards stay a usable size, and it tail merges so recent data doesn't sit in a long tail of small segments.

::::{applies-switch}
:::{applies-item} serverless: ga

{{ilm-init}} isn't available in {{serverless-short}}, so omitting a lifecycle would leave the stream unmanaged.
{{es}} writes an enabled data stream lifecycle onto every new stream so rollover, tail merging, and retention (including global retention) can run.

The default lifecycle runs these operations:

* **Rollover:** Rolls over the write index when the conditions in [`cluster.lifecycle.default.rollover`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#cluster-lifecycle-default-rollover) are met.
  This keeps shards a usable size and allows backwards incompatible mapping changes.
* **Tail merge:** After rollover, merges the long tail of small Lucene segments.
  Those segments usually hold recent, often-queried data.
  Tail merging costs a fraction of a full force merge.

{{es}} writes an enabled data stream lifecycle onto the stream at create time.
Retention, including global retention, can delete data.
Downsampling still needs an explicit configuration.
Frozen {{search-snaps}} aren't available.

A [data stream lifecycle](/manage-data/lifecycle/data-stream.md#data-streams-lifecycle-how-it-works) you configure replaces this fallback.
It can add retention and downsampling.

The default lifecycle applies when the matching index template has no lifecycle.
Turning the lifecycle off leaves the stream unmanaged.

:::

:::{applies-item} stack: ga 9.6+

A {{tsds}} with no lifecycle and no {{ilm-init}} policy was never rolled over automatically.
The minimal default lifecycle adds only rollover and tail merging.
It doesn't change the data set, so it's safe as a default on streams that already have no retention policy.

The minimal default lifecycle runs these operations:

* **Rollover:** Rolls over the write index when the conditions in [`cluster.lifecycle.default.rollover`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#cluster-lifecycle-default-rollover) are met.
  This keeps shards a usable size and allows backwards incompatible mapping changes.
* **Tail merge:** After rollover, merges the long tail of small Lucene segments.
  Those segments usually hold recent, often-queried data.
  Tail merging costs a fraction of a full force merge.

The minimal default lifecycle doesn't write a lifecycle onto the stream.
Retention is skipped even when global retention is set.
It doesn't downsample or move data to {{search-snaps}}.
Only a {{tsds-init}} gets this fallback. Other data streams stay unmanaged.

A [data stream lifecycle](/manage-data/lifecycle/data-stream.md#data-streams-lifecycle-how-it-works) you configure replaces this fallback.
It can add retention and downsampling.
It can also add frozen transitions to {{search-snaps}}.

The default lifecycle applies when the following are true:

* The data stream is a {{tsds-init}}.
* The data stream has no data stream lifecycle configured.
  A lifecycle that is turned off is still a configuration, so the minimum lifecycle doesn't apply.
* The [`data_streams.lifecycle.minimum.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-minimum-enabled) cluster setting is `true`.
* Backing indices are not managed by {{ilm-init}} policies.
  A backing index with an {{ilm-init}} policy stays managed by {{ilm-init}} unless [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) is `false`.
  A {{tsds-init}} that still uses the unmodified, deprecated `metrics` policy is the exception, because {{es}} sets `prefer_ilm` to `false` on new backing indices.
  <!--
  TO-DO: Add link when troubleshooting page exists
  Refer to [{{ilm-init}} no longer manages new indices that use the deprecated metrics policy](/troubleshoot/elasticsearch/metrics-policy-not-managed-by-ilm.md).
  -->

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

To check whether a data stream or an index is managed by a minimal default lifecycle, use the following APIs:

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
