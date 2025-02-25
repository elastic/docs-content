---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-filters.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-filter-your-data.html

navigation_title: "Filters"
---

# Filter application data [apm-filter-your-data]


Global filters are ways you can filter your APM data based on a specific time range or environment. When viewing a specific service, the filter persists as you move between tabs.

:::{image} ../../../images/observability-global-filters.png
:alt: Global filters view
:class: screenshot
:::

::::{note}
If you prefer to use advanced queries on your data to filter on specific pieces of information, see [Query your data](../../../solutions/observability/apps/use-advanced-queries-on-application-data.md).

::::



## Global time range [apm-filter-your-data-global-time-range]

The global time range filter restricts APM data to a specific time period.


## Service environment filter [apm-filter-your-data-service-environment-filter]

The environment selector is a global filter for `service.environment`. It allows you to view only relevant data and is especially useful for separating development from production environments. By default, all environments are displayed. If there are no environment options, you’ll see "not defined".

Service environments are defined when configuring your APM agents. It’s vital to be consistent when naming environments in your APM agents. To learn how to configure service environments, see the specific APM agent documentation:

* **Go:** [`ELASTIC_APM_ENVIRONMENT`](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md#config-environment)
* **iOS agent:** *Not yet supported*
* **Java:** [`environment`](asciidocalypse://docs/apm-agent-java/docs/reference/ingestion-tools/apm-agent-java/config-core.md#config-environment)
* **.NET:** [`Environment`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/ingestion-tools/apm-agent-dotnet/config-core.md#config-environment)
* **Node.js:** [`environment`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/ingestion-tools/apm-agent-nodejs/configuration.md#environment)
* **PHP:** [`environment`](asciidocalypse://docs/apm-agent-php/docs/reference/ingestion-tools/apm-agent-php/configuration-reference.md#config-environment)
* **Python:** [`environment`](asciidocalypse://docs/apm-agent-python/docs/reference/ingestion-tools/apm-agent-python/configuration.md#config-environment)
* **Ruby:** [`environment`](asciidocalypse://docs/apm-agent-ruby/docs/reference/ingestion-tools/apm-agent-ruby/configuration.md#config-environment)
* **Real User Monitoring (Elastic Stack only):** [`environment`](asciidocalypse://docs/apm-agent-rum-js/docs/reference/ingestion-tools/apm-agent-rum-js/configuration.md#environment)