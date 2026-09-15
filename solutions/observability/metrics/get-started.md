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

Start with a quickstart rather than a full design exercise. A quickstart gets data flowing in minutes on a single host or cluster, so you can confirm that collection, authentication, and storage all work end to end before you decide how to model your metrics across your estate. Once you can see data in {{kib}}, you have something concrete to plan against.

## Step 1: Get data flowing [metrics-get-started-quickstart]

Follow an {{edot}} quickstart for your deployment type and environment. Each quickstart sets up the full {{edot}} stack for collecting logs, metrics, and traces.

| Deployment | {{k8s}} | Docker | Hosts / VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

To send **custom application metrics** instead of infrastructure metrics, follow [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).

## Step 2: Plan your data model [metrics-get-started-plan]

Before you add more sources, decide whether to standardize on the OpenTelemetry schema or ECS. This choice determines your metric field names, which in turn determines which prebuilt dashboards work and how your queries and alerts are written. Changing it later means rewriting those assets, so it's worth settling early, while you only have one source to migrate.

Refer to [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md).

## Step 3: Add more sources [metrics-get-started-ingest]

With a data model chosen, extend collection to the rest of your estate. Beyond the quickstarts, you can send metrics using any OTLP-compliant client, Prometheus remote write, or {{agent}} integrations for specific services such as nginx, PostgreSQL, or Redis.

Refer to [Ingest metrics](/solutions/observability/metrics/ingest.md).

## Step 4: Explore and query your data [metrics-get-started-explore]

Once metrics are arriving from multiple sources, build the views and queries your team will use day to day.

- [Explore metrics](/solutions/observability/metrics/explore.md): Discover, the Infrastructure UI, dashboards, and Grafana.
- [Query metrics](/solutions/observability/metrics/query.md): {{esql}} time-series mode and PromQL.

## Step 5: Manage storage and retention [metrics-get-started-storage]

Metrics volume grows faster than most teams expect, and cardinality is the usual cause. Before your setup becomes production-critical, set up downsampling and retention so storage costs stay predictable. Refer to [Manage metrics storage](/solutions/observability/metrics/manage-storage.md) for more information.
