---
navigation_title: Prometheus Remote Write
description: Create a Prometheus Remote Write source in Streams and send metrics to it from a Prometheus server or Grafana Alloy.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Prometheus Remote Write source

A **Prometheus Remote Write** source accepts metrics from a Prometheus server, Grafana Alloy, or any other sender that implements the Prometheus Remote Write protocol. Use it to bring Prometheus metrics into the same pipelines and destinations as the rest of your telemetry, for example to drop high-cardinality series before they're indexed or to copy them to a second deployment.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

A Prometheus Remote Write source is different from your project's shared [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md), which writes straight to {{es}}. The source has its own URL and API keys, and its data goes through whatever you connect to it on the Streams Map.

## Before you begin [streams-prw-source-prereqs]

To create a Prometheus Remote Write source, you need:

* The **Admin** role. Refer to [Privileges and API keys](../security.md#streams-security-view-edit).
* A Prometheus server or another sender that sends Prometheus Remote Write 1.0 and can send a custom `Authorization` header. Remote Write 2.0 isn't supported.

## Create the source [streams-prw-source-create]

You create the source on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Source** in the toolbar at the bottom of the Map.
1. For **Source type**, select **Prometheus Remote Write**, and enter a **Source name**. The source accepts metrics only, so there are no signals to select.
1. Select **Continue**, then copy the **Endpoint** URL and the **API key**. The key isn't shown again.
1. Select **Done**, connect the source to a destination on the Map, and select **Save changes**.

The endpoint has the form `https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/prometheus-remote-write/<source-id>/api/v1/write`.

## Send metrics to the source [streams-prw-source-send]

The source's dialog has a snippet for each of the following senders under **Send data using**, with the endpoint and key filled in.

### Prometheus [streams-prw-source-prometheus]

Add a `remote_write` entry to your Prometheus configuration:

```yaml
remote_write:
  - url: https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/prometheus-remote-write/<source-id>/api/v1/write
    authorization:
      type: ApiKey
      credentials: <key>
```

Prometheus keeps sending to any other `remote_write` targets you have configured, so you can add Streams next to your current destination.

### Grafana Alloy [streams-prw-source-alloy]

Add a `prometheus.remote_write` component to your Alloy configuration:

```text
prometheus.remote_write "elastic" {
  endpoint {
    url = "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/prometheus-remote-write/<source-id>/api/v1/write"
    authorization {
      type = "ApiKey"
      credentials = "<key>"
    }
  }
}
```

## How the data is stored [streams-prw-source-storage]

The source converts each sample into an OpenTelemetry metric data point. Metric names, label names, and label values are kept as they are. Labels become attributes of the data point with their original names, such as `job` and `instance`, and aren't mapped to OpenTelemetry semantic conventions or moved to resource attributes. Processors in a pipeline work with the metrics in that form. Refer to [Process data](../process-data.md).

In a **Local Elasticsearch** destination, keep **Auto (default)** index mode for Prometheus metrics. In Auto mode, the metrics are written to OpenTelemetry metrics data streams, named `metrics-<dataset>.otel-<namespace>`, which are time series data streams. Refer to [How Auto mode picks a data stream](../destinations/elasticsearch.md#streams-es-destination-auto-data-stream). In Fixed mode, a plain index name you choose isn't a time series data stream, and the metrics lose the storage and query behavior that depends on one.

Because the metrics are stored as OpenTelemetry metrics, they don't have the same fields or data stream names as metrics sent to the Managed Prometheus Remote Write endpoint.

## Related pages [streams-prw-source-related]

* [Sources](../sources.md): Compare the source types and manage sources and their API keys.
* [OTLP source](otlp.md): Send OpenTelemetry logs, metrics, and traces instead of Prometheus metrics.
* [Managed _bulk source](elasticsearch-bulk.md): Send JSON documents with the {{es}} bulk API instead.
* [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md): Learn about the project's shared Prometheus endpoint, which writes straight to {{es}}.
* [Troubleshoot Streams](../troubleshooting.md): Fix `404`, `401`, and `403` responses from a source endpoint.
