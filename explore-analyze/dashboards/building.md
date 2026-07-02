---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/create-dashboards.html
description: Choose how to create Kibana dashboards — from the UI, programmatically using REST APIs, or using AI-powered tools — and find the right starting point for your workflow.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
---

# Building dashboards [create-dashboards]

{{product.kibana}} offers many ways to build powerful dashboards that help you visualize and keep track of the most important information in your {{product.elasticsearch}} data. Combine multiple visualizations, metrics, and interactive elements into a cohesive view that tells your data story and enables rapid decision-making.

Use the following table to find the right approach for building your dashboards, then follow the link to get started.

| Approach | When to use this | What you get |
|---|---|---|
| [Create a dashboard from the UI](create-dashboard.md) | Exploring data interactively and assembling dashboards panel by panel | Saved dashboard |
| [Create dashboards programmatically](create-dashboards-programmatically.md) | Automating deployments, managing dashboards and visualizations as code, CI/CD pipelines | Saved dashboard or visualization |
| [Create dashboards using AI](create-dashboards-using-ai.md) | Generating dashboards from natural language, or building AI tools that create dashboards | Dashboard through chat that you save when ready, or saved dashboard using the API |

Once you have a dashboard, you can enhance it:

* [Add filter controls](add-controls.md) to let viewers explore the data interactively
* [Add drilldowns](drilldowns.md) to navigate between dashboards or to external URLs
* [Arrange and resize panels](arrange-panels.md) to optimize its layout

To [manage your dashboards](managing.md) over time, you can [duplicate](duplicate-dashboards.md) them as a starting point for new ones, [import](import-dashboards.md) them from another space, instance, or deployment, and [share or export](sharing.md) them. For repeatable, auditable changes, [manage your dashboards as code](manage-dashboards-as-code.md) to version-control their definitions and deploy them across environments.

## Requirements [dashboard-minimum-requirements]

To create or edit dashboards, you need:

* [Data indexed into {{product.elasticsearch}}](/manage-data/ingest.md) and a [data view](../find-and-organize/data-views.md). A data view is a subset of your {{product.elasticsearch}} data, and allows you to load the right data when building a visualization or exploring it.

  ::::{tip}
  If you don't have data at hand and still want to explore dashboards, you can import one of the [sample data sets](../../manage-data/ingest/sample-data.md) available.
  ::::

* Sufficient privileges for the **Dashboard** feature. Without them, you might get a read-only indicator. A {{product.kibana}} administrator can [grant you the required privileges](../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
