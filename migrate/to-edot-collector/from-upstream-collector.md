---
navigation_title: Move from contrib OTel Collector
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: edot-collector
---

# Move from the contrib OpenTelemetry Collector to the {{edot}} Collector

The {{edot}} Collector is a curated distribution of the OpenTelemetry Collector, optimized for use with {{product.observability}}. If you're already running the contrib Collector, migrating to the {{edot}} Collector gives you:

- Pre-configured pipelines for common scenarios (standalone Linux/Windows, {{k8s}} DaemonSet/Gateway)
- Elastic-specific components not available in the contrib Collector, such as the `elasticsearchexporter` for native {{es}} ingestion and the `elasticapmconnector` for {{product.apm}} metrics aggregation
- Central management of Collector configuration through [OpAMP](opentelemetry://reference/central-configuration.md)
- Official Elastic support with SLAs

For a full comparison, refer to [EDOT compared to upstream OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md).

## Before you begin

- Review the [components included in the EDOT Collector](elastic-agent://reference/edot-collector/components.md) to confirm your required receivers, processors, and exporters are available.
- If you rely on a component not included in the {{edot}} Collector, you can [build a custom distribution](elastic-agent://reference/edot-collector/custom-collector.md) that adds it.

## Steps

:::::{stepper}

::::{step} Review your existing configuration

List the components your current Collector configuration uses:

- Receivers: data sources (for example OTLP, Prometheus, filelog, hostmetrics)
- Processors: transformations (batch, resource detection, attributes, and so on)
- Exporters: destinations (such as otlphttp to Elastic, {{es}} direct)
- Service pipelines: how components are wired together

Most standard contrib components are included in the EDOT Collector. Check the [components list](elastic-agent://reference/edot-collector/components.md) for any that aren't.

::::

::::{step} Install the EDOT Collector

Follow the [{{edot}} Collector setup guide](elastic-agent://reference/edot-collector/index.md) to download and install the EDOT Collector binary for your platform.

::::

::::{step} Adapt your configuration

The EDOT Collector uses the same YAML configuration format as the contrib Collector. You can use your existing configuration as a starting point.

**Replace the OTLP exporter with the {{es}} exporter (recommended for {{stack}} deployments)**

If you were exporting to {{es}} using an intermediate OTLP gateway, you can write directly to {{es}} using the `elasticsearchexporter`:

```yaml
exporters:
  elasticsearch:
    endpoint: "https://your-cluster:9200"
    api_key: "YOUR_API_KEY"
```

**Add the Elastic {{product.apm}} connector for traces ({{stack}} deployments)**

If you're collecting application traces, add the `elasticapmconnector` to generate {{product.apm}} metrics from span events. Without it, service and transaction metrics won't appear in the {{product.apm}} UIs:

```yaml
connectors:
  elasticapm:

processors:
  elasticapm:

service:
  pipelines:
    traces/in:
      receivers: [otlp]
      processors: [elasticapm]
      exporters: [elasticapm]
    traces/out:
      receivers: [elasticapm]
      processors: [batch]
      exporters: [elasticsearch]
    metrics:
      receivers: [elasticapm, otlp]
      processors: [batch]
      exporters: [elasticsearch]
```

Refer to the [default standalone configuration](elastic-agent://reference/edot-collector/config/default-config-standalone.md) as a reference for complete pipeline definitions.

**Use EDOT default configurations as a starting point (optional)**

If you're starting fresh or significantly restructuring, the EDOT Collector ships with default configurations for common scenarios that are ready to use with minimal changes. Refer to the [default configuration reference](elastic-agent://reference/edot-collector/config/default-config-standalone.md).

::::

::::{step} Validate the migration

Start the EDOT Collector with your updated config and verify:

1. The Collector starts without errors and reports healthy status.
2. Telemetry data (traces, metrics, logs) appears in the {{observability}} UIs in {{kib}}.
3. Existing dashboards and alerts continue to work as expected.

::::

:::::

## Next steps

- [Configure the {{edot}} Collector](elastic-agent://reference/edot-collector/config/default-config-standalone.md) for your deployment scenario
- [Enable central management](elastic-agent://reference/edot-collector/index.md) using OpAMP to manage Collector configuration from {{kib}}
- [Migrate deprecated components](elastic-agent://reference/edot-collector/components/migrate-components.md) if your configuration uses any components that have been superseded
