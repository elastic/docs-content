---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/otel-agent.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
  - id: edot-collector
---

# Run Elastic Agent as an EDOT Collector [otel-agent]

The [Elastic Distribution of OpenTelemetry (EDOT) Collector](elastic-agent://reference/edot-collector/index.md) is an open-source agent that can receive, process, and export telemetry data. {{agent}} includes an embedded EDOT Collector that allows you to instrument your applications and infrastructure once, and send data to multiple vendors and backends.

When you run {{agent}} in `otel` mode, it supports the standard OpenTelemetry Collector configuration format that defines a set of receivers, processors, exporters, and connectors. Logs, metrics, and traces can be collected and exported using OpenTelemetry data formats.

For a full overview and steps to configure {{agent}} in `otel` mode, including a guided onboarding, refer to [Elastic Distributions for OpenTelemetry](elastic-agent://reference/edot-collector/index.md). You can also check the [`elastic-agent otel` command](/reference/fleet/agent-command-reference.md#elastic-agent-otel-command) in the {{fleet}} and {{agent}} Command reference.

If you have a currently running {{agent}} you can [transform it to run as an OTel Collector](/reference/fleet/otel-agent-transform.md).