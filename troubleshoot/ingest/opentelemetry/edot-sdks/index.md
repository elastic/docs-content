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

Find solutions to common issues with EDOT SDKs for various programming languages and platforms.

* [Android SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/android/index.md): Troubleshoot common problems affecting the {{product.edot-android}} SDK.

* [.NET SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/dotnet/index.md): Troubleshoot common problems affecting the EDOT .NET SDK.

* [iOS SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/ios/index.md): Troubleshoot common problems affecting the {{product.edot-ios}} agent.

* [Java SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/java/index.md): Troubleshoot common problems affecting the EDOT Java agent, including connectivity, agent identification, and debugging.

* [Node.js SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/nodejs/index.md): Troubleshoot issues using EDOT Node.js SDK.

* [PHP SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/php/index.md): Troubleshoot issues using EDOT PHP agent.

* [Python SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/python/index.md): Troubleshoot issues using EDOT Python agent.

## Shared troubleshooting topics

These guides apply to all EDOT SDKs:

* [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md): Learn how to enable debug logging for EDOT SDKs to troubleshoot application-level instrumentation issues.

* [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md): Diagnose lack of telemetry flow due to issues with EDOT SDKs.

* [Proxy settings for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/proxy.md): Configure proxy settings for EDOT SDKs when your application runs behind a proxy.

* [Missing or incomplete traces due to SDK sampling](/troubleshoot/ingest/opentelemetry/edot-sdks/misconfigured-sampling-sdk.md): Troubleshoot missing or incomplete traces caused by SDK-level sampling configuration.

## See also

* [EDOT Collector troubleshooting](/troubleshoot/ingest/opentelemetry/edot-collector/index.md): For end-to-end issues that may involve both the Collector and SDKs.

* [Troubleshoot EDOT](/troubleshoot/ingest/opentelemetry/index.md): Overview of all EDOT troubleshooting resources.

:::{warning}
Avoid using EDOT SDKs alongside any other {{apm-agent}}, including Elastic {{product.apm}} agents. Running multiple agents in the same application process may lead to unexpected behavior, conflicting instrumentation, or duplicated telemetry.
:::
