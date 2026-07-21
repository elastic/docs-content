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
:applies_to: {"stack": "ga 9.2", "serverless": "ga"}

**Install OpenTelemetry content packs to work with OpenTelemetry data**

To visualize data from OpenTelemetry receivers which is stored natively as OpenTelemetry semantic conventions, you must install content-only packs that provide dashboards compatible with OpenTelemetry data.

In the Kibana Integrations UI, search for `otel` to find and install available integrations, like **System OpenTelemetry Assets**, to access the dashboards. We are adding more OpenTelemetry content packs every week, reach out by [opening an issue](https://github.com/elastic/integrations/issues) if what you are looking for is not available as an OTel content pack.

Other Integrations which are beats-based include dashboards based on ECS data and are not compatible with OpenTelemetry semantic conventions.
:::

Elastic offers several distributions of OpenTelemetry. Each [Elastic Distribution of OpenTelemetry](opentelemetry://reference/index.md) is a customized version of an OpenTelemetry language SDK and the OpenTelemetry Collector, ready to send data to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md), APM Server, or directly to {{es}}.

:::{include} /solutions/_snippets/edot-reference-arch.md
:::

## Integration options [otel-integration-options]

There are several ways to send OpenTelemetry data to Elastic. The right choice depends on your infrastructure, the technologies you're instrumenting, and whether you want Elastic to manage the pipeline.

### Instrument your applications

* **EDOT language SDKs**: Use Elastic's customized OpenTelemetry SDKs, which apply opinionated defaults and preselected instrumentations for zero-code setup, with full Elastic support. The recommended approach for most applications. Refer to [Why use the Elastic Distributions of OpenTelemetry?](#why-use-the-elastic-distributions-of-opentelemetry) for more information.
* **Contrib OpenTelemetry SDKs**: Use community OpenTelemetry SDKs for a language that doesn't have an EDOT SDK, such as Go or C++. These work with Elastic over OTLP but receive community support only. Refer to [Contrib OpenTelemetry Collector and SDKs](#apm-otel-upstream) for more information.
* **Elastic {{product.apm}} agents with the OpenTelemetry bridge**: Instrument your application with the vendor-neutral OpenTelemetry API while the Elastic {{apm-agent}} collects and exports the data. Useful for reusing existing manual OpenTelemetry instrumentation without vendor lock-in, though some OpenTelemetry API features aren't supported. Refer to [Contrib OpenTelemetry with Elastic {{apm-agent}}](#apm-otel-api-sdk-elastic-agent) for more information.

### Collect, process, and export data

* **OTel Collector in {{agent}}** {applies_to}`stack: ga 9.2+`: The OTel Collector runs embedded inside {{agent}}, sharing a single `elastic-agent.yml` configuration file. No separate Collector installation is needed. Refer to [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md) for more information.
* **Standalone {{agent}}**: Run {{agent}} independently as its own process. Refer to [{{agent}}](elastic-agent://reference/edot-collector/index.md) for more information.
* **Upstream `otelcol-contrib` Collector**: Use the community-built Collector to forward data to {{agent}} or directly to {{apm-server-or-mis}} using OTLP. Useful for a vendor-neutral pipeline or fanning out to multiple observability backends, but it's community-supported only. Refer to [Contrib OpenTelemetry Collectors and language SDKs](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md) for more information.

### Send data directly

* **Managed OTLP endpoint** ({{serverless-short}} and {{ech}}): Send OpenTelemetry data directly to the [Managed OTLP endpoint](opentelemetry://reference/motlp.md) without managing your own Collector.

## Why use the Elastic Distributions of OpenTelemetry?

With an [Elastic Distribution of OpenTelemetry language SDK](opentelemetry://reference/edot-sdks/index.md) you have access to all the features of the OpenTelemetry SDK that it customizes, plus:

* You can get access to SDK improvements and bug fixes contributed by the Elastic team before the changes are available in the OpenTelemetry repositories.
* The distribution configures the collection of tracing and metrics signals, applying opinionated defaults, such as which sources are collected by default.
* By sending data through [{{agent}}](elastic-agent://reference/edot-collector/index.md), you make sure to onboard infrastructure logs and metrics.

To set up OpenTelemetry with Elastic, refer to these guides for each SDK:

* [**Elastic Distribution of OpenTelemetry Java**](elastic-otel-java://reference/edot-java/index.md)
* [**Elastic Distribution of OpenTelemetry .NET**](elastic-otel-dotnet://reference/edot-dotnet/index.md)
* [**Elastic Distribution of OpenTelemetry Node.js**](elastic-otel-node://reference/edot-node/index.md)
* [**Elastic Distribution of OpenTelemetry Python**](elastic-otel-python://reference/edot-python/index.md)
* [**Elastic Distribution of OpenTelemetry PHP**](elastic-otel-php://reference/edot-php/index.md)
* [**Elastic Distribution of OpenTelemetry Browser**](elastic-otel-rum-js://reference/edot-browser/index.md)

::::{important}
For a complete overview of OpenTelemetry and Elastic, explore [**Elastic Distributions of OpenTelemetry**](opentelemetry://reference/index.md).
::::

## Contrib OpenTelemetry Collector and SDKs [apm-otel-upstream]

The {{stack}} natively supports the OpenTelemetry protocol (OTLP). This means trace data and metrics collected from your applications and infrastructure by an OpenTelemetry Collector or OpenTelemetry language SDK can be sent to Elastic.

You can set up an OpenTelemetry Collector based on contrib OpenTelemetry, instrument your application with an OpenTelemetry language SDK that sends data to the Collector, and use the Collector to process and export the data to either the [Managed OTLP endpoint](opentelemetry://reference/motlp.md) or {{apm-server-or-mis}}.

This approach works well when you need to instrument a technology that Elastic doesn’t provide a solution for. For example, if you want to instrument C or C++ you can use the [OpenTelemetry C++ client](https://github.com/open-telemetry/opentelemetry-cpp). However, there are some limitations when using contrib OpenTelemetry collectors and language SDKs, including:

* Elastic can’t provide implementation support on how to use contrib OpenTelemetry tools.
* You won’t have access to Elastic enterprise {{product.apm}} features.
* You might experience problems with performance efficiency.
* Data ingested through a contrib Collector won't trigger automatic installation of OpenTelemetry content-pack assets, such as dashboards. Only data ingested through {{agent}} does.

For more on the limitations associated with using contrib OpenTelemetry tools, refer to [Limitations](/solutions/observability/apm/opentelemetry/limitations.md).

[**Get started with contrib OpenTelemetry Collectors and language SDKs →**](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md)

:::{note}
To understand the differences between Elastic Distributions of OpenTelemetry and contrib OpenTelemetry, refer to [{{edot}} compared to contrib OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md).
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

To get started, follow the official AWS Distribution for OpenTelemetry Lambda documentation, and [configure {{agent}} in Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode) to send traces and metrics to your Elastic cluster:

[**Get started with the AWS Distro for OpenTelemetry Lambda**](https://aws-otel.github.io/docs/getting-started/lambda)
