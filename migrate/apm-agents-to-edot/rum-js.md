---
navigation_title: Move to EDOT Browser
applies_to:
  stack: ga
  serverless:
    observability: ga
  product:
    edot_browser: preview 0.1.0
products:
  - id: observability
---

# Move from the Elastic {{product.apm}} RUM JavaScript agent to EDOT Browser

EDOT Browser is Elastic's distribution of the OpenTelemetry Browser SDK. It collects traces, metrics, and logs from real user interactions in web applications and exports that data using OTLP.

:::{note}
EDOT Browser is currently in technical preview. A step-by-step migration guide from the Elastic {{product.apm}} RUM JavaScript agent will be published when EDOT Browser reaches general availability.
:::

## Current state

EDOT Browser provides the following capabilities:

- Automatic instrumentation of page loads, user interactions, and network requests
- Distributed tracing across browser and backend services
- OTLP export to the {{edot}} Collector or the [{{motlp}}](opentelemetry://reference/motlp.md)

Full feature parity with the classic Elastic {{product.apm}} browser agent and dedicated migration tooling are not yet available.

## Get started with EDOT Browser

If you want to try EDOT Browser now, refer to the [EDOT Browser documentation](elastic-otel-rum-js://reference/edot-browser/index.md) for installation and configuration instructions.

## Stay informed

Watch the [EDOT Browser release notes](elastic-otel-rum-js://release-notes/index.md) for updates on general availability and migration guide availability.
