---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover-search-for-relevance.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Sort search results by relevance score in Discover to identify the documents that best match your query. Use the score field to prioritize the most relevant data.
---

# Search for relevance [discover-search-for-relevance]

{{product.elasticsearch}} assigns a relevancy score to each document based on how well it matches your query. Sorting by this score helps you identify the most relevant results quickly. This guide shows how to use **Discover** to sort documents by relevance score, putting the best matches at the top of your results.

This example uses the [sample flights data set](../index.md#gs-get-data-into-kibana), or you can use your own data.

1. In **Discover**, open the {{data-source}} dropdown, and select the data that you want to work with.

    For the sample flights data, set the {{data-source}} to **Kibana Sample Data Flights**.

2. Run your search.  For the sample data, try:

    ```ts
    Warsaw OR Venice OR Clear
    ```

3. If you don’t see any results, expand the [time range](../query-filter/filtering.md), for example to **Last 7 days**.
4. From the list of **Meta fields** list in the sidebar, add `_score`.
5. Add any other fields you want to the document table.

    You're sorting by the`timestamp` field.

6. To turn off sorting by the `timestamp` field, click the **field sorted** option, and then click **Clear sorting.**
7. Open the **Pick fields to sort by** menu, and then click **_score**.
8. Select **High-Low**.
   
   ![Field sorting popover](/explore-analyze/images/kibana-field-sorting-popover.png "title =50%")
   
   Your table now sorts documents from most to least relevant.
   :::{image} /explore-analyze/images/kibana-discover-search-for-relevance.png
   :alt: Documents are sorted from most relevant to least relevant.
   :screenshot:
   :::


