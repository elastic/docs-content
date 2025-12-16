---
navigation_title: Docker
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.
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

# Quickstart for Docker on self-managed deployments

Learn how to set up the EDOT Collector and EDOT SDKs in a Docker environment to collect host metrics, logs and application traces.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Docker.

:::::{stepper}

::::{step} Create the config file

Create the `otel-collector-config.yml` file with your EDOT Collector configuration. Refer to the [configuration reference](elastic-agent://reference/edot-collector/config/default-config-standalone.md).
::::

::::{step} Retrieve your settings

Retrieve your [{{es}} endpoint](/solutions/search/search-connection-details.md) and [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md).
::::

::::{step} Create the .env file

Create an `.env` file with the following content. Replace the placeholder values with your Elastic Cloud credentials:

```bash subs=true
HOST_FILESYSTEM=/
DOCKER_SOCK=/var/run/docker.sock
ELASTIC_AGENT_OTEL=true
COLLECTOR_CONTRIB_IMAGE=elastic/elastic-agent:{{version.edot_collector}}
ELASTIC_API_KEY=<your_api_key_here>
ELASTIC_OTLP_ENDPOINT=<your_endpoint_here>
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
    user: 0:0
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

Start the Collector by running the following command:

```bash
docker compose up -d
```
::::

::::{step} (Optional) Instrument your applications

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
::::

::::{step} Install the content packs

Install the **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integration and the **[Docker OpenTelemetry Assets](integration-docs://reference/docker_otel.md)** integration in {{kib}}.

::::


::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

::::
:::::

## Troubleshooting

Having issues with EDOT? Refer to the [Troubleshooting common issues with the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md) for help.
