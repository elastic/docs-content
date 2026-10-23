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

## Select a data view and a time range [find-the-data-you-want-to-use]

In classic mode, you select the data to explore with a data view, and then set the time range in which to view that data.

1. Find **Discover** in the navigation menu or by using the [global search field](../find-and-organize/find-apps-and-objects.md).
2. Select the data view that contains the data you want to explore.
   ::::{tip}
   By default, {{kib}} requires a [{{data-source}}](../find-and-organize/data-views.md) to access your Elasticsearch data. A {{data-source}} can point to one or more indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md). When adding data to {{es}} using one of the many integrations available, sometimes data views are created automatically, but you can also create your own.

   You can also [use {{esql}}](try-esql.md), which lets you query any data you have in {{es}} without specifying a {{data-source}} first.

   If **Discover** asks you to add data or create a {{data-source}} instead of opening and you're not sure of what to do next, refer to [](/troubleshoot/kibana/discover-dashboards-no-data-screen.md).
   ::::
   If you're using sample data, data views are automatically created and are ready to use.
   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: How to set the {{data-source}} in Discover
   :screenshot:
   :width: 300px
   :::

3. If needed, adjust the [time range](../query-filter/filtering.md), for example by setting it to the **Last 7 days**.
    The range selection is based on the default time field in your data view. If you are using the sample data, this value was set when the data view was created. If you are using your own data view and it does not have a time field:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` The time filter stays visible, shows **All time**, and cannot be changed.
    - {applies_to}`stack: ga 9.0-9.5` The range selection is not available.

**Result:** **Discover** shows your data. By default, the table includes a column for the time field and a **Summary** column with an overview of each result. To narrow the results down, refer to [Search and filter with KQL, Lucene, and filters](search-and-filter-classic.md).

## More classic mode tasks in Discover

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
