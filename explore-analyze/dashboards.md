---
navigation_title: Dashboards
description: Kibana dashboards turn your Elasticsearch data into interactive charts, maps, and filters. Start with dashboard examples, then build and share your own.
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/dashboard.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# {{kib}} dashboards [dashboard]

{{kib}} **dashboards** provide the primary way to visualize and share insights from your {{es}} data. They allow you to build interactive displays that combine multiple visualizations, metrics, and controls into a single view that helps you and your team monitor trends, investigate issues, and make data-driven decisions.

A dashboard is composed of one or more **panels** that you arrange to tell your data story. Each panel can display visualizations such as charts, tables, metrics, and maps, static annotations like text or images, or specialized views for {{ml}} or {{observability}} data.

![Example dashboard](/explore-analyze/images/kibana-dashboard-overview.png "")

## Get started with dashboard examples [get-started-with-dashboards]

New to dashboards? These hands-on examples walk you through creating your first dashboards using sample data:

- [Example: Website logs](dashboards/create-dashboard-of-panels-with-web-server-data.md): Build a dashboard with charts, metrics, and filters to analyze web traffic patterns.
- [Example: Time series from eCommerce data](dashboards/create-dashboard-of-panels-with-ecommerce-data.md): Learn to visualize sales trends and patterns over time using eCommerce data.


## Work with dashboards [work-with-dashboards]

Once you understand the basics, explore these common tasks:

**Explore and interact**
- [](dashboards/using.md): Filter data, adjust time ranges, and interact with panels to uncover insights.

**Build and customize dashboards**
- [](dashboards/building.md): Compare the UI, REST APIs, and AI approaches to find the one that fits how you work.
- [Create a dashboard](dashboards/create-dashboard.md): Start with an empty dashboard and add your content.
- [Create dashboards using AI](dashboards/create-dashboards-using-ai.md): Generate dashboards from natural language through chat with {{agent-builder}}.
- [Add dashboard controls](visualize/dashboard-controls.md): Enable interactive filtering with options lists, range sliders, time sliders, and ES|QL variable controls.
- [Drilldowns](dashboards/drilldowns.md): Open another dashboard, a URL, or Discover from a panel.
- [Organize dashboard panels](dashboards/arrange-panels.md): Arrange panels using collapsible sections, resizing, and positioning.

**Manage and share**
- [Manage dashboards](dashboards/managing.md): Browse, search, organize, and track usage of your dashboards.
- [](dashboards/sharing.md): Share with your team using links or embeds, and export as PDF, PNG, CSV, or JSON.
- [Duplicate a dashboard](dashboards/duplicate-dashboards.md): Create customizable copies of existing dashboards.
- [Import a dashboard](dashboards/import-dashboards.md): Bring a dashboard from another space, instance, or deployment into your own.

## About managed dashboards [managed-dashboards]

Some dashboards are created and managed by the system, and are identified as `managed` in your list of dashboards. This generally happens when you set up an integration to add data. You can't edit managed dashboards directly, but you can [duplicate](dashboards/duplicate-dashboards.md) them and edit the duplicates.

