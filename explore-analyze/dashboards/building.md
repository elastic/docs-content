---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-dashboards.html
description: Build dashboards in Kibana with visualizations, charts, maps, and controls to track key metrics and enable data exploration across Elasticsearch data.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Build dashboards [create-dashboards]

Dashboards in {{product.kibana}} combine multiple visualizations, metrics, and controls into a single view that tells a story about your data. You can create dashboards from scratch, start with templates, or assemble panels from the Visualize Library.

This section covers the key concepts and requirements for building dashboards. To get started, you need indexed data in {{product.elasticsearch}} and a {{data-source}} that defines which data to analyze.

$$$dashboard-minimum-requirements$$$
To create or edit dashboards, you first need to:

* have [data indexed into {{product.elasticsearch}}](/manage-data/ingest.md) and a [data view](../find-and-organize/data-views.md). A data view is a subset of your {{product.elasticsearch}} data, and allows you to load the right data when building a visualization or exploring it.

  ::::{tip}
  If you don’t have data at hand and still want to explore dashboards, you can import one of the [sample data sets](../../manage-data/ingest/sample-data.md) available.
  ::::

* have sufficient permissions on the **Dashboard** feature. If that’s not the case, you might get a read-only indicator. A {{product.kibana}} administrator can [grant you the required privileges](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
