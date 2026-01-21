---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/save-load-delete-query.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Saved queries [save-load-delete-query]

Have you ever built a query that you wanted to reuse? With saved queries, you can save your query text, filters, and time range for reuse anywhere a query bar is present.

For example, suppose you’re in **Discover**, and you’ve put time into building a query that includes query input text, multiple filters, and a specific time range. Save this query, and you can embed the search results in dashboards, use them as a foundation for building a visualization, and share them in a link or CVS form.

Saved queries are different than [saved Discover sessions](/explore-analyze/discover/save-open-search.md), which include the **Discover** configuration—selected columns in the document table, sort order, and {{data-source}}—in addition to the query. Discover sessions are primarily used for adding search results to a dashboard.

:::{note}
Saved queries aren't available for {{esql}} queries. When using {{esql}}, the editor automatically keeps an [history of your most recent queries](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-query-history), and you can also [mark some as favorite](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-starred-queries) to find them faster later.
:::

## Saved queries requirements [_saved_query_access]

You must have **Saved Query Management** privileges in {{kib}} to use saved queries.


## Save a query [_save_a_query]

1. Once you’ve built a query worth saving, open the {icon}`filter` **Query menu**.
2. In the menu, select **Save query**.
3. Enter a unique name.
4. Choose whether to include or exclude filters and a time range. By default, filters are automatically included, but the time filter is not.
5. Save the query.

The query is saved. You can load it at any time by opening the **Query menu** again and selecting **Load query**.

When you load a saved query, the query text, filters, and time range are updated and your data refreshed. If you’re loading a saved query that did not include the filters or time range, those components remain as-is.
