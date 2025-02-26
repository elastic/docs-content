---
navigation_title: "OpenTelemetry"
mapped_urls:
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry.html
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html
---

# Use OpenTelemetry with APM [apm-open-telemetry]


::::{note}
For a complete overview of using OpenTelemetry with Elastic, explore [**Elastic Distributions of OpenTelemetry**](https://github.com/elastic/opentelemetry).

::::


[OpenTelemetry](https://opentelemetry.io/docs/concepts/what-is-opentelemetry/) is a set of APIs, SDKs, tooling, and integrations that enable the capture and management of telemetry data from your services and applications.

Elastic integrates with OpenTelemetry, allowing you to reuse your existing instrumentation to easily send observability data to the {{stack}}. There are several ways to integrate OpenTelemetry with the {{stack}}:

* [Elastic Distributions of OpenTelemetry language SDKs](../../../solutions/observability/apps/use-opentelemetry-with-apm.md#apm-otel-elastic-distros)
* [Upstream OpenTelemetry API/SDK + Elastic APM agent](../../../solutions/observability/apps/use-opentelemetry-with-apm.md#apm-otel-api-sdk-elastic-agent)
* [Upstream OpenTelemetry Collector and language SDKs](../../../solutions/observability/apps/use-opentelemetry-with-apm.md#apm-otel-upstream)
* [AWS Lambda collector exporter](../../../solutions/observability/apps/use-opentelemetry-with-apm.md#apm-otel-lambda)


## Elastic Distributions of OpenTelemetry language SDKs [apm-otel-elastic-distros]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Elastic offers several distributions of OpenTelemetry language SDKs. A *distribution* is a customized version of an upstream OpenTelemetry repository. Each Elastic Distribution of OpenTelemetry is a customized version of an [OpenTelemetry language SDK](https://opentelemetry.io/docs/languages/).

:::{image} ../../../images/observability-apm-otel-distro.png
:alt: apm otel distro
:class: screenshot
:::

With an Elastic Distribution of OpenTelemetry language SDK you have access to all the features of the OpenTelemetry SDK that it customizes, plus:

* You may get access to SDK improvements and bug fixes contributed by the Elastic team *before* the changes are available upstream in the OpenTelemetry repositories.
* The distribution preconfigures the collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.

Get started with an Elastic Distribution of OpenTelemetry language SDK:

* [**Elastic Distribution of OpenTelemetry Java →**](https://github.com/elastic/elastic-otel-java)
* [preview] [**Elastic Distribution of OpenTelemetry .NET →**](https://github.com/elastic/elastic-otel-dotnet)
* [preview] [**Elastic Distribution of OpenTelemetry Node.js →**](https://github.com/elastic/elastic-otel-node)
* [preview] [**Elastic Distribution of OpenTelemetry Python →**](https://github.com/elastic/elastic-otel-python)
* [preview] [**Elastic Distribution of OpenTelemetry PHP →**](https://github.com/elastic/elastic-otel-php)

::::{note}
For more details about OpenTelemetry distributions in general, visit the [OpenTelemetry documentation](https://opentelemetry.io/docs/concepts/distributions).

::::


## Upstream OpenTelemetry API/SDK + Elastic APM agent [apm-otel-api-sdk-elastic-agent]

Use the OpenTelemetry API/SDKs with [Elastic APM agents](../../../solutions/observability/apps/fleet-managed-apm-server.md#_step_3_install_apm_agents) to translate OpenTelemetry API calls to Elastic APM API calls.

:::{image} ../../../images/observability-apm-otel-api-sdk-elastic-agent.png
:alt: apm otel api sdk elastic agent
:class: screenshot
:::

This allows you to reuse your existing OpenTelemetry instrumentation to create Elastic APM transactions and spans — ​avoiding vendor lock-in and having to redo manual instrumentation.

However, not all features of the OpenTelemetry API are supported when using this approach, and not all Elastic APM agents support this approach.

Find more details about how to use an OpenTelemetry API or SDK with an Elastic APM agent and which OpenTelemetry API features are supported in the APM agent documentation:

* [**APM Java agent →**](asciidocalypse://docs/apm-agent-java/docs/reference/opentelemetry-bridge.md)
* [**APM .NET agent →**](asciidocalypse://docs/apm-agent-dotnet/docs/reference/opentelemetry-bridge.md)
* [**APM Node.js agent →**](asciidocalypse://docs/apm-agent-nodejs/docs/reference/opentelemetry-bridge.md)
* [**APM Python agent →**](asciidocalypse://docs/apm-agent-python/docs/reference/opentelemetry-api-bridge.md)


## Upstream OpenTelemetry Collector and language SDKs [apm-otel-upstream]

The {{stack}} natively supports the OpenTelemetry protocol (OTLP). This means trace data and metrics collected from your applications and infrastructure by an OpenTelemetry Collector or OpenTelemetry language SDK can be sent to the {{stack}}.

You can set up an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/), instrument your application with an [OpenTelemetry language SDK](https://opentelemetry.io/docs/languages/) that sends data to the collector, and use the collector to process and export the data to APM Server.

:::{image} ../../../images/observability-apm-otel-api-sdk-collector.png
:alt: apm otel api sdk collector
:class: screenshot
:::

::::{note}
It’s also possible to send data directly to APM Server from an upstream OpenTelemetry SDK. You might do this during development or if you’re monitoring a small-scale application. Read more about when to use a collector in the [OpenTelemetry documentation](https://opentelemetry.io/docs/collector/#when-to-use-a-collector).

::::


This approach works well when you need to instrument a technology that Elastic doesn’t provide a solution for. For example, if you want to instrument C or C++ you could use the [OpenTelemetry C++ client](https://github.com/open-telemetry/opentelemetry-cpp).

However, there are some limitations when using collectors and language SDKs built and maintained by OpenTelemetry, including:

* Elastic can’t provide implementation support on how to use upstream OpenTelemetry tools.
* You won’t have access to Elastic enterprise APM features.
* You may experience problems with performance efficiency.

For more on the limitations associated with using upstream OpenTelemetry tools, refer to [Limitations](../../../solutions/observability/apps/limitations.md).

[**Get started with upstream OpenTelemetry Collectors and language SDKs →**](../../../solutions/observability/apps/upstream-opentelemetry-collectors-language-sdks.md)


## AWS Lambda collector exporter [apm-otel-lambda]

AWS Lambda functions can be instrumented with OpenTelemetry and monitored with Elastic {{observability}} or {{obs-serverless}}.

To get started, follow the official AWS Distro for OpenTelemetry Lambda documentation, and configure the OpenTelemetry Collector to output traces and metrics to your Elastic cluster:

[**Get started with the AWS Distro for OpenTelemetry Lambda**](https://aws-otel.github.io/docs/getting-started/lambda)