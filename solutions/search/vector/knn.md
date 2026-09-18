---
navigation_title: kNN search in Elasticsearch
description: Find semantically similar documents using k-nearest neighbor (kNN) vector search in Elasticsearch.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/knn-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-knn-search.html
applies_to:
  stack:
  serverless:
---

# kNN search in {{es}} [knn-search]

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector using a similarity metric such as cosine or L2 norm. In {{es}}, kNN is the primary way to query [`dense_vector`](dense-vector.md) fields after you store embeddings.



## Common use cases for kNN vector similarity search

kNN vector similarity search supports use cases across search, recommendations, and analysis:

- **Search**
  - [Semantic text search](../semantic-search.md): Find documents that match the meaning of a query, even when the wording differs.
  - [Image and video similarity](vector-search-use-cases.md#multimodal-search): Search across text, images, audio, or video to find visually or semantically similar content.

- **Recommendations**
  - [Product recommendations](vector-search-use-cases.md#discovery-and-recommendations): Surface items similar to what a user is viewing or has interacted with.
  - [Collaborative filtering](vector-search-use-cases.md#discovery-and-recommendations): Match users or items based on shared behavior or preference patterns in vector space.
  - [Personalized content discovery](vector-search-use-cases.md#discovery-and-recommendations): Suggest articles, media, or other content tailored to individual user interests.

- **Analysis**
  - [{{anomaly-detect-cap}}](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Flag records whose vectors sit unusually far from their nearest neighbors.
  - [Pattern matching](vector-search-use-cases.md#duplicate-detection-fraud-and-anomaly-detection): Find near-duplicates, suspicious matches, or other patterns that exact matching would miss.

## Prerequisites for kNN search [knn-prereqs]

To run a kNN search in {{es}}:

- Your data must be vectorized. You can:
  - Use [`semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) to have Elastic generate embeddings automatically.
  - Use the [Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) for managed {{infer}}.
  - [Deploy an NLP model](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md) on an ML node.
  - Generate vectors outside of your Elastic deployment. Learn how to [Bring your own dense vectors](bring-own-vectors.md).

:::{tip}
Query vectors must have the same dimension and be created with the same model as the document vectors.
:::

- Required [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices):
  - `create_index` or `manage` to create an index with a `dense_vector` field
  - `create`, `index`, or `write` to add data
  - `read` to search the index

If you're using {{serverless-full}}, [compare {{es}} and {{vectordb}} projects](/solutions/vector-database.md#when-to-use-this-project-type) before implementing kNN search.

## kNN search methods [knn-methods]

{{es}} provides two ways to perform kNN search. Select a method based on your dataset size, latency requirements, and whether you need exact scoring.

[**Approximate kNN**](knn/approximate-knn.md) is best for most production workloads where low latency and scale matter more than perfect recall. It narrows the search to likely matches instead of scoring every document, reducing latency on large datasets.

[**Exact, brute-force kNN**](knn/exact-knn.md) is best for small datasets, pre-filtered subsets, or when you need precise scoring without approximate indexing. It scores every matching document, which guarantees accurate results but does not scale well for large datasets. You can improve latency by filtering your data to a small subset of documents.

## kNN search examples [knn-search-examples]

Every kNN search needs a query vector. You can provide it directly or have {{es}} generate or retrieve it at search time with `query_vector_builder`. The exact `dense_vector` query and the approximate kNN methods support query vector builders.

For examples that provide a query vector directly, refer to:

- [Approximate kNN search](knn/approximate-knn.md#approximate-knn-example)
- [Exact kNN with the `dense_vector` query](knn/exact-knn.md#exact-knn-dense-vector-query)
- [Exact kNN with a `script_score` query](knn/exact-knn.md#exact-knn-script-score-query)

### Generate or retrieve a query vector at search time [knn-build-query-vector]

The following examples use `query_vector_builder` with the top-level `knn` option. You can use the same builders with the exact `dense_vector` query. For all available builders and their parameters, refer to [Query vector builders](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#query-vector-builders-overview).

#### Use the `text_embedding` query vector builder [knn-semantic-search]

Use the `text_embedding` query vector builder to generate a query vector from text. Specify the same model that generated the document vectors.

Reference the deployed model or its deployment in the `query_vector_builder` object, and pass the search string as `model_text`:

```console
POST my-index/_search
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "my-text-embedding-model", <1>
        "model_text": "The opposite of blue" <2>
      }
    }
  }
}
```

1. The ID of the text embedding model that generates the query vector. Use the same model that produced the document embeddings in the target index. You can also provide a `deployment_id` as the `model_id` value.
2. The query string from which the model generates the dense vector representation.

For a walkthrough that covers deploying a model, generating document embeddings, and querying them, refer to this [end-to-end example](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

#### Use the `lookup` query vector builder [knn-lookup-similar-documents]
```{applies_to}
stack: ga 9.4
```

Use the [`lookup` query vector builder](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md#knn-query-builder-lookup) when the vector you want to search with is already stored in a document. This is the pattern behind "more like this" and recommendation features: instead of embedding new input, you take the vector from an item the user is viewing and find its nearest neighbors.

The following request finds the images most similar to document `2`:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index", <1>
        "id": "2", <2>
        "path": "image-vector" <3>
      }
    }
  }
}
```

1. The index that holds the document to look up. It doesn't have to be the index you're searching.
2. The ID of the document to look up. The request fails with a `404` if the document doesn't exist or has no value for `path`.
3. The vector field to read the query vector from. Its dimensions must match the field you're searching.

{{es}} reads the vector from the indexed field rather than from `_source`, so the lookup works even when vector values are excluded from `_source`.

The looked-up document is its own nearest neighbor, so it comes back as the top hit. Exclude it with a filter when you only want other documents:

```console
POST image-index/_search
{
  "knn": {
    "field": "image-vector",
    "k": 10,
    "query_vector_builder": {
      "lookup": {
        "index": "image-index",
        "id": "2",
        "path": "image-vector"
      }
    },
    "filter": {
      "bool": {
        "must_not": {
          "ids": {
            "values": ["2"]
          }
        }
      }
    }
  }
}
```

### Find more examples by method

For approximate kNN similarity thresholds, hybrid search, multiple vector fields, and aggregations, refer to [Approximate kNN query examples](knn/approximate-knn-query-examples.md). For filtering, refer to [Filter approximate kNN results](knn/filtered-knn-search.md).

For exact kNN filtering and scoring examples, refer to [Exact kNN search](knn/exact-knn.md).

## Next steps

Continue with the guide for the kNN search method that fits your use case:

- [Approximate kNN search](knn/approximate-knn.md): Learn how to map, index, and query `dense_vector` fields for fast, scalable approximate kNN search.
- [Exact kNN search](knn/exact-knn.md): Learn how to run exact brute-force kNN search for small datasets or precise scoring.
