---
navigation_title: Proxy settings
description: Configuration of the EDOT SDKs proxy settings.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Proxy settings for EDOT SDKs

EDOT SDKs generally use the standard proxy environment variables. However, there are exceptions and limitations depending on the language and exporter type. For general connectivity troubleshooting, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md).

## Python SDK

The Python SDK honors `HTTP_PROXY` and `HTTPS_PROXY` only when using the `http/protobuf` exporter.

If you use the default gRPC-based exporter, proxy settings are ignored. To enable proxy support, you can either:

* Switch to the `http/protobuf` exporter, which supports standard proxy environment variables.

* Route telemetry through a local EDOT Collector configured with proxy settings.

## Node.js SDK

The Node.js SDK does not currently support `HTTP_PROXY`, `HTTPS_PROXY`, or `NO_PROXY` by default. You can route telemetry through an EDOT Collector.

## Java SDK

If you're using Java SDK, you must configure Java system properties using the Java Virtual Machine (JVM). Refer to [Troubleshooting Java SDK proxy issues](/troubleshoot/ingest/opentelemetry/edot-sdks/java/proxy-issues.md) for more information.

## Other SDKs

Other EDOT SDKs honor standard proxy environment variables with no additional setup required. For example:

```
export HTTP_PROXY=http://<proxy.address>:<port>
export HTTPS_PROXY=http://<proxy.address>:<port>
```