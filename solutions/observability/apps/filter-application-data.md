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

* **Go:** [`ELASTIC_APM_ENVIRONMENT`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-environment)
* **iOS agent:** *Not yet supported*
* **Java:** [`environment`](https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-environment)
* **.NET:** [`Environment`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/config-core.html#config-environment)
* **Node.js:** [`environment`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#environment)
* **PHP:** [`environment`](https://www.elastic.co/guide/en/apm/agent/php/current/configuration-reference.html#config-environment)
* **Python:** [`environment`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-environment)
* **Ruby:** [`environment`](https://www.elastic.co/guide/en/apm/agent/ruby/current/configuration.html#config-environment)
* **Real User Monitoring:** [`environment`](https://www.elastic.co/guide/en/apm/agent/rum-js/current/configuration.html#environment)