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

If you're running Prometheus today, you can start sending metrics to Elastic while your existing scrape configurations and alerting rules continue to work.

:::::::{stepper}

::::::{step} Send samples to Elastic
:anchor: metrics-migrate-prometheus-remote-write

Add a remote write target so Prometheus also sends samples to Elastic. The configuration depends on your deployment.

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

For the endpoint URL, authentication, and how to route metrics to different data streams, refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).
::::

::::{applies-item} serverless: ga
Use [managed inputs](opentelemetry://reference/managed-inputs/prometheus-remote-write.md) to send Prometheus metrics. Managed inputs provide durable buffering, unified authentication, and back-pressure handling.
::::

:::::

::::::

::::::{step} Query and visualize
:anchor: metrics-migrate-prometheus-visualize

After samples are in Elastic, you can keep your existing Grafana dashboards and PromQL.

If you use Grafana and want to keep doing so, point it at {{es}} as a Prometheus data source. Grafana treats {{es}} like any other Prometheus backend, so existing dashboards and template variables keep working. For the data source URL and authentication, refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md).

To query those metrics with PromQL in Elastic, refer to [PromQL in {{es}}](elasticsearch://reference/query-languages/promql/functions.md).
::::::

:::::::

## Datadog migration [metrics-migrate-datadog]

If your Datadog agents already export OpenTelemetry data, point them at Elastic using the same OTLP paths as any other OTel client. For the endpoint and gateway options by deployment type, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).

## Related pages [metrics-migrate-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Query metrics](/solutions/observability/metrics/query.md)
