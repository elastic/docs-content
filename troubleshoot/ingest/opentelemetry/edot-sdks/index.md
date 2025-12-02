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

* [Android SDK](android/index.md): Troubleshoot common problems affecting the {{product.edot-android}} SDK.

* [.NET SDK](dotnet/index.md): Troubleshoot common problems affecting the EDOT .NET SDK.

* [iOS SDK](ios/index.md): Troubleshoot common problems affecting the {{product.edot-ios}} agent.

* [Java SDK](java/index.md): Troubleshoot common problems affecting the EDOT Java agent, including connectivity, agent identification, and debugging.

* [Node.js SDK](nodejs/index.md): Troubleshoot issues using EDOT Node.js SDK.

* [PHP SDK](php/index.md): Troubleshoot issues using EDOT PHP agent.

* [Python SDK](python/index.md): Troubleshoot issues using EDOT Python agent.

## Shared troubleshooting topics

These guides apply to all EDOT SDKs:

* [Enable debug logging](enable-debug-logging.md): Learn how to enable debug logging for EDOT SDKs to troubleshoot application-level instrumentation issues.

* [No application-level telemetry visible in {{kib}}](missing-app-telemetry.md): Diagnose lack of telemetry flow due to issues with EDOT SDKs.

* [Proxy settings for EDOT SDKs](proxy.md): Configure proxy settings for EDOT SDKs when your application runs behind a proxy.

* [Missing or incomplete traces due to SDK sampling](misconfigured-sampling-sdk.md): Troubleshoot missing or incomplete traces caused by SDK-level sampling configuration.

## See also

* [EDOT Collector troubleshooting](../edot-collector/index.md): For end-to-end issues that may involve both the Collector and SDKs.

* [Troubleshoot EDOT](../index.md): Overview of all EDOT troubleshooting resources.

:::{warning}
Avoid using EDOT SDKs alongside any other {{apm-agent}}, including Elastic {{product.apm}} agents. Running multiple agents in the same application process may lead to unexpected behavior, conflicting instrumentation, or duplicated telemetry.
:::
