---
navigation_title: EDOT iOS
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/swift/current/troubleshooting.html
description: Troubleshooting guide for the Elastic Distribution of OpenTelemetry (EDOT) iOS agent, covering common issues.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_ios: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT iOS agent [troubleshooting]

This page provides guidance for resolving common problems when instrumenting iOS applications with the {{edot}} (EDOT) SDK.

:::{tip}
If you're sending EDOT SDK telemetry directly to {{apm-server}}'s OTel intake, note that this flow is not supported. Send data to an [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md) instead.
:::

When troubleshooting the EDOT iOS agent, ensure your app is compatible with the agent’s [supported technologies](apm-agent-ios://reference/edot-ios/supported-technologies.md).


## SDK fails to export data

If your app is running but no telemetry reaches Elastic, the SDK might be failing to send data to the configured endpoint. For connectivity troubleshooting, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md). If telemetry data isn't appearing in {{kib}}, refer to [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md) or [No data visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

### Symptoms [symptoms-fail-to-export]

You might notice the following signs when the SDK cannot export data:

* No telemetry appears in Elastic.
* Application logs show errors such as:

  ```text
  [ElasticOtelExporter] Failed to send spans: Error Domain=NSURLErrorDomain Code=-1004 "Could not connect to the server"
  ```

* The OpenTelemetry Collector or Elastic endpoint shows no received data.

### Causes [causes-fail-to-export]

This usually happens if the iOS app cannot reach the configured OTLP endpoint due to:

* Incorrect endpoint URL or port.
* TLS/HTTPS certificate issues.
* Missing App Transport Security (ATS) configuration in `Info.plist`.

### Resolution [resolution-fail-to-export]

Try the following steps to resolve the issue:

* Verify the endpoint URL and port in your SDK configuration.
* If using HTTPS with self-signed certificates, add the certificate to the iOS trust store or configure ATS exceptions.
* Add required ATS exceptions to your app’s `Info.plist`. For example:

  ```xml
  <key>NSAppTransportSecurity</key>
  <dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
  </dict>
  ```


## No data when app is in the background

If data only appears while the app is in the foreground, the issue might be related to iOS background execution limits.

### Symptoms [symptoms-no-data]

The following behavior indicates that telemetry stops when the app moves to the background:

* Telemetry appears only when the app is in the foreground.

* Spans or metrics are missing after backgrounding the app.

### Causes [causes-no-data]

This issue can occur because of how iOS manages background tasks and network activity:

* iOS aggressively suspends background network activity. The SDK cannot flush telemetry if the app is suspended.

### Resolution [resolution-no-data]

Use the following recommendations to ensure data export continues as expected:

* Ensure that export intervals are short enough to flush before suspension.

* Use iOS background modes if appropriate for your app (for example `Background fetch`, `Background processing`).

* For crash or cold-start telemetry, rely on batching and retry when the app next resumes.


## Missing device or app metadata

If telemetry is sent but key attributes such as device model, OS version, or app version are missing, resource detection might not be working correctly.

### Symptoms [symptoms-missing-device]

You might encounter the following when resource detection is incomplete:

* Spans or metrics appear in Elastic, but expected resource attributes (for example device model, OS version, app version) are missing.

### Causes [causes-missing-device]

Common causes include turned off resource detectors or missing permissions:

* Resource detectors might not be enabled, or required permissions might not be granted.

### Resolution [resolution-missing-device]

To restore full metadata reporting, verify the following:

* Ensure the iOS resource detectors are enabled in the SDK initialization.

* Verify your build includes the `DeviceResourceDetector` and `OSResourceDetector`.

* Check privacy permissions (for example for network or device identifiers, if used).


## Crashes or startup delays after SDK initialization

If the app crashes or slows down significantly after integrating the SDK, initialization or exporter configuration might be the cause.

### Symptoms [symptoms-crash]

The following symptoms can indicate SDK-related performance or initialization issues:

* App crashes immediately after launching with the SDK enabled.

* Noticeable delays before the first screen appears.

### Causes [causes-crash]

Crashes or slow startup typically occur for one of these reasons:

* The SDK is initialized on the main thread with heavy configuration.

* Exporters are misconfigured and blocking startup.

### Resolution [resolution-crash]

Try these steps to resolve initialization and startup issues:

* Initialize the SDK on a background thread when possible.

* Use asynchronous exporters.

* Start with minimal configuration and gradually add exporters to isolate the issue.


## Next steps

If problems persist:

* Review the [iOS SDK reference documentation](apm-agent-ios://reference/edot-ios/index.md).

* [Enable debug logging for the Collector](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md) and [the SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).

  ::::{important}
  **Upload your complete debug logs** to a service like [GitHub Gist](https://gist.github.com) so that we can analyze the problem. Logs should include everything from when the application starts up until the first request executes.
  ::::

* If you’re an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm).

