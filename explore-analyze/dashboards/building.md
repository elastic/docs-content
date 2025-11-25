---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-dashboards.html
description: Build powerful Kibana dashboards using visualizations, metrics, text, images, and interactive controls to monitor and analyze your data.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Building dashboards [create-dashboards]

{{product.kibana}} offers many ways to build powerful dashboards that help you visualize and keep track of the most important information in your {{product.elasticsearch}} data. Combine multiple visualizations, metrics, and interactive elements into a cohesive view that tells your data story and enables rapid decision-making.

You can:

* Create and assemble visualizations such as charts or maps, and enrich them with helpful legends containing key data
* Extract and show key indicators and metrics to keep them visible and highlighted at all times
* Add text, images, and links to help viewers make the most of your dashboard
* Include additional controls to facilitate filtering and browsing the data

## Requirements [dashboard-minimum-requirements]

To create or edit dashboards, you need:

* [Data indexed into {{product.elasticsearch}}](/manage-data/ingest.md) and a [data view](../find-and-organize/data-views.md). A data view is a subset of your {{product.elasticsearch}} data, and allows you to load the right data when building a visualization or exploring it.

  ::::{tip}
  If you don't have data at hand and still want to explore dashboards, you can import one of the [sample data sets](../../manage-data/ingest/sample-data.md) available.
  ::::

* Sufficient permissions on the **Dashboard** feature. If that's not the case, you might get a read-only indicator. A {{product.kibana}} administrator can [grant you the required privileges](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
