---
navigation_title: Get started
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-getting-started-apm-server.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-get-started.html
applies_to:
  stack:
  serverless:
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Get started with APM [apm-getting-started-apm-server]

Elastic APM receives performance data from your APM agents, validates and processes it, and then transforms the data into {{es}} documents. 

To get started, select the deployment model that best suits your needs:

* **[Elastic Cloud Serverless](/solutions/observability/apm/get-started.md#get-started-apm-serverless)**
* **[Fleet-managed APM Server](/solutions/observability/apm/get-started.md#apm-setup-fleet-managed-apm)**
* **[APM Server binary](/solutions/observability/apm/get-started.md#apm-setup-apm-server-binary)**

## Elastic Cloud Serverless [get-started-apm-serverless]

```{applies_to}
serverless:
```

Elastic Cloud Serverless is a fully managed solution that allows you to deploy and use Elastic for your use cases without managing the underlying infrastructure. Refer to [**Get started with traces and APM**](/solutions/observability/apm/get-started-serverless.md) for more information.

:::{image} /solutions/images/observability-apm-otel-distro-serverless.png
:alt: APM data ingest path (Serverless)
:::

::::{important}
To learn more about using OpenTelemetry with Elastic APM, including ECH and self-managed options, refer to [**Use OpenTelemetry with APM**](/solutions/observability/apm/use-opentelemetry-with-apm.md).
::::

## Fleet-managed APM Server [apm-setup-fleet-managed-apm]

```{applies_to}
stack:
```

Fleet is a web-based UI in {{kib}} that is used to centrally manage {{agent}}s. In this deployment model, use {{agent}} to spin up APM Server instances that can be centrally-managed in a custom-curated user interface. Refer to [**Fleet-managed APM Server**](/solutions/observability/apm/get-started-fleet-managed-apm-server.md) for more information.

:::{image} /solutions/images/observability-fm-ov.png
:alt: APM Server fleet overview
:::

## APM Server binary [apm-setup-apm-server-binary]

```{applies_to}
stack:
```

In self-managed environments, you can also install, configure, and run the APM Server binary wherever you need it. Refer to [**APM Server binary**](/solutions/observability/apm/get-started-apm-server-binary.md) for more information.

:::{image} /solutions/images/observability-bin-ov.png
:alt: APM Server binary overview
:::
