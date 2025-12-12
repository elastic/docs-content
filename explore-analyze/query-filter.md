---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyze.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
---

# Querying and filtering [search-analyze]

{{es}} is not only great at storing and retrieving documents and their metadata, it also offers powerful querying and analytics capabilities that let you search, filter, and analyze your data at scale. These same capabilities are available in {{kib}} applications to facilitate interactive data exploration and visualization.

* **{{es}} makes JSON documents searchable and aggregatable.** The documents are stored in an [index](/manage-data/data-store/index-basics.md) or [data stream](/manage-data/data-store/data-streams.md), which represent one type of data.
* **Searchable means that you can find documents through multiple retrieval methods.** This includes filtering by yes/no conditions, keyword and full-text search with relevance scoring, and vector/semantic search to find content based on meaning rather than exact terms. {{kib}} provides many ways for you to construct these searches, from simple filters in dashboards to relevance-ranked queries in its search interfaces.
* **Aggregatable means that you can compute statistics and summaries from matching documents to reveal patterns and insights in your dataset.** The simplest aggregation is **count**, and it is frequently used in combination with the **date histogram**, to see count over time. The **terms** aggregation shows the most frequent values.

## Querying

You’ll use a combination of an API endpoint and a query language to interact with your data.

- Elasticsearch provides a number of [query languages](/explore-analyze/query-filter/languages.md). From Query DSL to the newest ES|QL, find the one that's most appropriate for you.

- You can call Elasticsearch's REST APIs by submitting requests directly from the command line or through the Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) in {{kib}}. From your applications, you can use a [client](/reference/elasticsearch-clients/index.md) in your programming language of choice.

- A number of [tools](/explore-analyze/query-filter/tools.md) are available for you to save, debug, and optimize your queries.

If you're just getting started with {{es}}, try the hands-on [](/solutions/elasticsearch-solution-project/get-started/index-basics.md) to learn how to add data and run basic searches using Query DSL and the `_search` endpoint.

## Filtering

When querying your data in Kibana, additional options let you filter the results to just the subset you need. Some of these options are common to most Elastic apps. Check [Filtering in Kibana](/explore-analyze/query-filter/filtering.md) for more details on how to recognize and use them in the UI.

$$$search-analyze-query-languages$$$
