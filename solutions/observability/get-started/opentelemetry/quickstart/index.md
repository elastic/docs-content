---
navigation_title: Quickstart
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

# Quickstart guides

Learn how to set up the Elastic Distributions for OpenTelemetry (EDOT) to monitor Kubernetes, applications, and hosts.

## Add data from the UI

You can quickly add data from hosts, Kubernetes, applications, and cloud services from the Observability UI.

1. Open Elastic Observability.
2. Go to **Add data**.
3. Select what you want to monitor.
4. Follow the instructions.

## Manual installation guides

The guides cover how to install the EDOT Collector, turn on auto-instrumentation, and configure data collection for metrics, logs, and traces in Elastic Observability.

Select a guide based on the environment of your target system and your Elastic deployment model.

| Deployment Model       | Kubernetes                              | Docker                                  | Hosts or VMs                          |
|-------------------------|-----------------------------------------|-----------------------------------------|---------------------------------------|
| Self-managed Elastic Stack | [Kubernetes on self-managed](/reference/quickstart/self-managed/k8s.md) | [Docker on self-managed](/reference/quickstart/self-managed/docker.md) | [Hosts or VMs on self-managed](/reference/quickstart/self-managed/hosts_vms.md) |
| {{serverless-full}}  | [Kubernetes on serverless](/reference/quickstart/serverless/k8s.md)     | [Docker on serverless](/reference/quickstart/serverless/docker.md)     | [Hosts or VMs on serverless](/reference/quickstart/serverless/hosts_vms.md)     |
| {{ech}}      | [Kubernetes on hosted](/reference/quickstart/ech/k8s.md)               | [Docker on hosted](/reference/quickstart/ech/docker.md)               | [Hosts or VMs on hosted](/reference/quickstart/ech/hosts_vms.md)               |

## Troubleshooting

Having issues with the EDOT Collector? Refer to the [Troubleshooting common issues with the EDOT Collector](docs-content://troubleshoot/ingest/opentelemetry/edot-collector/index.md) guide for help.