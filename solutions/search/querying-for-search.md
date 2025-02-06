---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data-the-search-api.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/retrievers-overview.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/master/retrievers-examples.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_retrievers_examples.html
---

# Query languages for search

::::{tip} 
This page is focused on the search use case. For an overview of Elastic query languages for every use case, refer to the [complete overview](/explore-analyze/query-filter/languages.md).
::::

Once you know which [search approaches](search-approaches.md) you need to use, you can start building and testing your search queries. {{es}} provides several query languages to help you express your search logic.

| Interface | Endpoint | Description | Best for |
|-----------|----------|-------------|----------|
| [**Query DSL**](/explore-analyze/query-filter/languages/querydsl.md) | `_search` | Original, JSON-based query language native to Elasticsearch. Powerful but complex syntax. | Full-text and semantic search queries |
| [**ESQL**](/explore-analyze/query-filter/languages/esql.md) | `_query` | Fast, SQL-like language with piped syntax, built on new compute architecture. | Filtering, analysis, aggregations |
| [**Retrievers**](retrievers-overview.md) | `_search` | Modern `_search` API syntax focused on composability. | Building complex search pipelines, especially those using semantic search. Required for [semantic reranking](ranking/semantic-reranking.md). |

These query languages are complementary, not mutually exclusive. You can use different query languages for different parts of your application, based on your specific needs. This flexibility allows you to gradually adopt newer interfaces as your requirements evolve.

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/search-your-data.md
% - [ ] ./raw-migrated-files/docs-content/serverless/elasticsearch-search-your-data.md
% - [ ] ./raw-migrated-files/docs-content/serverless/elasticsearch-search-your-data-the-search-api.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/retrievers-overview.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/_retrievers_examples.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$search-timeout$$$

$$$track-total-hits$$$