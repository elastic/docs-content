---
navigation_title: EDOT Collector
description: Troubleshooting common issues with the EDOT Collector.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Troubleshoot the EDOT Collector

Use the topics in this section to troubleshoot issues with the EDOT Collector.

:::{tip}
If you're sending EDOT SDK telemetry directly to {{apm-server}}'s OTel intake, keep in mind that this flow is not supported. Send data to an [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md) instead.
:::

If you're not sure where to start, review the Collector's logs for error messages and validate your configuration using the `--dry-run` option. For more detailed diagnostics, refer to [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md).

## Resource issues

* [Collector out of memory](/troubleshoot/ingest/opentelemetry/edot-collector/collector-oomkilled.md): Diagnose and resolve out-of-memory issues in the EDOT Collector using Go's Performance Profiler.

* [Insufficient resources in {{k8s}}](/troubleshoot/ingest/opentelemetry/edot-collector/insufficient-resources-kubestack.md): Troubleshoot resource allocation issues when running the EDOT Collector in {{k8s}} environments.

## Configuration issues

* [Collector doesn't start](/troubleshoot/ingest/opentelemetry/edot-collector/collector-not-starting.md): Resolve startup failures caused by invalid configuration, port conflicts, or missing components.

* [Missing or incomplete traces due to Collector sampling](/troubleshoot/ingest/opentelemetry/edot-collector/misconfigured-sampling-collector.md): Troubleshoot missing or incomplete traces caused by sampling configuration.

* [Collector doesn't propagate client metadata](/troubleshoot/ingest/opentelemetry/edot-collector/metadata.md): Learn why the Collector doesn't extract custom attributes and how to propagate such values using EDOT SDKs.

## Connectivity and export issues

* [Export failures when sending telemetry data](/troubleshoot/ingest/opentelemetry/edot-collector/trace-export-errors.md): Resolve export failures caused by `sending_queue` overflow and {{es}} exporter timeouts.

## Debugging

* [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md): Learn how to enable debug logging for the EDOT Collector in supported environments.

## See also

* [EDOT SDKs troubleshooting](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md): For end-to-end issues that may involve both the Collector and SDKs.

* [Troubleshoot EDOT](/troubleshoot/ingest/opentelemetry/index.md): Overview of all EDOT troubleshooting resources.

For in-depth details on troubleshooting, refer to the contrib [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/).
