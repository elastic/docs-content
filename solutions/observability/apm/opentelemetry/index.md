---
navigation_title: OpenTelemetry
description: Learn how to integrate OpenTelemetry with Elastic APM using Elastic Distributions, contrib SDKs, and APM agents. Includes setup for serverless, self-managed, and AWS Lambda.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry.html
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Use OpenTelemetry with Elastic APM

OpenTelemetry is a set of APIs, SDKs, tooling, and integrations that enable the capture and management of telemetry data from your services and applications. You can use OpenTelemetry to collect application performance data in Elastic APM, whether you’re running serverless, self-managed, or hybrid deployments.

:::{important}
**Install OpenTelemetry integrations to view data**

Native Elastic Observability user interfaces do not currently support native OpenTelemetry data. To view your data, you must install content-only integrations that provide compatible dashboards.

In the Kibana Integrations UI, search for `otel` to find and install the relevant integrations, like **System OpenTelemetry Assets**, to access the dashboards.
:::

Elastic offers several distributions of OpenTelemetry. Each [Elastic Distribution of OpenTelemetry](opentelemetry://reference/index.md) is a customized version of an OpenTelemetry language SDK and the OpenTelemetry Collector, ready to send data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md), APM Server, or directly to {{es}}.

:::{include} /solutions/_snippets/edot-reference-arch.md
:::

## Why use the Elastic Distributions of OpenTelemetry?

With an [Elastic Distribution of OpenTelemetry language SDK](opentelemetry://reference/edot-sdks/index.md) you have access to all the features of the OpenTelemetry SDK that it customizes, plus:

* You can get access to SDK improvements and bug fixes contributed by the Elastic team before the changes are available in the OpenTelemetry repositories.
* The distribution configures the collection of tracing and metrics signals, applying opinionated defaults, such as which sources are collected by default.
* By sending data through the [EDOT Collector](elastic-agent://reference/edot-collector/index.md), you make sure to onboard infrastructure logs and metrics.

To set up OpenTelemetry with Elastic, refer to these guides for each language:

* [**Elastic Distribution of OpenTelemetry Java**](elastic-otel-java://reference/edot-java/index.md)
* [**Elastic Distribution of OpenTelemetry .NET**](elastic-otel-dotnet://reference/edot-dotnet/index.md)
* [**Elastic Distribution of OpenTelemetry Node.js**](elastic-otel-node://reference/edot-node/index.md)
* [**Elastic Distribution of OpenTelemetry Python**](elastic-otel-python://reference/edot-python/index.md)
* [**Elastic Distribution of OpenTelemetry PHP**](elastic-otel-php://reference/edot-php/index.md)

::::{important}
For a complete overview of OpenTelemetry and Elastic, explore [**Elastic Distributions of OpenTelemetry**](opentelemetry://reference/index.md).
::::

## Contrib OpenTelemetry Collector and SDKs [apm-otel-upstream]

The {{stack}} natively supports the OpenTelemetry protocol (OTLP). This means trace data and metrics collected from your applications and infrastructure by an OpenTelemetry Collector or OpenTelemetry language SDK can be sent to Elastic.

You can set up an OpenTelemetry Collector based on contrib OpenTelemetry, instrument your application with an OpenTelemetry language SDK that sends data to the Collector, and use the Collector to process and export the data to either the [Managed OTLP endpoint](opentelemetry://reference/motlp.md) or {{apm-server-or-mis}}.

This approach works well when you need to instrument a technology that Elastic doesn’t provide a solution for. For example, if you want to instrument C or C++ you can use the [OpenTelemetry C++ client](https://github.com/open-telemetry/opentelemetry-cpp). However, there are some limitations when using contrib OpenTelemetry collectors and language SDKs, including:

* Elastic can’t provide implementation support on how to use contrib OpenTelemetry tools.
* You won’t have access to Elastic enterprise APM features.
* You might experience problems with performance efficiency.

For more on the limitations associated with using contrib OpenTelemetry tools, refer to [Limitations](/solutions/observability/apm/opentelemetry/limitations.md).

[**Get started with contrib OpenTelemetry Collectors and language SDKs →**](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md)

:::{note}
To understand the differences between Elastic Distributions of OpenTelemetry and contrib OpenTelemetry, refer to [EDOT compared to contrib OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md).
:::

## Contrib OpenTelemetry with Elastic APM agent [apm-otel-api-sdk-elastic-agent]

You can use the OpenTelemetry API/SDKs with [Elastic APM agents](/solutions/observability/apm/apm-server/fleet-managed.md#_step_3_install_apm_agents) to translate OpenTelemetry API calls to Elastic APM API calls. This allows you to reuse your existing OpenTelemetry instrumentation to create Elastic APM transactions and spans, avoiding vendor lock-in and having to redo manual instrumentation.

However, not all features of the OpenTelemetry API are supported when using this approach, and not all Elastic APM agents support this approach.

Find more details about how to use an OpenTelemetry API or SDK with an Elastic APM agent and which OpenTelemetry API features are supported in the APM agent documentation:

* [**APM Java agent**](apm-agent-java://reference/opentelemetry-bridge.md)
* [**APM .NET agent**](apm-agent-dotnet://reference/opentelemetry-bridge.md)
* [**APM Node.js agent**](apm-agent-nodejs://reference/opentelemetry-bridge.md)
* [**APM Python agent**](apm-agent-python://reference/opentelemetry-api-bridge.md)

## AWS Lambda Collector Exporter [apm-otel-lambda]

AWS Lambda functions can be instrumented with OpenTelemetry and monitored with Elastic {{observability}} or {{obs-serverless}}.

To get started, follow the official AWS Distribution for OpenTelemetry Lambda documentation, and [configure the EDOT Collector in Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode) to send traces and metrics to your Elastic cluster:

[**Get started with the AWS Distro for OpenTelemetry Lambda**](https://aws-otel.github.io/docs/getting-started/lambda)
