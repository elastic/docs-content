---
navigation_title: Plan your setup
description: Choose between the OpenTelemetry and ECS data models for metrics, and select the ingest path that matches your deployment type.
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

Before you start ingesting metrics at scale, you need to make two decisions that affect how your data looks in {{es}} and how you query it later: the data model to use, and the ingest path that fits your deployment.

## Choose a data model [metrics-plan-data-model]

Metrics ingested into Elastic can follow one of two schemas:

**OpenTelemetry (OTel) schema**
:   Metrics are stored under the OTel semantic conventions (for example, `system.cpu.utilization` instead of `system.cpu.pct`). This schema is the recommended default. It matches the OpenTelemetry ecosystem and the {{edot}} ingest path, gives you maximum compatibility with the OTel ecosystem and positions you well for future Elastic features that build on OTel semantics.

    Use this schema unless your use case is listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

**ECS (Elastic Common Schema)**
:   Metrics are stored under Elastic's original field naming conventions (for example, `system.cpu.pct`). {{agent}} integrations and {{metricbeat}} write this schema.

    Use this schema when your use case is listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic), for example when you need existing ECS integrations, dashboards, and alerts to keep working without customization.

:::{note}
Mixing schemas in a single deployment is possible but increases query complexity. Prefer one schema. Keep ECS only when you need it for a listed OpenTelemetry limitation.
:::

### Implications of your choice [metrics-plan-data-model-implications]

| | OTel schema | ECS schema |
|---|---|---|
| **Ingest using** | EDOT SDK, OTLP exporters, Prometheus remote write | {{agent}} integrations, {{metricbeat}} |
| **Field names** | OTel semantic conventions (`system.cpu.utilization`) | ECS (`system.cpu.pct`) |
| **PromQL support** | Yes (metrics stored as TSDS) | Limited |
| **Prebuilt dashboards** | OTel dashboards | Infrastructure UI, Elastic prebuilt dashboards |
| **Recommended for** | Default | Use cases listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic) |

## Choose an ingest path [metrics-plan-ingest-path]

Your deployment type constrains which ingest paths are available. Refer to [Ingest metrics](/solutions/observability/metrics/ingest.md) for the full set of options and configuration details. Use {{agent}} integrations when your use case is listed in [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic).

| Deployment | Recommended path | Also available |
|---|---|---|
| {{serverless-full}} | Managed OTLP endpoint | Prometheus remote write |
| {{ech}} | Managed OTLP endpoint | Prometheus remote write, {{agent}} integrations |
| Self-managed {{stack}} | {{agent}} in gateway mode | Prometheus remote write, {{agent}} integrations |

## Related [metrics-plan-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Get started with metrics](/solutions/observability/metrics/get-started.md)
- [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic)
