---
navigation_title: Monitor streams
description: Read the states and statistics the Streams Map shows about running streams, check the indices behind a destination, and learn what Streams doesn't report yet.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Monitor streams

Once data flows, the Streams Map shows whether each part of a stream is working, how much data arrives, and how fast it moves. This page explains what those numbers and states mean, how to look at the indices a destination can write to, and what Streams doesn't report, so you know when to look elsewhere.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

To view the statistics, you need at least the **Viewer** role.

## Statistics on the Map [streams-monitor-map]

Statistics on the Streams Map cover the last 15 minutes and refresh every 30 seconds while the Map is open. A rate is the average over those 15 minutes, not the rate at this instant, and no rate is a total since the stream was created. Each kind of node shows something different:

Source nodes
:   A state and the rate of accepted records per second. **Live** with a rate means the source accepted records in the last 15 minutes. **Waiting for data...** means it accepted none. Refused records don't count, so a source whose requests all fail authentication, or arrive on the wrong path, keeps waiting. All three source types show these statistics.

Destination nodes
:   The rate of records that reached the destination per second and the average time a write took, shown in microseconds, milliseconds, or seconds. **Data not flowing in** means no records reached the destination in the last 15 minutes. Only Local Elasticsearch destinations show statistics. Remote Elasticsearch and Amazon S3 destinations don't report them. A Local Elasticsearch destination node also shows a count of indices. That count isn't a statistic. It's the number of existing indices and data streams that match the destination's write patterns, and it can be above zero before any data flows.

Pipeline nodes
:   The rate of records per second and the average time a record spends in the pipeline, shown in microseconds, milliseconds, or seconds. The node doesn't show how many processors the pipeline has. Select it to see them in the **Processing** panel.

Router nodes
:   The rules, without statistics per rule.

Two things about these states are easy to misread. Because the rate is an average over 15 minutes, a node keeps showing a rate for up to 15 minutes after data stops, and a short gap doesn't change the state. And because the destination rate counts every record that reaches the destination, including records it rejects, a destination that stores nothing still shows a rate. To confirm that data is indexed, [check the data itself](#streams-monitor-check-data).

A few conventions apply to how the numbers are shown. Rates are shown per second, for example `0.27/s`. A rate below `0.01` is shown as `<0.01/s`, and a rate above 1,000 is abbreviated, for example `12.5k/s`. A value of `-` means no value was received yet. A warning icon next to the numbers means they can't be trusted. Its message is either **Could not refresh. Showing the last known values.**, when the last refresh failed and the numbers are from the last successful one, or **Could not load stats** followed by the reason, when no values are available at all.

## Indices behind a destination [streams-monitor-indices]

A Local Elasticsearch destination can write to many data streams and indices, and {{es}} reports on each of them. Streams lists the ones that exist in your project and match the destination's write patterns. To see the list, expand the destination on the **Destinations** tab, or select the destination on the Streams Map to open its panel. The panel also has a **Documents** chart for the time range you pick, with **Docs total**, **Docs in time range**, and **Peak ingest rate** under it. Refer to [Open a destination from the Map](destinations.md#streams-destinations-open).

The list is based on the write patterns, not on what the stream delivered. With the default patterns, it includes every `logs-*-*`, `metrics-*-*`, and `traces-*-*` data stream in the project, including ones that integrations or other shippers write to. Data streams that this stream created are among them, with `.otel` after the dataset when the data came from OTLP or Prometheus, for example `logs-demo.otel-audit` or `metrics-prw.otel-change`. That suffix is the naming of OpenTelemetry data streams, not a sign that something went wrong. To find out which data streams a record landed in, [check the data itself](#streams-monitor-check-data). Refer to [how Auto mode picks a data stream](destinations/elasticsearch.md#streams-es-destination-auto-data-stream).

The list has a column for each index's name, document count, ingestion rate, storage, health, data quality, failure store, and retention. Refer to [Manage destinations](destinations.md#streams-destinations-manage) for what each column shows. When a stream isn't behaving, read these columns:

* **Health**: **Red** means part of the data stream is unavailable and writes to it fail. **Green** and **Yellow** accept writes.
* **Data quality**: **Degraded** or **Poor** means a share of the records had fields ignored or failed to index. Open the index to see the **Top failure reasons**.
* **Failure store**: When it's **On**, {{es}} keeps records that failed to index, for example because of a mapping conflict, instead of dropping them, so you can see what was rejected and why. Refer to [Failure stores](../../data-store/data-streams/failure-store.md).

Select an index name to open its read-only **Overview** and **Retention** tabs. To change retention or mappings, select **Manage in Stack Management**. Refer to [View the details of an index](destinations.md#streams-destinations-index).

## Check the data itself [streams-monitor-check-data]

Statistics tell you that data flows, not what it looks like or whether it was stored. To check the effect of processors and routing rules, open **Discover** and query the destination's data streams, for example with {{esql}}:

```esql
FROM logs-*
| WHERE resource.attributes.service.name == "checkout"
| STATS count = COUNT(*) BY data_stream.dataset
```

Compare the fields you see with what the shipper sent. A field added by an Add fields processor, a record that a Filter should have dropped, or a dataset that a routing rule should have changed are all visible here within a minute of arrival.

## What isn't reported [streams-monitor-not-reported]

Streams doesn't show:

* **Drops and errors.** Records that a destination couldn't store, that a processor dropped, or that matched no routing rule aren't counted on the Streams Map. A destination that rejects everything it receives still shows a rate, because the rate counts records that arrive, not records that are stored.
* **End-to-end latency.** How long a record takes from the source to the index isn't measured for a stream. The duration on a pipeline node covers that pipeline only, and the duration on a destination node covers the write to {{es}} only.
* **Per-rule statistics** on routers, and statistics on Remote Elasticsearch and Amazon S3 destinations.
* **Alerting** on any of the above. There's no rule type for Streams statistics.

Keep the monitoring you already have on the shipper side, such as the collector's own metrics, and on the destination side, such as data stream health and the failure store. Refer to [Streams limitations](limitations.md#streams-limitations-data).

## Related pages [streams-monitor-related]

* [Streams Map](streams-map.md): Learn how to read and edit the Map that the statistics appear on.
* [Destinations](destinations.md): Learn what the **Destinations** tab, the destination panel, and the index view show.
* [Troubleshooting](troubleshooting.md): Learn what to check when a destination shows **Data not flowing in** or a shipper gets an error.
