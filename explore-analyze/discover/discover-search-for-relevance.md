---
navigation_title: Search for relevance
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-search-for-relevance.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
products:
  - id: kibana
description: Sort results by relevance score in Discover to see the documents that best match your query first, in classic mode or with an ES|QL query.
---

# Sort Discover results by relevance [discover-search-for-relevance]

{{product.elasticsearch}} gives each document a relevance score based on how well it matches your query. In **Discover**, you can sort by this score to see the best matches first.

## Before you begin

Open **Discover**.

## Sort by relevance score

The steps differ by mode, so select the tab for the mode you use.

:::::{tab-set}
:group: query-mode

::::{tab-item} {{esql}} mode
:sync: esql

This example uses the [web logs sample data](/manage-data/ingest/sample-data.md), or you can use your own data.

1. In **Discover**, make sure you're in {{esql}} mode. If **Discover** opens in classic mode, refer to [Switch between {{esql}} and classic mode](switch-esql-mode.md#switch-discover-query-mode).
2. To get scores, add `METADATA _score` to the `FROM` command, and match text with a full-text function such as `MATCH`. Then sort by `_score`. For the sample data, enter:

    ```esql
    FROM kibana_sample_data_logs METADATA _score
    | WHERE MATCH(message, "Mozilla")
    | SORT _score DESC
    | KEEP _score, message
    | LIMIT 10
    ```

3. If you don't see any results, expand the [time range](../query-filter/filtering.md), for example to **Last 7 days**.

**Result:** The table lists the best matches first, with their scores in the `_score` column.

:::{tip}
Very small scores show as `0` in the table. To see the difference between them, multiply the score in your query. For example, add `| EVAL score_x100000 = _score * 100000` before `KEEP`, then add `score_x100000` to the `KEEP` command.
:::

For more about scores, refer to [Relevance scoring](/solutions/search/esql-for-search.md#esql-for-search-scoring) and to the [`_score` metadata field](elasticsearch://reference/query-languages/esql/esql-metadata-fields.md).
::::

::::{tab-item} Classic mode
:sync: classic

This example uses the [flights sample data](/manage-data/ingest/sample-data.md), or you can use your own data.

1. In **Discover**, if it opens in {{esql}} mode, [switch to classic mode](switch-esql-mode.md#revert-to-classic-mode). Then, from the data view menu, select the data that you want to work with.

    For the flights sample data, set the data view to **Kibana Sample Data Flights**.

2. Run your search. For the sample data, try:

    ```ts
    Warsaw OR Venice OR Clear
    ```

3. If you don't see any results, expand the [time range](../query-filter/filtering.md), for example to **Last 7 days**.
4. In the fields list in the sidebar, expand the **Meta fields** list. Next to `_score`, select {icon}`plus` (**Add "_score" field**) to add it as a column.
5. Optional: Add any other fields you want to the document table.
6. By default, the table sorts by the time field of your data view, which is `timestamp` in the flights sample data. To turn off that sorting, select the **field sorted** option, and then select **Clear sorting**.
7. Open the **Pick fields to sort by** menu, and then select **_score**.
8. Select **High-Low**.

   :::{image} /explore-analyze/images/kibana-field-sorting-popover.png
   :alt: Field sorting menu with _score selected and High-Low chosen
   :screenshot:
   :width: 50%
   :::

**Result:** The table sorts documents from most to least relevant.

:::{image} /explore-analyze/images/kibana-discover-search-for-relevance.png
:alt: Documents are sorted from most relevant to least relevant.
:screenshot:
:::
::::

:::::

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)
- [Search and filter with KQL, Lucene, and filters in Discover's classic mode](search-and-filter-classic.md)
- [{{esql}} for search](/solutions/search/esql-for-search.md)
