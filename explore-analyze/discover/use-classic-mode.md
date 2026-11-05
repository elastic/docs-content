---
navigation_title: Use Discover in classic mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Find the Discover tasks that only exist in classic mode, from searching with Kibana Query Language (KQL) and filters to adding runtime fields.
---

# Use Discover in classic mode

Classic mode in **Discover** lets you explore the documents of a [data view](../find-and-organize/data-views.md), a saved definition of the data to query. You search them with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two search syntaxes, and narrow them down with filters.

## More classic mode tasks in Discover

| When you need this | Guide |
| --- | --- |
| You want to select a data view and a time range, then search with KQL or Lucene or narrow the results with filters | [Search and filter with KQL, Lucene, and filters](search-and-filter-classic.md) |
| You need a field that your data view doesn't have | [Add a runtime field to a data view from Discover](add-fields-to-data-views.md) |
| You want to chart a field from the fields list | [Visualize a field from Discover](visualize-field.md) |
| You want to see how the values of each field are distributed | [View field statistics](show-field-statistics.md) |
| You want to group log messages into patterns | [Run a pattern analysis on your log data](run-pattern-analysis-discover.md) |

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Switch between {{esql}} and classic mode](switch-esql-mode.md)
- [Data views](../find-and-organize/data-views.md)
