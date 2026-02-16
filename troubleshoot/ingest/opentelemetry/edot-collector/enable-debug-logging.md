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

You can enable debug-level logging in the Elastic Distributions of OpenTelemetry (EDOT) Collector by either modifying the configuration file or passing a runtime override. This is useful when troubleshooting startup issues or configuration problems.

This guide shows how to enable debug logging in different environments.

## Standalone EDOT Collector

If you're running the EDOT Collector directly, you can choose between two approaches:

* [Configuration file](#configuration-file) - to persist debug logging across restarts
* [Temporary override: runtime flag](#temporary-override-runtime-flag) - for temporary debugging or quick tests

Both approaches increase log verbosity and help surface misconfigurations.

### Configuration file

Add the following section to your EDOT Collector configuration file (typically `otel.yml`):

```yaml
service:
  telemetry:
    logs:
      level: debug
```

This method works across all deployment environments.

### Temporary override: runtime flag

Pass the log level as a runtime argument using the `--set` flag:

```bash
otelcol --set=service.telemetry.logs.level=debug
```

This applies debug-level logging without modifying your configuration file.

## Kubernetes (Helm deployment)

If you're deploying the EDOT Collector using the OpenTelemetry Helm charts, enable debug logging by adding the configuration directly in your values.yaml file:

```yaml
config:
  service:
    telemetry:
      logs:
        level: debug
```

Alternatively, use a CLI override when installing or upgrading the [OpenTelemetry Collector Helm Chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-collector) release:

```bash subs=true
helm upgrade my-opentelemetry-collector open-telemetry/opentelemetry-collector --set mode=daemonset --set image.repository="docker.elastic.co/elastic-agent/elastic-otel-collector" --set image.tag="{{version.edot_collector}}" --set config.service.telemetry.logs.level=debug
```

This ensures the Collector logs at debug level when deployed into your cluster.

## Other environments

Standalone and Kubernetes are currently the only officially supported deployment environments for the EDOT Collector.

However, if you're running the Collector in a different context, such as a manually containerized setup, you can still enable debug logging using the same methods:

* Add it to your configuration file using the `service.telemetry.logs.level` setting

* Pass it at runtime with `--set=service.telemetry.logs.level=debug`

:::{{note}}
Debug logging for the Collector is not currently configurable through {{fleet}}.
:::


## Resources

To learn how to enable debug logging for the EDOT SDKs, refer to [Enable debug logging for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).
