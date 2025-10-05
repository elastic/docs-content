---
description: Learn how to use the Elastic Cloud Managed OTLP Endpoint to send logs, metrics, and traces to Elastic Observability.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/collect-data-with-native-otlp.html
applies_to:
  serverless:
---

# Quickstart: Send data to the {{motlp}}

The {{motlp}} is a fully managed offering exclusively for Elastic Cloud users that simplifies OpenTelemetry data ingestion. It provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage. Refer to [{{motlp}}](opentelemetry://reference/motlp.md) for more information.

This endpoint is designed for the following use cases:

* Logs & Infrastructure Monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format.
* APM: Application telemetry in OTLP format.

In this quickstart guide, you'll learn how to use the {{motlp}} to send logs, metrics, and traces to Elastic.

## Prerequisites

* An {{obs-serverless}} project. To learn more, refer to [create an Observability project](/solutions/observability/get-started.md).
* A system forwarding logs, metrics, or traces in OTLP (any EDOT Collector or SDK—EDOT or community).

## Get started

## Send data to Elastic

Follow these steps to send data to Elastic using the {{motlp}}.

::::::{stepper}

:::::{step} Check the requirements

To use the {{motlp}} you need the following:

* An Elastic Observability Serverless project. Security projects are not yet supported.
* An OTLP-compliant shipper capable of forwarding logs, metrics, or traces in OTLP format. This can include the OpenTelemetry Collector (EDOT, Contrib, or other distributions), OpenTelemetry SDKs (EDOT, upstream, or other distributions), or any other forwarder that supports the OTLP protocol.

:::::

:::::{step} Locate your {{motlp}}

To retrieve your {{motlp}} endpoint address and an API key, follow these steps:

1. In {{ecloud}}, create an Observability project or open an existing one.
2. Select your project's name and then select **Manage project**.
3. Locate the **Connection alias** and select **Edit**.
4. Copy the **Managed OTLP endpoint** URL.

% ## commented out until mOTLP on ECH is available
% ### Elastic Cloud on Elasticsearch ({{ech}})
% 1. Open your deployment in the Elastic Cloud console.
% 2. Navigate to **Integrations** and find **OpenTelemetry** or **Managed OTLP**.
% 3. Copy the endpoint URL shown.
% ## Self-Managed
% For self-managed environments, you can deploy and expose an OTLP-compatible endpoint using the EDOT Collector as a gateway. Refer to [EDOT deployment docs](https://www.elastic.co/docs/reference/opentelemetry/edot-collector/modes#edot-collector-as-gateway).
%
% :::{note}
% Please reach out to support, and then Engineering can look into increasing it based on the license tier or for experimentation purposes.
% :::

:::::

:::::{step} Create an API key

Generate an API key with appropriate ingest privileges to authenticate OTLP traffic:

1. In {{ecloud}}, go to **Manage project** → **API Keys**.
2. Select **Create API Key**.
3. Name the key. For example, `otlp-client`.
4. Edit the optional security settings.
5. Select **Create API Key**.
6. Copy the key to the clipboard.

Add this key to your final API key string. For example:

```
Authorization: ApiKey <your-api-key>
```

:::{important}
The API key copied from Kibana does not include the `ApiKey` scheme. Always prepend `ApiKey ` before using it in your configuration or encoding it for Kubernetes secrets. For example:

  - Correct: `Authorization: ApiKey abc123`
  - Incorrect: `Authorization: abc123`
:::

:::::

:::::{step} Send data to the {{motlp}}

The final step is to use the {{motlp}} endpoint and your Elastic API key to send data to {{ecloud}}.

::::{tab-set}

:::{tab-item} OpenTelemetry Collector example
To send data to the {{motlp}} from the {{edot}} Collector or the contrib Collector, configure the `otlp` exporter:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint> <1>
    headers:
      Authorization: ApiKey <your-api-key> <2>
```

1. The endpoint retrieved at [step 2](#locate-your-motlp)
2. The API key created at [step 3](#create-an-api-key)

Set the API key as an environment variable or directly in the configuration as shown in the example.
:::

:::{tab-item} OpenTelemetry SDK example
To send data to the {{motlp}} from {{edot}} SDKs or contrib SDKs, set the following variables in your application's environment:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>" <1>
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <your-api-key>" <2>
```

1. The endpoint retrieved at [step 2](#locate-your-motlp)
2. The API key created at [step 3](#create-an-api-key)
:::

:::{tab-item} Kubernetes example
You can store your API key in a Kubernetes secret and reference it in your OTLP exporter configuration. This is more secure than hardcoding credentials.

The API key from Kibana does not include the `ApiKey` scheme. You must prepend `ApiKey ` before storing it.

For example, if your API key from Kibana is `abc123`, run:

```bash
kubectl create secret generic otlp-api-key \
  --namespace=default \
  --from-literal=api-key="ApiKey abc123"
```

Mount the secret as an environment variable or file, then reference it in your OTLP exporter configuration:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint> <1>
    headers:
      Authorization: ${API_KEY} <2>
```

1. The endpoint retrieved at [step 2](#locate-your-motlp)
2. The API key created at [step 3](#create-an-api-key)

And in your deployment spec:

```yaml
env:
  - name: API_KEY
    valueFrom:
      secretKeyRef:
        name: otlp-api-key
        key: api-key
```

:::{important}
When creating a Kubernetes secret, always encode the full string in Base64, including the scheme (for example, `ApiKey abc123`).
:::
:::

::::

:::::

::::::

## Differences from the Elastic APM Endpoint

The Elastic Cloud Managed OTLP Endpoint ensures that OpenTelemetry data is stored without any schema translation, preserving both OpenTelemetry semantic conventions and resource attributes. It supports ingesting OTLP logs, metrics, and traces in a unified manner, ensuring consistent treatment across all telemetry data. This marks a significant improvement over the [existing functionality](/solutions/observability/apm/opentelemetry/index.md), which primarily focuses on traces and the APM use case.

## Troubleshoot

The following sections provide troubleshooting information for the {{motlp}}.

### I don't have a Collector or SDK running

Don't have a collector or SDK running? Spin up an EDOT collector in just a few steps:

* [Kubernetes Quickstart](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md)
* [Hosts & VMs Quickstart](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md)
* [Docker Quickstart](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md)

### Api Key prefix not found

The following error is due to an improperly formatted API key:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

You must format your API key as `"Authorization": "ApiKey <api-key-value-here>"` or `"Authorization=ApiKey <api-key>"` depending on whether you're using a collector or SDK.

### Error: too many requests

The Managed OTLP endpoint has per-project rate limits in place. If you hit this limit, reach out to our [support team](https://support.elastic.co). Refer to [Rate limiting](opentelemetry://reference/motlp.md#rate-limiting) for more information.

## Provide feedback

Help improve the Elastic Cloud Managed OTLP Endpoint by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup#/domain-signup).

For EDOT collector feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).

## What's next?

Visualize your OpenTelemetry data. Learn more in [](/solutions/observability/otlp-visualize.md).
