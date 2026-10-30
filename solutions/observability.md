---
navigation_title: Observability solution
meta_title: Elastic Observability overview
description: Unify logs, metrics, traces, user experience data, and synthetic monitoring with Elastic Observability to investigate application and infrastructure problems.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/what-is-observability-serverless.html
  - https://www.elastic.co/guide/en/observability/current/index.html
  - https://www.elastic.co/guide/en/kibana/current/observability.html
applies_to:
  stack:
  serverless:
products:
  - id: cloud-serverless
  - id: observability
  - id: kibana
  - id: edot-collector
sub:
  search-load-sources: Alerting rules, SLOs, transforms, dashboards, Discover, ES|QL queries, and external clients that query the project
  search-saturation-signals: failed or timed-out alerting rule runs
  search-reduce-load: disable alerting rules you don't need, stagger rule schedules, and narrow time ranges on dashboards and in Discover
---

# Elastic Observability solution overview

:::{include} ../get-started/_snippets/observability-overview.md
:::

## Search performance [observability-search-performance]
```{applies_to}
serverless: ga
```

:::{include} /solutions/_snippets/serverless-search-performance.md
:::

## Related reference [_reference_documentation]

The {{observability}} reference documentation is available in the [Elastic reference documentation](/reference/observability/index.md).

You can also browse reference documentation for the following components:

- [{{edot}}](opentelemetry://reference/index.md)
- [Fleet and Elastic Agent](/reference/fleet/index.md)
- [Elastic APM](/reference/apm/observability/apm.md)
- [Elastic APM agents](/reference/apm-agents/index.md)

Browse the latest [{{observability}} release notes](/release-notes/elastic-observability/index.md) for more information on new features, enhancements, and fixes.

