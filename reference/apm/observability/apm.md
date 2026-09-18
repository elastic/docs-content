---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm.html
products:
  - id: observability
description: Monitor instrumented services with Elastic APM using traces, errors, and runtime metrics to analyze application performance and failures.
---

# APM [apm]

Elastic APM is an application performance monitoring system built on the {{stack}}. It continuously collects performance data from instrumented services and applications. For supported frameworks and libraries, this data includes response times for incoming requests, database queries, cache calls, and external HTTP requests.

:::{image} /reference/apm/images/observability-apm-app-landing.png
:alt: Service inventory showing latency, throughput, and failed transaction rate
:screenshot:
:::

Elastic APM agents automatically report exceptions captured by their supported instrumentations. Errors are grouped using their exception type and stack frames, with a message-based fallback when no usable stack trace exists. You can identify new error groups and track how often each error occurs.

Server-side APM agents collect a language-specific set of system, process, and runtime metrics, such as Java virtual machine (JVM) metrics from the Java agent and Go runtime metrics from the Go agent.


## Give Elastic APM a try [_give_elastic_apm_a_try]

To start collecting application telemetry, refer to [Get started with traces and APM](/solutions/observability/apm/get-started.md). We recommend using [{{edot}}](/solutions/observability/apm/opentelemetry/index.md). For self-managed OpenTelemetry ingestion, [deploy {{agent}} in Gateway mode](elastic-agent://reference/edot-collector/config/default-config-standalone.md#gateway-mode). If you use classic Elastic APM agents, you can instead [set up APM Server](/solutions/observability/apm/apm-server/setup.md).
