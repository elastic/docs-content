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

* **[Explore fields and data with Discover](discover/discover-get-started.md)** - Explore with data views and KQL or Lucene in classic mode.
* **[Get started with {{esql}} in Discover](discover/try-esql.md)** - A hands-on tutorial for a first session in {{esql}} mode.

Discover has two query modes. {{esql}} does not require a data view. Classic mode uses data views with KQL or Lucene.

## Common tasks

Once you're familiar with the basics, explore these guides for specific tasks:

* **[Use Discover with {{esql}}](discover/use-esql.md)** - Switch modes, work with results, and the other {{esql}} jobs in Discover.
* **[Search and filter data](discover/discover-get-started.md)** - Build queries and apply filters to narrow down your results.
* **[Customize the Discover view](discover/document-explorer.md)** - Adjust the layout, columns, and display options to suit your needs.
* **[Save a search for reuse](discover/save-open-search.md)** - Save your Discover sessions and add them to dashboards.

## Advanced features

The following guides cover additional features you can use in Discover:

* [Add runtime fields to your {{data-source}}](discover/discover-get-started.md#add-field-in-discover)
* [Run queries in the background](discover/background-search.md)
* [Analyze field statistics and patterns](discover/run-pattern-analysis-discover.md)
* {applies_to}`stack: ga 9.5+` [Detect change points in time series data](discover/detect-change-points.md)
* [Search for relevance](discover/discover-search-for-relevance.md)
