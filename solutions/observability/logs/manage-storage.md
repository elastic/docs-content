---
navigation_title: Manage storage
description: Keep logs storage predictable with logsdb index mode, the default logs index template, per-stream retention in Streams, and data set quality monitoring.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Manage logs storage [logs-manage-storage]

You can control logs storage costs by deciding how logs are stored on disk, configuring the default index template, and setting long each stream keeps data. Tracking data set quality can also tell you when a parsing or mapping problem is impacting storage or data ingestion.

Use this page decide how to configure each of these steps in managing your log data.

## Before you begin [logs-manage-storage-prereqs]

- To change index templates and lifecycle policies on the {{stack}}, you need the `manage_index_templates` and `manage_ilm` cluster privileges, and `manage_data_stream_lifecycle` on the data streams you change. On {{serverless-full}}, you need the **Admin** role. For the full list of Streams privileges and prerequisites, refer to [Get data into Streams](/solutions/observability/streams/get-data-in.md#get-data-in-prerequisites).
- Know which data streams you're sending logs to. If you haven't started sending logs to Elastic, start with [Ingest logs](/solutions/observability/logs/ingest.md).

## Choose your storage settings [logs-manage-storage-steps]

:::::{stepper}

::::{step} Use logsdb index mode

Logsdb is an {{es}} index mode built for logs. It sorts and compresses documents by host and time and, with the right subscription, reconstructs `_source` on read instead of storing it. In Elastic's benchmarks it cut the storage footprint of log data by up to 60%, with a 10% to 20% cost to indexing throughput.

{applies_to}`serverless: ga`{applies_to}`stack: ga 9.0+` Logsdb is on by default for new logs data streams . The exception is a cluster upgraded from 8.x: `logs-*-*` data streams that already existed, including integration and {{product.apm}} data streams, keep their old mode, and new data streams in that cluster only get logsdb automatically if no logs data streams existed at upgrade time. Enable logsdb for those yourself, a few data streams at a time on a busy cluster, by following [Enable logsdb for integrations](/manage-data/data-store/data-streams/logs-data-stream-integrations.md).

For more on configuring logsdb, refer to [Logs data streams](/manage-data/data-store/data-streams/logs-data-stream.md) and [Configure a logs data stream](/manage-data/data-store/data-streams/logs-data-stream-configure.md).
::::

::::{step} Customize the default logs index template through `logs@custom`

Every `logs-*-*` data stream gets the managed `logs` index template unless you override it with a higher-priority template of your own. It sets logsdb mode, ECS-compatible dynamic mappings, and the default lifecycle, and it reserves a `logs@custom` component template and a `logs@custom` ingest pipeline for you. Neither exists until you create it.

Put your changes there, such as extra mappings, a different `default_field`, or index settings, rather than editing the managed templates, which Elastic updates on upgrade. For what each component template does, refer to [Default `logs` index template](/solutions/observability/logs/logs-index-template-defaults.md). For the steps, refer to [Logs index template reference](/solutions/observability/logs/logs-index-template-reference.md).
::::

::::{step} Set data retention

**Streams UI**

{applies_to}`stack: preview =9.1, ga 9.2+` {applies_to}`serverless: ga` Use the **Data lifecycle** tab (**Retention** tab in earlier versions) in the Streams UI to set lifecycle policies per stream, monitor storage in one view, and reduce storage with downsampling. Configure how long each stream retains data without touching ILM policies, index templates, or index settings directly.

The Streams UI shows the stream's storage size and ingestion rate so you can where you might need to make adjustments. You can set data retention using:

- A retention period on the stream itself, when the period is specific to that stream. Data stays in the hot tier and is deleted after the period.
- {applies_to}`serverless: unavailable` An existing {{ilm}} ({{ilm-init}}) policy, when several streams share one policy or you need warm, cold, or frozen tiers.

Refer to [Configure data lifecycle with Streams](/solutions/observability/streams/configure-retention.md).

**Data streams and index templates**

If you want to manage configuration as code, set retention on the data streams and index templates directly:

- **Data stream lifecycle**: Set a retention period on a data stream, or in the index template so new data streams inherit it. Works on {{serverless-full}} and the {{stack}}. Refer to [Update the lifecycle of a data stream](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md) and [Setting retention for {{es}} data streams](/manage-data/lifecycle/data-stream/tutorial-data-stream-retention.md).
- {applies_to}`serverless: unavailable` **{{ilm-cap}}**: Add a delete phase or move data through warm, cold, and frozen tiers. Don't edit the managed `logs@lifecycle` policy, because {{es}} updates might overwrite your changes. Duplicate it, change the copy, and apply the copy to your data streams. Refer to [Customize built-in {{ilm-init}} policies](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md).

For a summary of the options for logs, refer to [Configure log data retention](/solutions/observability/logs/logs-data-retention.md).
::::

::::{step} Track data set quality
```{applies_to}
stack: beta
serverless: beta
```

The **Data Set Quality** page shows the share of degraded documents in each data set, meaning documents with fields that {{es}} ignored because they were malformed or exceeded a limit. Those fields are stored but not searchable, so you pay for data you can't query.

Documents that fail ingestion entirely can be kept in a failure store instead of being dropped, so you can inspect them and fix the processor that rejected them. Refer to [Failure store](/solutions/observability/streams/manage-data-quality.md#streams-data-quality-failure).

Check the page after you change a parsing rule or add a source, and create a [degraded docs rule](/solutions/observability/incident-management/create-a-degraded-docs-rule.md) so you hear about it before your users do. Refer to [Data set quality](/solutions/observability/data-set-quality-monitoring.md) and [Manage your data quality with Streams](/solutions/observability/streams/manage-data-quality.md).
::::

:::::

## Related pages [logs-manage-storage-related]

- [Ingest logs](/solutions/observability/logs/ingest.md)
- [Process logs](/solutions/observability/logs/process.md): routing decides which streams exist, and therefore where retention applies.
- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md)
- [Configure log data sources](/solutions/observability/logs/log-data-sources.md)
