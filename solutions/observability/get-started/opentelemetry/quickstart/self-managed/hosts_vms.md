---
navigation_title: Hosts / VMs
description: Learn how to set up the EDOT Collector and EDOT SDKs to collect host metrics, logs and application traces.
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

# Quickstart for hosts / VMs on self-managed deployments

Learn how to set up the EDOT Collector and EDOT SDKs to collect host metrics, logs and application traces.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs.

::::::{stepper}

:::::{step} Download the EDOT Collector

[Download the EDOT Collector](elastic-agent://reference/edot-collector/download.md) for your operating system, extract the archive and move to the extracted directory.
:::::

:::::{step} Configure the EDOT Collector

Retrieve your [{{es}} endpoint](/solutions/elasticsearch-solution-project/search-connection-details.md) and [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) and replace `<ELASTICSEARCH_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following command.

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

:::::

:::::{step} Run the EDOT Collector

Run the following command to run the EDOT Collector.

:::{note}
The Collector will open the ports `4317` and `4318` to receive application data from locally running OTel SDKs.
:::

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
:::::

:::::{step} (Optional) Instrument your applications

To collect telemetry from applications and use the EDOT Collector as a gateway,
instrument your target applications following the setup instructions:

- [Android](apm-agent-android://reference/edot-android/index.md)
- [.NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
- [iOS](apm-agent-ios://reference/edot-ios/index.md)
- [Java](elastic-otel-java://reference/edot-java/setup/index.md)
- [Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
- [PHP](elastic-otel-php://reference/edot-php/setup/index.md)
- [Python](elastic-otel-python://reference/edot-python/setup/index.md)

Configure your SDKs to send the data to the local EDOT Collector using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).

:::{tip}
Activate Central Configuration to configure your EDOT SDKs from within {{product.kibana}}. Refer to [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md).
:::
:::::

:::::{step} Install the content pack

Install the **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integration in {{kib}}.

:::::

:::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

:::::
::::::

## Troubleshooting

Having issues with EDOT? Refer to the [Troubleshooting common issues with the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md) for help.