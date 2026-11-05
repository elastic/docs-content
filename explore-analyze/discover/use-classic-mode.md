---
navigation_title: Use Discover in classic mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Find everything you can do in Discover's classic mode, from searching with Kibana Query Language (KQL) and filters to adding runtime fields and saving what you find.
---

# Use Discover in classic mode

Classic mode in **Discover** lets you explore the documents of a [data view](../find-and-organize/data-views.md), a saved definition of the data to query. You search them with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two search syntaxes, and narrow them down with filters.

## What you can do in classic mode

**Query your data**

* [Select a data view and a time range](search-and-filter-classic.md#find-the-data-you-want-to-use) to choose the data you explore (classic mode only).
* [Search with KQL or Lucene and narrow the results with filters](search-and-filter-classic.md) (classic mode only).
* [Switch to {{esql}} mode](switch-esql-mode.md) and see what happens to your search.
* [Open Discover from a dashboard panel](../dashboards/create-discover-drilldown.md) with a drilldown.
* Learn how to handle long-running queries with [background search](background-search.md).
* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2` Keep [several explorations open side by side](work-with-tabs.md) in tabs.

**Understand your data**

* Explore [individual results and documents](inspect-documents.md).
* See [which fields your data has](explore-fields.md) and what they contain, and break the chart down by a field.
* [Compare documents](compare-documents.md) side by side.
* Find patterns in your log data with [pattern analysis](run-pattern-analysis-discover.md) (classic mode only).
* Check [how the values of each field are distributed](show-field-statistics.md) (classic mode only).
* [Chart a field](visualize-field.md) from the fields list (classic mode only).

**Shape what your queries return and show**

* [Customize the Discover view](document-explorer.md) to show the columns, density, and layout you need.
* Add [runtime fields](add-fields-to-data-views.md) to your data views (classic mode only).
* [Sort your results by relevance](discover-search-for-relevance.md).

**Save and share your explorations**

* [Save sessions](save-open-search.md#_save_a_discover_session) to reuse your queries, filters, and views later.
* [Add Discover content to dashboards](save-open-search.md#_add_search_results_to_a_dashboard), as charts, tables, or whole sessions.
* [Export your results](../report-and-share.md#manually-generate-reports) as a file.
* [Copy results](copy-and-share-documents.md#copy-row-content) as text, JSON, or Markdown, or [share a link](copy-and-share-documents.md#share-your-findings) to a session or a document.
* [Create an alert rule](generate-alerts-from-discover.md) from the query and filters of a session.

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Switch between {{esql}} and classic mode](switch-esql-mode.md)
- [Data views](../find-and-organize/data-views.md)
