---
navigation_title: Filters
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-filters.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-filter-your-data.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Filter application data [apm-filter-your-data]

Global filters are ways you can filter your APM data based on a specific time range or environment. When viewing a specific service, the filter persists as you move between tabs.

:::{image} /solutions/images/observability-global-filters.png
:alt: Global filters view
:screenshot:
:::

::::{note}
If you prefer to use advanced queries on your data to filter on specific pieces of information, see [Query your data](/solutions/observability/apm/advanced-queries.md).

::::

## Global time range [apm-filter-your-data-global-time-range]

The global time range filter restricts APM data to a specific time period.

## Service environment filter [apm-filter-your-data-service-environment-filter]

The environment selector is a global filter for `service.environment`. It allows you to view only relevant data and is especially useful for separating development from production environments. By default, all environments are displayed. If there are no environment options, you’ll see "not defined".

Service environments are defined when configuring your APM agents. It’s vital to be consistent when naming environments in your APM agents. To learn how to configure service environments, see the specific APM agent documentation:

* **Go:** [`ELASTIC_APM_ENVIRONMENT`](apm-agent-go://reference/configuration.md#config-environment)
* **iOS agent:** *Not yet supported*
* **Java:** [`environment`](apm-agent-java://reference/config-core.md#config-environment)
* **.NET:** [`Environment`](apm-agent-dotnet://reference/config-core.md#config-environment)
* **Node.js:** [`environment`](apm-agent-nodejs://reference/configuration.md#environment)
* **PHP:** [`environment`](apm-agent-php://reference/configuration-reference.md#config-environment)
* **Python:** [`environment`](apm-agent-python://reference/configuration.md#config-environment)
* **Ruby:** [`environment`](apm-agent-ruby://reference/configuration.md#config-environment)
* **Real User Monitoring (Elastic Stack only):** [`environment`](apm-agent-rum-js://reference/configuration.md#environment)