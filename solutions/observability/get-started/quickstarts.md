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

Quickstarts are the fastest way to get data into {{product.observability}} and see it in {{kib}}. Each one follows a single, opinionated path with sensible defaults, so you need minimal configuration to go from an empty deployment to populated dashboards.

If you're starting fresh, use the recommended {{edot}} quickstarts. Use one of the other quickstarts when you have a specific source or tool in mind, such as {{agent}} integrations, synthetic monitors, or AWS Firehose.

## Recommended: {{edot}} quickstarts [_otel-quickstarts]

For new setups, collect logs, metrics, and traces with {{edot}}. There's a guide for every combination of deployment model ({{ech}}, {{serverless-full}}, or a self-managed {{stack}}) and environment ({{k8s}}, Docker, or hosts and VMs).

* [**{{edot}} quickstarts**](/solutions/observability/get-started/opentelemetry/quickstart/index.md): select your deployment model and environment, then follow that guide.
* [**Start using OpenTelemetry with Elastic**](/solutions/observability/get-started/opentelemetry/start-with-otel.md): if you're not sure which ingestion path suits your deployment, decide here first.
* [**Quickstart: Monitor your application performance**](/solutions/observability/get-started/quickstart-monitor-your-application-performance.md): instrument your application with the {{edot}} SDKs and explore its traces, metrics, and logs.
* [**Quickstart: Ingest custom metrics with {{edot}}**](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md): send application metrics you define yourself, in any environment.

## {{agent}} quickstarts [_elastic-agent-quickstarts]

These quickstarts install {{agent}} with its integrations. Data is formatted in the {{product.ecs}} rather than OpenTelemetry semantic conventions.

* [**Quickstart: Monitor hosts with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md): runs a script that scans your host, detects its logs and metrics, and installs {{agent}} to collect them.
* [**Quickstart: Monitor your {{k8s}} cluster with {{agent}}**](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md): installs {{agent}} with a single command to collect cluster logs and metrics.

## Other quickstarts [_other-quickstarts]

These quickstarts cover other sources and tools:

* [**Quickstart: Create a Synthetic monitor**](/solutions/observability/get-started/quickstart-create-synthetic-monitor.md): test and monitor your applications by simulating user journeys.
* [**Quickstart: Send OTLP data to Elastic Cloud**](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md): send data from an OTLP-compatible collector or SDK you already run straight to the {{motlp}}.
* [**Quickstart: Collect data from AWS Firehose**](/solutions/observability/get-started/quickstart-collect-data-with-aws-firehose.md): stream logs and metrics from AWS services to Elastic.

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

* [](/get-started/index.md) for new users.
* [Adding data to {{es}}](/manage-data/ingest.md) for other ways to ingest data.
