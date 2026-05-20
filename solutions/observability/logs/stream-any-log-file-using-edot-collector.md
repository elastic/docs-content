---
navigation_title: Send any log file using OTel Collector
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-stream-edot.html
  - https://www.elastic.co/guide/en/serverless/current/observability-stream-log-files-edot.html
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
  - id: cloud-serverless
---

# Send any log file using OTel Collector [logs-stream-edot]

This guide shows you how to manually configure the {{edot}} (EDOT) Collector to send your log data to {{es}} by configuring the `otel.yml` file. For an Elastic Agent equivalent, refer to [Send any log file using {{agent}}](/solutions/observability/logs/stream-any-log-file.md).

For more OpenTelemetry quickstarts, refer to [EDOT quickstarts](/solutions/observability/get-started/opentelemetry/quickstart/index.md).

## Prerequisites [logs-stream-edot-prereq]

::::{applies-switch}

:::{applies-item} stack:

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Because many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.
* Integrations Server (included by default in every {{ech}} deployment)

To get started quickly, create an {{ech}} deployment and host it on AWS, GCP, or Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).


:::

:::{applies-item} serverless:

The **Admin** role or higher is required to onboard log data. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

:::

::::

## Install the EDOT Collector [logs-stream-edot-install-config]

Complete these steps to install and configure the EDOT Collector and send your log data to Elastic Observability.

::::::{stepper}

:::::{step} Download and install the EDOT Collector

On your host, download the EDOT Collector installation package that corresponds with your system:

::::{tab-set}

:::{tab-item} Linux

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
```
:::

:::{tab-item} macOS

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf elastic-agent-{{version.stack}}-darwin-x86_64.tar.gz
```
:::

:::{tab-item} Windows

```powershell subs=true
# PowerShell 5.0+
wget https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-windows-x86_64.zip -OutFile elastic-agent-{{version.stack}}-windows-x86_64.zip
Expand-Archive .\elastic-agent-{{version.stack}}-windows-x86_64.zip
```
:::

::::
:::::

:::::{step} Configure the EDOT Collector

Follow these steps to retrieve the managed OTLP endpoint URL for your Serverless project:

1. In Elastic Cloud Serverless, open your Observability project.
2. Go to **Add data** → **Application** → **OpenTelemetry**.
3. Select **Managed OTLP Endpoint** in the second step.
4. Copy the OTLP endpoint configuration value.
5. Select **Create API Key** to generate an API key.

Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` before applying the following commands:

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
:::::

:::::{step} Configure log file collection

To collect logs from specific log files, you need to modify the `otel.yml` configuration file. The configuration includes receivers, processors, and exporters that handle log data.

::::{applies-switch}

:::{applies-item} stack:

Here's an example configuration for collecting log files with Elastic Stack:

:::{dropdown} otel.yml for logs collection (Elastic Stack)

```yaml
receivers:
  # Receiver for platform specific log files
  filelog/platformlogs:
    include: [ /var/log/*.log ]
    retry_on_failure:
      enabled: true
    start_at: end
    storage: file_storage
#   start_at: beginning

extensions:
  file_storage:
    directory: ${env:STORAGE_DIR}

processors:
  resourcedetection:
    detectors: ["system"]
    system:
      hostname_sources: ["os"]
      resource_attributes:
        host.name:
          enabled: true
        host.id:
          enabled: false
        host.arch:
          enabled: true
        host.ip:
          enabled: true
        host.mac:
          enabled: true
        host.cpu.vendor.id:
          enabled: true
        host.cpu.family:
          enabled: true
        host.cpu.model.id:
          enabled: true
        host.cpu.model.name:
          enabled: true
        host.cpu.stepping:
          enabled: true
        host.cpu.cache.l2.size:
          enabled: true
        os.description:
          enabled: true
        os.type:
          enabled: true

exporters:
  # Exporter to print the first 5 logs/metrics and then every 1000th
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 1000

  # Exporter to send logs and metrics to Elasticsearch
  elasticsearch/otel:
    endpoints: ["${env:ELASTIC_ENDPOINT}"]
    api_key: ${env:ELASTIC_API_KEY}
    mapping:
      mode: otel

service:
  extensions: [file_storage]
  pipelines:
    logs/platformlogs:
      receivers: [filelog/platformlogs]
      processors: [resourcedetection]
      exporters: [debug, elasticsearch/otel]
```

:::
:::

:::{applies-item} serverless:

Here's an example configuration for collecting log files with Elastic Cloud Serverless:

:::{dropdown} otel.yml for logs collection (Serverless)

```yaml
receivers:
  # Receiver for platform specific log files
  filelog/platformlogs:
    include: [/var/log/*.log]
    retry_on_failure:
      enabled: true
    start_at: end
    storage: file_storage
#   start_at: beginning

extensions:
  file_storage:
    directory: ${env:STORAGE_DIR}

processors:
  resourcedetection:
    detectors: ["system"]
    system:
      hostname_sources: ["os"]
      resource_attributes:
        host.name:
          enabled: true
        host.id:
          enabled: false
        host.arch:
          enabled: true
        host.ip:
          enabled: true
        host.mac:
          enabled: true
        host.cpu.vendor.id:
          enabled: true
        host.cpu.family:
          enabled: true
        host.cpu.model.id:
          enabled: true
        host.cpu.model.name:
          enabled: true
        host.cpu.stepping:
          enabled: true
        host.cpu.cache.l2.size:
          enabled: true
        os.description:
          enabled: true
        os.type:
          enabled: true

exporters:
  # Exporter to print the first 5 logs/metrics and then every 1000th
  debug:
    verbosity: detailed
    sampling_initial: 5
    sampling_thereafter: 1000

  # Exporter to send logs and metrics to Elasticsearch Managed OTLP Input
  otlp/ingest:
    endpoint: ${env:ELASTIC_OTLP_ENDPOINT}
    headers:
      Authorization: ApiKey ${env:ELASTIC_API_KEY}

service:
  extensions: [file_storage]
  pipelines:
    logs/platformlogs:
      receivers: [filelog/platformlogs]
      processors: [resourcedetection]
      exporters: [debug, otlp/ingest]
```
:::
:::
::::

Key configuration elements:

* `receivers.filelog/platformlogs.include`: Specifies the path to your log files. You can use patterns like `/var/log/*.log`.
* `processors.resourcedetection`: Automatically detects and adds host system information to your logs.
* `extensions.file_storage`: Provides persistent storage for the Collector's state.
* `exporters`: Configures how data is sent to Elasticsearch (Elastic Stack) or OTLP endpoint (Serverless).
:::::

:::::{step} Run the EDOT Collector

Run the following command to run the EDOT Collector:

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
The Collector opens ports `4317` and `4318` to receive application data from locally running OTel SDKs without authentication. This allows the SDKs to send data without any further configuration needed as they use this endpoint by default.
:::
:::::
::::::

## Troubleshoot your EDOT Collector configuration [logs-stream-edot-troubleshooting]

If you're not seeing your log files in the UI, verify the following:

* The path to your logs file under `include` is correct.
* Your API key is properly set in the environment variables.
* The OTLP endpoint URL is correct and accessible.
* The Collector is running without errors (check the console output).

If you're still running into issues, see [EDOT Collector troubleshooting](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Configure EDOT Collector](elastic-agent://reference/edot-collector/config/index.md).

## Next steps [logs-stream-edot-next-steps]

After you have your EDOT Collector configured and are streaming log data to {{es}}:

* Refer to the [Explore log data](/solutions/observability/logs/discover-logs.md) documentation for information on exploring your log data in the UI, including searching and filtering your log data, getting information about the structure of log fields, and displaying your findings in a visualization.
* Refer to the [Parse and organize logs](/solutions/observability/logs/parse-route-logs.md) documentation for information on extracting structured fields from your log data, rerouting your logs to different data streams, and filtering and aggregating your log data.
* Refer to the [Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md) documentation for information on filtering and aggregating your log data to find specific information, gain insight, and monitor your systems more efficiently.
* To collect telemetry from applications and use the EDOT Collector as a gateway, instrument your target applications following the setup instructions:
  - [Android](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/android/)
  - [.NET](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/dotnet/setup/)
  - [iOS](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/ios/)
  - [Java](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/java/setup/)
  - [Node.js](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/nodejs/setup/)
  - [PHP](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/php/setup/)
  - [Python](https://www.elastic.co/docs/reference/opentelemetry/edot-sdks/python/setup/)