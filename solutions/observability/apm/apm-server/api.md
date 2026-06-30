---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# {{apm-server}} API [apm-api]

{{apm-server}} exposes endpoints for:

* [{{apm-server}} information API](/solutions/observability/apm/apm-server/information-api.md)
* [Elastic {{product.apm}} events intake API](/solutions/observability/apm/elastic-apm-events-intake-api.md)
* [Elastic {{apm-agent}} configuration API](/solutions/observability/apm/elastic-apm-agent-configuration-api.md)
* [OpenTelemetry intake API](/solutions/observability/apm/opentelemetry-intake-api.md)
* [Jaeger event intake](/solutions/observability/apm/jaeger-event-intake.md)

:::{note}
For new users, Elastic recommends using the OpenTelemetry path through the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or [Managed OTLP](opentelemetry://reference/motlp.md) rather than sending data directly to the {{apm-server}}.
:::

