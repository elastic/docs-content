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

This page walks you through the fastest way to try metrics in Elastic. Start here to ingest metrics from a single source and use {{kib}} to explore and query your data. You'll use a quickstart to install {{agent}} configured as an OTel Collector and confirm that collection, authentication, and storage work end to end before you design a larger setup.

When you're ready to add more sources and plan a production rollout, continue with [Next steps](#metrics-get-started-next).

## Before you begin [metrics-get-started-before]

You need:

- An Elastic deployment or project: {{serverless-full}}, {{ech}}, or a self-managed {{stack}} deployment.
- Access to install and run {{agent}} where your workloads run, or an application that can export OpenTelemetry metrics.

## Send and explore your first metrics [metrics-get-started-steps]

:::::::{stepper}

::::::{step} Get data flowing
:anchor: metrics-get-started-quickstart

Follow an {{edot}} quickstart for your deployment type and environment. Each quickstart deploys {{agent}} configured as an OTel Collector to collect logs, metrics, and traces. Use the row that matches your deployment and the column that matches where you run your workloads:

| Deployment | {{k8s}} | Docker | Hosts or VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

To send **custom application metrics** instead of infrastructure metrics, follow [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).
::::::

::::::{step} Confirm your metrics are flowing
:anchor: metrics-get-started-confirm

After the quickstart finishes, check that its metrics arrived in {{kib}}.

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }
1. Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select {icon}`code` **{{esql}}** to switch to {{esql}} mode, then run:

    ```esql
    TS metrics-*
    ```

    `TS` queries time-series metrics. `metrics-*` matches your metrics data streams, including the streams from the quickstart.

**Discover** shows the result as a grid of charts, one for each metric in your data. If the grid includes metrics your quickstart collects, such as `system.cpu.utilization`, your data is flowing.
::::

::::{applies-item} stack: deprecated 9.4+, ga 9.0-9.3
1. Find **Infrastructure** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Metrics Explorer**.
2. Search for a metric your quickstart collects, for example `system.cpu.utilization`.

If **Metrics Explorer** charts values for the metric, your data is flowing.
::::

:::::
::::::

::::::{step} Explore your metrics
:anchor: metrics-get-started-explore

With data flowing, try a few common tasks to find the metrics that matter to you and keep them at hand.

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }
From the chart grid in **Discover**:

- **Search for a metric.** Select **Search metrics** ({icon}`magnify`) at the top right of the chart grid and enter part of a metric name, for example `cpu`. The grid shows only the metrics whose names match, which is faster than scrolling when your sources send hundreds of them.

  :::{image} /solutions/images/explore-metrics-search.png
  :alt: The Discover chart grid filtered to metrics that contain cpu
  :screenshot:
  :::

- **Break a metric down by a dimension.** Select **Dimensions** and choose a dimension such as the host name. Each chart then shows a separate line for each host, so you can find the host that causes a CPU spike or uses the most memory.
- **View the details of a metric.** On a chart, select **View details** ({icon}`eye`) to find the metric type, its dimensions, and the {{esql}} query behind the chart. Use the query as a starting point for your own queries and alerts.
- **Add a chart to a dashboard.** On a chart, select **Copy to dashboard** ({icon}`add_to_dashboard`) to save it to a new or existing dashboard. A dashboard keeps the chart next to related charts, so you can return to it, follow the metric over time, and share it with your team.

For more ways to explore your metrics in **Discover**, refer to [](/solutions/observability/infra-and-hosts/discover-metrics.md).
::::

::::{applies-item} stack: deprecated 9.4+, ga 9.0-9.3
In **Metrics Explorer**:

- **Aggregate the metric.** Choose an aggregation, such as **Average** or **Max**, to control how values are combined in each time bucket.
- **Break the metric down by a field.** From the **graph per** dropdown, add a field such as `host.name` to get one chart for each host, so you can compare hosts and find the one that causes a spike.
- **Add the chart to a dashboard.** On a chart, select **Actions** → **Open in Visualize**, then save the visualization to a dashboard. A dashboard keeps the chart next to related charts, so you can return to it and share it with your team.

For the Metrics Explorer workflow, refer to [](/solutions/observability/infra-and-hosts/explore-infrastructure-metrics-over-time.md).
::::

:::::

To check the health of the resources you monitor instead of individual metrics, open **Infrastructure inventory**. It groups the resources you monitor, such as hosts, pods, and containers, and shows a metric for each one, so you can find a resource under pressure at a glance. Open **Hosts** to compare host metrics side by side.

For other ways to query, visualize, and alert on metrics, refer to [](/solutions/observability/metrics/explore.md).
::::::

:::::::

## Next steps [metrics-get-started-next]

A quickstart gets one source flowing. Before you roll metrics out across your infrastructure:

- **Choose a data model.** Decide whether to standardize on the OpenTelemetry schema (recommended) or Elastic Common Schema (ECS). The ingest path you use determines the schema, the schema determines your metric field names, and the field names determine which prebuilt dashboards work and how your queries and alerts are written. Changing it later means rewriting those assets, so settle it early, while you only have one source to migrate. Refer to [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md) for more information.
- **Add more sources.** Send metrics using any OTLP-compatible client, Prometheus remote write, or {{agent}} integrations for specific services such as Nginx, PostgreSQL, or Redis. For path-by-path configuration, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).
- **Migrate an existing stack.** If you're moving from Prometheus or Datadog, you can run both systems side by side and switch over gradually. Refer to [Migrate metrics to Elastic](/solutions/observability/metrics/migrate.md) for more information.
- **Manage storage and retention.** Metrics volume grows faster than most teams expect, and cardinality is the usual cause. Before your setup becomes production-critical, set up downsampling and retention so storage costs stay predictable. Refer to [Manage metrics storage](/solutions/observability/metrics/manage-storage.md) for more information.
