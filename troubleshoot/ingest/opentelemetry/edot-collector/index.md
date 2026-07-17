---
navigation_title: Elastic Agent
description: Troubleshooting common issues with the Elastic Agent.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Troubleshoot the {{agent}} [troubleshoot-the-edot-collector]

Use the topics in this section to troubleshoot issues with the {{agent}}.

If you're not sure where to start, review the Collector's logs for error messages and validate your configuration using the `--dry-run` option. For more detailed diagnostics, refer to [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md).

## Resource issues

* [Collector out of memory](/troubleshoot/ingest/opentelemetry/edot-collector/collector-oomkilled.md): Diagnose and resolve out-of-memory issues in the {{agent}} using Go's Performance Profiler.

* [Insufficient resources in {{k8s}}](/troubleshoot/ingest/opentelemetry/edot-collector/insufficient-resources-kubestack.md): Troubleshoot resource allocation issues when running the {{agent}} in {{k8s}} environments.

## Configuration issues

* [Collector doesn't start](/troubleshoot/ingest/opentelemetry/edot-collector/collector-not-starting.md): Resolve startup failures caused by invalid configuration, port conflicts, or missing components.

* [Missing or incomplete traces due to Collector sampling](/troubleshoot/ingest/opentelemetry/edot-collector/misconfigured-sampling-collector.md): Troubleshoot missing or incomplete traces caused by sampling configuration.

* [{{product.apm}} services missing due to misconfigured elasticapm connector](/troubleshoot/ingest/opentelemetry/edot-collector/misconfigured-elasticapm-connector.md): Resolve missing {{product.apm}} services and metrics caused by placing the `elasticapm` connector under `processors:` instead of `connectors:`.

* [Collector doesn't propagate client metadata](/troubleshoot/ingest/opentelemetry/edot-collector/metadata.md): Learn why the Collector doesn't extract custom attributes and how to propagate such values using Elastic OTel SDKs.

## Connectivity and export issues

* [Export failures when sending telemetry data](/troubleshoot/ingest/opentelemetry/edot-collector/trace-export-errors.md): Resolve export failures caused by `sending_queue` overflow and {{es}} exporter timeouts.

* [`ResourceExhausted` errors and decompression limits in Collector-to-Collector pipelines](/troubleshoot/ingest/opentelemetry/edot-collector/c2c-resourceexhausted.md): Troubleshoot `ResourceExhausted` errors caused by gRPC message size limits, decompression limits, memory pressure, or backpressure in Collector-to-Collector pipelines.

## Debugging

* [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md): Learn how to enable debug logging for the {{agent}} in supported environments.

## See also

* [Elastic OTel SDKs troubleshooting](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md): For end-to-end issues that may involve both the Collector and SDKs.

* [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md): Overview of all {{edot}} troubleshooting resources.

For in-depth details on troubleshooting, refer to the contrib [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/).
