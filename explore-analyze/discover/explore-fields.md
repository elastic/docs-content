---
navigation_title: Explore fields
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: See which fields your data has, check the most frequent values of a field, and add the ones you need as columns in the Discover results table.
---

# Explore the fields in your data

When you open **Discover** on data you don't know yet, the fields list shows what that data contains. You can check the most frequent values of a field and add the fields you need as columns in the results table.

## Before you begin

Open **Discover** and run a query that returns results. If you haven't run a query in {esql} mode yet, refer to [Get started with {esql} in Discover](try-esql.md). In classic mode, select a data view first. Refer to [Use Discover in classic mode](use-classic-mode.md).

## Explore the fields

**Discover** provides utilities designed to help you make sense of your data:

1. In the sidebar, check the available fields. It's common to have hundreds of fields. Use the search at the top of that sidebar to look for specific terms in the field names.
   In this example, we’ve entered `ma` in the search field to find the `manufacturer` field.
   ![Fields list that displays the top five search results](/explore-analyze/images/kibana-discover-sidebar-available-fields.png "title =40%")
   ::::{tip}
   You can combine multiple keywords or characters. For example, `geo dest` finds `geo.dest` and `geo.src.dest`.
   ::::

   {applies_to}`stack: ga 9.2` For some searches, Discover suggests recommended fields to explore. These suggestions are based on the data you query and are managed by Elastic.

2. Select a field to view its most frequent values.
  **Discover** shows the top 10 values and the number of records used to calculate those values.

3. Select the **Plus** icon to add fields to the results table. You can also drag them from the list into the table.

   ![How to add a field as a column in the table](/explore-analyze/images/kibana-discover-add-field.png "title =50%")

   When you add fields to the table, the **Summary** column is replaced. For {{esql}}-specific details about the time field and CSV exports, refer to [Show specific columns in the results table](esql-results.md#esql-kibana-results-table).

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` In **JSON** view, adding fields limits the tree to those fields. Refer to [View documents as JSON](document-explorer.md#document-explorer-view-mode).

   ![Document table with fields for manufacturer](/explore-analyze/images/kibana-document-table.png "")

4. Arrange the view to your liking to display the fields and data you care most about using the various display options of **Discover**. For example, you can change the order and size of columns, expand the table to be in full screen or collapse the chart and the list of fields. Check [Customize the Discover view](document-explorer.md) for more information.
5. **Save** your changes to be able to open the same view later on and explore your data further.

**Result:** The table shows the fields you added as columns.

## Related pages

- [Customize the Discover view](document-explorer.md)
- [Show specific columns in the results table](esql-results.md#esql-kibana-results-table)
