# The search API [elasticsearch-search-your-data-the-search-api]

A *search* consists of one or more queries that are combined and sent to {{es}}. Documents that match a search’s queries are returned in the *hits*, or *search results*, of the response.

A search may also contain additional information used to better process its queries. For example, a search may be limited to a specific index or only return a specific number of results.

You can use the [search API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/group/endpoint-search) to search and aggregate data stored in {{es}} data streams or indices.

For more information, refer to [the search API overview](../../../solutions/search/querying-for-search.md) in the core {{es}} docs.


## Query DSL [elasticsearch-search-your-data-the-query-dsl] 

[Query DSL](../../../explore-analyze/query-filter/languages/querydsl.md) is full-featured JSON-style query language that enables complex searching, filtering, and aggregations.

The `_search` API’s `query` request body parameter accepts queries written in Query DSL.


## Retrievers [elasticsearch-search-your-data-the-retrievers] 

Retrievers are an alternative to Query DSL that allow you to configure complex retrieval pipelines using a simplified syntax. Retrievers simplify the user experience by allowing entire retrieval pipelines to be configured in a single `_search` API call.

Learn more in the [Retrievers overview](../../../solutions/search/querying-for-search.md) in the core {{es}} docs.

