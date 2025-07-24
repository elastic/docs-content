---
navigation_title: Contact support
description: Learn how to contact Elastic Support and what information to include to help resolve issues faster.
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

# Contact support

If you're unable to resolve an issue with the Elastic Distributions of OpenTelemetry (EDOT) using the troubleshooting guides, you can contact Elastic Support for further assistance.

Providing a clear description of your issue and relevant technical context helps our support engineers respond more quickly and effectively.

## What to include in your support request

To help Elastic Support investigate the problem efficiently, please include the following details whenever possible:

### Basic information

* A brief description of the issue
* When the issue started and whether it is intermittent or consistent
* Affected environments (dev, staging, production)
* Whether you’re using Elastic Cloud or self-managed deployments

### Deployment context

* Are you using a standalone EDOT Collector or Kubernetes?
* If applicable, include:
  * Helm chart version and values (for Kubernetes)
  * Container image version

### Configuration

* Your full or partial EDOT Collector configuration file or files, redacted as needed
* Any overrides or runtime flags, such as `--log-level=debug` or `--config` path
* Environment variables that may affect telemetry

### Logs and diagnostics

* Recent Collector logs with relevant errors or warning messages
* Output from:

  ```bash
  edot-collector --config=/path/to/config.yaml --dry-run
  ```
* Output from:

  ```bash
  lsof -i :4317
  kubectl logs <collector-pod>
  ```

### Data and UI symptoms

* Are traces, metrics, or logs missing from the UI?
* Are you using the [Elastic Managed OTLP endpoint](https://www.elastic.co/docs/observability/apm/otel/managed-otel-ingest/)?

## Next steps

When you’ve gathered the information above relevant to your case:

1. Log in to the [Elastic Support portal](https://support.elastic.co/)
2. Open a new case and fill in the form.
3. Attach your logs, configs, or example files. Redact sensitive data.

Our support team will review your request and get back to you as soon as possible.

