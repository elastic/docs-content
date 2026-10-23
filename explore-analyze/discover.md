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

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: A view of the Discover app in ES|QL mode
:screenshot:
:::

**Discover** has two query modes. In {{esql}} mode, a query defines the data, so you don't need a data view. Classic mode uses data views with Kibana Query Language (KQL) or Lucene.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Discover** opens in {{esql}} mode by default. To use data views with KQL or Lucene, switch to classic mode. Refer to [Switch between {{esql}} and classic mode](discover/switch-esql-mode.md).

## Where to go next

* **[Introduction to Discover](discover/discover-get-started.md)** - See what **Discover** shows you, what people use it for, and where to find the guide for each task.
* **[Get started with {{esql}} in Discover](discover/try-esql.md)** - Run your first {{esql}} query on sample data, step by step.
* **[Use Discover with {{esql}}](discover/use-esql.md)** - Find the Discover tasks that are specific to {{esql}} mode.
* **[Use Discover in classic mode](discover/use-classic-mode.md)** - Find the tasks that are specific to classic mode, such as searching with KQL or Lucene and adding filters.
* **[Customize the Discover view](discover/document-explorer.md)** - Adjust the layout, columns, and display options to suit your needs.
* **[Save a Discover session for reuse](discover/save-open-search.md)** - Save your Discover sessions and add them to dashboards.

## More guides

* [Inspect documents and requests in Discover](discover/inspect-documents.md)
* [Run queries in the background](discover/background-search.md)
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [Detect change points in time series data](discover/detect-change-points.md)
* [Search for relevance](discover/discover-search-for-relevance.md)
* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` [Analyze your data with AI in Discover](discover/analyze-discover-data-with-ai.md)
