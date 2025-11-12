---
description: Learn how to use the Elastic Cloud Managed OTLP Endpoint to send logs, metrics, and traces to Elastic Serverless and Elastic Cloud Hosted.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/collect-data-with-native-otlp.html
applies_to:
  serverless: unavailable
  deployment:
    ess: preview
  stack: preview 9.2
---

# Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted

You can send OpenTelemetry data to Elastic Serverless and Elastic Cloud Hosted using the {{motlp}} endpoint.

The {{motlp}} provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage. Refer to [{{motlp}}](opentelemetry://reference/motlp.md) for more information.

The {{motlp}} is designed for the following use cases:

* Logs & Infrastructure Monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format.
* APM: Application telemetry in OTLP format.

Keep reading to learn how to use the {{motlp}} to send logs, metrics, and traces to your Serverless project or {{ech}} cluster.

:::{note}
:applies_to: { ess:, stack: preview 9.2 }
The Managed OTLP endpoint might not be available in all {{ech}} regions during the Technical Preview.
:::

## Send data to Elastic

Follow these steps to send data to Elastic using the {{motlp}}.

::::::{stepper}

:::::{step} Retrieve your endpoint and API key

To retrieve your {{motlp}} endpoint address and API key, follow these steps:

::::{applies-switch}
:::{applies-item} serverless:
1. In {{ecloud}}, create an Observability project or open an existing one.
2. Go to **Add data**, select **Applications** and then select **OpenTelemetry**.
3. Copy the endpoint and authentication headers values.

Alternatively, you can retrieve the endpoint from the **Manage project** page and create an API key manually from the **API keys** page.
:::

:::{applies-item} ess:
{applies_to}`stack: preview 9.2`
1. In {{ecloud}}, create an {{ech}} deployment or open an existing one.
2. Go to **Add data**, select **Applications** and then select **OpenTelemetry**.
3. Copy the endpoint and authentication headers values.

Alternatively, you can retrieve the endpoint from the **Manage project** page and create an API key manually from the **API keys** page.
:::
::::

:::::

:::::{step} Configure your OTLP shipper

The final step is to configure your Collector or SDK to use the {{motlp}} endpoint and your Elastic API key to send data to {{ecloud}}.

::::{tab-set}

:::{tab-item} OpenTelemetry Collector example
To send data to the {{motlp}} from the {{edot}} Collector or the contrib Collector, configure the `otlp` exporter:

```yaml
exporters:
  otlp:
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ApiKey <your-api-key>
```

Set the API key as an environment variable or directly in the configuration as shown in the example.
:::

:::{tab-item} OpenTelemetry SDK example
To send data to the {{motlp}} from {{edot}} SDKs or contrib SDKs, set the following variables in your application's environment:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://<motlp-endpoint>"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey <your-api-key>"
```
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
    endpoint: https://<motlp-endpoint>
    headers:
      Authorization: ${API_KEY}
```

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

The Elastic Cloud Managed OTLP Endpoint ensures that OpenTelemetry data is stored without any schema translation, preserving both OpenTelemetry semantic conventions and resource attributes. It supports ingesting OTLP logs, metrics, and traces in a unified manner, ensuring consistent treatment across all telemetry data.

## Troubleshooting

The following sections provide troubleshooting information for the {{motlp}}.

### You don't have a Collector or SDK running

Don't have a collector or SDK running? Spin up an EDOT collector in few steps:

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

If you see HTTP `429 Too Many Requests` errors when sending data through the Elastic Cloud Managed OTLP Endpoint (mOTLP) endpoint, your project might be hitting ingest rate limits.

Refer to the dedicated [429 errors when using the Elastic Cloud Managed OTLP Endpoint](/troubleshoot/ingest/opentelemetry/429-errors-motlp.md) troubleshooting guide for details on causes, rate limits, and solutions.


## Provide feedback

Help improve the Elastic Cloud Managed OTLP Endpoint by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup#/domain-signup).

For EDOT collector feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).

## What's next

Visualize your OpenTelemetry data. Learn more in [](/solutions/observability/otlp-visualize.md).
