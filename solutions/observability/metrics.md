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

Start here if you need to get metrics into Elastic, or decide how to ingest them:

[Get started with metrics](/solutions/observability/metrics/get-started.md)
:   Get data flowing quickly using an {{edot}} quickstart for your deployment type and environment. Start here if you're evaluating Elastic or want a working pipeline before you commit to a data model.

[Migrate metrics to Elastic](/solutions/observability/metrics/migrate.md)
:   Move an existing Prometheus or Datadog stack to Elastic. Because Elastic accepts OpenTelemetry Protocol (OTLP) and Prometheus remote write, you can run both systems side by side and migrate gradually.

[Ingest metrics](/solutions/observability/metrics/ingest.md)
:   Compare every ingest path in detail: {{edot}} and OTLP, Prometheus remote write, and {{agent}} integrations, including which path is recommended for your deployment type.

[Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
:   Understand how each ingest path stores your metrics (OpenTelemetry, Elastic Common Schema (ECS), or Prometheus names) and pick the path for your deployment type before you scale up.

## Work with metrics already in Elastic [metrics-work-with]

After metrics are in Elastic, use these pages to query, visualize, and control storage:

[Query metrics](/solutions/observability/metrics/query.md)
:   Query metrics with Elasticsearch Query Language ({{esql}}) time-series mode for counters, rates, and per-series aggregations, or with PromQL to reuse existing Prometheus queries and alerting rules.

[Explore metrics](/solutions/observability/metrics/explore.md)
:   {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Explore and visualize metrics in **Discover**, the Infrastructure UI, or {{kib}} dashboards.

    {applies_to}`stack: deprecated 9.4+, ga 9.0-9.3` Explore and visualize metrics in **Metrics Explorer**, the Infrastructure UI, or {{kib}} dashboards.

[Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
:   Control storage costs and retention using time series data streams (TSDS), downsampling, cardinality management, and lifecycle policies.

## Already using Prometheus? [metrics-prometheus-users]

Keep Prometheus scraping and add Elastic as a `remote_write` target. Your scrape configurations don't change. On {{serverless-full}} and {{ech}}, send to the Managed Prometheus Remote Write endpoint. On self-managed {{stack}}, {{ece}}, and {{eck}}, send to the {{es}} `/_prometheus/api/v1/write` endpoint.

{applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` If you use Grafana, point its Prometheus data source at {{es}} and keep your PromQL dashboards. {{es}} runs a subset of PromQL, so check each dashboard and alert rule against the PromQL limitations before you switch it over.

Use these pages to add remote write, keep Grafana, and reuse PromQL:

[Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md) {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+`
:   The recommended remote write destination on {{serverless-full}} and {{ech}}.

[Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md) {applies_to}`stack: preview =9.4, ga 9.5+`
:   The {{es}} `/_prometheus/api/v1/write` endpoint for self-managed {{stack}}, {{ece}}, and {{eck}}.

[Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md) {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga`
:   Point Grafana at {{es}} and keep your existing PromQL dashboards.

[PromQL reference](elasticsearch://reference/query-languages/promql.md) {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga`
:   Learn how {{es}} evaluates PromQL and which functions and constructs it supports.
