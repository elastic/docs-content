---
navigation_title: elasticapm connector misconfigured
description: Troubleshoot missing APM services and metrics in Kibana when the elasticapm connector is incorrectly placed under processors instead of connectors in your OTel Collector configuration.
applies_to:
  serverless: ga
  product:
    edot_collector: ga
products:
  - id: observability
  - id: edot-collector
---

# {{product.apm}} services missing due to misconfigured `elasticapmconnector`

If {{product.apm}} services and metrics don't appear in {{kib}} despite a healthy-looking traces pipeline, check the `elasticapmconnector` for misconfiguration. This is one of the most common causes of a silent, empty {{product.apm}} UI when using the EDOT Collector with direct {{es}} ingestion.

:::{note}
This page applies when exporting directly to {{es}} using the `elasticsearch` exporter (typically with `mapping.mode: otel`). If you're sending data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md) or {{apm-server-or-mis}} using OTLP, neither the `elasticapmprocessor` nor the `elasticapmconnector` is required.
:::

For general no-data troubleshooting, refer to [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

## Symptoms

The pipeline looks healthy, but no {{product.apm}} data reaches {{kib}}:

* Collector traces pipeline runs without errors
* Traces are exported successfully (no errors in the Collector logs)
* No {{product.apm}} services, transactions, or service map entries appear in {{kib}} {{product.apm}}
* {{product.apm}} metrics data streams remain empty

## Causes

There are two distinct `elasticapm` components in the EDOT Collector:

* **`elasticapm` processor**, which enriches OpenTelemetry spans with Elastic-specific attributes. Declare it under `processors`.
* **`elasticapm` connector**, which generates pre-aggregated {{product.apm}} metrics from trace data. Declare it under `connectors`. This component is used as an exporter in the `traces` pipeline, and as a receiver in a dedicated `metrics` pipeline.

A common misconfiguration is placing the connector under `processors` instead of `connectors`, or omitting the connector declaration entirely. Because the traces pipeline continues to function even without the connector, the Collector logs no errors. However, {{product.apm}} metrics are never produced, so service maps, transaction histograms, and service-level indicators don't appear in {{kib}}.

## Resolution

::::{stepper}

:::{step} Check that the connector is declared under `connectors`

Open your Collector configuration and confirm `elasticapm` appears under `connectors`, not only under `processors`:

```yaml
connectors:
  elasticapm: {}
```

:::

:::{step} Wire the connector as an exporter in `traces` and a receiver in `metrics` pipeline

The `elasticapmconnector` must appear in two places in `service.pipelines`: as an exporter in `traces` (to receive trace data and generate metrics) and as a receiver in a separate `metrics` pipeline (to forward those metrics to {{es}}):

```yaml
processors:
  elasticapm: {}  

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, elasticapm]         
      exporters: [elasticapm, elasticsearch/otel]  
    metrics/aggregated-otel-metrics:
      receivers: [elasticapm]                 
      processors: []
      exporters: [elasticsearch/otel]
```

For the complete configuration example, refer to [Elastic {{product.apm}} connector](elastic-agent://reference/edot-collector/components/elasticapmconnector.md).

:::

:::{step} Restart the Collector and verify

Restart the Collector after updating your configuration. Wait a few minutes for data to accumulate, then check {{kib}} {{product.apm}} for services and service maps.

:::

::::

If data still doesn't appear, refer to [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md) to increase Collector verbosity and check for export errors.

## Resources

* [Elastic {{product.apm}} connector reference](elastic-agent://reference/edot-collector/components/elasticapmconnector.md)
* [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md)
