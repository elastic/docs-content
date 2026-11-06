---
navigation_title: Search performance
description: Understand what affects search performance in Observability serverless projects, how to recognize saturated search capacity, and how to reduce load.
applies_to:
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
type: overview
sub:
  search-load-sources: Alerting rules, SLOs, transforms, dashboards, Discover, ES|QL queries, and external clients that query the project
  search-saturation-signals: failed or timed-out alerting rule runs
  search-reduce-load: disable alerting rules you don't need, stagger rule schedules, and narrow time ranges on dashboards and in Discover
---

# Understand search capacity and alerting performance

:::{include} /solutions/_snippets/serverless-search-performance-intro.md
:::

:::{include} /solutions/_snippets/serverless-search-performance.md
:::
