---
navigation_title: Hosts and VMs
description: Learn how to set up the {{agent}} and EDOT SDKs with Elastic Cloud Hosted to collect host metrics, logs, and application traces using the Managed OTLP Endpoint.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Quickstart for hosts and VMs on {{product.cloud-hosted}}

Learn how to set up the {{agent}} and EDOT SDKs on hosts and VMs with {{ech}} (ECH) to collect host metrics, logs, and application traces. This quickstart uses the [{{motlp}}](opentelemetry://reference/motlp.md), which is the recommended ingestion path for ECH.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

If you need to manage credentials manually, for example, to use them in automation or to configure multiple environments, follow the steps below.

## Prerequisites

- An {{ech}} deployment running version 9.0 or later.
- The host or VM running a supported operating system (Linux, macOS, or Windows).

## Manual installation

Follow these steps to deploy the {{agent}} and EDOT SDKs with ECH:

::::::{stepper}

:::::{step} Download the {{agent}}

[Download the {{agent}}](elastic-agent://reference/edot-collector/download.md) for your operating system.

:::::

:::::{step} Find your endpoint and create an API key

:::{include} ../../_snippets/retrieve-credentials-ech-motlp.md
:::

:::::

:::::{step} Configure the {{agent}}

Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following commands.

::::{tab-set}

:::{tab-item} Linux
```bash
ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} macOS
```bash
ELASTIC_OTLP_ENDPOINT=<ELASTIC_OTLP_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i '' "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} Windows
```powershell
Remove-Item -Path .\otel.yml -ErrorAction SilentlyContinue
Copy-Item .\otel_samples\managed_otlp\logs_metrics_traces.yml .\otel.yml
New-Item -ItemType Directory -Force -Path .\data\otelcol | Out-Null

$content = Get-Content .\otel.yml
$content = $content -replace '\${env:STORAGE_DIR}', "$PWD\data\otelcol"
$content = $content -replace '\${env:ELASTIC_OTLP_ENDPOINT}', "<ELASTIC_OTLP_ENDPOINT>"
$content = $content -replace '\${env:ELASTIC_API_KEY}', "<ELASTIC_API_KEY>"
$content | Set-Content .\otel.yml
```
:::
::::

For details about the pipelines, refer to [Using the Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-standalone.md#using-the-managed-otlp-endpoint).

:::::

:::::{step} Run the {{agent}}

Use the following command to start the {{agent}}.

::::{tab-set}

:::{tab-item} Linux and macOS
```bash
sudo ./otelcol --config otel.yml
```
:::

:::{tab-item} Windows
```powershell
.\elastic-agent.exe otel --config otel.yml
```
:::
::::

:::{note}
By default, the Collector opens ports `4317` and `4318` to receive application data from locally running EDOT SDKs.
:::

:::::

:::::{step} (Optional) Instrument your applications

To collect telemetry from applications and use the {{agent}} as a gateway, instrument your target applications following the setup instructions:

- [Android](apm-agent-android://reference/edot-android/index.md)
- [.NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
- [iOS](apm-agent-ios://reference/edot-ios/index.md)
- [Java](elastic-otel-java://reference/edot-java/setup/index.md)
- [Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
- [PHP](elastic-otel-php://reference/edot-php/setup/index.md)
- [Python](elastic-otel-python://reference/edot-python/setup/index.md)

Configure your SDKs to send the data to the local {{agent}} using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).

:::::

:::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

:::::
::::::

## Using the `elasticsearch` exporter

If you need to write telemetry directly to {{es}} using the `elasticsearch` exporter (for example, for pipeline customizations not yet supported through {{motlp}}), follow these steps. For a full list of features and limitations that apply to each path, refer to [Elastic features available with {{edot}}](opentelemetry://reference/compatibility/features.md).

:::{include} ../../_snippets/retrieve-credentials.md
:::

Replace `<ELASTICSEARCH_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following commands.

::::{tab-set}

:::{tab-item} Linux
```bash
ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_ENDPOINT}#${ELASTICSEARCH_ENDPOINT}#g" ./otel.yml && \
sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} macOS
```bash
ELASTICSEARCH_ENDPOINT=<ELASTICSEARCH_ENDPOINT> && \
ELASTIC_API_KEY=<ELASTIC_API_KEY> && \
cp ./otel_samples/logs_metrics_traces.yml ./otel.yml && \
mkdir -p ./data/otelcol && \
sed -i '' "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_ENDPOINT}#${ELASTICSEARCH_ENDPOINT}#g" ./otel.yml && \
sed -i '' "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml
```
:::

:::{tab-item} Windows
```powershell
Remove-Item -Path .\otel.yml -ErrorAction SilentlyContinue
Copy-Item .\otel_samples\logs_metrics_traces.yml .\otel.yml
New-Item -ItemType Directory -Force -Path .\data\otelcol | Out-Null

$content = Get-Content .\otel.yml
$content = $content -replace '\${env:STORAGE_DIR}', "$PWD\data\otelcol"
$content = $content -replace '\${env:ELASTIC_ENDPOINT}', "<ELASTICSEARCH_ENDPOINT>"
$content = $content -replace '\${env:ELASTIC_API_KEY}', "<ELASTIC_API_KEY>"
$content | Set-Content .\otel.yml
```
:::
::::

For details about the pipelines, refer to [Direct ingestion into {{es}}](elastic-agent://reference/edot-collector/config/default-config-standalone.md#direct-ingestion-into-elasticsearch).

## Troubleshooting

The following issues might occur.

### API key prefix not found

The following error is due to an improperly formatted API key, and typically occurs when credentials are configured manually:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

For a Collector, format the header as `"Authorization": "ApiKey <api-key>"`. For an SDK, format it as `"Authorization=ApiKey <api-key>"`.

For additional troubleshooting, refer to [Troubleshooting common issues with the {{agent}}](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md).
