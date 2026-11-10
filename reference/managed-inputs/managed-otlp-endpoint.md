---
navigation_title: Managed OTLP Endpoint
description: Reference documentation for the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Elastic Cloud Managed OTLP Endpoint (mOTLP)

The {{motlp}} allows you to send OpenTelemetry data directly to {{ecloud}} using the OTLP protocol. 

The endpoint provides a resilient ingestion layer that integrates with serverless autoscaling and offloads ingestion processing from {{ech}} clusters.

:::{important}
The {{motlp}} endpoint is not available for Elastic [self-managed](/deploy-manage/deploy/self-managed.md), [ECE](/deploy-manage/deploy/cloud-enterprise.md), or [ECK](/deploy-manage/deploy/cloud-on-k8s.md) clusters. To send OTLP data to any of these cluster types, deploy and expose an OTLP-compatible endpoint using the [{{agent}} as a gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway).
:::

## Prerequisites

To use the {{ecloud}} {{motlp}} you need the following:

- An {{serverless-full}} project or an {{ech}} (ECH) deployment.
- An OTLP-compliant shipper capable of forwarding logs, metrics, or traces in OTLP format. This can include:
  - [OpenTelemetry Collector](elastic-agent://reference/edot-collector/index.md) ({{edot}}, Contrib, or other distributions)
  - [OpenTelemetry SDKs](opentelemetry://reference/edot-sdks/index.md) ({{edot}}, upstream, or other distributions)
  - [{{edot-cf}}](opentelemetry://reference/edot-cloud-forwarder/index.md)
  - Any other forwarder that supports the OTLP protocol.

You don't need APM Server when ingesting data through the Managed OTLP Endpoint. The APM integration (`.apm` endpoint) is a legacy ingest path that translates OTLP telemetry to ECS, whereas {{motlp}} natively ingests OTLP data.

## Send data to the Managed OTLP Endpoint

To send data to Elastic through the {{motlp}}, follow the [Send data to the Elastic Cloud Managed OTLP Endpoint](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) quickstart.

### Find your {{motlp}}

:::{include} _snippets/find-motlp-endpoint.md
:::

### Configure SDKs to send data directly

To configure OpenTelemetry SDKs to send data directly to the {{motlp}}, set the `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variables.

For example:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <key>"
```

### Routing telemetry to dedicated datasets or namespace

You can route signals to dedicated datasets by setting the `data_stream.dataset` attribute on the record. This attribute is used to route the signal to the corresponding dataset.

For example, if you want to route the {{edot-cf}} logs to custom datasets, you can add the following attributes to the log records:

```yaml
processors:
  transform:
    log_statements:
      - set(log.attributes["data_stream.dataset"], "aws.cloudtrail") where log.attributes["aws.cloudtrail.event_id"] != nil
```

You can also set the `OTEL_RESOURCE_ATTRIBUTES` environment variable to set the `data_stream.dataset` attribute for all logs. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES="data_stream.dataset=app.orders"
```

The  `data_stream.namespace` attributes is also honored for all signals: logs, metrics, and traces.

:::{important}
Any `data_stream.dataset` or `data_stream.namespace` resource attribute present in an OTLP payload overrides mOTLP's default routing for that signal. This applies whether the attribute is set intentionally or by a collector, SDK, or integration.

If data is landing in an unexpected data stream, inspect a sample document from that data stream for the field `resource.attributes.data_stream.dataset`. If the field is present and matches the unexpected data stream name, the attribute was set in the payload, not by the pipeline.

To restore default routing, remove the `data_stream.dataset` and `data_stream.namespace` resource attributes from your OTLP payload configuration. Once removed, mOTLP falls back to routing based on `service.name`.
:::

## Authentication

Managed inputs use a shared authentication model. Refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication) for the required API key format and generation steps.

:::{note}
Index-level privilege scoping is not supported for managed inputs.
:::

## OTLP client configuration

When using OpenTelemetry collectors to send data to the {{motlp}}, configure the OTLP exporter with an explicit timeout, an in-memory queue, and batching. Use the following configuration as a starting point to improve throughput and allow requests to complete during temporary increases in ingestion latency.

```yaml
exporters:
  otlp/elastic:
    endpoint: "${MOTLP_ENDPOINT}"
    timeout: 30s
    headers:
      Authorization: "ApiKey <key>"
    sending_queue:
      enabled: true
      sizer: bytes
      queue_size: 50_000_000
      block_on_overflow: true
      batch:
        flush_timeout: 1s
        min_size: 1_000_000
        max_size: 4_000_000
```

The key settings are:

* **`timeout`**: Sets the timeout for each export attempt to 30 seconds. The upstream Collector default of 5 seconds can cancel requests during temporary increases in ingestion latency. This timeout is separate from the batching flush timeout and the retry budget. It does not make successful requests wait for 30 seconds.
* **`sending_queue`**: Enables an in-memory queue with byte-based sizing (`sizer: bytes`) and a 50 MB capacity. `block_on_overflow: true` applies backpressure by waiting for space when the queue is full. Enqueueing can still fail if the caller's request times out before space becomes available. Queued data does not survive a Collector crash or forced termination.
* **`batch`**: Controls how queued data is batched before export. A `flush_timeout` of 1 second ensures low latency, while `min_size` (1 MB) and `max_size` (4 MB) keep payloads within the {{motlp}} limits. Refer to the [Payload too large](troubleshooting.md#error-payload-too-large) troubleshooting section for details on payload size limits.

The upstream Collector enables retries for retryable export failures by default, with a retry budget (`retry_on_failure.max_elapsed_time`) of 5 minutes. These retries are separate from the timeout for each attempt. Increasing the attempt timeout allows slower requests to complete instead of repeatedly cancelling them at the same short deadline. For details, refer to the [OpenTelemetry Collector exporter helper configuration](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/exporterhelper#configuration).

Tune the timeout and queue capacity for your workload. Monitor export failures and queue utilization during traffic spikes to check whether the configuration provides enough headroom.

## Reference architecture

This diagram shows data ingest using {{edot}} and the {{motlp}}:

:::{image} images/motlp-reference-architecture.png
:alt: mOTLP Reference architecture
:width: 100%
:::

Telemetry is stored in Elastic in OTLP format, preserving resource attributes and original semantic conventions. If no specific dataset or namespace is provided, telemetry is routed to the generic data streams: `traces-generic.otel-default`, `metrics-generic.otel-default`, and `logs-generic.otel-default`.

For a detailed comparison of how OTel data streams differ from classic Elastic APM data streams, refer to [OTel data streams compared to classic APM](opentelemetry://reference/compatibility/data-streams.md).

## Metrics ingestion on {{ech}}

For {{ech}} deployments running Elastic Stack 9.5.3 or later, the {{motlp}} routes metrics to the native {{es}} OTLP endpoint. Deployments running Elastic Stack 9.0 through 9.5.2 use the {{es}} bulk API compatibility path instead. This routing is automatic and does not require client-side configuration changes.

The native {{es}} OTLP endpoint supports both `delta` and `cumulative` temporality starting in Elastic Stack 9.5. When sending metrics through the {{motlp}} on {{ech}}, use Elastic Stack 9.5.3 or later to access these capabilities. Refer to [Histogram and counter temporality](opentelemetry://reference/compatibility/limitations.md#histogram-and-counter-temporality) for details.

## Indexing errors and the failure store

A successful response from the {{motlp}} means your data was durably accepted for processing, not that {{es}} has indexed it. For what happens when indexing fails and how to verify your data was indexed, refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store).

## Limitations

The following limitations apply when using the {{motlp}}:

* Universal Profiling is not available.
* The endpoint only writes to data streams with `logs-`, `metrics-`, or `traces-` prefixes. Data routed to other prefixes is silently dropped and will not appear in {{es}}.
* For supported metric temporality for histograms and counters, refer to [Histogram and counter temporality](opentelemetry://reference/compatibility/limitations.md#histogram-and-counter-temporality).
* Latency distributions based on histogram values have limited precision due to the fixed boundaries of explicit bucket histograms.
* Tail-based sampling (TBS) is not available. The {{motlp}} does not provide centralized hosted sampling. If you need tail-based sampling, configure it on the edge using the [Tail Sampling Processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor) in your {{edot}} or OpenTelemetry Collector before sending data to the endpoint.
* For how IP filters and private connectivity apply to all managed inputs, refer to [Network security](authentication-delivery-and-failure-handling.md#network-security).

## Billing

For more information on billing, refer to [Elastic Cloud pricing](https://www.elastic.co/pricing/serverless-observability).
