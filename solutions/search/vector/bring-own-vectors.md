---
navigation_title: "Bring your own dense vectors"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bring-your-own-vectors.html
applies_to:
  stack:
  serverless:
---

# Bring your own dense vectors [bring-your-own-vectors]


This tutorial demonstrates how to index documents that already have dense vector embeddings into {{es}}. You’ll also learn the syntax for searching these documents using a `knn` query.

You’ll find links at the end of this tutorial for more information about deploying a text embedding model in {{es}}, so you can generate embeddings for queries on the fly.

::::{tip}
This is an advanced use case. Refer to [Semantic search](../semantic-search.md) for an overview of your options for semantic search with {{es}}.

::::


## Step 1: Create an index with `dense_vector` mapping [bring-your-own-vectors-create-index]

Each document in our simple dataset will have:

* A review: stored in a `review_text` field
* An embedding of that review: stored in a `review_vector` field

    * The `review_vector` field is defined as a [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) data type.


::::{tip}
The `dense_vector` type automatically uses `int8_hnsw` quantization by default to reduce the memory footprint required when searching float vectors. Learn more about balancing performance and accuracy in [Dense vector quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization).

::::


```console
PUT /amazon-reviews
{
  "mappings": {
    "properties": {
      "review_vector": {
        "type": "dense_vector",
        "dims": 8, <1>
        "index": true, <2>
        "similarity": "cosine" <3>
      },
      "review_text": {
        "type": "text"
      }
    }
  }
}
```

1. The `dims` parameter must match the length of the embedding vector. Here we’re using a simple 8-dimensional embedding for readability. If not specified, `dims` will be dynamically calculated based on the first indexed document.
2. The `index` parameter is set to `true` to enable the use of the `knn` query.
3. The `similarity` parameter defines the similarity function used to compare the query vector to the document vectors. `cosine` is the default similarity function for `dense_vector` fields in {{es}}.
%  TEST SETUP


## Step 2: Index documents with embeddings [bring-your-own-vectors-index-documents]


### Index a single document [_index_a_single_document]

First, index a single document to understand the document structure.

```console
PUT /amazon-reviews/_doc/1
{
  "review_text": "This product is lifechanging! I'm telling all my friends about it.",
  "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] <1>
}
```

1. The size of the `review_vector` array is 8, matching the `dims` count specified in the mapping.
%  TEST


### Bulk index multiple documents [_bulk_index_multiple_documents]

In a production scenario, you’ll want to index many documents at once using the [`_bulk` endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk).

Here’s an example of indexing multiple documents in a single `_bulk` request.

```console
POST /_bulk
{ "index": { "_index": "amazon-reviews", "_id": "2" } }
{ "review_text": "This product is amazing! I love it.", "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] }
{ "index": { "_index": "amazon-reviews", "_id": "3" } }
{ "review_text": "This product is terrible. I hate it.", "review_vector": [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] }
{ "index": { "_index": "amazon-reviews", "_id": "4" } }
{ "review_text": "This product is great. I can do anything with it.", "review_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] }
{ "index": { "_index": "amazon-reviews", "_id": "5" } }
{ "review_text": "This product has ruined my life and the lives of my family and friends.", "review_vector": [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1] }
```
%  TEST[continued]


## Step 3: Search documents with embeddings [bring-your-own-vectors-search-documents]

Now you can query these document vectors using a [`knn` retriever](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever). `knn` is a type of vector search, which finds the `k` most similar documents to a query vector. Here we’re simply using a raw vector for the query text, for demonstration purposes.

```console
POST /amazon-reviews/_search
{
  "retriever": {
    "knn": {
      "field": "review_vector",
      "query_vector": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], <1>
      "k": 2, <2>
      "num_candidates": 5 <3>
    }
  }
}
```

1. In this simple example, we’re sending a raw vector as the query text. In a real-world scenario, you’ll need to generate vectors for queries using an embedding model.
2. The `k` parameter specifies the number of results to return.
3. The `num_candidates` parameter is optional. It limits the number of candidates returned by the search node. This can improve performance and reduce costs.
%  TEST[skip:flakeyknnerror]


## Learn more [bring-your-own-vectors-learn-more]

In this simple example, we’re sending a raw vector for the query text. In a real-world scenario you won’t know the query text ahead of time. You’ll need to generate query vectors, on the fly, using the same embedding model that generated the document vectors.

For this you’ll need to deploy a text embedding model in {{es}} and use the [`query_vector_builder` parameter](elasticsearch://reference/query-languages/query-dsl-knn-query.md#knn-query-top-level-parameters). Alternatively, you can generate vectors client-side and send them directly with the search request.

Learn how to [use a deployed text embedding model](dense-versus-sparse-ingest-pipelines.md) for semantic search.

::::{tip}
If you’re just getting started with vector search in {{es}}, refer to [Semantic search](../semantic-search.md).

::::


