---
navigation_title: Migrate from Prometheus
description: Migrate from Prometheus to Elastic. Add a remote write target, explore metrics in Kibana while Grafana keeps working, and recreate alerts before switching over.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate from Prometheus [metrics-migrate-prometheus]

If you're already running Prometheus, you can start sending metrics to Elastic while your existing scrape configurations and alerting rules continue to work. Grafana Alloy and other Prometheus remote write clients use the same endpoint.

## Before you begin [metrics-migrate-prereqs]

:::{include} /solutions/observability/metrics/_snippets/migrate-prereqs.md
:::

## Migration steps [metrics-migrate-prometheus-steps]

:::::::{stepper}

::::::{step} Send samples to Elastic
:anchor: metrics-migrate-prometheus-remote-write

Add a remote write target so Prometheus also sends samples to Elastic. The endpoint depends on your deployment.

:::::{applies-switch}

::::{applies-item} serverless:
Use the Managed Prometheus Remote Write endpoint. In the {{ecloud}} Console, open your project, select **Manage**, then under **Application endpoints, cluster and component IDs** select **Prometheus** and copy the endpoint. Authenticate with an API key that has the `event:write` privilege for the `apm` application.

```yaml
remote_write:
  - url: "<prometheus-endpoint>"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<prometheus-endpoint>` with the value you copied and `<api_key>` with that API key.

Managed inputs provide durable buffering, unified authentication, and back-pressure handling. URL-path routing to custom data streams isn't supported on this endpoint. Use label-based routing instead. For authentication, routing labels, and limitations, refer to [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md).
::::

::::{applies-item} ech:
{applies_to}`stack: ga 9.4+` Use the Managed Prometheus Remote Write endpoint. In the {{ecloud}} Console, open your deployment, select **Manage**, then under **Application endpoints, cluster and component IDs** select **Prometheus** and copy the endpoint. Authenticate with an API key that has the `event:write` privilege for the `apm` application.

```yaml
remote_write:
  - url: "<prometheus-endpoint>"
    authorization:
      type: ApiKey
      credentials: <api_key>
```

Replace `<prometheus-endpoint>` with the value you copied and `<api_key>` with that API key.

Managed inputs provide durable buffering, unified authentication, and back-pressure handling. URL-path routing to custom data streams isn't supported on this endpoint. Use label-based routing instead. For authentication, routing labels, and limitations, refer to [Ingest Prometheus metrics with the Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md).

Use this endpoint rather than sending remote write traffic directly to {{es}}, which bypasses the buffering and back-pressure handling that managed inputs provide.
::::

::::{applies-item} { self:, ece:, eck: }
{applies_to}`stack: ga 9.5+, preview =9.4` The Managed Prometheus Remote Write endpoint isn't available. Send remote write traffic to {{es}} directly by adding this block to `prometheus.yml`:

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

To confirm that samples are arriving, open **{{index-manage-app}}** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), select the **Data Streams** tab, and check that the data stream exists and its storage size grows as Prometheus sends samples.
::::::

::::::{step} Query and visualize
:anchor: metrics-migrate-prometheus-visualize

After samples are in Elastic, explore and visualize the metrics in {{kib}}. Your existing Grafana dashboards can keep working while you migrate.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` In {{kib}}, run {{esql}} time-series queries over the migrated metrics, browse them in the **Discover** chart grid, and add charts to dashboards. For the query languages and the Discover workflow, refer to [Explore metrics](/solutions/observability/metrics/explore.md#metrics-query).

{applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga` To keep using PromQL, query the metrics with the `PROMQL` {{esql}} command or the Prometheus-compatible API. If you use Grafana, point it at {{es}} as a Prometheus data source. Grafana treats {{es}} like any other Prometheus backend, so existing dashboards and template variables keep working as long as they use supported PromQL. For the data source URL and authentication, refer to [Use {{es}} as a Prometheus data source in Grafana](elasticsearch://reference/query-languages/promql/promql-grafana.md). For constructs {{es}} doesn't support, refer to [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md).
::::::

::::::{step} Recreate alerts
:anchor: metrics-migrate-prometheus-alerts

Elastic has no built-in import for Prometheus Alertmanager rules. After you can query the same time series in Elastic, recreate the alerts you still need.

If your alerts already run in Grafana against Prometheus, point those alert rules at the {{es}} Prometheus data source after you switch the dashboards. Confirm each expression against [PromQL limitations](elasticsearch://reference/query-languages/promql/promql-limitations.md) before you stop alerting against Prometheus.

To alert in Elastic, create a [custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md) on the metrics data view. For host, pod, and similar resource checks, use an [inventory rule](/solutions/observability/incident-management/create-an-inventory-rule.md). For the full list of {{observability}} rule types, refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md).
::::::

:::::::
