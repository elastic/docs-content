---
navigation_title: Migrate to Elastic
description: Migration paths for moving your existing Prometheus or Datadog metrics stack to Elastic.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate to Elastic metrics [metrics-migrate]

:::{note}
This section is in progress. Detailed migration guides for Prometheus and Datadog are coming soon.
:::

Elastic supports migration paths from Prometheus and Datadog. Because Elastic speaks OTLP and supports Prometheus remote write natively, you can often run Elastic in parallel with your existing stack and migrate incrementally — without a hard cutover.

## Prometheus migration [metrics-migrate-prometheus]

If you're running Prometheus today, you can start sending metrics to Elastic with a four-line change to your `prometheus.yml`. Your existing scrape configs and alerting rules continue to work during and after the migration.

- To send metrics from Prometheus to Elastic: [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md)
- To run existing PromQL dashboards in Grafana against Elastic: [Use {{es}} as a Prometheus data source in Grafana](/reference/query-languages/promql/promql-grafana.md)
- To query metrics in Elastic using PromQL: [PromQL in {{es}}](/reference/query-languages/promql/functions.md)

## Datadog migration [metrics-migrate-datadog]

Content coming soon. Contact your Elastic account team for guidance on Datadog migration planning.

## Related [metrics-migrate-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Query metrics](/solutions/observability/metrics/query.md)
