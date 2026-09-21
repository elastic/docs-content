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

## Before you begin [metrics-migrate-prereqs]

You need:

- An Elastic deployment that can ingest metrics.
- An API key for the ingest path you use. Managed inputs authenticate with the `event:write` privilege for the `apm` application. The {{es}} remote write endpoint authenticates with an API key that can ingest metrics.
- Your existing Prometheus or Datadog pipeline left running. Send data to both systems until you have rebuilt the queries, dashboards, and alerts you rely on.

## Prometheus migration [metrics-migrate-prometheus]

If you're already running Prometheus, you can start sending metrics to Elastic while your existing scrape configurations and alerting rules continue to work. Grafana Alloy and other Prometheus remote write clients use the same endpoint.

:::::::{stepper}

::::::{step} Send samples to Elastic
:anchor: metrics-migrate-prometheus-remote-write

Add a remote write target so Prometheus also sends samples to Elastic. The endpoint depends on your deployment.

:::::{applies-switch}

::::{applies-item} serverless: ga
Use the Managed Prometheus Remote Write endpoint. In the Elastic Cloud Console, open your project, select **Manage**, then copy the **Prometheus** endpoint. Authenticate with an API key that has the `event:write` privilege for the `apm` application.

```yaml
remote_write:
  - url: "<prometheus-endpoint>"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<prometheus-endpoint>` with the value you copied and `<api_key>` with that API key.

Managed inputs provide durable buffering, unified authentication, and back-pressure handling. URL-path routing to custom data streams is not supported on this endpoint. Use label-based routing instead. For authentication, routing labels, and limitations, refer to [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md).
::::

::::{applies-item} ech:
```{applies_to}
stack: ga 9.4+
```

Use the Managed Prometheus Remote Write endpoint. In the Elastic Cloud Console, open your deployment, select **Manage**, then copy the **Prometheus** endpoint. Authenticate with an API key that has the `event:write` privilege for the `apm` application.

On {{ech}}, use this endpoint rather than sending remote write traffic directly to {{es}}. Direct ingest has no buffering before data reaches {{es}}, and it authenticates with {{es}} index privileges instead of the managed-inputs API key.

```yaml
remote_write:
  - url: "<prometheus-endpoint>"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<prometheus-endpoint>` with the value you copied and `<api_key>` with that API key.

For authentication, routing labels, and limitations, refer to [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md).
::::

::::{applies-item} { self:, ece:, eck: }
The Managed Prometheus Remote Write endpoint is not available. Send remote write traffic to {{es}} directly.

```{applies_to}
stack: ga 9.5+, preview =9.4
```

Add this block to `prometheus.yml`:

```yaml
remote_write:
  - url: "https://<es_endpoint>/_prometheus/api/v1/write"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<es_endpoint>` with your {{es}} URL and `<api_key>` with an API key that can ingest metrics.

For the endpoint URL, authentication, Grafana Alloy configuration, and how to route metrics to different data streams, refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).
::::

:::::

By default, samples land in the `metrics-generic.prometheus-default` data stream. Prometheus metric names become `metrics.<metric_name>` fields, and labels become `labels.<label_name>` dimensions. PromQL continues to use the original Prometheus names. {{esql}} uses the {{es}} field names. For the mapping table, refer to [Data mapping](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#data-mapping).

Grafana Alloy and other Prometheus remote write clients send to the same URL you configured in this step. For an Alloy example that targets the {{es}} endpoint, refer to [From Grafana Alloy](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#from-grafana-alloy). On {{serverless-full}} and {{ech}}, use the managed Prometheus endpoint as the URL instead.
::::::

::::::{step} Query and visualize
:anchor: metrics-migrate-prometheus-visualize

After samples are in Elastic, you can keep your existing Grafana dashboards and PromQL.

If you use Grafana and want to keep doing so, point it at {{es}} as a Prometheus data source. Grafana treats {{es}} like any other Prometheus backend, so existing dashboards and template variables keep working as long as they use supported PromQL. For the data source URL and authentication, refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md). For constructs {{es}} does not evaluate yet, refer to [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md).

To query those metrics with PromQL in Elastic, or with {{esql}} time-series mode, refer to [Query metrics](/solutions/observability/metrics/query.md).
::::::

::::::{step} Recreate alerts
:anchor: metrics-migrate-prometheus-alerts

Prometheus Alertmanager rules do not import into Elastic. After you can query the same time series in Elastic, recreate the alerts you still need.

If your alerts already run in Grafana against Prometheus, point those alert rules at the {{es}} Prometheus data source after you switch the dashboards. Confirm each expression against [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md) before you stop alerting against Prometheus.

To alert in Elastic, create a [custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md) on the metrics data view. For host, pod, and similar resource checks, use an [inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md). For the full list of {{observability}} rule types, refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md).
::::::

:::::::

## Datadog migration [metrics-migrate-datadog]

Elastic does not ingest the Datadog Agent's proprietary metrics protocol. You migrate by sending OpenTelemetry data to Elastic, or by replacing Datadog Agent collection with {{edot}} or {{agent}} integrations. Keep Datadog running until the Elastic queries and alerts match what you need, then stop the duplicate stream.

Pick the path that matches how you collect metrics today.

### Retarget applications that already emit OTLP [metrics-migrate-datadog-otlp]

If your services already export OTLP, retarget those exporters at Elastic. Change `OTEL_EXPORTER_OTLP_ENDPOINT` (and the authentication headers) to the Managed OTLP endpoint or an {{agent}} gateway, using the same settings as any other OTLP client.

The Datadog Agent can receive OTLP from your applications for Datadog. That ingest path does not forward the same telemetry to Elastic. Point the applications, or a collector in front of them, at Elastic.

For the endpoint and gateway options by deployment type, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md#metrics-ingest-otlp).

### Send the same metrics from an OpenTelemetry Collector [metrics-migrate-datadog-collector]

If a collector already receives your metrics and exports them to Datadog, add Elastic as a second exporter and send the same metrics to both backends. Keep the Datadog exporter until you have validated Elastic queries and alerts.

Any OpenTelemetry Collector distribution can do this, including vendor distributions. On {{ecloud}}, add an `otlp` exporter that points at the Managed OTLP endpoint. On self-managed {{stack}}, forward OTLP to an {{agent}} gateway.

For the Elastic OTLP destination, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md#metrics-ingest-otlp). For the self-managed gateway pattern, refer to [Send data from an upstream OpenTelemetry Collector](/solutions/observability/get-started/opentelemetry/use-cases/upstream-collector/index.md).

### Replace Datadog Agent host and Kubernetes collection [metrics-migrate-datadog-infra]

Checks that the Datadog Agent scrapes itself, such as host CPU and memory or Kubernetes state, are Datadog-native, not OTLP. To bring those metrics into Elastic, collect them with Elastic instead of forwarding the Datadog Agent.

For the OpenTelemetry schema, follow an {{edot}} quickstart for your hosts or cluster: [Get started with metrics](/solutions/observability/metrics/get-started.md). For ECS field names and existing Elastic integrations, use {{agent}} integrations: [Ingest with {{agent}} integrations](/solutions/observability/metrics/ingest.md#metrics-ingest-agent-integrations).

### Recreate dashboards and monitors [metrics-migrate-datadog-assets]

Datadog dashboards and monitors do not import into Elastic. After metrics are in Elastic, rebuild the views and alerts you still need:

- Explore and chart the new field names in **Discover**, the Infrastructure UI, or {{kib}} Lens. Refer to [Explore metrics](/solutions/observability/metrics/explore.md).
- Recreate monitors with a [custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md), or with an [inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md) for resource-centric checks.

Metric names and tags from Datadog do not match OpenTelemetry semantic conventions or ECS one-for-one. Confirm each chart and rule against the fields you ingested before you stop Datadog.

## Related pages [metrics-migrate-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Query metrics](/solutions/observability/metrics/query.md)
- [Explore metrics](/solutions/observability/metrics/explore.md)
- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
