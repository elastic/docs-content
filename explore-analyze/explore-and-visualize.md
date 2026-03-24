---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: >
  Explore your Elasticsearch data, build visualizations, and compose dashboards
  to monitor trends and share insights across your organization.
type: overview
---

# Explore and visualize your data

The {{es}} platform provides tools to explore, visualize, and monitor your data. They are available across all Elastic solutions and project types.

The typical workflow progresses through three stages:

1. **Explore** your data interactively with Discover.
2. **Visualize** patterns by building panels with Lens and other editors.
3. **Compose dashboards** that your team can use for ongoing monitoring and decision-making.

## Start exploring with Discover

[Discover](discover.md) gives you direct access to documents in your {{es}} indices to search, filter, and examine data in real time.

:::{image} /explore-analyze/images/kibana-esql-full-query.png
:alt: Discover in ES|QL mode showing a query with filtered results and a visualization
:screenshot:
:::

With Discover, you can:

- Search using KQL, Lucene, or {{esql}}
- Drill into individual documents and compare fields across records
- Spot patterns in your log data
- Save sessions and add them to dashboards

[Learn more about Discover →](discover.md)

## Compose views for monitoring and sharing with dashboards

[Dashboards](dashboards.md) bring multiple visualizations together into a single, interactive view. They combine charts, metrics, maps, and text, and anyone on your team can use filters, time controls, and drilldowns to explore further.

:::{image} /explore-analyze/images/kibana-learning-tutorial-dashboard-polished.png
:alt: A dashboard with metrics, time series charts, a bar chart, and a table
:screenshot:
:::

Dashboards are the primary way teams monitor deployment health, security posture, business metrics, or application performance. They're also shareable, embeddable, and can power scheduled reports.

[Learn more about dashboards →](dashboards.md)

## Add building blocks to your dashboards with panels and visualizations

Every chart, table, map, or metric on a dashboard is a **panel**. [Panels and visualizations](visualize.md) are the building blocks you use to represent your data visually.

- **Lens**: drag-and-drop editor for charts, tables, metrics, and more. Lens also supports an {{esql}} query mode for building visualizations directly from queries.
- **Maps**: geospatial data visualization
- **Canvas**: dynamic, multi-page presentations combining live data with custom styling, images, and text
- **Vega**: fully custom visualizations

You can also add context with text, images, and link panels.

[Learn more about panels and visualizations →](visualize.md)

## Find and organize your content

As your collection grows, these tools help you keep everything organized:

- [{{data-sources-cap}}](find-and-organize/data-views.md): define which {{es}} indices a visualization or Discover session queries
- [Tags](find-and-organize/tags.md) and [spaces](/deploy-manage/manage-spaces.md): group related content by team, project, or domain
- [Saved objects](find-and-organize/saved-objects.md): manage and export your dashboards, visualizations, and saved searches

[Learn more about finding and organizing content →](find-and-organize.md)

## How these tools work across Elastic solutions

These capabilities form a shared foundation across all Elastic solutions:

- **{{product.observability}}**: dashboards and Discover surface infrastructure metrics, application traces, and log patterns. SLO panels and anomaly charts plug directly into dashboards.
- **{{elastic-sec}}**: specialized views for detection alerts, investigation timelines, and threat intelligence, built on the same dashboard and visualization infrastructure.
- **{{es}} projects**: search analytics, relevance tuning, and content exploration.

What you learn here applies to every solution and project type.

## Next steps

- **[Learn data exploration and visualization](kibana-data-exploration-learning-tutorial.md)**: A hands-on tutorial that walks you through exploring data with Discover, building a visualization with Lens, and composing a dashboard.
- **[Get started with Discover](discover/discover-get-started.md)**: Explore fields, apply filters, and get familiar with the Discover interface.
- **[Create your first dashboard](dashboards/create-dashboard.md)**: Start with a blank dashboard and add panels to build your first view.
