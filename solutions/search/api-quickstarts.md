---
applies_to:
  stack:
  serverless:
---
# API quickstarts

:::{tip}
Prefer working in Python? Check out our executable [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks#readme) in the Elasticsearch Labs repository.
::::

Use the following quickstarts to get hands-on experience with Elasticsearch APIs and tools:

- [Index and search data using Elasticsearch APIs](elasticsearch-basics-quickstart.md): Learn about indices, documents, and mappings, and perform a basic search using the Query DSL.
- [Basic full-text search and filtering in Elasticsearch](querydsl-full-text-filter-tutorial.md): Learn about different options for querying data, including full-text search and filtering, using the Query DSL.
- [Analyze eCommerce data with aggregations using Query DSL](/explore-analyze/query-filter/aggregations/tutorial-analyze-ecommerce-data-with-aggregations-using-query-dsl.md): Learn how to analyze data using different types of aggregations, including metrics, buckets, and pipelines.
% - [Getting started with ES|QL](esql-getting-started.md): Learn how to query and aggregate your data using ES|QL.
- [Semantic search](semantic-search/semantic-search-semantic-text.md): Learn how to create embeddings for your data with `semantic_text` and query using the `semantic` query.
 - [Hybrid search](hybrid-semantic-text.md): Learn how to combine semantic search using`semantic_text` with full-text search.
- [Bring your own dense vector embeddings](vector/bring-own-vectors.md): Learn how to ingest dense vector embeddings into Elasticsearch.

:::{note}
To run the quickstarts, you need a running Elasticsearch cluster. Use [`start-local`](https://github.com/elastic/start-local) to set up a fast local dev environment in Docker, together with Kibana. Run the following command in your terminal:

```sh
curl -fsSL https://elastic.co/start-local | sh
```
<br>
Alternatively, refer to our other [deployment options](/deploy-manage/index.md).
% TODO: UPDATE LINK
:::