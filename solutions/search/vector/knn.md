---
navigation_title: kNN search on Elasticsearch
description: Find semantically similar documents using k-nearest neighbor (kNN) vector search in Elasticsearch.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
---

# kNN search on {{es}} [knn-search]

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector using a similarity metric such as cosine or L2 norm. In {{es}}, kNN is the primary way to query [`dense_vector`](dense-vector.md) fields after you store embeddings.



## Common use cases for kNN vector similarity search

- **Search**
  - [Semantic text search](../semantic-search.md): Find documents that match the meaning of a query, even when the wording differs.
  - [Image and video similarity](vector-search-use-cases.md#multimodal-search): Search across text, images, audio, or video to find visually or semantically similar content.

- **Recommendations**
  - [Product recommendations](vector-search-use-cases.md#discovery-and-recommendations): Surface items similar to what a user is viewing or has interacted with.
  - [Collaborative filtering](vector-search-use-cases.md#discovery-and-recommendations): Match users or items based on shared behavior or preference patterns in vector space.
  - [Personalized content discovery](vector-search-use-cases.md#discovery-and-recommendations): Suggest articles, media, or other content tailored to individual user interests.

- **Analysis**
  - [Anomaly detection](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Flag records whose vectors sit unusually far from their nearest neighbors.
  - [Pattern matching](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Find near-duplicates, suspicious matches, or other patterns that exact matching would miss.

## Prerequisites for kNN search [knn-prereqs]

To run a kNN search in {{es}}:

- Your data must be vectorized. You can [use an NLP model in {{es}}](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md) or generate vectors outside {{es}}.
  - Use the [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field type for dense vectors.
  - Query vectors must have the same dimension and be created with the same model as the document vectors.
  - Already have vectors? Refer to [Bring your own dense vectors](bring-own-vectors.md).

- Required [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):
  - `create_index` or `manage` to create an index with a `dense_vector` field
  - `create`, `index`, or `write` to add data
  - `read` to search the index

:::{tip}
The default type of {{es-serverless}} project is suitable for this use case unless you plan to use uncompressed dense vectors (`int4` or `int8` quantization strategies) with high dimensionality.
To learn more, refer to [General purpose and vector optimized projects](dense-vector.md#vector-profiles).
:::

## kNN search methods [knn-methods]

{{es}} provides several ways to perform kNN search. Which one you use depends on your field type and whether you need to combine kNN with other queries.

- **Approximate kNN**
  - Best for most production workloads where low latency and scale matter more than perfect recall.
  - Uses graph-based or clustered index structures to find similar vectors quickly without scoring every document in the index.
  - Refer to [Approximate kNN search](knn/approximate-knn.md) for mapping, indexing, and search examples.

- **Exact, brute-force kNN**
  - Best for small datasets, pre-filtered subsets, or when you need precise scoring without approximate indexing.
  - Uses a [`script_score` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) with a vector function to compute similarity against each matching document.
  - Refer to [Exact kNN search](knn/exact-knn.md) for search examples.

Approximate kNN offers low latency and good accuracy, while exact kNN guarantees accurate results but does not scale well for large datasets. With exact kNN, a `script_score` query must scan each matching document to compute the vector function, which can result in slow search speeds. However, you can improve latency by using a [query](../../../explore-analyze/query-filter/languages/querydsl.md) to limit the number of matching documents passed to the function. If you filter your data to a small subset of documents, you can get good search performance using this approach.

## Resources

- [Approximate kNN search](knn/approximate-knn.md): Learn how to map, index, and query `dense_vector` fields for fast, scalable approximate kNN search.
- [Build search queries](knn/build-search-queries.md): Learn how to construct approximate kNN queries for filtering, hybrid retrieval, semantic search, multiple vector fields, and similarity thresholds.
- [Nested kNN search](knn/nested-knn-search.md): Learn how to run approximate kNN search on nested vectors for passage retrieval, filtering, inner hits, and chunked content.
- [Optimize performance and accuracy](knn/optimize-performance-accuracy.md): Learn how to tune search speed, recall, vector storage, quantization, and rescoring for approximate kNN search.
- [Exact kNN search](knn/exact-knn.md): Learn how to run exact brute-force kNN search with `script_score` queries for small datasets or precise scoring.
- [Vector search in {{es}}](../vector.md): Learn the core concepts and terminology for vector search in {{es}}, including embeddings, field types, and how vector retrieval fits with other search strategies.
- [Knn query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.

