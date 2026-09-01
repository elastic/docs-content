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

Before you start ingesting metrics at scale, make two decisions that affect how your data looks in {{es}} and how you query it later: the data model to use, and the ingest path that fits your deployment.

## Choose a data model [metrics-plan-data-model]

Metrics ingested into Elastic can follow one of two schemas:

**OpenTelemetry (OTel) schema**
:   Metrics are stored under the OTel semantic conventions — for example, `system.cpu.utilization` instead of `system.cpu.pct`. This schema is the recommended default for new setups. It gives you maximum compatibility with the OTel ecosystem and positions you well for future Elastic features that build on OTel semantics.

    Use this schema when you're starting fresh, migrating from Prometheus (which maps cleanly to OTel conventions), or want to align with OpenTelemetry-native tooling.

**ECS (Elastic Common Schema)**
:   Metrics are stored under Elastic's original field naming conventions. This schema is used by {{agent}} integrations (for example, `system.cpu.pct`) and by existing infrastructure monitoring setups.

    Use this schema when you already have {{agent}} integrations deployed, you have existing dashboards and alerts built on ECS fields, or you want to minimize migration effort.

:::{note}
Mixing schemas in a single deployment is possible but increases query complexity. If you already use one schema, extend it consistently before considering a migration.
:::

### Implications of your choice [metrics-plan-data-model-implications]

| | OTel schema | ECS schema |
|---|---|---|
| **Ingest using** | EDOT SDK, OTLP exporters, Prometheus remote write | {{agent}} integrations, {{metricbeat}} |
| **Field names** | OTel semantic conventions (`system.cpu.utilization`) | ECS (`system.cpu.pct`) |
| **PromQL support** | Yes (metrics stored as TSDS) | Limited |
| **Out-of-box dashboards** | OTel dashboards | Infrastructure UI, Elastic prebuilt dashboards |
| **Recommended for** | New setups, Prometheus migrations | Existing {{agent}} deployments |

## Choose an ingest path [metrics-plan-ingest-path]

Your deployment type constrains which ingest paths are available. Refer to [Ingest metrics](/solutions/observability/metrics/ingest.md) for the full set of options and configuration details.

| Deployment | Recommended path | Also available |
|---|---|---|
| {{serverless-full}} | Managed OTLP endpoint | Prometheus remote write |
| {{ech}} | Managed OTLP endpoint | Prometheus remote write, {{agent}} integrations |
| Self-managed {{stack}} | {{agent}} in gateway mode | Prometheus remote write, {{agent}} integrations |

## Related [metrics-plan-related]

- [Ingest metrics](/solutions/observability/metrics/ingest.md)
- [Get started with metrics](/solutions/observability/metrics/get-started.md)
