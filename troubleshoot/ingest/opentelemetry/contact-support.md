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

In some cases, you may unable to resolve an issue with the Elastic Distributions of OpenTelemetry (EDOT) using the troubleshooting guides.

If you have an [Elastic subscription](https://www.elastic.co/pricing), you can contact Elastic support for assistance. You can reach us in the following ways:

* **Through the [Elastic Support Portal](https://support.elastic.co/):** The Elastic Support Portal is the central place where you can access all of your cases, subscriptions, and licenses.

* **By email:** [support@elastic.co](mailto:support@elastic.co)

  :::{tip}
  If you contact us by email, use the email address you registered with so we can help you more quickly. If your registered email is a distribution list, you can register a second email address with us. Just open a case to let us know the name and email address you want to add.
  :::

  :::{warning}
  All cases opened by email default to a normal severity level. For incidents, open a case through the [Elastic Support Portal](https://support.elastic.co/) and select the [appropriate severity](https://www.elastic.co/support/welcome#what-to-say-in-a-case).
  :::

Providing a clear description of your issue and relevant technical context helps our support engineers respond more quickly and effectively.

## What to include in your support request

To help Elastic Support investigate the problem efficiently, please include the following details whenever possible:

### Basic information

* A brief description of the issue
* When the issue started and whether it is intermittent or consistent
* Affected environments (dev, staging, production)
* Whether you’re using Elastic Cloud or self-managed deployments
* The version of the Elastic Stack you're using
* Any additional context to help support understand the full data flow (from the instrumented applications at the edge to {{es}})

### Deployment context

* Are you using a [standalone EDOT Collector](elastic-agent://reference/edot-collector/config/default-config-standalone.md) or [Kubernetes](elastic-agent://reference/edot-collector/config/default-config-k8s.md)?
* If applicable, include:
  * Helm chart version and values (for Kubernetes)
  * Container image version

### Configuration

* Your full or partial EDOT Collector configuration file or files, redacted as needed
* Environment variables that may affect telemetry
* Any overrides or runtime flags, such as `--log-level=debug` or `--config` path
* To enable debug logging in Kubernetes environments using the Helm chart, set the log level explicitly with:

  ```yaml
  collector:
    args:
      - "--config=/etc/otel/config.yaml"
      - "--log-level=debug"
  ```

  In Kubernetes environments with multiple EDOT Collector pods, be sure to collect logs and configuration from all instances. You can use `kubectl` to list and inspect each:

  ```sh
  kubectl get pods -l app=edot-collector
  kubectl logs <pod-name> --container edot-collector
  ```
  Repeat for each Collector pod to provide complete context for support.

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
* If data is missing or incomplete, consider enabling the [debug exporter](https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/debugexporter/README.md) to inspect the raw signal data emitted by the Collector. 

  You can use it for specific signals (logs, metrics, or traces) by adding a pipeline like:

  ```yaml
  exporters:
    debug:
      verbosity: detailed  # options: normal, detailed

  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [batch]
        exporters: [debug]
  ```

  This helps verify whether the Collector is receiving and processing telemetry as expected before it's sent to Elasticsearch.

## Next steps

When you’ve gathered the information above relevant to your case:

1. Log in to the [Elastic Support portal](https://support.elastic.co/)
2. Open a new case and fill in the form.
3. Attach your logs, configs, or example files. Redact sensitive data.

Our support team will review your request and get back to you as soon as possible.

