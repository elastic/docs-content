---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/painlesslab.html
---

# Painless lab [painlesslab]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::

The **Painless Lab** is an interactive code editor that lets you test and debug [Painless scripts](modules-scripting-painless.md) in real-time. You can use the Painless scripting language to create [{{kib}} runtime fields](../find-and-organize/data-views.md#runtime-fields), process [reindexed data](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex), define complex [Watcher conditions](../alerts-cases/watcher.md), and work with data in other contexts.

Find **Painless Lab** by navigating to the **Developer tools** page using the navigation menu or the [global search field](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} ../../images/kibana-painless-lab.png
:alt: Painless Lab
:class: screenshot
:::
