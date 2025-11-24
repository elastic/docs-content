---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Explore and analyze your Elasticsearch data with Discover in Kibana. Search, filter, visualize, and investigate documents to answer questions about your data.
---

# Explore and analyze data with Discover [discover]

**Discover** in {{kib}} is your primary tool for exploring and analyzing data stored in {{es}}. Use Discover to search and filter your data, investigate document structure and field values, create visualizations, and save your analysis for later use or sharing with your team.

Discover helps you answer questions about your data: What pages on your website contain specific terms? What events occurred most recently? Which processes exceed performance thresholds? With flexible querying using KQL, Lucene, or {{esql}}, you can quickly find the information you need.

:::{image} /explore-analyze/images/kibana-hello-field.png
:alt: A view of the Discover app
:screenshot:
:::

## What you can do with Discover

**Search and explore**
: Search through your data using KQL, Lucene, or {{esql}}. Filter results to focus on what matters. Discover adapts its interface based on the type of data you're exploring, providing specialized experiences for logs, metrics, and other data types.

**Analyze fields and documents**
: View field statistics, examine individual documents, compare multiple documents side by side, and find patterns in your log data.

**Visualize on the fly**
: Create quick visualizations from aggregatable fields, or use {{esql}} to build charts directly from your queries.

**Save and share**
: Save your Discover sessions to reuse later, add them to dashboards, or share them with your team. You can also generate reports and create alerts based on your searches.

## Get started

New to Discover? Start with these resources:

* **[Get started with Discover](discover/discover-get-started.md)** - A hands-on tutorial that walks you through exploring data, from loading data to filtering and visualizing your findings.
* **[Using {{esql}}](discover/try-esql.md)** - Learn how to use the {{es}} Query Language for powerful data exploration.

## Common tasks

Once you're familiar with the basics, explore these guides for specific tasks:

* **[Search and filter data](discover/search-and-filter.md)** - Build queries and apply filters to narrow down your results.
* **[Customize the Discover view](discover/document-explorer.md)** - Adjust the layout, columns, and display options to suit your needs.
* **[Save a search for reuse](discover/save-open-search.md)** - Save your Discover sessions and add them to dashboards.

## Advanced features

For more sophisticated use cases, see **[Advanced Discover features](discover/discover-advanced-guides.md)**:

* Compare documents side by side
* Add runtime fields to your {{data-source}}
* Work with multiple tabs
* Understand context-aware experiences
* Run queries in the background
* Generate alerts
* Analyze field statistics and patterns
* Search for relevance

