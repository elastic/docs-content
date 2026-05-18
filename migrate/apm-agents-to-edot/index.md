---
navigation_title: Move APM agents to EDOT
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
---

# Move {{apm-agent}}s to {{edot}}

The Elastic {{product.apm}} language agents are being superseded by Elastic Distributions of OpenTelemetry (EDOT) — Elastic's OpenTelemetry-native instrumentation libraries. Migrating to EDOT aligns your application instrumentation with the OpenTelemetry standard and gives you access to the full EDOT ecosystem.

Each language has a dedicated migration guide that includes step-by-step instructions, configuration mapping tables, and known limitations.

## Migration guides by language

Select the guide for your language:

- [**Java**](elastic-otel-java://reference/edot-java/migration.md) — Migrate from the {{apm-java-agent}} to EDOT Java
- [**Node.js**](elastic-otel-node://reference/edot-node/migration.md) — Migrate from the Elastic {{product.apm}} Node.js agent to EDOT Node.js
- [**Python**](elastic-otel-python://reference/edot-python/migration.md) — Migrate from the Elastic {{product.apm}} Python agent to EDOT Python
- [**.NET**](elastic-otel-dotnet://reference/edot-dotnet/migration.md) — Migrate from the Elastic {{product.apm}} .NET agent to EDOT .NET
- [**PHP**](elastic-otel-php://reference/edot-php/migration.md) — Migrate from the Elastic {{product.apm}} PHP agent to EDOT PHP
- [**Browser/RUM JS**](/migrate/apm-agents-to-edot/rum-js.md) — Migration guide for the Elastic {{product.apm}} RUM JavaScript agent
