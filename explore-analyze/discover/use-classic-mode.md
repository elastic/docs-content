---
navigation_title: Use Discover in classic mode
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Find the Discover tasks that only exist in classic mode, from searching with KQL and filters to adding runtime fields and viewing field statistics.
---

# Use Discover in classic mode

Classic mode in **Discover** lets you explore the documents of a data view. You search them with Kibana Query Language (KQL) or Lucene, and narrow them down with filters. In {{esql}} mode, the query defines the data instead, so you don't need a data view.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Discover** opens in {{esql}} mode by default. To use the tasks in this section, switch to classic mode. Refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md#revert-to-classic-mode).

Tasks that work the same way in both modes, such as customizing the table or saving a session, are in the other Discover guides. Start with [Explore fields and data with Discover](discover-get-started.md).

## Classic mode tasks in Discover

| When you need this | Guide |
| --- | --- |
| You want to search documents with KQL or Lucene, or narrow them down with filters | [Search and filter with KQL, Lucene, and filters](search-and-filter-classic.md) |
| You need a field that your data view doesn't have | [Add a runtime field to a data view from Discover](add-fields-to-data-views.md) |
| You want to chart a field from the fields list | [Visualize a field from Discover](visualize-field.md) |
| You want to open a document on its own page, or see the documents around it | [View a single document or the documents around it](view-single-document.md) |
| You want to see how the values of each field are distributed | [View field statistics](show-field-statistics.md) |
| You want to group log messages into patterns | [Run a pattern analysis on your log data](run-pattern-analysis-discover.md) |

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Switch between {{esql}} and classic mode](switch-esql-mode.md)
- [Data views](../find-and-organize/data-views.md)
