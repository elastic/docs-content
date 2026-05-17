---
navigation_title: Move between ingest tools
applies_to:
  stack: ga
  serverless: ga
---

# Move between ingest tools

Whether you're replacing standalone {{beats}} with {{agent}}, moving your application instrumentation from Elastic {{product.apm}} language agents to EDOT, or migrating from an upstream OpenTelemetry Collector to the EDOT Collector, these guides walk you through each transition.

## Available guides

[Move from {{beats}} to {{agent}}](/migrate/beats-to-elastic-agent/index.md)
:   Replace {{filebeat}}, {{metricbeat}}, or {{auditbeat}} with {{agent}}, a unified agent for logs, metrics, and security data.

[Move from {{apm-agent}}s to {{edot}}](/migrate/apm-agents-to-edot/index.md)
:   Move your application instrumentation from Elastic {{product.apm}} language agents to Elastic Distributions of OpenTelemetry (EDOT).

[Move to the {{edot}} Collector](/migrate/to-edot-collector/index.md)
:   Move from {{apm-server}} ingestion or a contrib OpenTelemetry Collector to the EDOT Collector.
