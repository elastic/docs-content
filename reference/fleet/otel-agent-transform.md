---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/otel-agent-transform.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
  - id: edot-collector
---

# Transform an installed {{agent}} to run as an EDOT Collector [otel-agent-transform]

If you have a currently installed standalone {{agent}}, you can configure it to run as an [Elastic Distribution of OpenTelemetry Collector](otel-agent.md). This allows you to run {{agent}} both as a service and in an OTel Collector mode.

To configure an installed standalone {{agent}} to run as an OTel Collector, include a valid [OTel Collector](otel-agent.md) configuration in the `elastic-agent.yml` file, as shown in the following example.

## Example: Configure {{agent}} to ingest host logs and metrics into Elasticsearch using the OTel Collector [_example_configure_agent_to_ingest_host_logs_and_metrics_into_elasticsearch_using_the_otel_collector]

### Prerequisites

To ingest host logs and metrics into Elasticsearch using the OTel Collector, you need the following:

1. A suitable [{{es}} API key](grant-access-to-elasticsearch.md#create-api-key-standalone-agent) for authenticating on Elasticsearch.
2. An installed standalone {{agent}}.
3. A valid OTel Collector configuration. This example uses the OTel sample configuration included in the {{agent}} repository: `otel_samples/platformlogs_hostmetrics.yml`.

    * [Linux version](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/samples/linux/platformlogs_hostmetrics.yml)
    * [MacOS version](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/samples/darwin/platformlogs_hostmetrics.yml)

### Steps

To change a running standalone {{agent}} to run as an OTel Collector:

1. Create a directory where the OTel Collector can save its state. This example uses `<Elastic Agent install directory>/data/otelcol`.
2. Open the `<Elastic Agent install directory>/otel_samples/platformlogs_hostmetrics.yml` file for editing.
3. Set the environment variables to be used by the OTel Collector:

    * **Option 1:** Define environment variables for the {{agent}} service:

        * `ELASTIC_ENDPOINT`: The URL of the {{es}} instance where data will be sent
        * `ELASTIC_API_KEY`: The API Key to use to authenticate with {{es}}
        * `STORAGE_DIR`: The directory where the OTel Collector can persist its state

    * **Option 2:** Replace the environment variable references in the sample configuration with the corresponding values:

        * `${env:ELASTIC_ENDPOINT}`:The URL of the {{es}} instance where data will be sent
        * `${env:ELASTIC_API_KEY}`: The API Key to use to authenticate with {{es}}
        * `${env:STORAGE_DIR}`: The directory where the OTel Collector can persist its state

4. Save the OTel configuration as `elastic-agent.yml`, overwriting the default configuration of the installed agent.
5. Run the `elastic-agent status` command to verify that the new configuration has been correctly applied:

    ```shell
    elastic-agent status
    ```

    The OTel Collector running configuration appears under `elastic-agent` key (note the `extensions` and `pipeline` keys):

    ```shell
    ┌─ fleet
    │  └─ status: (STOPPED) Not enrolled into Fleet
    └─ elastic-agent
       ├─ status: (HEALTHY) Running
       ├─ extensions
       │  ├─ status: StatusOK
       │  └─ extension:file_storage
       │     └─ status: StatusOK
       ├─ pipeline:logs/platformlogs
       │  ├─ status: StatusOK
       │  ├─ exporter:elasticsearch/otel
       │  │  └─ status: StatusOK
       │  ├─ processor:resourcedetection
       │  │  └─ status: StatusOK
       │  └─ receiver:filelog/platformlogs
       │     └─ status: StatusOK
       └─ pipeline:metrics/hostmetrics
          ├─ status: StatusOK
          ├─ exporter:elasticsearch/ecs
          │  └─ status: StatusOK
          ├─ processor:attributes/dataset
          │  └─ status: StatusOK
          ├─ processor:elasticinframetrics
          │  └─ status: StatusOK
          ├─ processor:resource/process
          │  └─ status: StatusOK
          ├─ processor:resourcedetection
          │  └─ status: StatusOK
          └─ receiver:hostmetrics/system
             └─ status: StatusOK
    ```

Host logs and metrics are now being collected and ingested by the {{agent}} service running an OTel Collector instance. For further details about OpenTelemetry Collector components supported by {{agent}}, refer to [Components](elastic-agent://reference/edot-collector/components.md).
