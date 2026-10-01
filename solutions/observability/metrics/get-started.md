---
navigation_title: Get started
description: Get metrics flowing into Elastic quickly using the OpenTelemetry quickstart for your deployment type and environment.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Get started with metrics [metrics-get-started]

This page walks you through the fastest way to try metrics in Elastic: add one source, get its data flowing, and explore and query that data in {{kib}}. A quickstart gets data flowing in minutes on a single host or cluster, so you can confirm that collection, authentication, and storage work end to end before you design a larger setup.

When you're ready to add more sources and plan a production rollout, continue with [Next steps](#metrics-get-started-next).

## Before you begin [metrics-get-started-before]

You need:

- An Elastic deployment or project: {{serverless-full}}, {{ech}}, or a self-managed {{stack}} deployment.
- Access to install and run {{agent}} where your workloads run, or an application that can export OpenTelemetry metrics.

:::::::{stepper}

::::::{step} Get data flowing
:anchor: metrics-get-started-quickstart

Follow an {{edot}} quickstart for your deployment type and environment. Each quickstart deploys {{agent}} in OTel mode to collect logs, metrics, and traces. Use the row that matches your deployment and the column that matches where you run your workloads:

| Deployment | {{k8s}} | Docker | Hosts or VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

To send **custom application metrics** instead of infrastructure metrics, follow [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).
::::::

::::::{step} Explore and query your data
:anchor: metrics-get-started-explore

After metrics are flowing, confirm they arrived and run your first query in {{kib}}:

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }
1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select {icon}`code` **{{esql}}** to switch to {{esql}} mode, then run a `TS` query to select your metrics data:

    ```esql
    TS metrics-*
    ```

3. Search the chart grid for a metric your quickstart collects, for example `system.cpu.utilization`, then break it down by a dimension such as the host name, or add its chart to a dashboard.

For the full workflow, refer to [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md).
::::

::::{applies-item} stack: deprecated 9.4+, ga 9.0-9.3
1. Find **Infrastructure** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Metrics Explorer**.
2. Search for a metric your quickstart collects, for example `system.cpu.utilization`.
3. Visualize or aggregate the metric data, and add the chart to a dashboard.

For the Metrics Explorer workflow, refer to [Explore infrastructure metrics over time](/solutions/observability/infra-and-hosts/explore-infrastructure-metrics-over-time.md).
::::

:::::

To view infrastructure health by resource, such as hosts or pods, rather than by metric, use the **Infrastructure inventory** and **Hosts** views. For all the ways to query, visualize, and alert on metrics, refer to [Explore metrics](/solutions/observability/metrics/explore.md).
::::::

:::::::

## Next steps [metrics-get-started-next]

The quickstart gets one source flowing. Before you roll metrics out across your infrastructure:

- **Choose a data model.** Decide whether to standardize on the OpenTelemetry schema (recommended) or Elastic Common Schema (ECS). The ingest path you use determines the schema, the schema determines your metric field names, and the field names determine which prebuilt dashboards work and how your queries and alerts are written. Changing it later means rewriting those assets, so settle it early, while you only have one source to migrate. Refer to [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md).
- **Add more sources.** Send metrics using any OTLP-compatible client, Prometheus remote write, or {{agent}} integrations for specific services such as Nginx, PostgreSQL, or Redis. For path-by-path configuration, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).
- **Migrate an existing stack.** If you're moving from Prometheus or Datadog, you can run both systems side by side and switch over gradually. Refer to [Migrate metrics to Elastic](/solutions/observability/metrics/migrate.md).
- **Manage storage and retention.** Metrics volume grows faster than most teams expect, and cardinality is the usual cause. Before your setup becomes production-critical, set up downsampling and retention so storage costs stay predictable. Refer to [Manage metrics storage](/solutions/observability/metrics/manage-storage.md).
