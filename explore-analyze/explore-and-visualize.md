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

You've ingested data into Elasticsearch. Now it's time to make sense of it. Whether you're a security analyst hunting for threats, an SRE investigating a latency spike, or a data engineer validating a pipeline, the exploration and visualization tools in the Elasticsearch platform help you move from raw data to understanding. These tools are available in every Elastic solution and project type, so the skills you build here apply everywhere.

The journey typically follows a natural progression: start by exploring your data interactively, then build visualizations to surface patterns, and finally compose dashboards that you and your team can use for ongoing monitoring and decision-making.

## Discover: start with exploration

[Discover](discover.md) is where most analysis begins. It gives you direct access to the documents in your Elasticsearch indices, letting you search, filter, and examine your data in real time.

:::{image} /explore-analyze/images/explore-analyze-discover.png
:alt: The Discover interface showing document exploration
:screenshot:
:::

Use Discover when you need to investigate a specific issue, understand what data you have, or validate the results of an ingestion pipeline. You can search using KQL, Lucene, or ES|QL, then drill into individual documents, compare fields across records, and spot patterns in your log data. When you find something worth keeping, save your session and add it to a dashboard.

[Learn more about Discover →](discover.md)

## Dashboards: compose views for monitoring and sharing

[Dashboards](dashboards.md) bring multiple visualizations together into a single, interactive view. A dashboard can combine charts, metrics, maps, and text to tell a complete data story — and anyone on your team can use filters, time controls, and drilldowns to explore the data further without needing to build anything from scratch.

:::{image} /explore-analyze/images/kibana-dashboard-overview.png
:alt: A dashboard combining multiple visualization panels
:screenshot:
:::

Dashboards are the primary way teams monitor ongoing activity: deployment health, security posture, business metrics, or application performance. They're shareable, embeddable, and can power scheduled reports.

[Learn more about dashboards →](dashboards.md)

## Panels and visualizations: the building blocks

Every chart, table, map, or metric on a dashboard is a **panel**. [Panels and visualizations](visualize.md) are the building blocks you use to represent your data visually.

The primary editor is **Lens**, which provides a drag-and-drop interface for building charts, tables, metrics, and more. For specialized needs, you can use **Maps** for geospatial data, **Canvas** for pixel-perfect presentations, **Vega** for fully custom visualizations, or **ES|QL** for query-driven charts. You can also add context with text, images, and link panels.

[Learn more about panels and visualizations →](visualize.md)

## Find and organize your content

As your collection of dashboards, visualizations, and saved searches grows, [data views](find-and-organize/data-views.md), [tags](find-and-organize/tags.md), and [saved objects](find-and-organize/saved-objects.md) help you keep everything organized and easy to find. Data views define which Elasticsearch indices a visualization or Discover session queries, while tags and spaces let you group related content by team, project, or domain.

[Learn more about finding and organizing content →](find-and-organize.md)

## How these tools work across Elastic solutions

The exploration and visualization capabilities described here aren't limited to a single use case. They form a shared foundation that Elastic solutions build on:

- **Elastic Observability** uses dashboards and Discover to surface infrastructure metrics, application traces, and log patterns. SLO panels and anomaly charts plug directly into dashboards.
- **Elastic Security** adds specialized views for detection alerts, investigation timelines, and threat intelligence — but the underlying dashboard and visualization infrastructure is the same.
- **Elasticsearch projects** use these tools for search analytics, relevance tuning, and content exploration.

No matter which solution or project type you're using, the skills and workflows you learn here transfer directly.

## Next steps

- **[Learn data exploration and visualization](kibana-data-exploration-learning-tutorial.md)**: A hands-on tutorial that walks you through exploring data with Discover, building a visualization with Lens, and composing a dashboard.
- **[Get started with Discover](discover/discover-get-started.md)**: Explore fields, apply filters, and get familiar with the Discover interface.
- **[Create your first dashboard](dashboards/create-dashboard.md)**: Start with a blank dashboard and add panels to build your first view.
