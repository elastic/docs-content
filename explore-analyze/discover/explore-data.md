---
navigation_title: Explore your data
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Explore fields, read and compare documents, sort by relevance, and find patterns or change points in your Discover results.
---

# Explore your data in Discover

After a query returns results, you can use **Discover** to find out what your fields contain, read and compare documents, and spot patterns and changes over time.

* Explore [fields](explore-fields.md), see what they contain, and break the chart down by a field.
* Read [individual results and documents](inspect-documents.md), and see the search request behind them.
* [Compare documents](compare-documents.md) side by side.
* [Sort your results by relevance](discover-search-for-relevance.md).
* [Inspect grouped results](inspect-grouped-stats.md), the results of a `STATS ... BY` query, including groups of similar log messages ({{esql}} mode only).
* [Detect change points](detect-change-points.md) in a time series ({{esql}} mode only).
* [Analyze your data with AI](analyze-discover-data-with-ai.md) ({{esql}} mode only).
* Find patterns in your log data with [pattern analysis](run-pattern-analysis-discover.md) (classic mode only).
* Check [how the values of each field are distributed](show-field-statistics.md) (classic mode only).
* [Chart a field](visualize-field.md) from the fields list in the sidebar (classic mode only).

## Related pages

- [How Discover works](discover-get-started.md)
- [How to query in Discover's {{esql}} mode](use-esql.md)
- [How to query in Discover's classic mode](use-classic-mode.md)
- [Manage your Discover view and sessions](manage-discover.md)
