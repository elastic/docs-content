---
navigation_title: Troubleshooting
description: Fix common Streams problems, such as 404, 401, and 403 errors at a source endpoint, data that doesn't appear in Discover, and destinations that stop receiving it.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
---

# Troubleshoot Streams

This page collects the problems that come up most often while you build a stream, with the symptoms you see and the steps that resolve them. Most problems at a source come down to the URL path or the API key. Most problems after that come down to an unsaved change on the Streams Map or a destination that can't store what it's given.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

To understand what the Streams Map does and doesn't tell you, refer to [Monitor streams](monitor-streams.md). For what Streams doesn't support yet, refer to [Streams limitations](limitations.md).

## The source returns 404 [streams-troubleshoot-404]

**Symptoms**

* The source endpoint returns `404 page not found` to every request.
* The shipper logs `404` for every request to the source endpoint.

**Cause**

The URL path doesn't match a source. A wrong source ID, a missing or doubled signal segment, or a wrong prefix all return `404`.

**Resolution**

1. Compare the URL with the endpoints shown in the source's details on the **Sources** tab. The path must be exactly `/inputs/otlp/<source-id>/v1/<signal>` for an OTLP source or `/inputs/prometheus-remote-write/<source-id>/api/v1/write` for a Prometheus Remote Write source, with the source ID as shown, not the display name.
1. For an OpenTelemetry Collector, check that the `otlphttp` exporter's `endpoint` doesn't already include `/v1/logs`. The exporter appends the signal path itself. Use `logs_endpoint`, `metrics_endpoint`, and `traces_endpoint` if you need the full URL per signal.

## The source returns 401 [streams-troubleshoot-401]

**Symptoms**

* The source endpoint returns `401 missing header "Authorization"`.
* The source endpoint returns `401 Unauthenticated`.

**Cause**

The `Authorization` header isn't reaching the endpoint, or the API key it carries no longer exists.

**Resolution**

1. For `missing header "Authorization"`, send the header as `Authorization: ApiKey <encoded key>`, with the key exactly as copied from the source. In a collector, check that the `otlphttp` exporter's `headers` contain `Authorization: "ApiKey <key>"`, and if you read the key from an environment variable, that the variable is set in the collector's environment, not only in your shell. In a Prometheus server, set `authorization: type: ApiKey, credentials: <key>` in the `remote_write` block, not `basic_auth` or `bearer_token`.
1. For `Unauthenticated`, generate a new key. The key was deleted from the source, or the source itself was deleted and recreated with the same name. Open the source on the **Sources** tab, select **Generate key**, and update the shipper. For what a source key can do, refer to [Privileges and API keys](security.md#streams-security-source-keys).

## The source returns 403 [streams-troubleshoot-403]

**Symptoms**

* The source endpoint returns `403 PermissionDenied` to the whole request.
* A Managed _bulk source accepts the request, but individual documents in the response have a `403` status with a `security_exception` error.

**Cause**

The API key is valid but doesn't grant what the request asks for. A source key grants write access to its own source only, and a Managed _bulk source accepts only documents whose index name starts with `logs-`, `metrics-`, or `traces-`.

**Resolution**

1. For `PermissionDenied`, use the key from the source you're sending to. A key copied from one source can't send to another.
1. Check that the source ID in the path matches the source the key was generated for. The ID is derived from the source's name at creation time.
1. For per-document `403` errors from a Managed _bulk source, change the `_index` in the action, or the target in the path, to a name that starts with `logs-`, `metrics-`, or `traces-`. If the sender gets `400 Bad Request` instead, it isn't using the `create` action. Refer to [Managed _bulk source](sources/elasticsearch-bulk.md#streams-bulk-source-accepts).

## OTLP over gRPC doesn't connect [streams-troubleshoot-grpc]

**Symptoms**

* A collector with an `otlp` exporter, or an SDK with `OTEL_EXPORTER_OTLP_PROTOCOL=grpc`, can't connect to the source endpoint, or the endpoint returns `404`.

**Cause**

A source is identified by its URL path, which gRPC requests don't carry. Sources accept OTLP over HTTP only.

**Resolution**

1. In a collector, use the `otlphttp` exporter instead of `otlp`.
1. In an SDK, set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`.

## Requests succeed but nothing appears in Discover [streams-troubleshoot-no-data]

**Symptoms**

* The source endpoint returns `200`, and the shipper reports success.
* On the Streams Map, the source node shows **Live** but the destination node shows **Data not flowing in**, or the destination shows a rate while **Discover** stays empty.
* **Discover** shows nothing in the expected data stream.

**Resolution**

1. Wait a minute and refresh. Statistics on the Streams Map refresh every 30 seconds, and Discover shows records once they're indexed.
1. On the Streams Map, check that the source is connected to a destination and that you selected **Save changes**. A connection you drew but didn't save doesn't exist. A confirmation message appears after a successful save.
1. Check that the source accepts the signal you're sending. A source takes only the signals selected when it was created. Open the source's details on the **Sources** tab to see its signals.
1. Check that the destination accepts that signal. In **Fixed index per signal** mode, a signal left blank isn't written. In **Auto** mode, data outside the destination's write patterns is dropped.
1. Check the processors on the path. A Filter processor drops matching records before any destination, and dropped records aren't counted on the Map. Temporarily remove the Filter, select **Save and apply**, and see whether data appears.
1. Check the router, if there is one. A record that matches no rule is dropped, and unmatched records aren't counted on the Map. Select the router to read the rules' conditions and check their order. Refer to [Route data](route-data.md).
1. If the destination shows a rate, the records reach it and {{es}} rejects them. In the **Destinations** tab, expand the destination to see each index and its **Health**. A **Red** data stream rejects writes. If the failure store is **On**, open the index and read the **Top failure reasons**.
1. In **Discover**, widen the time range and query the broad pattern for the signal, for example `FROM logs-*`. In **Auto** mode a record with `data_stream.dataset` set lands in that dataset's data stream, with `.otel` after the dataset, for example `logs-demo.otel-default`, not in the default one.

## A Local Elasticsearch destination shows Data not flowing in after working [streams-troubleshoot-destination-stopped]

**Symptoms**

* A Local Elasticsearch destination node on the Streams Map that showed a rate shows **Data not flowing in**.
* The source endpoints upstream still return `200`, and the shippers report success.

**Cause**

The state counts the records that reached the destination in the last 15 minutes, including records that {{es}} rejected. **Data not flowing in** after a rate means that nothing has reached the destination for 15 minutes, so the problem is on the path before the destination, not in {{es}}. If the source node upstream shows **Waiting for data...** too, the shippers stopped sending or their requests are refused; if it shows **Live**, the records are lost between the source and the destination.

**Resolution**

1. On the Streams Map, check that the source is still connected to the destination. A save or an **Undo** can remove a connection.
1. Check the processors on the path. A Filter processor that was added or changed recently can drop every record. Temporarily remove it, select **Save and apply**, and see whether the destination shows a rate again.
1. Check the router, if there is one. A rule whose condition or order changed can send records to another destination, or to none. Select the router to read the rules. Refer to [Route data](route-data.md).
1. Check that the shippers still send to the source this destination is connected to, and not to another source or endpoint.

If the destination shows a rate but the data isn't in **Discover**, the records reach it and {{es}} rejects them. Refer to [Requests succeed but nothing appears in Discover](#streams-troubleshoot-no-data). Remote Elasticsearch and Amazon S3 destinations don't show a state, so for those, check for the data on the remote side. Streams doesn't report rejected credentials, so a revoked API key or access key looks like silence. Destinations can't be edited, so create a new destination with the new credential, reconnect the routing rules, and delete the old one. Records that fail at a destination are dropped after the retry window and aren't recovered when the destination comes back. Refer to [Streams limitations](limitations.md#streams-limitations-data).

## The processor list is empty or can't be edited [streams-troubleshoot-processor-list]

**Symptoms**

* The **Processing** panel shows **Unable to load the available processors**.
* The **Processing** panel shows **The list of available processors may be out of date**.
* The **Processing** panel shows **This version of {{kib}} cannot edit this processing** and a **Read only** badge.

**Resolution**

1. For **Unable to load the available processors** or **The list of available processors may be out of date**, select **Try again**. If it persists for more than a few minutes, contact your Elastic account team with the time and the project ID.
1. For **This version of {{kib}} cannot edit this processing**, wait for the {{kib}} update, which happens automatically on {{serverless-short}}. You can still view the processors in the meantime.

## Related pages [streams-troubleshoot-related]

* [Monitor streams](monitor-streams.md): Learn what the states and statistics on the Streams Map mean, and what Streams doesn't report yet.
* [Work with the Streams Map](streams-map.md): Learn how to read the Map, connect nodes, and save your changes.
* [Build your first stream](get-started/build-your-first-stream.md): Follow the tutorial that most of these problems come up in.
* [OTLP source](sources/otlp.md), [Prometheus Remote Write source](sources/prometheus-remote-write.md), and [Managed _bulk source](sources/elasticsearch-bulk.md): Find the endpoint URLs, the API key, and the sender configuration for each source type.
* [Process data before it reaches Elasticsearch](process-data.md): Learn how pipelines run and how to add and manage processors.
* [Streams limitations](limitations.md): Check what Streams doesn't support yet before you treat it as a problem.
