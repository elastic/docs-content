---
navigation_title: OTLP
description: Create an OTLP endpoint source in Streams and send OpenTelemetry logs, metrics, and traces to it from a collector, an SDK, or the Kubernetes Operator.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# OTLP source

An **OTLP endpoint** source accepts OpenTelemetry Protocol (OTLP) data over HTTP from any OpenTelemetry Collector, SDK, or agent, including {{agent}} in OpenTelemetry mode. Use it for OpenTelemetry-native telemetry, and when you want to process and route several signals together. One source can accept logs, metrics, and traces.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

An OTLP source is different from your project's [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md). The {{motlp}} is a single shared endpoint that writes straight to {{es}}, and the data sent to it doesn't appear on the Streams Map. An OTLP source has its own URL and API keys, and its data goes through the pipelines, routers, and destinations you connect to it on the Map.

## Before you begin [streams-otlp-source-prereqs]

To create an OTLP endpoint source, you need:

* The **Admin** role. Refer to [Privileges and API keys](../security.md#streams-security-view-edit).
* A sender that supports OTLP over HTTP with protobuf or JSON encoding. OTLP over gRPC isn't supported, because the source is identified by the URL path and gRPC requests don't carry one.

## Create the source [streams-otlp-source-create]

You create the source on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Source** in the toolbar at the bottom of the Map.
1. For **Source type**, select **OTLP endpoint**, and enter a **Source name**.
1. Under **Signals**, clear any of **Logs**, **Metrics**, and **Traces** that the source shouldn't accept. All three are selected by default, and at least one must stay selected.
1. Select **Continue**. Copy the **Logs endpoint**, **Metrics endpoint**, and **Traces endpoint** URLs, one for each signal you selected, and the **API key**. The key isn't shown again.
1. Select **Done**, connect the source to a destination on the Map, and select **Save changes**.

The endpoints have the form `https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>/v1/<signal>`. There's no endpoint for a signal you didn't select. Senders that take a base endpoint and append `/v1/<signal>` themselves, such as the OpenTelemetry Collector's `otlphttp` exporter and the OpenTelemetry SDKs, use the URL without the `/v1/<signal>` suffix. The snippets in the source's dialog use that base URL.

## Send data to the source [streams-otlp-source-send]

Every request carries the header `Authorization: ApiKey <key>`. The following examples show how to configure the most common senders.

### OpenTelemetry Collector [streams-otlp-source-collector]

The **OTel Collector** tab under **Send data using** gives you an `otlphttp` exporter with the endpoint and key filled in. Add it to your collector configuration and reference it from the pipelines for the signals the source accepts:

```yaml
exporters:
  otlphttp/elastic:
    endpoint: "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>"
    headers:
      Authorization: "ApiKey <key>"
    sending_queue:
      enabled: true

service:
  pipelines:
    logs:
      receivers: [otlp]
      exporters: [otlphttp/elastic]
```

To send to Streams and to your current output at the same time, list both exporters in the pipeline.

### OpenTelemetry Kubernetes Operator and SDKs [streams-otlp-source-operator-sdks]

The **K8s Operator** tab gives you the standard OTLP exporter environment variables. They also work for an application instrumented with an OpenTelemetry SDK. Some SDKs default to gRPC, so also set `OTEL_EXPORTER_OTLP_PROTOCOL` to an HTTP protocol, as in this example:

```yaml
env:
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>"
  - name: OTEL_EXPORTER_OTLP_HEADERS
    value: "Authorization=ApiKey <key>"
  - name: OTEL_EXPORTER_OTLP_PROTOCOL
    value: "http/protobuf"
```

### Test with curl [streams-otlp-source-curl]

To confirm that the source and key work, send a single JSON log record to the **Logs endpoint**:

```bash
curl -sS -X POST "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>/v1/logs" \
  -H 'Content-Type: application/json' \
  -H "Authorization: ApiKey <key>" \
  -d '{"resourceLogs":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"streams-test"}}]},"scopeLogs":[{"logRecords":[{"timeUnixNano":"'"$(date +%s)"'000000000","severityText":"INFO","body":{"stringValue":"hello from Streams"}}]}]}]}'
```

If the request returns `404`, `401`, or `403`, refer to [Troubleshoot Streams](../troubleshooting.md#streams-troubleshoot-404).

## How the data is stored [streams-otlp-source-storage]

Where the data is stored depends on the destinations you connect. A **Local Elasticsearch** destination in Auto mode writes each record to an OpenTelemetry data stream named `<signal>-<dataset>.otel-<namespace>`, chosen from the record's `data_stream.dataset` and `data_stream.namespace` attributes, and records without them go to the default data stream for their signal. Refer to [How Auto mode picks a data stream](../destinations/elasticsearch.md#streams-es-destination-auto-data-stream).

Processors in a pipeline see the OTLP data model, which has resource attributes, scope attributes, and the record's own fields and attributes. Refer to [Process data](../process-data.md).

## Related pages [streams-otlp-source-related]

* [Sources](../sources.md): Compare the source types and manage sources and their API keys.
* [Build your first stream](../get-started/build-your-first-stream.md): Follow an end-to-end walkthrough that sends OTLP logs to an {{es}} destination.
* [Prometheus Remote Write source](prometheus-remote-write.md): Send Prometheus metrics instead of OTLP.
* [Managed _bulk source](elasticsearch-bulk.md): Send JSON documents with the {{es}} bulk API instead of OTLP.
* [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md): Learn about the project's shared OTLP endpoint and OTLP client configuration in detail.
* [Troubleshoot Streams](../troubleshooting.md): Fix `404`, `401`, and `403` responses and gRPC connection failures.
