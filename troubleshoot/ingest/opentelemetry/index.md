---
navigation_title: Elastic Distributions of OpenTelemetry (EDOT)
description: Troubleshoot EDOT issues using these guides.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshoot Elastic Distributions of OpenTelemetry (EDOT)

Find solutions to common issues in EDOT components and SDKs.

## Component troubleshooting

* [EDOT Collector troubleshooting](/troubleshoot/ingest/opentelemetry/edot-collector/index.md): Troubleshoot issues with the EDOT Collector, including resource problems, configuration errors, and connectivity issues.

* [EDOT SDKs troubleshooting](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md): Troubleshoot issues with EDOT SDKs for Android, .NET, iOS, Java, Node.js, PHP, and Python.

## Common troubleshooting topics

These guides apply to both the Collector and SDKs:

* [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md): Resolve connection problems between EDOT components and Elastic, including firewall, proxy, and network configuration issues.

* [No data visible in Kibana](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md): Diagnose why telemetry data (logs, metrics, traces) doesn't appear in Kibana after setting up EDOT.

* [429 errors when using the mOTLP endpoint](/troubleshoot/ingest/opentelemetry/429-errors-motlp.md): Resolve HTTP 429 `Too Many Requests` errors when sending data through the Elastic Cloud Managed OTLP endpoint.

* [Contact support](/troubleshoot/ingest/opentelemetry/contact-support.md): Learn how to contact Elastic Support and what information to include to help resolve issues faster.

## Additional resources

* [Troubleshoot ingestion tools](/troubleshoot/ingest.md): Overview of troubleshooting for all ingestion tools, including EDOT, Logstash, Fleet, and Beats.

* [Elastic Support Portal](https://support.elastic.co/): Access support cases, subscriptions, and licenses.

* [Elastic community forums](https://discuss.elastic.co): Get answers from experts in the community, including Elastic team members.
