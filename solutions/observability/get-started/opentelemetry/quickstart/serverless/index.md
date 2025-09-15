---
navigation_title: Elastic Cloud Serverless
description: Quickstart guide for setting up EDOT on Elastic Cloud Serverless.
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

# Quickstart on Elastic Cloud Serverless

The [{{motlp}}](opentelemetry://reference/motlp.md) simplifies OpenTelemetry data ingestion. It provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage. The endpoint is exclusively for Elastic Cloud users, initially available in {{serverless-full}} only.

The {{motlp}} is designed for the following use cases:

* Logs and Infrastructure Monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format.
* APM: Application telemetry in OTLP format.

## Prerequisites

* An Elastic Observability Serverless project.
* An {{edot}} or any system that can forward logs, metrics, or traces in OTLP format.

You also need to retrieve your OTLP endpoint address and an API key.

:::{include} ../../_snippets/serverless-endpoint-api.md
:::

## Quickstart guides

Select the quickstart guide for your environment from the following list:

- [Kubernetes on serverless](k8s.md)
- [Docker on serverless](docker.md)
- [Hosts or VMs on serverless](hosts_vms.md)

## Differences with Elastic APM Endpoint

The {{motlp}} ensures that OpenTelemetry data is stored without any schema translation, preserving both OpenTelemetry semantic conventions and resource attributes. It supports ingesting OTLP logs, metrics, and traces in a unified manner, ensuring consistent treatment across all telemetry data.

## Provide feedback

Help improve the {{motlp}} by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup).

For EDOT Collector feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).
