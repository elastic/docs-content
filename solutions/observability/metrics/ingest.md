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

Elastic supports multiple ingestion paths for metrics. {{edot}} is the recommended path for new setups. {{agent}} integrations are recommended for existing Elastic deployments.

## Ingest with {{edot}} (recommended) [metrics-ingest-otlp]

{{edot}} is the recommended distribution. Any compliant OTLP client is first-class.

:::::{applies-switch}

::::{applies-item} serverless:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA for {{serverless-full}} {{observability}} projects.

- **Application metrics**: point your EDOT SDKs or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics** (host, {{k8s}}, Docker): run {{agent}} in OTel mode on your hosts or cluster and configure the OTLP exporter to send data to the endpoint.

Refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for authentication, endpoint URL, and protocol details.
::::

::::{applies-item} ech:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA on {{ech}}.

- **Application metrics**: point your EDOT SDKs or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics**: run {{agent}} in OTel mode on your hosts or cluster and configure the OTLP exporter to send data to the endpoint.

Refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for authentication, endpoint URL, and protocol details.
::::

::::{applies-item} self:
**Run {{agent}} in OTel mode as a gateway.**

The Managed OTLP endpoint is not available for self-managed {{stack}}, {{ece}} (ECE), or {{eck}} (ECK) deployments. Run {{agent}} in OTel mode as a gateway: it exposes an OTLP endpoint that your EDOT SDKs and edge collectors send data to, and forwards the data to {{es}}.

For {{stack}} 9.2 and later, you can also send OTLP data directly to the {{es}} OTLP endpoint. Refer to [{{es}} OTLP/HTTP ingest endpoint](/manage-data/ingest/otlp-endpoint.md).

Refer to [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md) for setup instructions.
::::

:::::

### Reference pages [metrics-ingest-otlp-reference]

- [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md)
- [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md)
- [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md)
- [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md) — cumulative vs delta behavior for counters and histograms

## Ingest with {{agent}} integrations [metrics-ingest-agent-integrations]

Use {{agent}} integrations to collect metrics from specific infrastructure components and services — for example, system metrics from hosts, {{k8s}} cluster metrics, or metrics from nginx, PostgreSQL, or Redis. Integrations use {{product.ecs}} (ECS) field naming conventions.

Use this path when you already have {{agent}} deployed, when you need out-of-box dashboards for specific technologies, or when you want to keep existing ECS-schema data unchanged.

- [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)
- Browse available integrations in the [{{integrations}} catalog](https://www.elastic.co/integrations)

## Ingest using Prometheus remote write [metrics-ingest-prometheus]

Send metrics from Prometheus to {{es}} using the Prometheus remote write protocol. Add a `remote_write` target to your `prometheus.yml` — your existing scrape configs continue to work unchanged.

This path is useful when you want to try Elastic without changing your Prometheus setup, or as part of a gradual migration.

- [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md)

## Related [metrics-ingest-related]

- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
