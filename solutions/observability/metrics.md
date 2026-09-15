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

## Send metrics to Elastic [metrics-send]

[Get started with metrics](/solutions/observability/metrics/get-started.md)
:   Get data flowing quickly using an {{edot}} quickstart for your deployment type and environment. Start here if you're evaluating Elastic or want a working pipeline before you commit to a data model.

[Migrate to Elastic metrics](/solutions/observability/metrics/migrate.md)
:   Move an existing Prometheus or Datadog stack to Elastic. Because Elastic accepts OTLP and Prometheus remote write, you can run both systems side by side and migrate gradually.

[Ingest metrics](/solutions/observability/metrics/ingest.md)
:   Compare every ingest path in detail: {{edot}} and OTLP, Prometheus remote write, and {{agent}} integrations, including which path is recommended for your deployment type.

[Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
:   Choose between the OpenTelemetry and ECS data models before you scale up, and understand what that choice means for field names, dashboards, and queries.

## Work with metrics already in Elastic [metrics-work-with]

[Query metrics](/solutions/observability/metrics/query.md)
:   Query metrics with {{esql}} time-series mode for counters, rates, and per-series aggregations, or with PromQL to reuse existing Prometheus queries and alerting rules.

[Explore metrics](/solutions/observability/metrics/explore.md)
:   Explore and visualize metrics in Discover, the Infrastructure UI, {{kib}} dashboards, or Grafana.

[Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
:   Control storage costs and retention using time series data streams (TSDS), downsampling, cardinality management, and lifecycle policies.

## Already using Prometheus? [metrics-prometheus-users]

You can send metrics to Elastic with a minimal change to your existing Prometheus setup, without a full migration. Add a `remote_write` target to your `prometheus.yml` pointing at {{es}}, and your existing scrape configs continue to work unchanged.

If you use Grafana, you can also point it at {{es}} as a Prometheus data source and run your existing PromQL dashboards and alerts without rewriting them.

- [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md)
- [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md)
- [PromQL in {{es}}](elasticsearch://reference/query-languages/promql/functions.md)
