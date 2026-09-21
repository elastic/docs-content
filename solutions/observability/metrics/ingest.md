---
navigation_title: Ingest metrics
description: Send metrics to Elastic using OpenTelemetry, Prometheus remote write, or Elastic Agent integrations. Includes guidance for Serverless, Elastic Cloud Hosted, and self-managed deployments.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Ingest metrics [metrics-ingest]

Elastic supports multiple ingestion paths for metrics. {{edot}} is the recommended path, except for the use cases listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

## Ingest with {{edot}} (recommended) [metrics-ingest-otlp]

{{edot}} is the recommended distribution. You can also send metrics with any OTLP-compliant client. The setup depends on your deployment type.

:::::{applies-switch}

::::{applies-item} serverless:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA for {{serverless-full}} {{observability}} projects. Use a different setup depending on the telemetry you collect:

- **Application metrics:** Point your EDOT SDKs or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics (host, {{k8s}}, Docker):** Run {{agent}} in OTel mode on your hosts or cluster and configure the OTLP exporter to send data to the endpoint.

For authentication, endpoint URL, and protocol details, refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).
::::

::::{applies-item} ech:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA on {{ech}}. Use a different setup depending on the telemetry you collect:

- **Application metrics:** Point your EDOT SDKs or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics:** Run {{agent}} in OTel mode on your hosts or cluster and configure the OTLP exporter to send data to the endpoint.

For authentication, endpoint URL, and protocol details, refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).
::::

::::{applies-item} { self:, ece:, eck: }
**Run {{agent}} in OTel mode as a gateway.**

The Managed OTLP endpoint is not available for self-managed {{stack}}, {{ece}} (ECE), or {{eck}} (ECK) deployments. Run {{agent}} in OTel mode as a gateway: it exposes an OTLP endpoint that your EDOT SDKs and edge collectors send data to, and forwards the data to {{es}}.

{applies_to}`stack: ga 9.2+` You can also send OTLP data directly to the {{es}} OTLP endpoint. For endpoint configuration, refer to [{{es}} OTLP/HTTP ingest endpoint](/manage-data/ingest/otlp-endpoint.md).

For gateway versus edge setup, refer to [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md).
::::

:::::

For language SDK setup, refer to [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md). For how counters and histograms behave after ingest, refer to [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md).

## Ingest with {{agent}} integrations [metrics-ingest-agent-integrations]

Use {{agent}} integrations to collect metrics from specific infrastructure components and services. For example, system metrics from hosts, {{k8s}} cluster metrics, or metrics from nginx, PostgreSQL, or Redis. {{integrations}} use {{product.ecs}} (ECS) field naming conventions.

Use this path when your use case is listed in the {{edot}} limitations, for example, when you need existing ECS integrations and dashboards to keep working without customization.

To collect host metrics this way, follow [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md). To find which services have a prebuilt integration, browse the [{{integrations}} catalog](https://www.elastic.co/integrations).

## Ingest using Prometheus remote write [metrics-ingest-prometheus]

Send metrics from Prometheus, Grafana Alloy, or another Prometheus remote write client. Add a remote write target so your existing scrape configurations continue to work unchanged.

This path is useful when you want to try Elastic without changing your Prometheus setup, or as part of a gradual migration. The endpoint depends on your deployment:

:::::{applies-switch}

::::{applies-item} serverless:
Use the [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md). Managed inputs provide durable buffering, unified authentication, and back-pressure handling.
::::

::::{applies-item} ech:
```{applies_to}
stack: ga 9.4+
```

Use the [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md). On {{ech}}, this is the recommended remote write destination; sending Prometheus traffic directly to {{es}} skips that buffering.
::::

::::{applies-item} { self:, ece:, eck: }
```{applies_to}
stack: ga 9.5+, preview =9.4
```

Send remote write traffic to the {{es}} `/_prometheus/api/v1/write` endpoint. For the URL, authentication, Grafana Alloy configuration, and data-stream routing, refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).
::::

:::::

For the side-by-side ingest sequence and how to switch over, refer to [Migrate to Elastic metrics](/solutions/observability/metrics/migrate.md#metrics-migrate-prometheus).

## Related pages [metrics-ingest-related]

- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
