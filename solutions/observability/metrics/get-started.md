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

The fastest path to getting metrics into Elastic is to follow an {{edot}} quickstart for your deployment type and environment. Each quickstart sets up the full {{edot}} stack — logs, metrics, and traces.

Select the quickstart that matches your deployment type and environment:

| Deployment | {{k8s}} | Docker | Hosts / VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on {{serverless-short}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

For **custom application metrics**, follow the dedicated guide: [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).

## What's next [metrics-get-started-next]

- **Plan your data model**: Before adding more sources, read [Plan your metrics setup](/solutions/observability/metrics/plan-your-setup.md) to understand the OTel schema versus ECS choice and what it means for metric names, dashboards, and queries.
- **Add more sources**: See [Ingest metrics](/solutions/observability/metrics/ingest.md) for the full set of ingest options, including {{agent}} integrations and Prometheus remote write.
- **Explore your data**: See [Explore metrics](/solutions/observability/metrics/explore.md) to start building dashboards and visualizations.
