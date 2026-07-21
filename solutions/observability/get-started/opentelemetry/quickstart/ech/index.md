---
navigation_title: Elastic Cloud Hosted
description: Quickstart setup guides for the {{edot}} on Elastic Cloud Hosted.
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

# Quickstart on Elastic Cloud Hosted

Select the quickstart guide for your environment from the following list:

- [Kubernetes on hosted](k8s.md)
- [Docker on hosted](docker.md)
- [Hosts or VMs on hosted](hosts_vms.md)

:::{note}
Before version 9.5, the **EDOT Collector** was a standalone product. From 9.5 onwards, this OpenTelemetry collector capability is built into **{{agent}}**.
:::

## Troubleshooting

Having issues with {{edot}}? Refer to the [Troubleshooting common issues with the {{agent}}](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md) for help.