---
navigation_title: "OpenTelemetry"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry.html
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry.html
applies_to:
  stack:
  serverless:
---

# Use OpenTelemetry with APM [apm-open-telemetry]

:::{include} _snippets/apm-server-vs-mis.md
:::

::::{note}
For a complete overview of using OpenTelemetry with Elastic, explore [**Elastic Distributions of OpenTelemetry**](https://github.com/elastic/opentelemetry).
::::

[OpenTelemetry](https://opentelemetry.io/docs/concepts/what-is-opentelemetry/) is a set of APIs, SDKs, tooling, and integrations that enable the capture and management of telemetry data from your services and applications.

Elastic integrates with OpenTelemetry, allowing you to reuse your existing instrumentation to easily send observability data to the {{stack}}. You can integrate OpenTelemetry with the {{stack}} the following ways:

* [Elastic Distributions of OpenTelemetry language SDKs](#apm-otel-elastic-distros)
* [AWS Lambda collector exporter](#apm-otel-lambda)

## Elastic Distributions of OpenTelemetry language SDKs [apm-otel-elastic-distros]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

Elastic offers several distributions of OpenTelemetry language SDKs. A *distribution* is a customized version of an upstream OpenTelemetry repository. Each Elastic Distribution of OpenTelemetry is a customized version of an [OpenTelemetry language SDK](https://opentelemetry.io/docs/languages/).

:::{image} /solutions/images/observability-apm-otel-distro.png
:alt: apm otel distro
:screenshot:
:::

With an Elastic Distribution of OpenTelemetry language SDK you have access to all the features of the OpenTelemetry SDK that it customizes, plus:

* You may get access to SDK improvements and bug fixes contributed by the Elastic team *before* the changes are available upstream in the OpenTelemetry repositories.
* The distribution preconfigures the collection of tracing and metrics signals, applying some opinionated defaults, such as which sources are collected by default.

Get started with an Elastic Distribution of OpenTelemetry language SDK:

* [**Elastic Distribution of OpenTelemetry Java →**](https://elastic.github.io/opentelemetry/edot-sdks/java/index.html)
* [preview] [**Elastic Distribution of OpenTelemetry .NET →**](https://elastic.github.io/opentelemetry/edot-sdks/dotnet/index.html)
* [preview] [**Elastic Distribution of OpenTelemetry Node.js →**](https://elastic.github.io/opentelemetry/edot-sdks/nodejs/index.html)
* [preview] [**Elastic Distribution of OpenTelemetry Python →**](https://elastic.github.io/opentelemetry/edot-sdks/python/index.html)
* [preview] [**Elastic Distribution of OpenTelemetry PHP →**](https://elastic.github.io/opentelemetry/edot-sdks/php/index.html)

::::{note}
For more details about OpenTelemetry distributions in general, visit the [OpenTelemetry documentation](https://opentelemetry.io/docs/concepts/distributions).

::::

## AWS Lambda collector exporter [apm-otel-lambda]

AWS Lambda functions can be instrumented with OpenTelemetry and monitored with Elastic {{observability}} or {{obs-serverless}}.

To get started, follow the official AWS Distro for OpenTelemetry Lambda documentation, and configure the OpenTelemetry Collector to output traces and metrics to your Elastic cluster:

[**Get started with the AWS Distro for OpenTelemetry Lambda**](https://aws-otel.github.io/docs/getting-started/lambda)