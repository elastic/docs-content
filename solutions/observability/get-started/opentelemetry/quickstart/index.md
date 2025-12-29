---
navigation_title: OpenTelemetry quickstarts
description: Learn how to set up the Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts. The guides cover installing the EDOT Collector, enabling auto-instrumentation, and configuring data collection for metrics, logs, and traces in Elastic Observability.
applies_to:
   stack:
   serverless:
     observability:
   product:
     edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# OpenTelemetry quickstarts

Learn how to set up the Elastic Distributions for OpenTelemetry (EDOT) to monitor {{k8s}}, applications, and hosts.

## Add data from the UI

You can quickly add data from hosts, {{k8s}}, applications, and cloud services from the {{observability}} UI.

1. Open {{product.observability}}.
2. Go to **Add data**.
3. Select what you want to monitor.
4. Follow the instructions.

## Manual installation guides

These guides cover how to install the EDOT Collector, turn on auto-instrumentation, and configure data collection for metrics, logs, and traces in {{product.observability}}.

Select a guide based on the environment of your target system and your Elastic deployment model.

| Deployment Model       | {{k8s}}                              | Docker                                  | Hosts or VMs                          |
|-------------------------|-----------------------------------------|-----------------------------------------|---------------------------------------|
| {{product.self}} Stack | [{{k8s}} on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts or VMs on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |
| {{serverless-full}}  | [{{k8s}} on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md)     | [Docker on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md)     | [Hosts or VMs on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md)     |
| {{ech}}      | [{{k8s}} on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md)               | [Docker on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md)               | [Hosts or VMs on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md)               |
| Multiple      | [Ingest custom metrics with EDOT](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md) | [Ingest custom metrics with EDOT](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md) | [Ingest custom metrics with EDOT](/solutions/observability/get-started/opentelemetry/custom-metrics-quickstart.md) |

## Troubleshooting

Having issues with the EDOT Collector? Refer to the [Troubleshooting common issues with the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) guide for help.