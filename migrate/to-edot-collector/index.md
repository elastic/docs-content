---
navigation_title: Move to the EDOT Collector
applies_to:
  stack: ga 9.2+
  serverless:
    observability:
products:
  - id: observability
  - id: edot-collector
---

# Move to the {{edot}} Collector

The {{edot}} Collector is a distribution of the OpenTelemetry Collector that is optimized for use with Elastic. It can replace both the {{apm-server}} and an contrib OpenTelemetry Collector in your telemetry pipeline.

## Migration paths

[](/migrate/to-edot-collector/from-apm-agents.md)
:   Use the Elastic {{apm-agent}} intake receiver to route classic {{apm-agent}} data through the {{edot}} Collector. This enables a gradual migration to OpenTelemetry without requiring immediate agent re-instrumentation.

[Migrate deprecated components](elastic-agent://reference/edot-collector/components/migrate-components.md)
:   Update your {{edot}} Collector configuration to replace deprecated components with their current equivalents.

[](/migrate/to-edot-collector/from-upstream-collector.md)
:   Move from a contrib OpenTelemetry Collector deployment to the {{edot}} Collector.
