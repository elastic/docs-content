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
:   The rate of records that reached the destination per second and the average time a write took, shown in microseconds, milliseconds, or seconds. All three destination types show them. **Data not flowing in** means no records reached the destination in the last 15 minutes, or that no saved source feeds it. A destination that rejects what it's sent shows a **Failures** badge instead. Refer to [Delivery failures](#streams-monitor-failures). A Local Elasticsearch destination node also shows a count of indices. That count isn't a statistic. It's the number of existing indices and data streams that match the destination's write patterns, and it can be above zero before any data flows.

Pipeline nodes
:   The rate of records per second and the average time a record spends in the pipeline, shown in microseconds, milliseconds, or seconds, or **No data** when nothing has flowed through it. The statistics describe the saved pipeline, so a pipeline you moved or added shows nothing until you save. The node doesn't show how many processors the pipeline has. Select it to see them in the **Processing** panel.

Router nodes
:   The rules, without statistics per rule.

Two things about these states can mislead you. Because the rate is an average over 15 minutes, a node keeps showing a rate for up to 15 minutes after data stops, and a short gap doesn't change the state. And because the destination rate counts every record that reaches the destination, including records it rejects, a destination that stores nothing still shows a rate. To confirm that data is indexed, [check the data itself](#streams-monitor-check-data).

A few conventions apply to how the numbers are shown. Rates are shown per second, for example `0.27/s`. A rate below `0.01` is shown as `<0.01/s`, and a rate above 1,000 is abbreviated, for example `12.5k/s`. A value of `-` means no value was received yet. A warning icon next to the numbers means they can't be trusted. Its message is either **Could not refresh. Showing the last known values.**, when the last refresh failed and the numbers are from the last successful one, or **Could not load stats** followed by the reason, when no values are available at all.

## Delivery failures [streams-monitor-failures]

Streams reports the records a destination refused because of its credential, in two classes:

* **Authentication**: the destination didn't recognize the credential. For an {{es}} destination, that's a `401` response, for example from an API key that was invalidated or mistyped. For an Amazon S3 destination, it's an error code such as `InvalidAccessKeyId`, `SignatureDoesNotMatch`, or `ExpiredToken`.
* **Authorization**: the destination recognized the credential but didn't allow the write. For an {{es}} destination, that's a `403` response, for example from a key without `create_doc` on the target data stream, or a Local Elasticsearch destination whose record is headed for an index outside its write patterns. For an Amazon S3 destination, it's a code such as `AccessDenied`.

On the Streams Map, a destination with failures of either class in the last 15 minutes shows a red **Failures** badge in place of **Data not flowing in**. Hover over the badge to see, for each class, the percentage of records that failed, the failure rate, and how the percentage is trending. The badge doesn't open the details. Select the node to do that.

In the destination's panel, the **Delivery** section covers the time range you pick with the time picker. It charts **Delivered** records next to **Authentication**, **Authorization**, and **Other failures**. When records failed in one of the two classes, the section is titled **Delivery failures** and adds, for each class, its percentage and rate and a table of causes: the **Index name** the records were headed for and the **Error type** {{es}} reported, or for Amazon S3 the error code, each with its percentage and rate. Drag across the chart to narrow the time range. When nothing failed, the section says **No delivery failures in this time range.**, and when nothing was sent, **No delivery attempts in this time range.** For a Local Elasticsearch destination, the **Documents** chart above the section shows what was delivered, and the section lists only the failures.

The figures are a share of what the destination attempted in the time range, not a count of lost records. For an {{es}} destination, a failure is a rejected record. For an Amazon S3 destination, it's a failed upload, and a retry counts as another attempt. Records a destination refuses for another reason, such as a mapping conflict or a bucket that doesn't exist, appear in the chart as **Other failures** but have no class and don't raise the badge. Refer to [What isn't reported](#streams-monitor-not-reported) and, for what to do about a failing destination, [Troubleshooting](troubleshooting.md#streams-troubleshoot-destination-failures).

## Indices behind a destination [streams-monitor-indices]

A Local Elasticsearch destination can write to many data streams and indices, and {{es}} reports on each of them. Streams lists the ones that exist in your project and match the destination's write patterns. To see the list, expand the destination on the **Destinations** tab, or select the destination on the Streams Map to open its panel. The panel also has a **Documents** chart for the time range you pick, with **Docs total**, **Docs in time range**, and **Peak ingest rate** under it. Refer to [Open a destination from the Map](destinations.md#streams-destinations-open).

The list is based on the write patterns, not on what the stream delivered. With the default patterns, it includes every `logs-*-*`, `metrics-*-*`, and `traces-*-*` data stream in the project, including ones that integrations or other shippers write to. Data streams that this stream created are among them, with `.otel` after the dataset when the data came from OTLP or Prometheus, for example `logs-demo.otel-audit` or `metrics-prw.otel-change`. That suffix is the naming of OpenTelemetry data streams, not a sign that something went wrong. To find out which data streams a record landed in, [check the data itself](#streams-monitor-check-data). Refer to [how Automatic mode picks a data stream](destinations/elasticsearch.md#streams-es-destination-auto-data-stream).

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

* **Most drops.** Records that a processor dropped or that matched no routing rule aren't counted anywhere. On a destination, only authentication and authorization failures raise the **Failures** badge. Other rejections, such as a mapping conflict, show up only as **Other failures** in the destination's delivery chart, and a destination that rejects everything it receives still shows a rate, because the rate counts records that arrive, not records that are stored. Refer to [Delivery failures](#streams-monitor-failures).
* **Source errors.** Requests a source refused, for example with a bad API key or on a wrong path, aren't counted or shown. The source keeps showing **Waiting for data...**.
* **End-to-end latency.** How long a record takes from the source to the index isn't measured for a stream. The duration on a pipeline node covers that pipeline only, and the duration on a destination node covers the write only.
* **Per-rule statistics** on routers.
* **Alerting** on any of the above. There's no rule type for Streams statistics.

Keep the monitoring you already have on the shipper side, such as the collector's own metrics, and on the destination side, such as data stream health and the failure store. Refer to [Streams limitations](limitations.md#streams-limitations-data).

## Related pages [streams-monitor-related]

* [Streams Map](streams-map.md): Learn how to read and edit the Map that the statistics appear on.
* [Destinations](destinations.md): Learn what the **Destinations** tab, the destination panel, and the index view show.
* [Troubleshooting](troubleshooting.md): Learn what to check when a destination shows **Data not flowing in** or a shipper gets an error.
