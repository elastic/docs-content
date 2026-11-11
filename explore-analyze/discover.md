---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Use Discover to search and filter documents, analyze field structures, visualize patterns, and save findings to reuse later or share with dashboards.
type: overview
---

# Discover [discover]

If you need to find out why something happened, spot a trend, or check that your data arrived as expected, use **Discover** to query your {{product.elasticsearch}} data in {{product.kibana}}. The results appear as a table and, when the data allows it, a chart. From there, you can look into fields and documents, and save what you find to reuse later or share with dashboards.

:::{image} /explore-analyze/images/kibana-discover-overview.png
:alt: Discover in ES|QL mode with two tabs, a query on the sample web logs, the fields list, a chart of results over time, the results table with a search term highlighted, and the document flyout open
:screenshot:
:::

## Where to start [where-to-start]

- To learn the basics, including the two query modes, tabs, and context-aware experiences, read [How Discover works](discover/discover-get-started.md).
- To learn by running a first query, follow [Get started with {{esql}} in Discover](discover/try-esql.md).
- To work from a data view with KQL or Lucene, start with [Search and filter with KQL, Lucene, and filters in Discover's classic mode](discover/search-and-filter-classic.md).

## What you can do with Discover [what-you-can-do]

**Discover** has two query modes: {{esql}} mode, where you write an {{esql}} query, and classic mode, where you search a data view with KQL or Lucene. Tasks that work in only one mode say which.

**Query your data**

* Query your data in [{{esql}} mode](discover/use-esql.md) or in [classic mode](discover/use-classic-mode.md).
* [Open Discover from a dashboard panel](dashboards/create-discover-drilldown.md) with a drilldown.
* Run long queries in the [background](discover/background-search.md).
* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Keep [several explorations open side by side](discover/work-with-tabs.md) in tabs.

**Understand your data**

* Explore [individual results and documents](discover/inspect-documents.md).
* See [which fields your data has](discover/explore-fields.md) and what they contain, and break the chart down by a field.
* [Compare documents](discover/compare-documents.md) side by side.
* Find patterns in your log data with [pattern analysis](discover/run-pattern-analysis-discover.md) in classic mode, or with an [{{esql}} query that groups by pattern](discover/inspect-grouped-stats.md).
* Check [how the values of each field are distributed](discover/show-field-statistics.md) (classic mode only).
* [Chart a field](discover/visualize-field.md) from the fields list (classic mode only).
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [Detect change points](discover/detect-change-points.md) in a time series ({{esql}} mode only).
* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` [Analyze your data with AI](discover/analyze-discover-data-with-ai.md) ({{esql}} mode only).

**Shape what your queries return and show**

* [Customize the Discover view](discover/document-explorer.md) to show the columns, density, and layout you need.
* Read, sort, and filter [{{esql}} results](discover/esql-results.md) in the table.
* Add [variable controls](discover/esql-variable-controls.md) to make your {{esql}} query dynamic without having to duplicate it.
* Add [runtime fields to a data view](discover/add-fields-to-data-views.md) (classic mode only).
* [Sort your results by relevance](discover/discover-search-for-relevance.md).

**Save and share your explorations**

* [Save sessions](discover/save-open-search.md#_save_a_discover_session) to reuse your queries, filters, and views later.
* [Add Discover content to dashboards](discover/use-sessions-in-dashboards.md), as charts, tables, or whole sessions.
* [Export your results](discover/export-discover-session.md) as a CSV file, or the session itself as JSON.
* [Copy results](discover/copy-and-share-documents.md#copy-row-content) as text, JSON, or Markdown, or [share a link](discover/copy-and-share-documents.md#share-your-findings) to a session or a document.
* [Create an alert rule](discover/generate-alerts-from-discover.md) from the query and filters of a session.
