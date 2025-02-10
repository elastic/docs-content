---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-analyze.html
---

# Querying and filtering [search-analyze]

You can use {{es}} as a basic document store to retrieve documents and their metadata. However, the real power of {{es}} comes from its advanced search and analytics capabilities.

## Querying

You’ll use a combination of an API endpoint and a query language to interact with your data.

- Elasticsearch provides a number of [query languages](/explore-analyze/query-filter/languages.md). From Query DSL to the newest ES|QL, find the one that's most appropriate for you.

- You can call Elasticsearch's REST APIs by submitting requests directly from the command line or through the Dev Tools [Console](/explore-analyze/query-filter/tools/console.md) in {{kib}}. From your applications, you can use a [client](https://www.elastic.co/guide/en/elasticsearch/client/index.html) in your programming language of choice.

- A number of [tools](/explore-analyze/query-filter/tools.md) are available for you to save, debug, and optimize your queries.

% todo: update link to the best target
If you're just getting started with Elasticsearch, try the hands-on [API quickstart](/solutions/search/elasticsearch-basics-quickstart.md) to learn how to add data and run basic searches using Query DSL and the `_search` endpoint.

## Filtering

When querying your data in Kibana, additional options let you filter the results to just the subset you need. Some of these options are common to most Elastic apps. Check [Filtering in Kibana](/explore-analyze/query-filter/filtering.md) for more details on how to recognize and use them in the UI.

$$$search-analyze-query-languages$$$
