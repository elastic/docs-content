---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-search-for-relevance.html
---

# Search for relevance [discover-search-for-relevance]

{{es}} assigns a relevancy, or score to each document, so you can can narrow your search to the documents with the most relevant results. The higher the score, the better it matches your query.

This example shows how to use **Discover** to list your documents from most relevant to least relevant. This example uses the [sample flights data set](../index.md#gs-get-data-into-kibana), or you can use your own data.

1. In **Discover**, open the {{data-source}} dropdown, and select the data that you want to work with.

    For the sample flights data, set the {{data-source}} to **Kibana Sample Data Flights**.

2. Run your search.  For the sample data, try:

    ```ts
    Warsaw OR Venice OR Clear
    ```

3. If you don’t see any results, expand the [time range](../query-filter/filtering.md), for example to **Last 7 days**.
4. From the list of **Meta fields** list in the sidebar, add `_score`.
5. Add any other fields you want to the document table.

    At this point, you’re sorting by the`timestamp` field.

6. To turn off sorting by the `timestamp` field, click the **field sorted** option, and then click **Clear sorting.**
7. Open the **Pick fields to sort by** menu, and then click **_score**.
8. Select **High-Low**.
   ![Field sorting popover](../../images/kibana-field-sorting-popover.png "title =50%")
   Your table now sorts documents from most to least relevant.
   :::{image} ../../images/kibana-discover-search-for-relevance.png
   :alt: Documents are sorted from most relevant to least relevant.
   :class: screenshot
   :::


