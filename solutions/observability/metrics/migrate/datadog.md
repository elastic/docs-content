---
navigation_title: Migrate from Datadog
description: Migrate from Datadog to Elastic. Send OpenTelemetry metrics, replace Datadog Agent host and Kubernetes collection, and rebuild dashboards and monitors.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate from Datadog [metrics-migrate-datadog]

Elastic endpoints don't accept the Datadog Agent's native metrics protocol. You migrate by sending OpenTelemetry data to Elastic, or by replacing Datadog Agent collection with {edot} or {agent} integrations. Keep Datadog running until the Elastic queries and alerts match what you need, then stop the duplicate stream.

## Before you begin [metrics-migrate-prereqs]

:::{include} /solutions/observability/metrics/_snippets/migrate-prereqs.md
:::

## Migration steps [metrics-migrate-datadog-steps]

::::::{stepper}

:::::{step} Send your metrics to Elastic
:anchor: metrics-migrate-datadog-send

Pick the path that matches how you collect metrics:

#### Retarget applications that already emit OTLP [metrics-migrate-datadog-otlp]

If your services already export OTLP, retarget those exporters at Elastic. Change `OTEL_EXPORTER_OTLP_ENDPOINT` (and the authentication headers) to the Managed OTLP Endpoint or to {{agent}} configured as an OTel Collector gateway, using the same settings as any other OTLP client.

The Datadog Agent can receive OTLP from your applications and forward it to Datadog. That ingest path doesn't forward the same telemetry to Elastic. Point the applications, or a collector in front of them, at Elastic.

For the endpoint and gateway options by deployment type, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md#metrics-ingest-otlp).

#### Send the same metrics from an OpenTelemetry Collector [metrics-migrate-datadog-collector]

If a collector already receives your metrics and exports them to Datadog, add Elastic as a second exporter and send the same metrics to both backends. Keep the Datadog exporter until you have validated Elastic queries and alerts.

Any OpenTelemetry Collector distribution can do this, including vendor distributions. On {{ecloud}}, add an `otlp` exporter that points at the Managed OTLP Endpoint. On self-managed {{stack}}, forward OTLP to {{agent}} configured as an OTel Collector gateway.

For the Elastic OTLP destination, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md#metrics-ingest-otlp). For the self-managed gateway pattern, refer to [Send data from an upstream OpenTelemetry Collector](/solutions/observability/get-started/opentelemetry/use-cases/upstream-collector/index.md).

#### Replace Datadog Agent host and {{k8s}} collection [metrics-migrate-datadog-infra]

Checks that the Datadog Agent scrapes itself, such as host CPU and memory or Kubernetes state, are Datadog-native, not OTLP. To bring those metrics into Elastic, collect them with Elastic instead of forwarding data from the Datadog Agent.

For the OpenTelemetry schema, follow an {{edot}} quickstart for your hosts or cluster: [Get started with metrics](/solutions/observability/metrics/get-started.md). 

For {{product.ecs}} field names and existing {{product.integrations}}, use {{agent}} integrations: [Ingest with {{agent}} integrations](/solutions/observability/metrics/ingest.md#metrics-ingest-agent-integrations).
:::::

:::::{step} Recreate dashboards and monitors
:anchor: metrics-migrate-datadog-assets

Elastic has no built-in import for Datadog dashboards and monitors. After metrics are in Elastic, rebuild the views and alerts you still need:

- Explore and chart the new field names. Refer to [Explore metrics](/solutions/observability/metrics/explore.md) for how to query and chart them.
- Recreate monitors with a [custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md), or with an [inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md) for resource-centric checks.

Metric names and tags from Datadog don't match OpenTelemetry semantic conventions or ECS one-for-one. Confirm each chart and rule against the fields you ingested before you stop Datadog.
:::::

::::::
