---
navigation_title: Proxy issues
description: Troubleshooting guide for the EDOT Java SDK, covering proxy issues.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_java: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Proxy issues with EDOT Java SDK

If your Java SDK sends telemetry but fails to communicate with the APM server, the issue might be due to missing or misconfigured proxy settings, which are required for outbound HTTP/S communication in some environments. For general proxy configuration guidance, refer to [Proxy settings for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/proxy.md). For connectivity troubleshooting, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md).

## Symptoms

These symptoms typically indicate that your Java SDK is experiencing a proxy issue:

* Telemetry data is not received in Elastic APM after instrumenting the app.
* Logs show errors like `Connection timed out`, `TLS handshake failure`, or other network-related issues when connecting to Elastic APM.

## Resolution

Set standard Java system properties to configure proxy settings. 

Configure the following JVM system properties to enable outbound HTTP/HTTPS communication through a proxy:

```bash
java \
-Dhttp.proxyHost=proxy.example.com \
-Dhttp.proxyPort=8080 \
-Dhttps.proxyHost=proxy.example.com \
-Dhttps.proxyPort=8080 \
```

## Best practices

You can test end-to-end connectivity to validate proxy routing. To confirm that your application or collector can reach the endpoint through the proxy, use `curl` with the `--proxy` option:

```bash
curl --proxy http://proxy.example.com:8080 https://example.elastic.co
```

If the proxy is working, you'll get a valid response. If not, common errors include:

* `Connection timed out`
* `Could not resolve host`
* `Proxy CONNECT aborted`

## Resources

* [Java networking and proxies](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.html)
* [Java agent configuration - upstream documentation](https://opentelemetry.io/docs/zero-code/java/agent/configuration/)