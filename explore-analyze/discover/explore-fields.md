---
navigation_title: Explore fields
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Find out which fields your data has and what they contain, add fields as columns, and split the chart by a field in Discover.
---

# Explore fields in Discover

When you open **Discover** on data you don't know yet, the fields list in the sidebar shows what that data contains. From there, you can look at a field's details, split the chart by it, or put it in the results table as a column. In classic mode, the details include the field's most frequent values.

## Before you begin

Open **Discover** and run a query that returns results. In {{esql}} mode, run a query first. Refer to [Get started with {{esql}} in Discover](try-esql.md). In classic mode, select a [data view](../find-and-organize/data-views.md) and a time range first. Refer to [Select a data view and a time range](search-and-filter-classic.md#find-the-data-you-want-to-use).

## Explore the fields

1. In the sidebar, check the available fields in the fields list. It's common to have hundreds of fields. Use the search at the top of the sidebar to look for specific terms in the field names.
   For example, enter `ma` in the search field to find the `manufacturer` field.

   :::{image} /explore-analyze/images/kibana-discover-sidebar-available-fields.png
   :alt: Fields list in the sidebar showing the top five results of a field name search
   :screenshot:
   :width: 40%
   :::

   ::::{tip}
   You can combine multiple keywords or characters. For example, `geo dest` finds `geo.dest` and `geo.src.dest`.
   ::::

   {applies_to}`stack: ga 9.2` When you explore logs data in the Observability solution view, the fields list starts with a **Recommended fields** group. It holds fields that are most useful for logs, such as `log.level`, `service.name`, and `host.name`.

2. Select a field name to open its details. In classic mode, **Discover** shows the field's top 10 values and the number of records used to calculate them. In {{esql}} mode, the field details don't include top values. To see the most frequent values of a field, run a query such as `STATS COUNT(*) BY <field>`.

   To split the chart by that field, select **Add breakdown** in the field details. In {{esql}} mode, this works only when the data source has a time field and your query doesn't reshape the results with a command such as `STATS` or `KEEP`.

3. Next to a field in the fields list, select {icon}`plus` to add it to the results table as a column. You can also drag the field from the list into the table. To manage the columns after you add them, refer to [Manage the columns in the table](document-explorer.md#document-explorer-columns).

   :::{image} /explore-analyze/images/kibana-discover-add-field.png
   :alt: Plus icon next to a field in the fields list that adds the field as a column in the table
   :screenshot:
   :width: 50%
   :::

   By default, the table shows a **Summary** column with each document's key-value pairs, and adding a field replaces it. In {{esql}} mode, the columns that the table starts with depend on your query. Refer to [Show specific columns in the results table](esql-results.md#esql-kibana-results-table).

   :::{image} /explore-analyze/images/kibana-document-table.png
   :alt: Document table with the manufacturer field added as a column
   :screenshot:
   :::

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` In **JSON** view, adding fields limits the tree to those fields. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

   ::::{tip}
   The fields you add as columns are also the fields that **Discover** includes when you export the results as CSV. Refer to [Export Discover session results as CSV](export-discover-session.md#export-discover-session-csv).
   ::::

4. Optional: To reopen this view later, [save your work as a Discover session](save-open-search.md#_save_a_discover_session).

**Result:** You can see what your data contains, and the table shows the fields you added as columns.

## Next steps

- To chart a field in classic mode, refer to [Visualize a field from Discover](visualize-field.md).
- To read every field of a single result, refer to [Inspect documents and requests in Discover](inspect-documents.md).

## Related pages

- [Customize the Discover view](document-explorer.md)
- [Show specific columns in the results table](esql-results.md#esql-kibana-results-table)
