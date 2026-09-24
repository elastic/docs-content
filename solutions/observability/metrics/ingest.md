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

Send metrics to Elastic over the OpenTelemetry Protocol (OTLP), with Prometheus remote write, or with {{agent}} integrations. Use OTLP unless one of these constraints applies:

- You need existing Elastic Common Schema (ECS) integrations, dashboards, and alerts to keep working without customization: use {{agent}} integrations.
- Prometheus already scrapes the metrics you need: keep it and add Prometheus remote write.

For the other cases where classic Elastic components, such as {{agent}} integrations, {{metricbeat}}, and Elastic APM agents, still work better, refer to [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

## Ingest with OpenTelemetry (recommended) [metrics-ingest-otlp]

You don't need {{edot}} to send OpenTelemetry metrics. Any OTLP-compatible SDK or Collector can send to the endpoints in this section. {{edot}} is the distribution that Elastic supports and recommends, and the [quickstarts](/solutions/observability/metrics/get-started.md) use it. The endpoint depends on your deployment type.

:::::{applies-switch}

::::{applies-item} { serverless:, ech: }
Send metrics to the Managed OTLP Endpoint. Use a different setup depending on the telemetry you collect:

- **Application metrics:** Point your EDOT SDKs or any OTLP-compatible exporter directly at the endpoint. No {{agent}} required.
- **Infrastructure metrics (host, {{k8s}}, Docker):** Run {{agent}} in OTel mode on your hosts or cluster and configure its OTLP exporter to send data to the endpoint.

{{es}} doesn't expose an OTLP endpoint of its own on {{serverless-full}} or {{ech}}. For authentication, endpoint URL, and protocol details, refer to [Managed OTLP Endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).
::::

::::{applies-item} { self:, ece:, eck: }
Run {{agent}} in OTel mode as a gateway. The Managed OTLP Endpoint isn't available for self-managed {{stack}}, {{ece}}, or {{eck}} deployments. The gateway exposes an OTLP endpoint that your EDOT SDKs and edge collectors send to, and it writes to {{es}} with the `elasticsearch` exporter. For gateway versus edge setup, refer to [{{agent}} deployment modes](elastic-agent://reference/edot-collector/modes.md).

{applies_to}`self: ga 9.2+` {applies_to}`ece: ga` {applies_to}`eck: ga` {{es}} also accepts OTLP/HTTP directly on `/_otlp/v1/metrics`. Use it when an application exports OTLP natively and you don't want to run a Collector. Metrics land in a time series data stream (TSDS) through built-in index templates. Refer to [Ingest metrics into a TSDS using the OTLP/HTTP endpoint](/manage-data/data-store/data-streams/tsds-ingest-otlp.md) and [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md).
::::

:::::

For language SDK setup, refer to [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md).

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` For how counters and histograms behave after ingest, refer to [Metric temporality](/manage-data/data-store/data-streams/metric-temporality.md).

## Ingest with {{agent}} integrations [metrics-ingest-agent-integrations]

Use {{agent}} integrations to collect metrics from specific infrastructure components and services: system metrics from hosts, {{k8s}} cluster metrics, or metrics from services such as Nginx, PostgreSQL, or Redis. {{integrations}} store ECS documents and send them to the output you configure in {{fleet}}, the {{kib}} app that manages {{agent}} policies. That output is {{es}} by default. You don't send this data through the Managed OTLP Endpoint, and you don't convert it to OTLP.

Use this path when you need existing ECS integrations, dashboards, and alerts to keep working without customization. To collect host metrics this way, follow [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md). To find which services have a prebuilt integration, browse the [{{integrations}} catalog](https://www.elastic.co/integrations).

### ECS and OpenTelemetry integration tiles [metrics-ingest-agent-integrations-otel]
```{applies_to}
stack: preview 9.2+
serverless: preview
```

Some services have two tiles in the {{kib}} {{integrations}} UI, for example **Nginx** and **Nginx (OpenTelemetry)**. The **(OpenTelemetry)** tile is an OpenTelemetry input package: a {{fleet}}-managed {{agent}} runs the matching OTel Collector receiver, stores the data with OpenTelemetry semantic conventions, and {{kib}} installs the matching OpenTelemetry content pack with dashboards. The other tile is the ECS integration.

Pick the ECS tile when you need the integration's ECS dashboards and alerts. Pick the OpenTelemetry tile when you standardize on the OpenTelemetry schema and manage agents with {{fleet}}. OpenTelemetry input packages run only on {{agent}} in default mode, not on {{agent}} in OTel mode. Refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md).

### {{metricbeat}} [metrics-ingest-metricbeat]

{{metricbeat}} is the standalone {{beats}} shipper for metrics. It writes ECS documents and isn't deprecated, but new setups use {{agent}}: in OTel mode for the OpenTelemetry schema, or with integrations for ECS. If you already run {{metricbeat}}, refer to [Move from {{metricbeat}} or {{agent}} integrations](/solutions/observability/metrics/migrate.md#metrics-migrate-metricbeat).

### {{ls}} [metrics-ingest-logstash]

If your {{agent}} integrations already send through {{ls}}, keep that setup by using the {{fleet}} [{{ls}} output](/reference/fleet/logstash-output.md). OTLP and Prometheus remote write don't pass through {{ls}}: {{agent}} in OTel mode has no {{ls}} exporter, and {{ls}} has no OTLP or remote write input.

## Ingest Prometheus metrics [metrics-ingest-prometheus]

Elastic accepts Prometheus metrics in three ways:

- **Prometheus remote write.** Recommended when Prometheus already scrapes your targets. Add a `remote_write` target and keep your scrape configurations unchanged. Any client that sends Prometheus remote write 1.0 works, including Prometheus and Grafana Alloy. Keep clients on remote write 1.0: the endpoint accepts 2.0 requests but discards their samples without returning an error. Metrics keep their Prometheus names and land in a TSDS.
- **OpenTelemetry Collector.** Scrape targets with the `prometheus` receiver in {{agent}} in OTel mode or another Collector, and export OTLP to the endpoints in [Ingest with OpenTelemetry](#metrics-ingest-otlp). Use this when you're retiring Prometheus rather than keeping it. The Collector's `prometheusremotewrite` exporter also works against the remote write endpoint, but it rewrites metric names with Prometheus suffixes and underscores, and the endpoint drops the native histograms it produces for OpenTelemetry exponential histograms. Use it only when you can't change the exporter.
- **{{agent}} Prometheus integration.** Scrapes exporters or a Prometheus server's federation endpoint, receives remote write on the agent, or runs PromQL queries against a Prometheus server. It stores ECS documents under `prometheus.*` and isn't deprecated. Use it when you need the ECS schema or {{fleet}} management. Refer to the [Prometheus integration](https://www.elastic.co/docs/reference/integrations/prometheus).

Not supported: {{es}} doesn't implement Prometheus remote read or the federation endpoint, and the Managed OTLP Endpoint and {{apm-server-or-mis}} don't accept remote write.

The remote write endpoint depends on your deployment:

:::::{applies-switch}

::::{applies-item} { serverless:, ech: }
Use the [Managed Prometheus Remote Write endpoint](opentelemetry://reference/managed-inputs/prometheus-remote-write.md). Managed inputs, the endpoints {{ecloud}} runs for you, provide durable buffering, unified authentication, and back-pressure handling before data reaches {{es}}. Sending remote write traffic directly to the {{es}} endpoint bypasses that.

{applies_to}`stack: ga 9.4+` Available for {{ech}} deployments.
::::

::::{applies-item} { self:, ece:, eck: }
{applies_to}`stack: preview =9.4, ga 9.5+` Send remote write traffic to the {{es}} `/_prometheus/api/v1/write` endpoint. Managed inputs aren't available on these deployments. For the URL, authentication, Grafana Alloy configuration, and data stream routing, refer to [Prometheus remote write endpoint](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md).
::::

:::::

For the side-by-side ingest sequence and how to switch over, refer to [Migrate metrics to Elastic](/solutions/observability/metrics/migrate.md#metrics-migrate-prometheus).

## Related pages [metrics-ingest-related]

- [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md)
- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
