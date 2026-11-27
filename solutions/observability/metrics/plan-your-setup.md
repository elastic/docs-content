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

Before you ingest metrics at scale, decide on two things: the data model your metrics are stored in, and the ingest path for your deployment type. Elastic doesn't convert metrics between schemas at ingest, so the ingest path you use determines how your data is stored, which field names you query, and which prebuilt dashboards work.

## Choose a data model [metrics-plan-data-model]

The data model is the schema your metrics are stored with: the naming conventions that determine your metric and field names. Use the OpenTelemetry schema unless you need existing Elastic Common Schema (ECS) integrations, dashboards, and alerts to keep working without customization. For that and other use cases where ECS might work better, refer to [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

**OpenTelemetry (OTel) schema**
:   Metrics follow the OpenTelemetry semantic conventions, for example the metric `system.cpu.utilization`, with attributes stored under `attributes.*` and `resource.attributes.*`. This is the default. It matches the OpenTelemetry ecosystem and the {{edot}} ingest paths.

**Elastic Common Schema (ECS)**
:   Metrics follow Elastic's original field naming conventions, for example `system.cpu.user.pct`. {{agent}} integrations write this schema, as does [{{metricbeat}}](beats://reference/metricbeat/index.md), the standalone {{beats}} shipper for metrics. Use ECS when you need existing ECS integrations, dashboards, and alerts to keep working without customization.

**Prometheus names**
:   Prometheus remote write uses neither schema. It stores Prometheus metric and label names as they arrive, for example the metric `node_cpu_seconds_total`, with labels stored under `labels.*`. You get this data model when you keep Prometheus and add Elastic as a remote write target.

Use one schema. Mixing OpenTelemetry and ECS in one deployment works, but requires two sets of field names in your queries and dashboards.

### How each ingest path stores metrics [metrics-plan-ingest-path-storage]

| Ingest path | Stored as | Metric values and labels |
|---|---|---|
| Managed OTLP Endpoint, {{agent}} configured as an OTel Collector gateway, {{es}} OTLP/HTTP endpoint | OpenTelemetry-native | `metrics.<metric_name>`, with OpenTelemetry attributes under `attributes.*` and `resource.attributes.*`, in `metrics-*.otel-*` data streams |
| {{agent}} integrations, {{metricbeat}}, Beat receivers | ECS | ECS field names, for example `system.cpu.user.pct`, in the integration's data streams |
| {{apm-server-or-mis}} OTLP intake (the `.apm` endpoint) | ECS | Legacy path that translates OTLP data to ECS. Not recommended for new setups. |
| Prometheus remote write (Managed Prometheus Remote Write endpoint or {{es}} endpoint) | Prometheus names, unchanged | `metrics.<metric_name>`, with labels as `labels.<label_name>` dimensions, in `metrics-*.prometheus-*` data streams. No conversion to OpenTelemetry or ECS. |

For the OpenTelemetry Protocol (OTLP) paths, refer to [How your ingest path determines the data format](opentelemetry://reference/compatibility/data-streams.md#ingest-path-data-format). For Prometheus remote write, refer to [Data mapping](/manage-data/data-store/data-streams/tsds-ingest-prometheus-remote-write.md#data-mapping).

### Implications of your choice [metrics-plan-data-model-implications]

The schema you choose affects how you ingest, which metric names you query, and which dashboards work without customization:

| Aspect | OTel schema | ECS |
|---|---|---|
| **Ingest using** | EDOT SDKs, any OTLP-compatible client, {{agent}} configured as an OTel Collector | {{agent}} integrations, {{metricbeat}} |
| **Metric names** | OpenTelemetry semantic conventions (`system.cpu.utilization`) | ECS (`system.cpu.user.pct`) |
| **Prebuilt dashboards** | OpenTelemetry content packs from the {{kib}} {{integrations}} UI | {{agent}} integration dashboards |
| {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga` **PromQL support** | Yes | Yes, when the integration stores data as a time series data stream (TSDS) |
| **Recommended for** | Default | Existing ECS integrations, dashboards, and alerts |

Prometheus remote write isn't in the table because it isn't a schema you choose: metrics ingested that way always keep their Prometheus names.

PromQL support depends on storage, not schema. {{es}} evaluates PromQL over any TSDS matched by `metrics-*`, whichever ingest path filled it. OTLP and Prometheus remote write metrics always land in a TSDS. {{agent}} integration data streams are a TSDS when the integration enables it. Refer to the [PromQL reference](elasticsearch://reference/query-languages/promql.md) for how {{es}} evaluates PromQL.

## Choose an ingest path [metrics-plan-ingest-path]

Your deployment type determines the recommended path. Use {{agent}} integrations instead of the recommended path only when you need ECS.

| Deployment | Recommended path | Also available |
|---|---|---|
| {{serverless-full}} | Managed OTLP Endpoint | - Managed Prometheus Remote Write endpoint<br>- {{agent}} integrations |
| {{ech}} | Managed OTLP Endpoint | - Managed Prometheus Remote Write endpoint {applies_to}`stack: ga 9.4+`<br>- {{agent}} integrations |
| Self-managed {{stack}}, {{ece}}, {{eck}} | {{agent}} configured as an OTel Collector gateway | - {{es}} OTLP/HTTP endpoint {applies_to}`stack: ga 9.2+`<br>- {{es}} Prometheus remote write endpoint {applies_to}`stack: ga 9.5+, preview =9.4`<br>- {{agent}} integrations |

For configuration details for each path, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).
