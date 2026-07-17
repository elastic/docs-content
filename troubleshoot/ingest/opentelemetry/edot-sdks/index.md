---
navigation_title: Elastic OTel SDKs
description: Troubleshoot issues with the Elastic OTel SDKs using these guides.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the Elastic OTel SDKs [troubleshooting-the-edot-sdks]

Find solutions to common issues with Elastic OTel SDKs for various programming languages and platforms.

* [Android SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/android/index.md): Troubleshoot common problems affecting the {{product.edot-android}} SDK.

* [Browser SDK](elastic-otel-rum-js://reference/edot-browser/troubleshooting.md): Troubleshoot common problems affecting the Elastic OTel Browser SDK.

* [.NET SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/dotnet/index.md): Troubleshoot common problems affecting the Elastic OTel .NET SDK.

* [iOS SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/ios/index.md): Troubleshoot common problems affecting the {{product.edot-ios}} agent.

* [Java SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/java/index.md): Troubleshoot common problems affecting the Elastic OTel Java agent, including connectivity, agent identification, and debugging.

* [Node.js SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/nodejs/index.md): Troubleshoot issues using Elastic OTel Node.js SDK.

* [PHP SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/php/index.md): Troubleshoot issues using Elastic OTel PHP agent.

* [Python SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/python/index.md): Troubleshoot issues using Elastic OTel Python agent.

## Shared troubleshooting topics

These guides apply to all Elastic OTel SDKs:

* [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md): Learn how to enable debug logging for Elastic OTel SDKs to troubleshoot application-level instrumentation issues.

* [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md): Diagnose lack of telemetry flow due to issues with Elastic OTel SDKs.

* [Proxy settings for Elastic OTel SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/proxy.md): Configure proxy settings for Elastic OTel SDKs when your application runs behind a proxy.

* [Missing or incomplete traces due to SDK sampling](/troubleshoot/ingest/opentelemetry/edot-sdks/misconfigured-sampling-sdk.md): Troubleshoot missing or incomplete traces caused by SDK-level sampling configuration.

* [Troubleshoot trace context header propagation](/troubleshoot/ingest/opentelemetry/edot-sdks/trace-context-propagation.md): Troubleshoot missing or broken distributed traces when combining OpenTelemetry instrumentation with Elastic {{product.apm}} agents.

## Supported architectures

Elastic OTel SDKs are tested and supported only with [{{agent}} Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md). Using Elastic OTel SDKs directly with {{apm-server}}'s OTel intake is not supported.

## See also

* [{{agent}} troubleshooting](/troubleshoot/ingest/opentelemetry/edot-collector/index.md): For end-to-end issues that may involve both the Collector and SDKs.

* [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md): Overview of all {{edot}} troubleshooting resources.

:::{warning}
Avoid using Elastic OTel SDKs alongside any other {{apm-agent}}, including Elastic {{product.apm}} agents. Running multiple agents in the same application process may lead to unexpected behavior, conflicting instrumentation, or duplicated telemetry.
:::
