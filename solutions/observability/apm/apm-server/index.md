---
applies_to:
  stack: ga
  serverless: unavailable
---

# Work with {{apm-server}}

When self-managing the {{stack}}, {{apm-server}} receives performance data from {{product.apm}} agents,
validates and processes it, and transforms the data into {{es}} documents.

This section contains information on working with {{apm-server}} including:

* Learning how to [set up {{apm-server}}](/solutions/observability/apm/apm-server/setup.md)
* Browsing all available [{{apm-server}} configuration options](/solutions/observability/apm/apm-server/configure.md)
* [Monitoring the real-time health and performance](/solutions/observability/apm/apm-server/monitor.md) of your {{apm-server}}

:::{tip}
If you're using {{serverless-full}}, there is no {{apm-server}} running. Instead the _managed intake service_ receives and transforms data. Read more in [](/solutions/observability/apm/get-started.md).
:::

:::{note}
For new users, Elastic recommends using the OpenTelemetry path through the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or [Managed OTLP](opentelemetry://reference/motlp.md) rather than sending data directly to the {{apm-server}}.
:::
