---
navigation_title: OpenTelemetry
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry.html
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html
applies_to:
  stack:
  serverless:
products:
  - id: cloud-serverless
  - id: observability
---

# Use OpenTelemetry with APM [apm-otel-elastic-distros]

[OpenTelemetry](https://opentelemetry.io/docs/concepts/what-is-opentelemetry/) is a set of APIs, SDKs, tooling, and integrations that enable the capture and management of telemetry data from your services and applications.

Elastic offers several distributions of OpenTelemetry. Each Elastic Distribution of OpenTelemetry is a customized version of an [OpenTelemetry language SDK](https://opentelemetry.io/docs/languages/) and the OpenTelemetry Collector, ready to send data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md), APM Server, or directly to {{es}}.

:::{include} /solutions/_snippets/edot-reference-arch.md
:::

With an Elastic Distribution of OpenTelemetry language SDK you have access to all the features of the OpenTelemetry SDK that it customizes, plus:

* You can get access to SDK improvements and bug fixes contributed by the Elastic team before the changes are available in the OpenTelemetry repositories.
* The distribution configures the collection of tracing and metrics signals, applying opinionated defaults, such as which sources are collected by default.
* By sending data through the [EDOT Collector](opentelemetry://reference/edot-collector/index.md), you make sure to onboard infrastructure logs and metrics.

Get started with an Elastic Distribution of OpenTelemetry language SDK:

* [**Elastic Distribution of OpenTelemetry Java**](opentelemetry://reference/edot-sdks/java/index.md)
* [**Elastic Distribution of OpenTelemetry .NET**](opentelemetry://reference/edot-sdks/dotnet/index.md)
* [**Elastic Distribution of OpenTelemetry Node.js**](opentelemetry://reference/edot-sdks/nodejs/index.md)
* [**Elastic Distribution of OpenTelemetry Python**](opentelemetry://reference/edot-sdks/python/index.md)
* [**Elastic Distribution of OpenTelemetry PHP**](opentelemetry://reference/edot-sdks/php/index.md)

::::{important}
For a complete overview of OpenTelemetry and Elastic, explore [**Elastic Distributions of OpenTelemetry**](opentelemetry://reference/index.md).
::::

## Contrib OpenTelemetry Collector and SDKs [apm-otel-upstream]

The {{stack}} natively supports the OpenTelemetry protocol (OTLP). This means trace data and metrics collected from your applications and infrastructure by an OpenTelemetry Collector or OpenTelemetry language SDK can be sent to the {{stack}}.

You can set up an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/), instrument your application with an [OpenTelemetry language SDK](https://opentelemetry.io/docs/languages/) that sends data to the Collector, and use the Collector to process and export the data to either the [Managed OTLP endpoint](opentelemetry://reference/motlp.md) or {{apm-server-or-mis}}.

This approach works well when you need to instrument a technology that Elastic doesn’t provide a solution for. For example, if you want to instrument C or C++ you could use the [OpenTelemetry C++ client](https://github.com/open-telemetry/opentelemetry-cpp). However, there are some limitations when using contrib OpenTelemetry collectors and language SDKs, including:

* Elastic can’t provide implementation support on how to use contrib OpenTelemetry tools.
* You won’t have access to Elastic enterprise APM features.
* You may experience problems with performance efficiency.

For more on the limitations associated with using contrib OpenTelemetry tools, refer to [Limitations](/solutions/observability/apm/limitations.md).

[**Get started with contrib OpenTelemetry Collectors and language SDKs →**](/solutions/observability/apm/upstream-opentelemetry-collectors-language-sdks.md)

:::{note}
To understand the differences between Elastic Distributions of OpenTelemetry and contrib OpenTelemetry, refer to [EDOT compared to contrib OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md).
:::

## Contrib OpenTelemetry with Elastic APM agent [apm-otel-api-sdk-elastic-agent]

You can use the OpenTelemetry API/SDKs with [Elastic APM agents](/solutions/observability/apm/apm-server-fleet-managed.md#_step_3_install_apm_agents) to translate OpenTelemetry API calls to Elastic APM API calls. This allows you to reuse your existing OpenTelemetry instrumentation to create Elastic APM transactions and spans, avoiding vendor lock-in and having to redo manual instrumentation.

However, not all features of the OpenTelemetry API are supported when using this approach, and not all Elastic APM agents support this approach.

Find more details about how to use an OpenTelemetry API or SDK with an Elastic APM agent and which OpenTelemetry API features are supported in the APM agent documentation:

* [**APM Java agent**](apm-agent-java://reference/opentelemetry-bridge.md)
* [**APM .NET agent**](apm-agent-dotnet://reference/opentelemetry-bridge.md)
* [**APM Node.js agent**](apm-agent-nodejs://reference/opentelemetry-bridge.md)
* [**APM Python agent**](apm-agent-python://reference/opentelemetry-api-bridge.md)

## AWS Lambda Collector Exporter [apm-otel-lambda]

AWS Lambda functions can be instrumented with OpenTelemetry and monitored with Elastic {{observability}} or {{obs-serverless}}.

To get started, follow the official AWS Distribution for OpenTelemetry Lambda documentation, and configure the OpenTelemetry Collector to output traces and metrics to your Elastic cluster:

[**Get started with the AWS Distro for OpenTelemetry Lambda**](https://aws-otel.github.io/docs/getting-started/lambda)