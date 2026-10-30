---
navigation_title: Ingest metrics
description: Send metrics to Elastic using OpenTelemetry, Prometheus remote write, or Elastic Agent integrations, with the recommended path for each deployment type.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Ingest metrics [metrics-ingest]

You can send metrics to Elastic over the OpenTelemetry Protocol (OTLP), with {{agent}} integrations, or with Prometheus remote write:

- [**OTLP**](#metrics-ingest-otlp): Recommended in most cases.
- [**{{agent}} integrations**](#metrics-ingest-agent-integrations): Use when you need existing Elastic Common Schema (ECS) integrations, dashboards, and alerts to keep working without customization.
- [**Prometheus metrics**](#metrics-ingest-prometheus): Use when Prometheus already scrapes the metrics you need.

To understand when classic Elastic components, such as {{agent}} integrations, {{metricbeat}}, and Elastic APM agents, are a better fit, refer to [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

## Ingest with OpenTelemetry (recommended) [metrics-ingest-otlp]

Elastic supports and recommends using the {{edot}} distribution to send your metric data to {{es}}, and the [quickstarts](/solutions/observability/metrics/get-started.md) use it. The endpoint you send data to depends on your deployment type.

:::::{applies-switch}

::::{applies-item} serverless:
Send metrics to the Managed OTLP Endpoint. Use the setup that matches the source of your metrics:

- **Application metrics:** Point your [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md) or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics (host, {{k8s}}, Docker):** Run {{agent}} configured as an OTel Collector on your hosts or cluster and point its OTLP exporter at the endpoint. The [quickstarts](/solutions/observability/metrics/get-started.md#metrics-get-started-quickstart) set this up for you. For the exporter and pipeline configuration, refer to [Using the Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-standalone.md#using-the-managed-otlp-endpoint).

The {{es}} OTLP endpoint isn't a supported ingest path on {{serverless-full}}: use the Managed OTLP Endpoint instead. For authentication, endpoint URL, and protocol details, refer to [Managed OTLP Endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).
::::

::::{applies-item} ech:
Send metrics to the Managed OTLP Endpoint. Use the setup that matches the source of your metrics:

- **Application metrics:** Point your [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md) or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics (host, {{k8s}}, Docker):** Run {{agent}} configured as an OTel Collector on your hosts or cluster and point its OTLP exporter at the endpoint. The [quickstarts](/solutions/observability/metrics/get-started.md#metrics-get-started-quickstart) set this up for you. For the exporter and pipeline configuration, refer to [Using the Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-standalone.md#using-the-managed-otlp-endpoint).

The {{es}} OTLP endpoint isn't a supported ingest path on {{ech}}: use the Managed OTLP Endpoint instead. For authentication, endpoint URL, and protocol details, refer to [Managed OTLP Endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).
::::

::::{applies-item} { self:, ece:, eck: }
Run {{agent}} configured as an OTel Collector gateway. The gateway exposes an OTLP endpoint that your [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md) and edge collectors send to, and it writes to {{es}} with the `elasticsearch` exporter. For gateway versus edge setup, refer to [{{agent}} deployment modes](elastic-agent://reference/edot-collector/modes.md).

The `elasticsearch` exporter drops histograms with cumulative temporality, the default in most OpenTelemetry SDKs. Export histograms with delta temporality, add the `cumulativetodelta` processor to the gateway, or send metrics to `/_otlp`, which accepts both temporalities from 9.5. For temporality support by deployment type, refer to [Histogram and counter temporality](opentelemetry://reference/compatibility/limitations.md#histogram-and-counter-temporality).

{applies_to}`stack: ga 9.2+` {{es}} also accepts OTLP/HTTP on `/_otlp/v1/metrics` from a gateway Collector. Use it when that gateway prefers the OTLP/HTTP exporter over the `elasticsearch` exporter. Don't send applications or pods directly to `/_otlp`. Metrics land in a time series data stream (TSDS) through built-in index templates. Refer to [Ingest metrics into a TSDS using the OTLP/HTTP endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md) for how metrics are stored and to [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) for request details.
::::

:::::

## Ingest with {{agent}} integrations [metrics-ingest-agent-integrations]

Use {{agent}} integrations to collect metrics from specific infrastructure components and services, for example system metrics from hosts, {{k8s}} cluster metrics, or metrics from Nginx, PostgreSQL, or Redis. {{integrations}} store ECS documents and send them to the output you configure in {{fleet}}, where you manage {{agent}} policies in {{kib}}. That output is {{es}} by default. The data doesn't go through the Managed OTLP Endpoint and isn't converted to OTLP.

Use this path when you need existing ECS integrations, dashboards, and alerts to keep working without customization. To collect host metrics this way, follow [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md). To find which services have a prebuilt integration, browse the [{{integrations}} catalog](https://www.elastic.co/integrations).

### ECS and OpenTelemetry integrations [metrics-ingest-agent-integrations-otel]
```{applies_to}
stack: preview 9.2+
serverless: preview
```

Some services have both an ECS integration and an OpenTelemetry integration, for example **Nginx** and **Nginx (OpenTelemetry)**. The **(OpenTelemetry)** integration is an OpenTelemetry input package: a {{fleet}}-managed {{agent}} runs the matching OTel Collector receiver. The integration without **(OpenTelemetry)** is the ECS integration.

| Aspect | ECS integration | OpenTelemetry integration |
|---|---|---|
| **Stores data with** | ECS field names | OpenTelemetry semantic conventions |
| **Prebuilt content** | The integration's ECS dashboards and alerts | Dashboards from the matching OpenTelemetry content pack, which {{kib}} installs |
| **Use when** | You need the integration's ECS dashboards and alerts | You standardize on the OpenTelemetry schema and manage agents with {{fleet}} |

OpenTelemetry input packages run only on {{agent}} in its default mode, not on {{agent}} configured as an OTel Collector. Refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md) for how to set up an OpenTelemetry input package.

### {{metricbeat}} [metrics-ingest-metricbeat]

{{metricbeat}}, the standalone {{beats}} shipper for metrics, writes ECS documents. While it isn't deprecated, we recommend that new setups use {{agent}} instead: configured as an OTel Collector for the OpenTelemetry schema, or with integrations for ECS. If you already run {{metricbeat}}, refer to [Move from {{metricbeat}} or {{agent}} integrations](/solutions/observability/metrics/migrate.md#metrics-migrate-metricbeat) for how to switch to OpenTelemetry.

### {{ls}} [metrics-ingest-logstash]

If your {{agent}} integrations already send through {{ls}}, keep that setup by using the {{fleet}} [{{ls}} output](/reference/fleet/logstash-output.md). {{agent}} configured as an OTel Collector includes a {{ls}} exporter for ECS events produced by [Beat receivers](/reference/fleet/elastic-agent-as-otel-collector.md#beat-receivers), but it doesn't forward OTLP metrics or Prometheus remote write traffic through {{ls}}, and {{ls}} has no OTLP or remote write input.

## Ingest Prometheus metrics [metrics-ingest-prometheus]

Elastic accepts Prometheus metrics in three ways:

- **Prometheus remote write.** Recommended when Prometheus already scrapes your targets. Add a `remote_write` target and keep your scrape configurations unchanged. Any client that sends Prometheus remote write 1.0 works, including Prometheus and Grafana Alloy. Remote write 2.0 is not supported, so configure clients to use 1.0. Metrics keep their Prometheus names and land in a [TSDS](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#index-template).
- **OpenTelemetry Collector.** Scrape targets with the `prometheus` receiver in {{agent}} configured as an OTel Collector, or in another Collector, and export OTLP to the endpoints in [Ingest with OpenTelemetry](#metrics-ingest-otlp). Use this when you're retiring Prometheus rather than keeping it. The Collector's `prometheusremotewrite` exporter also works against the remote write endpoint, but it rewrites metric names with Prometheus suffixes and underscores, and the endpoint drops the native histograms it produces for OpenTelemetry exponential histograms. Use it only when you can't change the exporter.
- **{{agent}} Prometheus integration.** Scrapes exporters or a Prometheus server's federation endpoint, receives remote write on the agent, or runs PromQL queries against a Prometheus server. It stores ECS documents under `prometheus.*` and isn't deprecated. Use it when you need ECS or {{fleet}} management. Refer to the [Prometheus integration](https://www.elastic.co/docs/reference/integrations/prometheus) for setup instructions.

:::{note}
{{es}} doesn't implement Prometheus remote read or the federation endpoint, and the Managed OTLP Endpoint and {{apm-server-or-mis}} don't accept remote write.
:::

The remote write endpoint depends on your deployment:

:::::{applies-switch}

::::{applies-item} serverless:
Use the [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md). Managed inputs, the endpoints {{ecloud}} runs for you, provide durable buffering, unified authentication, and back-pressure handling before data reaches {{es}}. Sending remote write traffic directly to the {{es}} endpoint bypasses that.
::::

::::{applies-item} ech:
{applies_to}`stack: ga 9.4+` Use the [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md). Managed inputs, the endpoints {{ecloud}} runs for you, provide durable buffering, unified authentication, and back-pressure handling before data reaches {{es}}. Sending remote write traffic directly to the {{es}} endpoint bypasses that.
::::

::::{applies-item} { self:, ece:, eck: }
{applies_to}`stack: ga 9.5+, preview =9.4` Send remote write traffic to the {{es}} `/_prometheus/api/v1/write` endpoint. Managed inputs aren't available on these deployments. For the URL, authentication, Grafana Alloy configuration, and data stream routing, refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).
::::

:::::

For the side-by-side ingest sequence and how to switch over, refer to [Migrate from Prometheus](/solutions/observability/metrics/migrate/prometheus.md).

## Next steps [metrics-ingest-next]

After metrics are flowing, [explore and query them](/solutions/observability/metrics/explore.md) in {{kib}}. Metrics volume grows quickly, so [set up storage and retention](/solutions/observability/metrics/manage-storage.md) before your rollout becomes production-critical.
