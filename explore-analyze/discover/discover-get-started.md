---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-get-started.html
navigation_title: Introduction
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Learn what you can do in Discover, from querying your data to inspecting, visualizing, saving, and sharing results, and find the guide for each task.
---

# Introduction to Discover [discover-get-started]

When you need to look at the documents in your data, find out why something happened, or check that data arrived as expected, **Discover** is where you start. This page introduces what **Discover** shows you, how you work in it, and where to find the guide for each task. To learn by running a first query, follow [Get started with {{esql}} in Discover](try-esql.md).

To open **Discover**, find it in the navigation menu or use the [global search field](../find-and-organize/find-apps-and-objects.md).

## What people use Discover for

**Investigate a problem**
: Narrow your documents to the time range and the query that matter, then open individual documents to read every field. To run a first query, start with [Get started with {{esql}} in Discover](try-esql.md). Then use [Work with {{esql}} results in Discover](esql-results.md) and [Inspect documents and requests in Discover](inspect-documents.md).

**Check that your data is what you expect**
: See which fields exist and how their values are spread. Start with [Explore the fields in your data](explore-fields.md). In classic mode, [View field statistics](show-field-statistics.md) summarizes every field at once.

**Explore data you haven't seen before**
: In {{esql}} mode, query any index or data stream by name, without setting up a data view first. Start with [Get started with {{esql}} in Discover](try-esql.md).

**Spot patterns, spikes, and shifts**
: Group results to see what's common, and look for changes over time. Try [Inspect grouped STATS results in Discover](inspect-grouped-stats.md) or [Detect change points in Discover](detect-change-points.md). In classic mode, you can also [run a pattern analysis](run-pattern-analysis-discover.md). To have an AI agent look at the data for you, refer to [Analyze your data with AI in Discover](analyze-discover-data-with-ai.md).

**Share what you found, or keep an eye on it**
: [Save a Discover session](save-open-search.md), [copy results or send a link to a document](copy-and-share-documents.md), or [create an alert rule](generate-alerts-from-discover.md).

## What you see in Discover [discover-screen]

:::{image} /explore-analyze/images/kibana-discover-try-esql-from.png
:alt: Discover in ES|QL mode, with a query on the sample web logs, a chart of the results over time, the fields list, and the results table
:screenshot:
:::

A **Discover** session combines data, a query, and a time range. The chart and the table show what that combination returns, and you can refine each part as you explore.

Query bar or editor
: Where you write the query. In {{esql}} mode, it is an editor, and the query defines the data. In classic mode, you select a data view and write a Kibana Query Language (KQL) or Lucene query.

Time filter
: Keeps only the results in the time range you select.

Fields list
: Lists the fields of your data. Select a field to see its most frequent values.

Chart
: By default, shows how the results spread over the time range.

Results table
: Lists the results. The table is named **Results** in {{esql}} mode and **Documents** in classic mode.

Tabs
: {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Keep several explorations open side by side. Each tab has its own query, time range, and view.

## Two query modes [query-modes]

**Discover** has two query modes. In {{esql}} mode, you write a query that defines the data, so you don't need a data view. In classic mode, you select a data view, search with KQL or Lucene, and add filters.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Discover** opens in {{esql}} mode by default.

{applies_to}`stack: ga 9.0-9.5` **Discover** opens in classic mode by default.

To learn how the modes differ and what happens to your query when you switch, refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md). For the tasks in each mode, refer to [Use Discover with {{esql}}](use-esql.md) and [Use Discover in classic mode](use-classic-mode.md).

## How you work in Discover

### Get the data you need

Pick a query mode, then select the data and the time range, and narrow the results with a query.

- In {{esql}} mode, write a query that starts from a data source. The editor helps you [browse data sources and fields](browse-esql-sources.md), [change values without rewriting the query](esql-variable-controls.md), and [write or fix queries with AI](../query-filter/languages/esql-kibana.md#esql-kibana-ai-assistance).
- In classic mode, [select a data view and a time range](use-classic-mode.md#find-the-data-you-want-to-use), then [search and filter with KQL, Lucene, and filters](search-and-filter-classic.md).
- To keep working while a long query runs, [run it in the background](background-search.md).

### Shape and read the results

Control what the table and the chart show, and learn what your fields contain.

- To change columns, sorting, density, or switch to the JSON view, refer to [Customize the Discover view](document-explorer.md).
- To check what a field contains, refer to [Explore the fields in your data](explore-fields.md).
- To filter, sort, and keep the chart or the table from {{esql}} results, refer to [Work with {{esql}} results in Discover](esql-results.md).
- To run several explorations side by side, refer to [Run multiple explorations with tabs](work-with-tabs.md).
- To rank results by how well they match a search, refer to [Search for relevance](discover-search-for-relevance.md).

### Take it further

Look closer at a result, turn it into a chart, and keep or share your work.

- To read every field of a result or compare results, refer to [Inspect documents and requests in Discover](inspect-documents.md) and [Compare documents](compare-documents.md).
- To turn results into a visualization, refer to [Keep the chart or the table](esql-results.md#_edit_the_esql_visualization). In classic mode, you can also [visualize a field](visualize-field.md).
- To keep a session and use it in dashboards, refer to [Save a Discover session for reuse](save-open-search.md).
- To copy results or share links, refer to [Copy results and share links to documents](copy-and-share-documents.md).
- To be notified when data crosses a threshold, refer to [Create an alert rule from Discover](generate-alerts-from-discover.md).

## Context-aware experiences [context-aware-discover]

**Discover** provides tailored interfaces and features for the following data types when accessed from Observability or Security project types or {{kib}} solution views:

* Observability:
  * **[Logs exploration](/solutions/observability/logs/discover-logs.md)**
  * **[Metrics exploration](/solutions/observability/infra-and-hosts/discover-metrics.md)** {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2`
  * **[Traces exploration](/solutions/observability/apm/discover-traces.md)**
  {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2`
* Security:
  * **[Security data exploration](/solutions/security/investigate/discover-security.md)** {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1`

This context-aware experience is determined by both your solution context and the type of data you query. When both conditions align, **Discover** provides specific capabilities useful for exploring that specific type of data, and integrates features or paths to other relevant solution applications.

When you access **Discover** outside of a specific solution context, or when working with data types that don't have specialized experiences, you get the default **Discover** interface with all its core functionality for general-purpose data exploration.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.5` The active profile also shapes [AI-powered deep analysis](analyze-discover-data-with-ai.md): when you query logs, metrics, or traces from the matching solution context, the agent receives domain-specific guidance on which fields to group by and which {{esql}} commands to use. For example, it uses the `TS` command for time series metrics.

### Context-awareness with multiple data types

Your query may include multiple data types that each have tailored experiences; for example, if you query both `logs-*` and `traces-*` indices within an Observability context.

In this case **Discover** provides the default experience until it detects that you're interacting with a single type of data. For example, when you [look inside a document](inspect-documents.md#look-inside-a-document).

To check which experience is active, refer to [Check which context-aware experience is active](inspect-documents.md#view-active-context-aware-experience).

## Troubleshooting

If **Discover** asks you to add data or create a data view, refer to [Discover or Dashboards asks you to add data or create a data view](/troubleshoot/kibana/discover-dashboards-no-data-screen.md). If fields show as empty when they shouldn't, refer to [Some fields show as empty in Discover](/troubleshoot/kibana/discover-empty-fields.md).
