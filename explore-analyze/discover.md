---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Use Discover to search and filter documents, analyze field structures, visualize patterns, and save findings to reuse later or share with dashboards.
---

# Discover [discover]

**Discover** is the primary tool for exploring your {{product.elasticsearch}} data in {{product.kibana}}. Search and filter documents, analyze field structures, visualize patterns, and save findings to reuse later or share with dashboards. Whether investigating issues, analyzing trends, or validating data quality, **Discover** offers a flexible interface for understanding your data.

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

* **[Search and filter data](discover/discover-get-started.md)** - Build queries and apply filters to narrow down your results.
* **[Customize the Discover view](discover/document-explorer.md)** - Adjust the layout, columns, and display options to suit your needs.
* **[Save a search for reuse](discover/save-open-search.md)** - Save your Discover sessions and add them to dashboards.

## Advanced features

The following guides cover additional features you can use in Discover:

* [Add runtime fields to your {{data-source}}](discover/discover-get-started.md#add-field-in-discover)
* [Run queries in the background](discover/background-search.md)
* [Analyze field statistics and patterns](discover/run-pattern-analysis-discover.md)
* [Search for relevance](discover/discover-search-for-relevance.md)