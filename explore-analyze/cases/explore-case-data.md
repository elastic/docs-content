---
navigation_title: Explore and visualize
applies_to:
  stack: preview 9.2-9.4, ga 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Use Discover and Lens to search, filter, and visualize case data from the case analytics indices.
---

# Explore and visualize case data [explore-case-analytics]

Case analytics data behaves like any other {{es}} data in [Discover](../discover.md) and [Lens](../visualize/lens.md), so you can inspect individual cases and build charts to spot trends. How you reach the data depends on your version.

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5", "serverless": "ga" }
In {{stack}} 9.5+ and {{serverless-short}}, the first time someone uses Cases in a space, {{kib}} creates a managed **Case Analytics** {{data-source}} for that space. The {{data-source}} covers all three analytics indices and is ready to use in Discover and Lens.

1. Go to [Discover](../discover.md) or [Lens](../visualize/lens.md).
2. Select the **Case Analytics** {{data-source}}.
3. Search, filter, and visualize case fields. To find typed case fields in the field list, filter by `_as_` (for example, `case.effort_as_integer`).

You can save visualizations to dashboards and use the same indices as the basis for [alerting rules](../alerting.md), like any other {{es}} data.
::::

::::{applies-item} stack: preview 9.2-9.4
In 9.2-9.4, create a [{{data-source}}](../find-and-organize/data-views.md) that points to one or more case analytics indices or their aliases. To point to all case analytics indices in your space, use the `.internal.cases*` index pattern.

:::{note}
Case data is stored in hidden indices. To display hidden indices, select **Show advanced settings**, then turn on **Allow hidden and system indices**.
:::
::::

:::::

## Next steps [explore-case-analytics-next]

[Query case data with {{esql}}](query-case-data-esql.md) to calculate metrics like case volume, closure rates, and MTTR.
