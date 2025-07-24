---
navigation_title: Enable debug logging
description: Learn how to enable debug logging for the EDOT Collector in supported environments.
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

# Enable debug logging

You can enable debug logging in the Elastic Distributions of OpenTelemetry (EDOT) Collector by setting the `--log-level=debug` flag. This is useful when troubleshooting startup issues or configuration problems.

This guide shows how to enable debug logging in different environments.

## Standalone EDOT Collector

If you're running the EDOT Collector directly, add the flag to your command:

```bash
edot-collector --config=/path/to/otel-collector-config.yaml --log-level=debug
```

This increases log verbosity and helps surface misconfigurations.

## Kubernetes (Helm deployment)

If you're deploying the EDOT Collector using the Elastic Helm charts, set the `logLevel` in your values file or CLI override:

```yaml
logLevel: debug
```

Example usage with `helm install`:

```bash
helm upgrade --install my-collector elastic/otel-collector \
--set logLevel=debug
```

This adds `--log-level=debug` to the Collector container’s command line.

## Other environments

Standalone and Kubernetes are currently the only officially supported deployment environments for the EDOT Collector.

However, if you're running the Collector in a different context, such as a manually containerized setup, you can still enable debug logging by passing the `--log-level=debug` flag as a runtime argument:

```bash
otel-collector --config=/path/to/config.yaml --log-level=debug
```

:::{{note}}
Debug logging for the Collector is not currently configurable through {{fleet}}.
:::


