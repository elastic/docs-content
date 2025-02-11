---
applies:
  stack:
  serverless:
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/save-load-delete-query.html
---

# Saved queries [save-load-delete-query]

% What needs to be done: Refine

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/search-analyze.md
% - [ ] ./raw-migrated-files/kibana/kibana/save-load-delete-query.md

Have you ever built a query that you wanted to reuse? With saved queries, you can save your query text, filters, and time range for reuse anywhere a query bar is present.

For example, suppose you’re in **Discover**, and you’ve put time into building a query that includes query input text, multiple filters, and a specific time range. Save this query, and you can embed the search results in dashboards, use them as a foundation for building a visualization, and share them in a link or CVS form.

Saved queries are different than [saved Discover sessions](/explore-analyze/discover/save-open-search.md), which include the **Discover** configuration—selected columns in the document table, sort order, and {{data-source}}—in addition to the query. Discover sessions are primarily used for adding search results to a dashboard.

## Saved query access [_saved_query_access]

If you have insufficient privileges to manage saved queries, you will be unable to load or save queries from the saved query management popover. For more information, see [Granting access to Kibana](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md)


## Save a query [_save_a_query]

1. Once you’ve built a query worth saving, click the save query icon ![save query icon](../../../images/kibana-saved-query-icon.png "").
2. In the menu, select the item to save the query.
3. Enter a unique name.
4. Choose whether to include or exclude filters and a time range. By default, filters are automatically included, but the time filter is not.
5. Save the query.
6. To load a saved query, select it in the **Saved query** menu.

    The query text, filters, and time range are updated and your data refreshed. If you’re loading a saved query that did not include the filters or time range, those components remain as-is.

7. To add filters and clear saved queries, use the **Saved query** menu.