# Search your data [search-with-elasticsearch]

$$$search-query$$$
A *search query*, or *query*, is a request for information about data in {{es}} data streams or indices.

You can think of a query as a question, written in a way {{es}} understands. Depending on your data, you can use a query to get answers to questions like:

* What processes on my server take longer than 500 milliseconds to respond?
* What users on my network ran `regsvr32.exe` within the last week?
* What pages on my website contain a specific word or phrase?

{{es}} supports several search methods:

Search for exact values
:   Search for [exact values or ranges](https://www.elastic.co/guide/en/elasticsearch/reference/current/term-level-queries.html) of numbers, dates, IPs, or strings.

[Full-text search](../../../solutions/search/full-text.md)
:   Use [full text queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html) to query [unstructured textual data](../../../solutions/search/full-text/text-analysis-during-search.md) and find documents that best match query terms.

Vector search
:   Store vectors in {{es}} and use [approximate nearest neighbor (ANN) or k-nearest neighbor (kNN) search](../../../solutions/search/vector/knn.md) to find vectors that are similar, supporting use cases like [semantic search](../../../solutions/search/semantic-search.md).


## Run a search [_run_a_search] 

To run a search request, you can use the search API or Search Applications.

[Search API](../../../solutions/search/querying-for-search.md)
:   The [search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) enables you to search and [aggregate](../../../explore-analyze/aggregations.md) data stored in {{es}} using a query language called the [Query DSL](../../../explore-analyze/query-filter/languages/querydsl.md).

[Search Applications](../../../solutions/search/applications.md)
:   Search Applications enable you to leverage the full power of {{es}} and its Query DSL, with a simplified user experience. Create search applications based on your {{es}} indices, build queries using search templates, and easily preview your results directly in the Kibana Search UI.

