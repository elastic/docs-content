---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Application performance monitoring (APM) [apm]

Elastic APM is an application performance monitoring system built on the {{stack}}. It allows you to monitor software services and applications in real time, by collecting detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more. This makes it easy to pinpoint and fix performance problems quickly.

:::{image} /solutions/images/observability-apm-app-landing.png
:alt: Applications UI in {{kib}}
:screenshot:
:::

Elastic APM also automatically collects unhandled errors and exceptions. Errors are grouped based primarily on the stack trace, so you can identify new errors as they appear and keep an eye on how many times specific errors happen.

Metrics are another vital source of information when debugging production systems. Elastic APM agents automatically pick up basic host-level metrics and agent-specific metrics, like JVM metrics in the Java Agent, and Go runtime metrics in the Go Agent.

## Give Elastic APM a try [give_elastic_apm_a_try]

Want to quickly spin up an APM deployment? Refer to [Get started for APM](/solutions/observability/apm/get-started.md). We recommend using the [Elastic Distributions of OpenTelemetry (EDOT)](/solutions/observability/apm/opentelemetry/index.md) as the preferred way to collect application telemetry data. To host everything yourself instead, refer to [Set up APM Server](/solutions/observability/apm/apm-server/setup.md).