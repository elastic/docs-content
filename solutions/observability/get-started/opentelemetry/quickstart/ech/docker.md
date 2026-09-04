---
navigation_title: Docker
description: Learn how to set up the {{agent}} and EDOT SDKs in a Docker environment with Elastic Cloud Hosted to collect host metrics, logs, and application traces using the Managed OTLP Endpoint.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Quickstart for Docker on {{product.cloud-hosted}}

Learn how to set up the {{agent}} and EDOT SDKs in a Docker environment with {{ech}} (ECH) to collect host metrics, logs, and application traces. This quickstart uses the [{{motlp}}](opentelemetry://reference/motlp.md), which is the recommended ingestion path for ECH.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

If you need to manage credentials manually, for example, to use them in automation or to configure multiple environments, follow the steps below.

## Prerequisites

- An {{ech}} deployment running version 9.0 or later.
- [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on the host.

## Manual installation

Follow these steps to deploy the {{agent}} and EDOT SDKs in Docker with ECH:

:::::{stepper}

::::{step} Create the config file

Create an {{agent}} configuration file for the {{motlp}}. This example uses the filename `otel-collector-config.yml`.

Start from the [logs, metrics, and traces sample for the {{motlp}}](https://github.com/elastic/elastic-agent/blob/v{{version.edot_collector}}/internal/edot/samples/linux/managed_otlp/logs_metrics_traces.yml). The sample is written for a host process, so adapt it for the Compose mounts in this quickstart:

1. In `file_log/platformlogs`, set `include` to `[/hostfs/var/log/*.log]`.
2. In `hostmetrics/system`, set `root_path: /hostfs`.
3. Add a `docker_stats` receiver and a pipeline that exports those metrics:

   ```yaml
   receivers:
     docker_stats: {}

   service:
     pipelines:
       metrics/docker:
         receivers: [docker_stats]
         processors: [resourcedetection]
         exporters: [otlp_grpc/ingest_metrics_traces]
   ```

Keep the other receivers, processors, exporters, and pipelines from the sample. The result is a Docker-specific configuration, as the adaptations replace host paths with `/hostfs` mount paths and add Docker metrics collection. For details about the pipelines, refer to [Using the Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-standalone.md#using-the-managed-otlp-endpoint).

::::

::::{step} Find your endpoint and create an API key

:::{include} ../../_snippets/retrieve-credentials-ech-motlp.md
:::

::::

::::{step} Create the .env file

Create a `.env` file with the following content. Replace the placeholders with your {{ecloud}} credentials and the path to the configuration file you created:

```bash subs=true
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:{{version.edot_collector}}
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_OTLP_ENDPOINT=<your_motlp_endpoint_here>
OTEL_COLLECTOR_CONFIG=/path/to/otel-collector-config.yml
```

::::

::::{step} Create the compose file

Create a `compose.yml` file with the following content:

```yaml
services:
 otel-collector:
   image: ${COLLECTOR_CONTRIB_IMAGE}
   container_name: otel-collector
   deploy:
     resources:
       limits:
         memory: 1.5G
   restart: unless-stopped
   command: ["--config", "/etc/otelcol-config.yml" ]
   network_mode: host
   user: "0:0"
   volumes:
     - ${HOST_FILESYSTEM}:/hostfs:ro
     - ${DOCKER_SOCK}:/var/run/docker.sock:ro
     - ${OTEL_COLLECTOR_CONFIG}:/etc/otelcol-config.yml
   environment:
     - HOST_FILESYSTEM
     - ELASTIC_AGENT_OTEL
     - ELASTIC_API_KEY
     - ELASTIC_OTLP_ENDPOINT
     - STORAGE_DIR=/usr/share/elastic-agent
```

::::

::::{step} Start the Collector

To start the Collector, run:

```bash
docker compose up -d
```

::::

::::{step} (Optional) Instrument your applications

To collect telemetry from applications and use the {{agent}} as a gateway, instrument your target applications following the setup instructions:

- [Android](apm-agent-android://reference/edot-android/index.md)
- [.NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
- [iOS](apm-agent-ios://reference/edot-ios/index.md)
- [Java](elastic-otel-java://reference/edot-java/setup/index.md)
- [Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
- [PHP](elastic-otel-php://reference/edot-php/setup/index.md)
- [Python](elastic-otel-python://reference/edot-python/setup/index.md)

Configure your SDKs to send the data to the local {{agent}} using OTLP/gRPC (`http://localhost:4317`) or OTLP/HTTP (`http://localhost:4318`).

:::{tip}
Enable Central Configuration to configure your EDOT SDKs from within {{product.kibana}}. Refer to [EDOT SDKs Central Configuration](opentelemetry://reference/central-configuration.md).
:::

::::

::::{step} Install the content packs

Install the **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integration and the **[Docker OpenTelemetry Assets](integration-docs://reference/docker_otel.md)** integration in {{kib}}.

::::

::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

::::
:::::

## Using the `elasticsearch` exporter

If you need to write telemetry directly to {{es}} (for example, for pipeline customizations not yet supported through {{motlp}}), use a different Collector configuration, `.env` file, and compose file. For a full list of features and limitations that apply to each path, refer to [Elastic features available with {{edot}}](opentelemetry://reference/compatibility/features.md).

Start from the [logs, metrics, and traces sample for direct ingestion into {{es}}](https://github.com/elastic/elastic-agent/blob/v{{version.edot_collector}}/internal/edot/samples/linux/logs_metrics_traces.yml). The sample is written for a host process, so adapt it for the Compose mounts in this quickstart:

1. In `file_log/platformlogs`, set `include` to `[/hostfs/var/log/*.log]`.
2. In `hostmetrics/system`, set `root_path: /hostfs`.
3. Add a `docker_stats` receiver and a pipeline that exports those metrics:

   ```yaml
   receivers:
     docker_stats: {}

   service:
     pipelines:
       metrics/docker:
         receivers: [docker_stats]
         processors: [resourcedetection]
         exporters: [elasticsearch/otel]
   ```

Keep the other receivers, processors, exporters, and pipelines from the sample. For details about the pipelines, refer to [Direct ingestion into {{es}}](elastic-agent://reference/edot-collector/config/default-config-standalone.md#direct-ingestion-into-elasticsearch).

:::{include} ../../_snippets/retrieve-credentials.md
:::

Create a `.env` file with your {{es}} endpoint, credentials, and the path to the configuration file:

```bash subs=true
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:{{version.edot_collector}}
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_ENDPOINT=<your_elasticsearch_endpoint_here>
OTEL_COLLECTOR_CONFIG=/path/to/otel-collector-config.yml
```

Use the following compose file, which passes `ELASTIC_ENDPOINT` instead of `ELASTIC_OTLP_ENDPOINT`:

```yaml
services:
 otel-collector:
   image: ${COLLECTOR_CONTRIB_IMAGE}
   container_name: otel-collector
   deploy:
     resources:
       limits:
         memory: 1.5G
   restart: unless-stopped
   command: ["--config", "/etc/otelcol-config.yml" ]
   network_mode: host
   user: "0:0"
   volumes:
     - ${HOST_FILESYSTEM}:/hostfs:ro
     - ${DOCKER_SOCK}:/var/run/docker.sock:ro
     - ${OTEL_COLLECTOR_CONFIG}:/etc/otelcol-config.yml
   environment:
     - HOST_FILESYSTEM
     - ELASTIC_AGENT_OTEL
     - ELASTIC_API_KEY
     - ELASTIC_ENDPOINT
     - STORAGE_DIR=/usr/share/elastic-agent
```

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
