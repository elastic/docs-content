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

## Recommended: {{edot}} quickstarts [_otel-quickstarts]

For new setups, collect logs, metrics, and traces with {{edot}}. There's a guide for every combination of deployment model ({{ech}}, {{serverless-full}}, or a self-managed {{stack}}) and environment ({{k8s}}, Docker, or hosts and VMs).

* [**{{edot}} quickstarts**](/solutions/observability/get-started/opentelemetry/quickstart/index.md): select your deployment model and environment, then follow that guide.
* [**Start using OpenTelemetry with Elastic**](/solutions/observability/get-started/opentelemetry/start-with-otel.md): if you're not sure which ingestion path suits your deployment, decide here first.

## Other quickstarts [_other-quickstarts]

These quickstarts cover additional ingest paths and use cases:

* [**Quickstart: Monitor your application performance**](/solutions/observability/get-started/quickstart-monitor-your-application-performance.md)
* [**Ingest custom metrics with {{edot}}**](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md) — for application metrics you define yourself, in any environment.
* [**Quickstart: Monitor hosts with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) — use this if you already run {{agent}} and want ECS-formatted metrics rather than OpenTelemetry semantic conventions.
* [**Quickstart: Monitor your {{k8s}} cluster with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md) — Agent-based alternative to the OpenTelemetry {{k8s}} quickstart.
* [**Quickstart: Create a Synthetic monitor**](/solutions/observability/get-started/quickstart-create-synthetic-monitor.md)
* [**Send OTLP data to Elastic Cloud**](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md) — use this if you already run an OTLP-compatible collector or SDK and want to send data straight to the {{motlp}}.
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
