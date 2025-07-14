---
navigation_title: EDOT SDKs
description: Troubleshoot issues with the EDOT SDKs using these guides.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT SDKs

Find solutions to common issues with EDOT SDKs.

- [.NET](/troubleshoot/ingest/opentelemetry/edot-sdks/dotnet/index.md)
- [Java](/troubleshoot/ingest/opentelemetry/edot-sdks/java/index.md)
- [Node.js](/troubleshoot/ingest/opentelemetry/edot-sdks/nodejs/index.md)
- [PHP](/troubleshoot/ingest/opentelemetry/edot-sdks/php/index.md)
- [Python](/troubleshoot/ingest/opentelemetry/edot-sdks/python/index.md)

:::{warning}
Avoid using EDOT SDKs alongside any other APM agent, including Elastic APM agents. Running multiple agents in the same application process may lead to unexpected behavior, conflicting instrumentation, or duplicated telemetry.
:::
