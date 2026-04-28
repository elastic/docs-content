---
description: Learn how to use the Elastic Cloud Managed OTLP Endpoint to send logs, metrics, and traces to Elastic Serverless and Elastic Cloud Hosted.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/collect-data-with-native-otlp.html
applies_to:
  serverless: ga
  deployment:
    ech:
---

# Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted

You can send OpenTelemetry data to Elastic Serverless and Elastic Cloud Hosted using the {{motlp}} endpoint.

The {{motlp}} provides an endpoint for OpenTelemetry SDKs and Collectors to send telemetry data, with Elastic handling scaling, data processing, and storage. Refer to [{{motlp}}](opentelemetry://reference/motlp.md) for more information.

The {{motlp}} is designed for the following use cases:

* Logs & Infrastructure Monitoring: Logs forwarded in OTLP format and host and Kubernetes metrics in OTLP format.
* APM: Application telemetry in OTLP format.

Keep reading to learn how to use the {{motlp}} to send logs, metrics, and traces to your Serverless project or {{ech}} cluster.

:::{note}
:applies_to: ech:
On {{ech}}, the Managed OTLP endpoint requires a deployment version 9.0 or later.
:::

## Send data to Elastic

Follow these steps to send data to Elastic using the {{motlp}}.

::::::{stepper}

:::::{step} Retrieve your endpoint and API key

Retrieve the {{motlp}} endpoint for your environment and generate an API key to authenticate your OTLP shipper.

::::{applies-switch}
:::{applies-item} serverless:
**Using the Add data wizard (recommended)**

The Add data wizard retrieves the endpoint and generates an API key with the required privileges automatically:

1. In {{ecloud}}, create an {{observability}} project or open an existing one.
2. Go to **Add data**, select **Applications**, and then select **OpenTelemetry**.
3. Copy the endpoint and authentication headers values.

**Creating an API key manually via {{kib}}**

1. Retrieve the endpoint from the **Manage project** page.
2. Open the **API keys** management page from the navigation menu.
3. Click **Create API key**, enter a name, and expand **Control security privileges**.
4. In the role descriptors box, enter the following privileges:

    ```json
    {
      "otlp_writer": {
        "cluster": [],
        "indices": [
          {
            "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
            "privileges": ["auto_configure", "create_doc"]
          }
        ]
      }
    }
    ```

5. Click **Create API key** and copy the encoded value.

**Creating an API key via the {{es}} API**

Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "cluster": [],
      "indices": [
        {
          "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    }
  }
}
```

:::{note}
The API key both authenticates the OTLP shipper to the {{motlp}} endpoint and authorizes writes to the destination {{es}} data streams. The `auto_configure` and `create_doc` privileges are required for all target data streams. If you route data to [custom datasets](opentelemetry://reference/motlp.md), add the corresponding index patterns to the `names` list.
:::
:::

:::{applies-item} ech:
**Find your endpoint**

1. Log in to the {{ecloud}} Console.
2. Find your deployment on the home page or on the **Hosted deployments** page, and then select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.

**Create an API key via {{kib}}**

1. Open the **API keys** management page from the navigation menu.
2. Click **Create API key**, enter a name, and select **Restrict privileges**.
3. In the role descriptors box, enter the following privileges:

    ```json
    {
      "otlp_writer": {
        "cluster": [],
        "indices": [
          {
            "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
            "privileges": ["auto_configure", "create_doc"]
          }
        ]
      }
    }
    ```

4. Click **Create API key** and copy the encoded value.

**Create an API key via the {{es}} API**

Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "cluster": [],
      "indices": [
        {
          "names": ["traces-generic.otel-*", "metrics-generic.otel-*", "logs-generic.otel-*"],
          "privileges": ["auto_configure", "create_doc"]
        }
      ]
    }
  }
}
```

:::{note}
The API key both authenticates the OTLP shipper to the {{motlp}} endpoint and authorizes writes to the destination {{es}} data streams. The `auto_configure` and `create_doc` privileges are required for all target data streams. If you route data to [custom datasets](opentelemetry://reference/motlp.md), add the corresponding index patterns to the `names` list.
:::
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

Refer to the [Troubleshoot EDOT](opentelemetry://reference/motlp/troubleshooting.md) guide for troubleshooting information for the {{motlp}}.

## Provide feedback

Help improve the Elastic Cloud Managed OTLP Endpoint by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup#/domain-signup).

For EDOT collector feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).

## What's next

Visualize your OpenTelemetry data. Learn more in [](/solutions/observability/otlp-visualize.md).
