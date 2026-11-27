---
navigation_title: Upstream OpenTelemetry Collector
description: Send data from an upstream OpenTelemetry Collector to a self-managed Elastic Stack by routing it through an {{agent}} gateway.
applies_to:
  deployment:
    self: ga 9.2+
products:
  - id: observability
  - id: edot-collector
---

# Send data from an upstream OpenTelemetry Collector [upstream-collector-self-managed]

This guide shows how to forward telemetry data from an existing (upstream) OpenTelemetry Collector to a self-managed {{stack}} using an [{{edot}} {{agent}}](elastic-agent://reference/edot-collector/index.md) configured as a gateway. The examples use the [contrib distribution](https://github.com/open-telemetry/opentelemetry-collector-releases/tree/main/distributions/otelcol-contrib) (`otelcol-contrib`), but the same approach works with any OTel Collector distribution, including vendor distributions and custom builds assembled with the [OpenTelemetry Collector Builder](https://opentelemetry.io/docs/collector/custom-collector/).

## When to use this setup

Use this setup if you:

* Already run an existing OpenTelemetry Collector and want to add Elastic as a backend without replacing your current setup
* Need to send telemetry to multiple observability backends from a single Collector
* Evaluate Elastic alongside another backend before committing to a full migration
* Use a technology or language for which Elastic doesn't provide an EDOT SDK

## Architecture

Your services send telemetry to an OpenTelemetry Collector (for example, `otelcol-contrib`), which forwards it over OTLP/gRPC to the {{agent}} gateway. The gateway applies Elastic-specific processing and writes directly to {{es}}.

```mermaid
flowchart LR
    S["Your services"] -->|OTLP| U["Upstream otelcol-contrib<br/>(one per host)"]
    U -->|"OTLP/gRPC :4317"| G

    subgraph G["Elastic Agent (gateway)"]
        P["elasticapm processor<br/>enriches spans"]
        C["elasticapm connector<br/>generates aggregated metrics"]
    end

    G -->|"traces and logs<br/>elasticsearch exporter<br/>mapping.mode: otel"| E[("Elasticsearch")]
    G -->|"metrics<br/>OTLP/HTTP exporter<br/>to /_otlp"| E
```

The gateway is the only component in this setup that writes to {{es}}, and it uses one exporter per destination API. The `elasticsearch` exporter writes traces and logs through the [bulk API]({{es-apis}}operation/operation-bulk) with `mapping.mode: otel`. The OTLP/HTTP exporter writes metrics to the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) on the `/_otlp` path. Both produce OTel-native documents.

Neither destination enriches traces or produces {{product.apm}} metrics on the {{es}} side, so the `elasticapm` processor and connector run in the gateway pipelines before the export.

:::{note}
The [{{motlp}}](/reference/managed-inputs/managed-otlp-endpoint.md) is an alternative ingest path available only on {{ecloud}}, so it doesn't apply to self-managed deployments. It's a separate ingestion host and isn't the same as the cluster's `/_otlp` paths. Sending directly to {{apm-server-or-mis}} through OTLP is also possible, but the {{edot}} gateway path in this guide is recommended for full {{product.apm}} functionality.
:::

## Before you begin

You’ll need:

* A running [self-managed](/deploy-manage/deploy/self-managed.md) {{es}} cluster
* The {{agent}} installed on the gateway host. It ships as part of the {{agent}} package and runs as {{agent}} in `otel` mode.
* An existing OpenTelemetry Collector installed on your agent hosts. This guide uses [`otelcol-contrib`](https://opentelemetry.io/docs/collector/installation/).
* Network connectivity from your Collector hosts to the {{edot}} gateway host on port 4317

## Set up the {{edot}} gateway [set-up-the-edot-gateway]

:::::{stepper}

::::{step} Create an {{es}} API key

The {{edot}} gateway authenticates to {{es}} using an API key.

1. Find **API keys** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create API key**.
3. Give the key a name (for example, `edot-gateway`) and assign it `auto_configure` and `create_doc` index privileges on the `logs-*.otel-*`, `metrics-*.otel-*`, and `traces-*.otel-*` indices.

    {applies_to}`stack: ga 9.6+` Add `exemplars-*.otel-*` as well. The `/_otlp` endpoint writes [metric exemplars](/manage-data/ingest/otlp-endpoint.md#metric-exemplars) to those data streams. Without the privilege, metric data points are still indexed, but their exemplars are rejected and each response reports a warning.

4. Copy the encoded key to use as the value of the `ELASTIC_API_KEY` environment variable in the gateway configuration.

::::

::::{step} Configure the {{edot}} gateway

1. Set the following environment variables on the gateway host before starting the Collector:

    ```bash
    export ELASTIC_ENDPOINT=https://your-elasticsearch:9200
    export ELASTIC_API_KEY=your-encoded-api-key
    ```

2. Create the following configuration file and save it as `gateway.yml` on the gateway host:

    ```yaml
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    connectors:
      elasticapm: {}

    processors:
      elasticapm: {}

    exporters:
      elasticsearch/otel:
        endpoints:
          - ${env:ELASTIC_ENDPOINT}
        api_key: ${env:ELASTIC_API_KEY}
        mapping:
          mode: otel
      # Elasticsearch exposes OTLP over HTTP only (no gRPC), on the /_otlp path.
      # The exporter appends the signal path (/v1/metrics) to the endpoint.
      otlp_http/ingest_metrics:
        endpoint: ${env:ELASTIC_ENDPOINT}/_otlp
        headers:
          Authorization: ApiKey ${env:ELASTIC_API_KEY}
        sending_queue:
          enabled: true
          sizer: bytes
          queue_size: 50000000 # 50MB uncompressed
          block_on_overflow: true
        timeout: 15s

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [elasticapm]
          exporters: [elasticapm, elasticsearch/otel]
        metrics:
          receivers: [otlp]
          processors: []
          exporters: [otlp_http/ingest_metrics]
        metrics/aggregated-otel-metrics:
          receivers: [elasticapm]
          processors: []
          exporters: [otlp_http/ingest_metrics]
        logs:
          receivers: [otlp]
          processors: []
          exporters: [elasticsearch/otel]
    ```

    Key components in this configuration:

    * **`elasticapm` processor** (under `processors`): Enriches spans with attributes required by the {{product.apm}} UI.
    * **`elasticapm` connector** (under `connectors`): Generates pre-aggregated {{product.apm}} metrics from trace data. It appears as an exporter in the `traces` pipeline and as a receiver in the `metrics/aggregated-otel-metrics` pipeline.
    * **`elasticsearch/otel` exporter**: Writes traces and logs to {{es}} through the [bulk API]({{es-apis}}operation/operation-bulk), using native OpenTelemetry data streams (`mapping.mode: otel`). The exporter handles batching automatically using `sending_queue`. To customize throughput for your environment, refer to [Performance and batching](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md#performance-and-batching).
    * **`otlp_http/ingest_metrics` exporter**: Writes metrics, including the pre-aggregated {{product.apm}} metrics from the connector, to the [{{es}} OTLP/HTTP endpoint](/manage-data/ingest/otlp-endpoint.md) on the `/_otlp` path. The endpoint derives time series data streams, dimensions, and metric mappings from the OTLP metadata.

    {applies_to}`edot_collector: ga 9.6+` This split matches the gateway sample configuration that ships with {{agent}}.

    {applies_to}`edot_collector: ga 9.2-9.5` The gateway sample configurations for these versions export every signal through `elasticsearch/otel`. To match them, remove `otlp_http/ingest_metrics` and use `elasticsearch/otel` in the `metrics` and `metrics/aggregated-otel-metrics` pipelines.

    :::{note}
    The `elasticapm` connector and processor are required for full {{product.apm}} functionality (service maps, transaction histograms, service-level indicators). Run them in the gateway whenever the gateway writes to {{es}} itself, with either exporter: the `/_otlp` endpoint stores records as they arrive, and so does the bulk API. If you send data to the {{motlp}} or {{apm-server-or-mis}} instead, they are not required.

    Refer to [{{product.apm}} services missing due to misconfigured elasticapm connector](/troubleshoot/ingest/opentelemetry/edot-collector/misconfigured-elasticapm-connector.md) for more information.
    :::

3. Start the {{edot}} gateway. The {{agent}} is the {{agent}} binary run in `otel` mode, so start it with the `otel` subcommand:

    ```bash
    elastic-agent otel --config gateway.yml
    ```

::::

::::{step} Configure the contrib Collector

1. Configure the OTLP exporter to point to the {{edot}} gateway. On each contrib Collector host, add or update the `exporters` and `service` sections in your existing `config.yml`:

    ```yaml
    exporters:
      otlp:
        endpoint: "gateway-host:4317"
        tls:
          insecure: true  # Set to `false` and configure `ca_file` for production

    service:
      pipelines:
        traces:
          exporters: [otlp]
        metrics:
          exporters: [otlp]
        logs:
          exporters: [otlp]
    ```

    Replace `gateway-host` with the hostname or IP of your {{edot}} gateway host. In production, set `insecure: false` and configure `ca_file` with the path to the CA certificate used to secure communication between the contrib Collector and the gateway. Refer to the [TLS configuration settings](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md) for the full list of options.

2. Set the `deployment.environment` resource attribute in your contrib Collector so that services appear under the correct environment in the {{kib}} {{product.apm}} Service Map. Without it, all services show as "unset" in the environment selector:

    ```yaml
    processors:
      resource:
        attributes:
          - key: deployment.environment
            action: insert
            value: production
    ```

    Refer to [Attributes and labels](/solutions/observability/apm/opentelemetry/attributes.md) for more details.

3. Restart the contrib Collector to apply the changes.

::::

::::{step} Verify data in {{kib}}

After starting both Collectors, wait a few minutes for data to appear. Then verify in {{kib}}:

* Find **Applications** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Services** to confirm your services appear.
* From **Applications**, go to **Service Map** to confirm environment-based filtering works.
* Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and check the `traces-generic.otel-default`, `logs-generic.otel-default`, and `metrics-generic.otel-default` data streams for incoming data.

If no data appears, refer to [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md) for troubleshooting tips.

::::

:::::

## Related pages

* [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md)
* [{{product.apm}} services missing due to misconfigured elasticapm connector](/troubleshoot/ingest/opentelemetry/edot-collector/misconfigured-elasticapm-connector.md)
* [Attributes and labels](/solutions/observability/apm/opentelemetry/attributes.md)
* [{{agent}}](elastic-agent://reference/edot-collector/index.md)
* [{{motlp}}](/reference/managed-inputs/managed-otlp-endpoint.md)
