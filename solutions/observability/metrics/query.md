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

Elastic supports two query experiences for metrics: {{esql}} and PromQL. Use the one that matches how your metrics were ingested and what you're trying to do. Since cross-schema analysis happens at query time, no normalization at ingest is required.

## Which query language to use [metrics-query-which]

| If you want to | Use |
|---|---|
| Run time-series queries over OTel or Prometheus remote write metrics, including counters, rates, and time buckets | [{{esql}} with time-series (TS) mode](#metrics-query-esql-ts) |
| Reuse existing Prometheus queries, alerting rules, or Grafana dashboards | [PromQL](#metrics-query-promql) |

## {{esql}} for metrics [metrics-query-esql]

{{esql}} is the recommended choice for ad hoc analysis, time-series aggregations, and building dashboards in {{kib}}.

### Time-series (TS) mode [metrics-query-esql-ts]
```{applies_to}
stack: ga 9.4+
serverless: ga
```

For metrics stored as TSDS, use {{esql}} time-series mode. The `TS` command operates on TSDS columnar storage and computes rates, averages, and other per-series aggregations over time windows, which makes it more efficient than the equivalent aggregations on regular indices and correct for per-series data.

Use TS mode when:

- Your metrics are stored as TSDS, which is the default for OTLP and Prometheus remote write ingestion.
- You need to compute rates, averages, or other time-window aggregations.
- You're building dashboards or alerts in {{kib}} Discover or Lens.

For example, the following query returns the 80th percentile of request duration per endpoint in one-minute buckets:

```esql
TS my-metrics
| STATS PERCENTILE(request_duration, 80) BY endpoint, TBUCKET(1m)
```

Refer to [{{esql}} overview](elasticsearch://reference/query-languages/esql.md) for the full language reference.

### Query downsampled data [metrics-query-downsampled]

When a TSDS is downsampled, you can still query the coarser buckets with {{esql}}. The `TS` command is optimized for a mix of raw and downsampled backing indices. Refer to [Query downsampled data](/manage-data/data-store/data-streams/query-downsampled-data.md) for more information.

### Metrics in Discover [metrics-query-discover]
```{applies_to}
stack: ga 9.4+
serverless: ga
```

In Discover, run a `TS` query in {{esql}} mode to open a chart grid of available metrics. You can search, filter, break metrics down by dimension, and add charts to a dashboard. Refer to [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md) for more information.

## PromQL for metrics [metrics-query-promql]

If you send metrics to Elastic with Prometheus remote write or OTLP, you can query them with PromQL in {{es}}. You can reuse existing Prometheus queries and alerting rules as long as they use supported PromQL. Metric names are schema-dependent, so they reflect the ingest path you used.

{{es}} implements a subset of PromQL functions for rates, range aggregations, and math. Some constructs are not evaluated yet and return a client error. Refer to [PromQL functions](elasticsearch://reference/query-languages/promql/functions.md) for the function list, and [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md) for unsupported constructs and differences from upstream Prometheus.

If you use Grafana, point its built-in Prometheus data source at the {{es}} `/_prometheus/` API. Grafana treats {{es}} like any other Prometheus backend: dashboard panels, autocompletion, and template variables run PromQL against metrics in {{es}}. Refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md) for more information.

## Related [metrics-query-related]

- [Explore metrics](/solutions/observability/metrics/explore.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
