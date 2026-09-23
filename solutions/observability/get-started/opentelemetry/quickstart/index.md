---
navigation_title: OpenTelemetry quickstarts
description: Step-by-step guides for setting up Elastic OpenTelemetry to monitor Kubernetes, applications, and hosts using Elastic Agent and auto-instrumentation.
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/quickstart-monitor-hosts-with-otel.html
  - https://www.elastic.co/guide/en/serverless/current/quickstart-monitor-hosts-with-otel.html
  - https://www.elastic.co/guide/en/observability/current/monitor-k8s-otel-edot.html
  - https://www.elastic.co/guide/en/serverless/current/monitor-k8s-otel-edot.html
applies_to:
  deployment:
    ech: ga
    self: ga
  serverless:
    observability: ga
  product:
    edot_collector: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# OpenTelemetry quickstarts

Learn how to set up {{edot}} to monitor {{k8s}}, applications, and hosts.

## Add data from the UI

You can quickly add data from hosts, {{k8s}}, applications, and cloud services from the {{observability}} UI.

1. Open {{product.observability}}.
2. Go to **Add data**.
3. Select what you want to monitor.
4. Follow the instructions.

## Manual installation guides

These guides cover how to install the {{agent}}, turn on auto-instrumentation, and configure data collection for metrics, logs, and traces in {{product.observability}}.

Select a guide based on the environment of your target system and your Elastic deployment model.

| Deployment Model       | {{k8s}}                              | Docker                                  | Hosts or VMs                          |
|-------------------------|-----------------------------------------|-----------------------------------------|---------------------------------------|
| {{product.self}} Stack | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts or VMs on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |
| {{serverless-full}}  | [{{k8s}} on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md)     | [Docker on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md)     | [Hosts or VMs on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md)     |
| {{ech}}      | [{{k8s}} on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md)               | [Docker on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md)               | [Hosts or VMs on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md)               |

For application metrics you define yourself, in any environment, refer to [Ingest custom metrics with {{edot}}](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md).

## Troubleshooting

Having issues with the {{agent}}? Refer to the [Troubleshooting common issues with the {{agent}}](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) guide for help.