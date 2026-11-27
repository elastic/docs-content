---
navigation_title: Deprecated metrics policy no longer manages new indices
description: Troubleshooting guide for new backing indices that still use the deprecated metrics ILM policy and are managed by data stream lifecycle instead of ILM after an upgrade.
type: troubleshooting
applies_to:
  stack: ga 9.6+
  serverless: unavailable
products:
  - id: elasticsearch
---

# {{ilm-init}} no longer manages new indices that use the deprecated metrics policy

After you upgrade, new backing indices of a {{tsds}} ({{tsds-init}}) that still uses the deprecated `metrics` [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) policy stop being managed by {{ilm-init}}.
The policy stays attached, but [data stream lifecycle](/manage-data/lifecycle/data-stream.md) manages those new indices instead.
This applies only to the deprecated `metrics` policy, not to the current `metrics@lifecycle` policy.
Use this page to confirm that is what happened and, if you want {{ilm-init}} to keep managing the indices, put them back under {{ilm-init}}.

## Symptoms

- The deprecated `metrics` {{ilm-init}} policy is still attached to the data stream or its backing indices.
- The [{{ilm-init}} explain API]({{es-apis}}operation/operation-ilm-explain-lifecycle) does not show {{ilm-init}} managing a new backing index.
- The [explain data stream lifecycle API]({{es-apis}}operation/operation-indices-explain-data-lifecycle) shows data stream lifecycle or the minimum lifecycle managing that index.
- Older backing indices remain managed by {{ilm-init}}.

<!--
TO-DO: Add link to [minimum lifecycle](/manage-data/lifecycle/data-stream/dlm-default-lifecycle.md) 
-->

## Diagnosis

{{es}} defaults [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) to `false` on a new backing index only when all the following are true:

- The index is a backing index of a {{tsds-init}}. Other data streams and standalone indices are not affected.
- The template resolves [`index.lifecycle.name`](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md#index-lifecycle-name) to the deprecated policy named `metrics`. Streams that use `metrics@lifecycle` are not affected.
- That policy is still the pre-installed one: version 1, `managed: true`, and a single hot phase whose only action is rollover at 50GB or 30 days. A custom policy, a modified `metrics` policy, or any later policy version stays under {{ilm-init}}.
- Nothing in the index template, the data stream settings, or the create index request sets [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm). An explicit value always takes precedence.
- The [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled) cluster setting is `true`.

Existing backing indices stay under {{ilm-init}}.
The switch happens the next time {{es}} creates a backing index, which is the next rollover after the upgrade.
If the data stream already has its own data stream lifecycle, that lifecycle manages the new index.
If it doesn't, the minimal default lifecycle does.
<!--
TO-DO: Add link [minimal default lifecycle](/manage-data/lifecycle/data-stream/dlm-default-lifecycle.md)
-->
The unmodified, deprecated `metrics` policy has no delete or downsample phase, so this switch doesn't stop a retention or downsample action that policy was running.
Rollover moves from that {{ilm-init}} action to data stream lifecycle and tail merging starts.

## Resolution

If you do not mind migrating from {{ilm-init}} to data stream lifecycle, you don't need to change anything.

To keep {{ilm-init}} managing the indices, select the option that matches the scope you need:

1. **All new backing indices in the cluster:** Set the dynamic cluster setting [`data_streams.lifecycle.prefer_by_default.metrics_enabled`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#data-streams-lifecycle-prefer-by-default-metrics-enabled) to `false`. This doesn't change backing indices that already have [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) set to `false`.

   ```console
   PUT _cluster/settings
   {
     "persistent": {
       "data_streams.lifecycle.prefer_by_default.metrics_enabled": false
     }
   }
   ```

2. **New backing indices of specific data streams:** Set [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) to `true` in the component or index template.
3. **Existing backing indices of a data stream:** Update the data stream settings. The following request changes [`index.lifecycle.prefer_ilm`](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md#index-lifecycle-prefer-ilm) on all backing indices of the data stream:

   ```console
   PUT _data_stream/my-time-series/_settings
   {
     "index.lifecycle.prefer_ilm": true
   }
   ```

## Resources

<!--
- [Default lifecycle for data streams](/manage-data/lifecycle/data-stream/dlm-default-lifecycle.md)
-->
- [Customize built-in {{ilm-init}} policies](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md)
- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
- [Data stream lifecycle settings](elasticsearch://reference/elasticsearch/configuration-reference/data-stream-lifecycle-settings.md)
