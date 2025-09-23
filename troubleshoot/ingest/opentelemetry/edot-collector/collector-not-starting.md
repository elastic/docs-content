---
navigation_title: Collector doesn't start
description: Learn what to do when the EDOT Collector doesn’t start.
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

# EDOT Collector doesn’t start


If your EDOT Collector fails to start, it's often due to configuration or environment-related issues. This guide walks you through the most common root causes and how to resolve them.

## Symptoms   

EDOT Collector fails to start or crashes immediately after launch.

Possible causes include:

* Invalid YAML configuration, including syntax errors or unsupported fields
* Port binding conflicts, for example ports 4317 or 4318 already in use
* Missing or misconfigured required components, such as `receivers` or `exporters`  
* Incorrect permissions or volume mounts in containerized environments

## Resolution

The solution depends on your EDOT Collector's setup:

* [Standalone](#standalone-edot-collector)
* [Kubernetes](#kubernetes-edot-collector)

### Standalone EDOT Collector

If you're deploying the EDOT Collector in a standalone configuration, try to:

* Validate configuration syntax

   Run the following to validate your configuration without starting the Collector:

   ```bash
   otelcol validate --config=/path/to/otel-collector-config.yaml
   ```
   
   This checks for syntax errors and missing components. 

* Check logs for stack traces or component errors
   
   Review the Collector logs for error messages indicating configuration problems. Common examples include:

   ```
   error initializing exporter: no endpoint specified
   ```
   
   Most critical issues, such as missing or invalid exporters or receivers, will be logged.
   
   To increase verbosity, run:
   
   ```bash
   ./otelcol --set=service.telemetry.logs.level=debug
   ```

   This is especially helpful for diagnosing configuration parsing issues or startup errors.


* Confirm required components are defined

   Ensure `service.pipelines` references valid `receivers`, `processors`, and `exporters`. The minimal configuration depends on your use case:
   
   * **For logs**: `filelog` receiver, `resourcedetection` processor, `elasticsearch` exporter
   
   * **For traces**: `otlp` receiver, `elastictrace` and `elasticapm` processors, `elasticsearch` exporter
   
   * **For managed OTLP endpoint**: use relevant receivers and export using the `otlp` exporter
   
   Refer to [Default configuration of the EDOT Collector (Standalone)](elastic-agent://reference/edot-collector/config/default-config-standalone.md) for full examples for each use case.


* Check for port conflicts

   By default, EDOT uses:
   
   * 4317 for OTLP/gRPC
   * 4318 for OTLP/HTTP
   
   Run this to check if a port is in use:

   ```bash
   lsof -i :4317
   ```

   If needed, adjust your configuration or free up the port.

### Kubernetes EDOT Collector

If you're deploying the EDOT Collector using the Elastic Helm charts, try to:

* Double-check your custom `values.yaml` or -`-set` overrides for typos or missing fields.

* Ensure volume mounts are correctly defined if you're using custom configuration files.

* If you're managing the Collector through {{fleet}}, confirm that the policy includes a valid configuration and hasn't been corrupted or partially applied.

* Use `kubectl logs <collector-pod>` to get Collector logs and diagnose startup failures.

* Check the status of the pod using:

    ```bash
    kubectl describe pod <collector-pod>
    ```

  Common issues include volume mount errors, image pull failures, or misconfigured environment variables.

## Resources

* [Collector configuration documentation](https://opentelemetry.io/docs/collector/configuration/)
* [Elastic Stack Kubernetes Helm Charts](https://github.com/elastic/helm-charts)