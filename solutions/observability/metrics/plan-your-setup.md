---
navigation_title: Plan your setup
description: Understand how each metrics ingest path stores data, when to use the OpenTelemetry or ECS data model, and which ingest path fits your deployment type.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Plan your metrics setup [metrics-plan-your-setup]

Before you ingest metrics at scale, decide on two things: the data model your metrics are stored in, and the ingest path for your deployment type. The two are linked. Elastic doesn't convert metrics between schemas at ingest, so the ingest path you use determines how your data is stored, which field names you query, and which prebuilt dashboards work.

## Choose a data model [metrics-plan-data-model]

Use the OpenTelemetry schema unless you need existing Elastic Common Schema (ECS) integrations, dashboards, and alerts to keep working without customization. That constraint, and the other cases where classic Elastic components still work better, are listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

**OpenTelemetry (OTel) schema**
:   Metrics follow the OpenTelemetry semantic conventions, for example the metric `system.cpu.utilization`, with attributes stored under `attributes.*` and `resource.attributes.*`. This is the default. It matches the OpenTelemetry ecosystem and the {{edot}} ingest paths.

**ECS**
:   Metrics follow Elastic's original field naming conventions, for example `system.cpu.user.pct`. {{agent}} integrations write this schema, as does [{{metricbeat}}](beats://reference/metricbeat/index.md), the standalone {{beats}} shipper for metrics. Use ECS when you need existing ECS integrations, dashboards, and alerts to keep working without customization.

Prefer one schema. Mixing them in one deployment works, but it means two sets of field names in your queries and dashboards.

Prometheus remote write is neither schema: it stores Prometheus metric and label names as they arrive.

### How each ingest path stores metrics [metrics-plan-ingest-path-storage]

| Ingest path | Stored as | Metric values and labels |
|---|---|---|
| Managed OTLP Endpoint, {{agent}} in OTel mode as a gateway, {{es}} OTLP/HTTP endpoint | OpenTelemetry-native | `metrics.<metric_name>`, with OpenTelemetry attributes under `attributes.*` and `resource.attributes.*`, in `metrics-*.otel-*` data streams |
| {{agent}} integrations, {{metricbeat}}, Beat receivers | ECS | ECS field names, for example `system.cpu.user.pct`, in the integration's data streams |
| {{apm-server-or-mis}} OTLP intake (the `.apm` endpoint) | ECS | Legacy path that translates OTLP data to ECS. Not recommended for new setups. |
| Prometheus remote write (Managed Prometheus Remote Write endpoint or {{es}} endpoint) | Prometheus names, unchanged | `metrics.<metric_name>`, with labels as `labels.<label_name>` dimensions, in `metrics-*.prometheus-*` data streams. No conversion to OpenTelemetry or ECS. |

For the OpenTelemetry Protocol (OTLP) paths, refer to [OpenTelemetry data streams compared to classic {{product.apm}} and ECS-based integrations](opentelemetry://reference/compatibility/data-streams.md). For Prometheus remote write, refer to [Data mapping](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#data-mapping).

### Implications of your choice [metrics-plan-data-model-implications]

The schema you end up with affects how you ingest, which metric names you query, and which dashboards work without customization:

| Aspect | OTel schema | ECS schema |
|---|---|---|
| **Ingest using** | EDOT SDKs, any OTLP-compatible client, {{agent}} in OTel mode | {{agent}} integrations, {{metricbeat}} |
| **Metric names** | OpenTelemetry semantic conventions (`system.cpu.utilization`) | ECS (`system.cpu.user.pct`) |
| **Prebuilt dashboards** | OpenTelemetry content packs from the {{kib}} {{integrations}} UI | {{agent}} integration dashboards |
| **PromQL support** {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | Yes | Yes, when the integration stores data as a time series data stream (TSDS) |
| **Recommended for** | Default | Existing ECS integrations, dashboards, and alerts |

PromQL support depends on storage, not schema. {{es}} evaluates PromQL over any TSDS matched by `metrics-*`, whichever ingest path filled it. OTLP and Prometheus remote write metrics always land in a TSDS. {{agent}} integration data streams are a TSDS when the integration enables it. Refer to the [PromQL reference](elasticsearch://reference/query-languages/promql.md).

## Choose an ingest path [metrics-plan-ingest-path]

Your deployment type determines the recommended path. Use {{agent}} integrations instead of the recommended path only when you need the ECS schema.

| Deployment | Recommended path | Also available |
|---|---|---|
| {{serverless-full}} | Managed OTLP Endpoint | Managed Prometheus Remote Write endpoint, {{agent}} integrations |
| {{ech}} | Managed OTLP Endpoint | Managed Prometheus Remote Write endpoint {applies_to}`stack: ga 9.4+`, {{agent}} integrations |
| Self-managed {{stack}}, {{ece}}, {{eck}} | {{agent}} in OTel mode as a gateway | {{es}} OTLP/HTTP endpoint {applies_to}`self: ga 9.2+` {applies_to}`ece: ga` {applies_to}`eck: ga`, {{es}} Prometheus remote write endpoint {applies_to}`stack: preview =9.4, ga 9.5+`, {{agent}} integrations |

For configuration details for each path, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).

## Related pages [metrics-plan-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Get started with metrics](/solutions/observability/metrics/get-started.md)
- [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic)
