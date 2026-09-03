---
navigation_title: Elastic Observability quickstarts
description: Quickstart guides for ingesting and visualizing Elastic Observability data with fast paths for hosts, Kubernetes, applications, and synthetic monitoring.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Elastic {{observability}} quickstarts

Our quickstarts reduce your time-to-value by offering a fast path to ingest and visualize your Observability data. Each quickstart provides:

* A highly opinionated, fast path to data ingestion
* Sensible configuration defaults with minimal configuration required
* Auto-detection of logs and metrics for monitoring hosts
* Quick access to related dashboards and visualizations

## {{edot}} quickstarts (recommended) [_otel-quickstarts]

The recommended path for new setups. Select a guide based on your deployment model and environment:

| Deployment | {{k8s}} | Docker | Hosts / VMs |
|---|---|---|---|
| {{ech}} | [{{k8s}} on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |
| {{serverless-full}} | [{{k8s}} on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| Self-managed {{stack}} | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |

For custom application metrics: [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).

## Other quickstarts [_other-quickstarts]

These quickstarts cover additional ingest paths and use cases:

* [**Quickstart: Monitor your application performance**](/solutions/observability/get-started/quickstart-monitor-your-application-performance.md)
* [**Quickstart: Monitor hosts with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) — use this if you have an existing {{agent}} deployment and want {{product.ecs}} metrics rather than OTel.
* [**Quickstart: Monitor your {{k8s}} cluster with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md) — Agent-based alternative to the OTel {{k8s}} quickstart.
* [**Quickstart: Create a Synthetic monitor**](/solutions/observability/get-started/quickstart-create-synthetic-monitor.md)
* [**Quickstart: Collect data from AWS Firehose**](/solutions/observability/get-started/quickstart-collect-data-with-aws-firehose.md)

## Get started with other features [_get_started_with_other_features]

Want to use {{fleet}} or some other feature not covered in the quickstarts? Follow the steps in these guides to get started:

* [Get started with system metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md).
* [Get started with synthetic monitoring](/solutions/observability/synthetics/index.md).
* [Get started with Universal Profiling](/solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md).

## Additional guides [_additional_guides]

Ready to dig into more features of Elastic Observability? See these guides:

* [Create an alert](/solutions/observability/incident-management/alerting.md).
* [Create a service-level objective (SLO)](/solutions/observability/incident-management/create-an-slo.md).

## Related content for {{stack}} [_related_content]

* [Starting with the {{es}} Platform and its Solutions](/get-started/index.md) for new users.
* [Adding data to {{es}}](/manage-data/ingest.md) for other ways to ingest data.
