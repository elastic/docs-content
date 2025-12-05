---
navigation_title: Dashboards
description: Visualize and share insights from your Elasticsearch data using interactive panels, charts, maps, and custom filters.
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/dashboard.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Dashboards [dashboard]

**Dashboards** provide the primary way to visualize and share insights from your {{es}} data. They allow you to build interactive displays that combine multiple visualizations, metrics, and controls into a single view that helps you and your team monitor trends, investigate issues, and make data-driven decisions.

A dashboard is composed of one or more **panels** that you arrange to tell your data story. Each panel can display visualizations such as charts, tables, metrics, and maps, static annotations like text or images, or specialized views for {{ml}} or {{observability}} data.

![Example dashboard](/explore-analyze/images/kibana-dashboard-overview.png "")

## Get started with dashboards [get-started-with-dashboards]

New to dashboards? Start with these hands-on tutorials that walk you through creating your first dashboards using sample data:

- [Create a simple dashboard to monitor website logs](dashboards/create-dashboard-of-panels-with-web-server-data.md): Build a dashboard with charts, metrics, and filters to analyze web traffic patterns.
- [Create a dashboard with time series charts](dashboards/create-dashboard-of-panels-with-ecommerce-data.md): Learn to visualize sales trends and patterns over time using ecommerce data.


## Work with dashboards [work-with-dashboards]

Once you understand the basics, explore these common tasks:

**Build and customize dashboards**:
- [Build dashboards](dashboards/building.md): Learn the fundamentals of creating and configuring dashboards.
- [Create a dashboard](dashboards/create-dashboard.md): Start with an empty dashboard and add your content.
- [Add filter controls](dashboards/add-controls.md): Enable interactive filtering with options lists, range sliders, and time sliders.
- [Add drilldowns](dashboards/drilldowns.md): Create interactive navigation between dashboards or to external URLs.
- [Organize dashboard panels](dashboards/arrange-panels.md): Arrange panels using collapsible sections, resizing, and positioning.

**Explore and interact**:
- [Explore dashboards](dashboards/using.md): Filter data, adjust time ranges, and interact with panels to uncover insights.

**Manage and share**:
- [Manage dashboards](dashboards/managing.md): Browse, search, organize, and track usage of your dashboards.
- [Share dashboards](dashboards/sharing.md): Share with your team using links, embeds, or file exports.
- [Duplicate a dashboard](dashboards/duplicate-dashboards.md): Create customizable copies of existing dashboards.
- [Import a dashboard](dashboards/import-dashboards.md): Bring dashboards from other environments.

## About managed dashboards [managed-dashboards]

Some dashboards are created and managed by the system, and are identified as `managed` in your list of dashboards. This generally happens when you set up an integration to add data. You can't edit managed dashboards directly, but you can [duplicate](dashboards/duplicate-dashboards.md) them and edit the duplicates.
