---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/otel-agent.html
---

# Run Elastic Agent as an OTel Collector [otel-agent]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) is a vendor-neutral way to receive, process, and export telemetry data. {{agent}} includes an embedded OTel Collector, enabling you to instrument your applications and infrastructure once, and send data to multiple vendors and backends.

When you run {{agent}} in `otel` mode it supports the standard OTel Collector configuration format that defines a set of receivers, processors, exporters, and connectors. Logs, metrics, and traces can be ingested using OpenTelemetry data formats.

For a full overview and steps to configure {{agent}} in `otel` mode, including a guided onboarding, refer to the [Elastic Distributions for OpenTelemetry](https://github.com/elastic/opentelemetry/tree/main) repository in GitHub. You can also check the [`elastic-agent otel` command](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-otel-command) in the {{fleet}} and {{agent}} Command reference.

If you have a currently running {{agent}} you can [transform it to run as an OTel Collector](/reference/ingestion-tools/fleet/otel-agent.md).