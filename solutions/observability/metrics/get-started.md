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

This page walks you through the recommended path for setting up metrics in Elastic, from a first working pipeline to a production setup you can maintain.

Start with a quickstart rather than a full design exercise. A quickstart gets data flowing in minutes on a single host or cluster, so you can confirm that collection, authentication, and storage all work end to end before you decide how to model your metrics across your estate. Once you can view data in {{kib}}, you have something concrete to plan against.

:::::{stepper}

::::{step} Get data flowing
:anchor: metrics-get-started-quickstart

Follow an {{edot}} quickstart for your deployment type and environment. Each quickstart sets up the full {{edot}} stack for collecting logs, metrics, and traces. Use the row that matches your deployment and the column that matches where you run your workloads:

| Deployment | {{k8s}} | Docker | Hosts or VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

To send **custom application metrics** instead of infrastructure metrics, follow [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).
::::

::::{step} Plan your data model
:anchor: metrics-get-started-plan

Before you add more sources, decide whether to standardize on the OpenTelemetry schema or ECS. This choice determines your metric field names, which in turn determines which prebuilt dashboards work and how your queries and alerts are written. Changing it later means rewriting those assets, so settle it early, while you only have one source to migrate.

For the trade-offs and the ingest path that matches your deployment, refer to [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md).
::::

::::{step} Add more sources
:anchor: metrics-get-started-ingest

With a data model chosen, extend collection to the rest of your estate. Beyond the quickstarts, you can send metrics using any OTLP-compliant client, Prometheus remote write, or {{agent}} integrations for specific services such as nginx, PostgreSQL, or Redis.

For path-by-path configuration, refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).
::::

::::{step} Explore and query your data
:anchor: metrics-get-started-explore

Once metrics are arriving from multiple sources, build the views and queries your team uses day to day.

[Explore metrics](/solutions/observability/metrics/explore.md)
:   {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Visualize metrics in **Discover**, the Infrastructure UI, dashboards, and Grafana.

    {applies_to}`stack: ga 9.0-9.3` Visualize metrics in **Metrics Explorer**, the Infrastructure UI, dashboards, and Grafana.

[Query metrics](/solutions/observability/metrics/query.md)
:   Run {{esql}} time-series queries or reuse PromQL.
::::

::::{step} Manage storage and retention
:anchor: metrics-get-started-storage

Metrics volume grows faster than most teams expect, and cardinality is the usual cause. Before your setup becomes production-critical, set up downsampling and retention so storage costs stay predictable.

For TSDS, downsampling, cardinality, and lifecycle options, refer to [Manage metrics storage](/solutions/observability/metrics/manage-storage.md).
::::

:::::
