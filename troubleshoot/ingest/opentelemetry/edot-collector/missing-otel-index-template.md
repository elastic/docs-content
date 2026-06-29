---
navigation_title: generic.otel template missing
description: Troubleshoot silent ingest failure when the `generic.otel` index template is missing or misconfigured in Elasticsearch.
applies_to:
  stack: ga
  serverless:
    observability: ga
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# {{es}} `generic.otel` index template missing or misconfigured [missing-otel-index-template]

When using the `elasticsearch` exporter with `mapping.mode: otel`, telemetry is written to the `generic.otel` data streams. If the backing index template is absent or misconfigured, ingest silently fails, which means that the Collector pipeline reports success, but no data appears in {{kib}}.

## Symptoms

* The Collector reports successful telemetry export with no errors in logs
* No data appears in {{kib}} {{product.apm}} or Discover
* The `logs-generic.otel-*`, `metrics-generic.otel-*`, or `traces-generic.otel-*` data streams are empty or absent
* {{es}} returns mapping errors on direct data stream queries

## Causes

<!-- TODO: SME confirmation needed — who installs the generic.otel templates (EDOT Collector on first run? {{fleet}}? ES itself?) and what triggers reinstallation? -->
* The template is not installed yet. On a fresh {{es}} installation where EDOT has not yet run successfully, the `generic.otel` templates might be missing.
* If the `elasticsearch` exporter is configured without `mapping.mode: otel`, data is written to the default {{es}} templates instead of the `generic.otel` ones. This can cause mapping conflicts or route data to unexpected indices.

## Resolution

::::{stepper}

:::{step} Verify the index template is installed

Run the following queries in {{kib}} **Dev Tools** or in the {{es}} API:

```bash
GET _index_template/logs-generic.otel
GET _component_template/generic.otel@mappings
```

If either one returns a 404, it means that the template is missing. Continue to [Reinstall the index template](#reinstall-the-index-template).

If both return results, the template is present. Skip to step 3 (*Verify `mapping.mode: otel` is set on the exporter*).
:::

:::{step} Reinstall the index template

<!-- TODO: SME confirmation needed — what are the exact steps to reinstall or repair the generic.otel template? Is it a Collector restart, a Fleet policy push, or a manual ES API call? -->

Restart the EDOT Collector to trigger template bootstrapping. If the Collector connects to {{es}} successfully on startup, it installs the required templates automatically.

If the template is still missing after a restart, contact [Elastic Support](https://www.elastic.co/support) to get help with manual template installation.
:::

:::{step} Verify `mapping.mode: otel` is set on the exporter

Check your Collector configuration and confirm the `elasticsearch` exporter includes `mapping.mode: otel`:

```yaml
exporters:
  elasticsearch/otel:
    endpoints:
      - ${env:ELASTIC_ENDPOINT}
    api_key: ${env:ELASTIC_API_KEY}
    mapping:
      mode: otel
```

Without this setting, the exporter writes to the default {{es}} templates, bypassing `generic.otel` entirely. Data might appear in unexpected indices or fail silently due to mapping conflicts.
:::

:::{step} Confirm data is flowing

After verifying the template and exporter configuration, check for incoming data:

```bash
GET logs-generic.otel-default/_count
GET metrics-generic.otel-default/_count
GET traces-generic.otel-default/_count
```

A non-zero count confirms that data is reaching {{es}}. If counts remain zero, refer to [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md) for further diagnostics.
:::

::::