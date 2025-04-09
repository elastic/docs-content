---
navigation_title: "Filter and search data"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-filter-and-search-data.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-filter-and-search-data.html
applies_to:
  stack:
  serverless:
---

# Filter and search application data [apm-filter-and-search-data]

Because Elastic APM is built on top of the {{stack}}, you have the full power of Elastic’s powerful search capabilities to filter and search through your application data. Mastering how to filter and search your data can help you find bottlenecks in your code faster:

* Use global filters to [filter data](/solutions/observability/apps/filter-application-data.md) across the Applications UI based on a specific time range or environment.
* Use [advanced queries](/solutions/observability/apps/use-advanced-queries-on-application-data.md) on your data to filter on specific pieces of information.
* Use {{es}}'s [cross-cluster search](/solutions/observability/apps/cross-cluster-search-with-application-data.md) functionality to search APM data across multiple sources.