---
navigation_title: Metrics
description: Ingest, store, query, and visualize metrics from any source using OpenTelemetry, Prometheus remote write, or Elastic Agent integrations.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Metrics [metrics]

Elastic lets you ingest, store, query, and visualize metrics from any source. Whether you're consolidating a Prometheus or Datadog stack, collecting infrastructure metrics, or sending custom application metrics, Elastic supports OpenTelemetry, Prometheus remote write, and {{agent}} integrations from a single platform.

## What do you want to do? [metrics-intent]

| I want to | Go to |
|---|---|
| Start sending metrics to Elastic | [Get started with metrics](/solutions/observability/metrics/get-started.md) |
| Move my existing Prometheus or Datadog stack to Elastic | [Migrate to Elastic metrics](/solutions/observability/metrics/migrate.md) |
| Understand my ingest options in detail | [Ingest metrics](/solutions/observability/metrics/ingest.md) |
| Query metrics already in Elastic | [Query metrics](/solutions/observability/metrics/query.md) |
| Explore and visualize metrics | [Explore metrics](/solutions/observability/metrics/explore.md) |
| Control storage costs and retention | [Manage metrics storage](/solutions/observability/metrics/manage-storage.md) |

## Recommended ingestion path [metrics-ingestion-path]

The recommended ingestion path depends on your Elastic deployment type.

:::::{applies-switch}

::::{applies-item} serverless:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA for {{serverless-full}} {{observability}} projects. For application metrics, point your EDOT SDK or any OTLP-compatible exporter directly at the endpoint — no {{agent}} required. For infrastructure metrics (host, {{k8s}}), run {{agent}} in OTel mode on your hosts or cluster and configure it to export data to the endpoint using the OTLP exporter.

Refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for configuration details and limitations.
::::

::::{applies-item} ech:
**Send metrics to the Managed OTLP endpoint.**

The Managed OTLP endpoint is GA on {{ech}}. For application metrics, point your EDOT SDK or any OTLP-compatible exporter directly at the endpoint — no {{agent}} required. For infrastructure metrics, run {{agent}} in OTel mode on your hosts or cluster and configure it to export using the OTLP exporter.

Refer to [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for configuration details and limitations.
::::

::::{applies-item} self:
**Run {{agent}} in OTel mode as a gateway.**

The Managed OTLP endpoint is not available for self-managed {{stack}}, {{ece}} (ECE), or {{eck}} (ECK) deployments. Run {{agent}} in OTel mode as a gateway to expose an OTLP endpoint that your edge collectors and EDOT SDKs send data to.

Refer to [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md) for setup instructions.
::::

:::::

## Already using Prometheus? [metrics-prometheus-users]

You can send metrics to Elastic with a minimal change to your existing Prometheus setup — no full migration required. Add a `remote_write` target to your `prometheus.yml` pointing at {{es}}, and your existing scrape configs continue to work unchanged.

If you use Grafana, you can also point it at {{es}} as a Prometheus data source and run your existing PromQL dashboards and alerts without rewriting them.

- [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md)
- [Use {{es}} as a Prometheus data source in Grafana](/reference/query-languages/promql/promql-grafana.md)
- [PromQL in {{es}}](/reference/query-languages/promql/functions.md)
