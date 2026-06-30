---
navigation_title: kNN search on Elasticsearch
description: Find semantically similar documents using k-nearest neighbor (kNN) vector search in Elasticsearch.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# kNN search on {{es}} [knn-search]

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector using a similarity metric such as cosine or L2 norm. In {{es}}, kNN is the primary way to query [`dense_vector`](dense-vector.md) fields after you store embeddings.

Common use cases for kNN vector similarity search include:

* **Search**
  * Semantic text search
  * Image and video similarity

* **Recommendations**
  * Product recommendations
  * Collaborative filtering
  * Personalized content discovery

* **Analysis**
  * Anomaly detection
  * Pattern matching

## Prerequisites for kNN search [knn-prereqs]

To run a kNN search in {{es}}:

* Your data must be vectorized. You can [use an NLP model in {{es}}](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md) or generate vectors outside {{es}}.
  * Use the [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field type for dense vectors.
  * Query vectors must have the same dimension and be created with the same model as the document vectors.
  * Already have vectors? Refer to [Bring your own dense vectors](bring-own-vectors.md).

* Required [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):
  * `create_index` or `manage` to create an index with a `dense_vector` field
  * `create`, `index`, or `write` to add data
  * `read` to search the index

:::{tip}
The default type of {{es-serverless}} project is suitable for this use case unless you plan to use uncompressed dense vectors (`int4` or `int8` quantization strategies) with high dimensionality.
Refer to [](dense-vector.md#vector-profiles).
:::

## kNN search methods [knn-methods]

{{es}} provides several ways to perform kNN search. Which one you use depends on your field type and whether you need to combine kNN with other queries.

### Approximate kNN [knn-methods-approximate]

Fast, scalable similarity search. Ideal for most production workloads. Refer to [Approximate kNN search](knn/approximate-knn.md) for mapping, indexing, and search examples. There are three ways to run approximate kNN search, with different field type support:

| Method | Supported field types | Use case |
|---|---|---|
| [Top-level `knn` option](knn/approximate-knn.md) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) | Standalone kNN search or hybrid search with score fusion |
| [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md), [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) | Composable with other queries in a `bool` clause. Required for `semantic_text` fields |
| [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md) | [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) | Use within a retriever pipeline for ranking and result merging |

::::{tip}
If you use `semantic_text` fields, query them with a [`match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) for the simplest approach, or use the [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-with-semantic-text) when you need more control over the search.
::::

### Exact, brute-force kNN [knn-methods-exact]

Uses a [`script_score` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) with a vector function. Best for small datasets or precise scoring. Refer to [exact kNN](knn/exact-knn.md).

### Choosing between approximate and exact kNN

Approximate kNN offers low latency and good accuracy, while exact kNN guarantees accurate results but does not scale well for large datasets. With exact kNN, a `script_score` query must scan each matching document to compute the vector function, which can result in slow search speeds. However, you can improve latency by using a [query](../../../explore-analyze/query-filter/languages/querydsl.md) to limit the number of matching documents passed to the function. If you filter your data to a small subset of documents, you can get good search performance using this approach.

For implementation details, refer to [Approximate kNN search](knn/approximate-knn.md) and [Exact kNN search](knn/exact-knn.md).

