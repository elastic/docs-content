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

:::{image} /explore-analyze/images/kibana-discover-esql-errors.png
:alt: Discover in {{esql}} mode, with a query, a chart of errors over time, and the results table
:screenshot:
:::

## What you can do with Discover

**Search and explore**
: Search through your data using Kibana Query Language (KQL), Lucene, or {{esql}}. Filter results to focus on what matters. Discover adapts its interface based on the type of data you're exploring, providing specialized experiences for logs, metrics, and other data types.

**Analyze fields and documents**
: View field statistics, examine individual documents, compare multiple documents side by side, and find patterns in your log data.

**Visualize on the fly**
: Create quick visualizations from aggregatable fields, or use {{esql}} to build charts directly from your queries.

**Save and share**
: Save your Discover sessions to reuse later, add them to dashboards, or share them with your team. To export a session, refer to [Export as a file](report-and-share.md#manually-generate-reports).

   Large CSV exports can reach some limits. To see the limits for your deployment, how they differ between query modes, and what to do when you reach them, refer to [Export Discover session results as CSV](discover/save-open-search.md#export-discover-session-csv).

## Get started

New to Discover? Start with [Explore fields and data with Discover](discover/discover-get-started.md).

Discover has two query modes that you can [switch between](discover/switch-esql-mode.md):

- Classic mode uses [data views](find-and-organize/data-views.md) with [KQL](query-filter/languages/kql.md) or [Lucene](query-filter/languages/lucene-query-syntax.md) queries to filter your data.
- {{esql}} mode queries your {{es}} data directly, without a data view. For your first {{esql}} queries, follow [Get started with {{esql}} in Discover](discover/try-esql.md).

## Common goals

Once you're familiar with the basics, find what you need by what you want to achieve:

* **Find the documents that answer a question**: In {{esql}} mode, [filter and sort your results](discover/esql-results.md). In classic mode, [search with KQL, Lucene, and filters](discover/search-and-filter-classic.md), then [sort by relevance score](discover/discover-search-for-relevance.md) to see the best matches first.
* **Understand what's in your data**:
  * In classic mode, [check field statistics](discover/show-field-statistics.md), [chart a field](discover/visualize-field.md), [run a pattern analysis](discover/run-pattern-analysis-discover.md), or [add a runtime field](discover/add-fields-to-data-views.md) when your data lacks a value you need.
  * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` In {{esql}} mode, [group log messages by pattern](discover/inspect-grouped-stats.md).
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` **Spot changes over time**: [Detect change points in time series data](discover/detect-change-points.md).
* **Investigate one event in depth**: In classic mode, [open a single document or the documents around it](discover/view-single-document.md).
* **Keep working while a slow query runs**: [Run queries in the background](discover/background-search.md).
* **Reuse and share what you found**: [Save a Discover session](discover/save-open-search.md), then add it to a dashboard or share it with your team.
* **Make Discover fit how you work**: [Customize the Discover view](discover/document-explorer.md). In {{esql}} mode, [add variable controls](discover/esql-variable-controls.md) to change values without keeping several copies of a query.
