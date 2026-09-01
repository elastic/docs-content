---
navigation_title: Query with ES|QL
description: Use ES|QL time-series mode to query TSDS metrics with counters, rates, and per-series aggregations.
applies_to:
  stack: ga 9.4+
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Query metrics with {{esql}} and time-series functions [metrics-query-esql-ts]

:::{note}
This page is a stub. Detailed {{esql}} time-series query guidance is coming soon.
:::

{{esql}} provides time-series functions designed for metrics stored in TSDS (Time Series Data Streams). These functions handle the ordered, columnar structure of time-series data natively, making aggregations like `RATE`, `AVERAGE`, and `MAX` over time windows more efficient than equivalent aggregations on regular indices.

## When to use time-series functions [metrics-query-esql-ts-when]

Use {{esql}} time-series functions when:
- Your metrics are stored as TSDS (this is the default for OTLP and Prometheus remote write ingestion)
- You need to compute rates, averages, or other time-window aggregations
- You're building dashboards or alerts in {{kib}} Discover or Lens

## Related [metrics-query-esql-ts-related]

- [{{esql}} overview](/reference/query-languages/esql/index.md)
- [Query metrics](/solutions/observability/metrics/query.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
