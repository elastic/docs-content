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

Elastic supports migration paths from Prometheus and Datadog. Because Elastic accepts OpenTelemetry Protocol (OTLP) and Prometheus remote write, you can run Elastic alongside your existing setup and migrate gradually, without switching everything at once.

## Prometheus migration [metrics-migrate-prometheus]

If you're running Prometheus today, you can start sending metrics to Elastic, with your existing scrape configurations and alerting rules continuing to work. Add a remote write target so Prometheus also sends samples to Elastic:

:::::{applies-switch}

::::{applies-item} stack: ga 9.5+, preview =9.4
Add this block to `prometheus.yml`:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/api/v1/write"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<es_endpoint>` with your {{es}} URL and `<api_key>` with an API key that can ingest metrics.

Refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md) for more information, including how to route metrics to different data streams.
::::

::::{applies-item} serverless: ga
Use [managed inputs](opentelemetry://reference/motlp/prometheus-remote-write.md) to send Prometheus metrics. Managed inputs provide durable buffering, unified authentication, and back-pressure handling.
::::

:::::

If you're using Grafana and want to keep doing so, point it at {{es}} as a Prometheus data source. Refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md) for more information.

To query those metrics with PromQL in Elastic, refer to [PromQL in {{es}}](elasticsearch://reference/query-languages/promql/functions.md) for more information.

## Datadog migration [metrics-migrate-datadog]

Coming soon

## Related [metrics-migrate-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Query metrics](/solutions/observability/metrics/query.md)
