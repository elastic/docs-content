---
navigation_title: Add internal telemetry
description: Add internal telemetry to an OpenTelemetry Collector monitored by Fleet.
type: how-to
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Add internal telemetry to an OTel Collector monitored by {{fleet}}

Monitor the health, resource usage, and pipeline performance of an OpenTelemetry (OTel) Collector in {{kib}} by sending its own metrics, logs, and traces to {{es}}. The collector emits this telemetry to its own OTLP (OpenTelemetry Protocol) receiver, which forwards it through a pipeline to {{es}}.

:::{note}
If you added your collector using the **Add collector** flow, the generated configuration already includes internal telemetry.
:::

## Before you begin

You'll need:

* An OTel Collector with OpAMP extension support, already added in {{fleet}}. For more information, refer to [Add an OTel Collector in Fleet](/reference/fleet/add-otel-collector.md).
* Access to your OTel Collector's configuration file
* An {{es}} API key with `create_index`, `write`, and `auto_configure` index privileges on `metrics-*`, `logs-*`, and `traces-*` data streams, or an existing exporter you can reuse for internal telemetry

## Configure internal telemetry components

To add internal telemetry to an existing collector configuration, extend it with the following components:

1. Configure the OTLP receiver:

    ```yaml
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318
    ```

2. Configure an exporter that sends telemetry to your {{es}} backend. If your collector already exports telemetry, you can reuse the existing exporter and add the OTLP receiver to its pipelines. Otherwise, configure the `elasticsearch/otel` exporter:

    ```yaml
    exporters:
      elasticsearch/otel:
        endpoints: [https://elasticsearch:9200] <1>
        api_key: "<es-api-key>" <2>
        mapping:
          mode: otel
    ```
    1. Replace with your {{es}} endpoint.
    2. Replace with an [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md).

    ::::{include} /reference/fleet/_snippets/otel-motlp-exporter-alternative.md
    ::::

3. Set up the service pipelines:

    ```yaml
    service:
      pipelines:
        metrics:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        logs:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
        traces:
          receivers: [otlp]
          exporters: [elasticsearch/otel]
    ```

4. Set up internal telemetry for the OTel Collector:

    ```yaml
    service:
      telemetry:
        resource:
          service.instance.id: "<instance-uid>" <1>
        metrics:
          level: detailed
          readers:
            - periodic:
                interval: 3000
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        logs:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
        traces:
          processors:
            - batch:
                exporter:
                  otlp:
                    protocol: grpc
                    endpoint: http://localhost:4317
    ```
    1. Replace with the UUID value provided in `extensions.opamp.instance_uid`.

5. Save your configuration, then start or restart the OTel Collector.

## Verify internal telemetry is flowing

When your collector is running, confirm that internal telemetry is reaching {{es}}:

1. The first time the collector ingests data, {{fleet}} automatically installs the **OTel Collector internal telemetry** dashboards in {{kib}}.
2. In {{kib}}, go to **Dashboards** and search for **OTel Collector internal telemetry**.
3. Open a dashboard and confirm that visualizations display your collector's metrics, logs, traces, resource usage, pipeline performance, and component health.

## Related pages

* [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md)
* [Troubleshoot OTel Collectors in Fleet](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet)
