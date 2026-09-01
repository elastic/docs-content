---
navigation_title: Query metrics
description: Query metrics in Elastic using ES|QL with time-series mode for TSDS data, or PromQL for Prometheus and Grafana workflows.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Query metrics [metrics-query]

Elastic supports two first-class query experiences for metrics: {{esql}} and PromQL. Use the one that matches how your metrics were ingested and what you're trying to do. Cross-schema analysis happens at query time — no normalization at ingest is required.

## Which query language to use [metrics-query-which]

:::::{applies-switch}

::::{applies-item} stack:
**OTel-ingested or Prometheus remote write metrics — time-series queries (counters, rates, time buckets):**
Use [{{esql}} with time-series (TS) mode](/solutions/observability/metrics/query-with-esql-ts.md). TS mode operates efficiently on TSDS columnar storage and handles per-series aggregation correctly.

**Prometheus or Grafana workflows:**
Use [PromQL](/reference/query-languages/promql/functions.md). Works against both Prometheus remote write and OTLP-ingested metrics, but metric names are schema-dependent.
::::

::::{applies-item} serverless:
**OTel-ingested or Prometheus remote write metrics — time-series queries (counters, rates, time buckets):**
Use [{{esql}} with time-series (TS) mode](/solutions/observability/metrics/query-with-esql-ts.md).

**Prometheus or Grafana workflows:**
Use [PromQL](/reference/query-languages/promql/functions.md). Works against both Prometheus remote write and OTLP-ingested metrics.
::::

:::::

## {{esql}} for metrics [metrics-query-esql]

{{esql}} is the recommended choice for ad hoc analysis, time-series aggregations, and building dashboards in {{kib}}. For metrics stored as TSDS, use {{esql}} time-series mode for counters, rates, and per-series aggregation.

- [Query metrics with {{esql}} TS mode](/solutions/observability/metrics/query-with-esql-ts.md)
- [Query downsampled data](/manage-data/data-store/data-streams/query-downsampled-data.md)
- [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md)

## PromQL for metrics [metrics-query-promql]

If you sent metrics to Elastic using Prometheus remote write or OTLP, you can query them using PromQL directly in {{es}}. This lets you reuse existing Prometheus queries and alerting rules without rewriting them. If you use Grafana, you can point it at {{es}} as a Prometheus data source.

- [PromQL functions reference](/reference/query-languages/promql/functions.md)
- [Use {{es}} as a Prometheus data source in Grafana](/reference/query-languages/promql/promql-grafana.md)
- [PromQL limitations in {{es}}](/reference/query-languages/promql/promql-limitations.md)

## Related [metrics-query-related]

- [Explore metrics](/solutions/observability/metrics/explore.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
