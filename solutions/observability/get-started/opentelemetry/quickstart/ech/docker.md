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

Learn how to set up the {{agent}} and EDOT SDKs in a Docker environment with {{ech}} (ECH) to collect host metrics, logs, and application traces. This quickstart uses the [{{motlp}}](opentelemetry://reference/motlp.md) — the recommended ingestion path for ECH.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Prerequisites

- An {{ech}} deployment running version 9.0 or later.
- [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on the host.

## Manual installation

Follow these steps to deploy the {{agent}} and EDOT SDKs in Docker with ECH.

:::::{stepper}

::::{step} Create the config file

Create an `otel-collector-config.yml` file with your {{agent}} configuration for the {{motlp}}. Refer to the [configuration reference](elastic-agent://reference/edot-collector/config/default-config-standalone.md).

::::

::::{step} Find your endpoint and create an API key

**Find your endpoint**

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co/).
2. From the home page, find your deployment in **Hosted deployments**, and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.

**Create an API key**

:::{dropdown} Using {{kib}}
1. Go to **{{stack-manage-app}}** → **API keys**.
2. Click **Create API key**, enter a name, and enable **Control security privileges**.
3. In the role descriptors box, enter the following:

   ```json
   {
     "otlp_writer": {
       "applications": [
         {
           "application": "apm",
           "resources": ["*"],
           "privileges": ["event:write"]
         }
       ]
     }
   }
   ```

4. Click **Create API key** and copy the encoded value.
:::

:::{dropdown} Using the {{es}} API
Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "applications": [
        {
          "application": "apm",
          "resources": ["*"],
          "privileges": ["event:write"]
        }
      ]
    }
  }
}
```

The `event:write` privilege for the `apm` application is the minimum required to send data through the {{motlp}}.
:::

::::

::::{step} Create the .env file

Create a `.env` file with the following content. Replace the placeholder values with your {{ecloud}} credentials:

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

If you need to write telemetry directly to {{es}} — for example, for pipeline customizations not yet supported through {{motlp}} — use the following `.env` and compose configuration instead.

:::{include} ../../_snippets/retrieve-credentials.md
:::

Create a `.env` file with your {{es}} endpoint and credentials:

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
   user: 0:0
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

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

Format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a Collector or SDK.

For additional troubleshooting, refer to [Troubleshooting common issues with the {{agent}}](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md).
