---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/dashboard.html
---

# Dashboards [dashboard]

Dashboards are the best way to visualize and share insights from your {{es}} data.

A **dashboard** is made of one or more **panels** that you can organize as you like. Each panel can display various types of content: **visualizations** such as charts, tables, metrics, and maps, **static annotations** like text or images, or even **specialized views** for Machine Learning or Observability data.

![Example dashboard](../images/kibana-dashboard-overview.png "")

There are several [panel editors](visualize.md#panels-editors) in {{kib}} that let you create and configure different types of visualizations.

At any time, you can [share a dashboard](dashboards/sharing.md) you’ve created with your team, in {{kib}} or outside.

Some dashboards are created and managed by the system, and are identified as `managed` in your list of dashboards. This generally happens when you set up an integration to add data. You can’t edit managed dashboards directly, but you can [duplicate](dashboards/duplicate-dashboards.md) them and edit these duplicates.
