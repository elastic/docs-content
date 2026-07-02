---
navigation_title: Exact kNN search
description: Run exact brute-force k-nearest neighbor (kNN) vector search in Elasticsearch using script_score queries for small datasets or precise scoring.
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Exact kNN search [exact-knn]

To run an exact kNN search, use a `script_score` query with a vector function.

1. Explicitly map one or more `dense_vector` fields. If you don’t intend to use the field for approximate kNN, set the `index` mapping option to `false`. This can significantly improve indexing speed.

    ```console
    PUT product-index
    {
      "mappings": {
        "properties": {
          "product-vector": {
            "type": "dense_vector",
            "dims": 5,
            "index": false
          },
          "price": {
            "type": "long"
          }
        }
      }
    }
    ```

2. Index your data.

    ```console
    POST product-index/_bulk?refresh=true
    { "index": { "_id": "1" } }
    { "product-vector": [230.0, 300.33, -34.8988, 15.555, -200.0], "price": 1599 }
    { "index": { "_id": "2" } }
    { "product-vector": [-0.5, 100.0, -13.0, 14.8, -156.0], "price": 799 }
    { "index": { "_id": "3" } }
    { "product-vector": [0.5, 111.3, -13.0, 14.8, -156.0], "price": 1099 }
    ...
    ```

3. Use the [search API]({{es-apis}}operation/operation-search) to run a `script_score` query containing a [vector function](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md#vector-functions).

    ::::{tip}
    To limit the number of matched documents passed to the vector function, we recommend you specify a filter query in the `script_score.query` parameter. If needed, you can use a [`match_all` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-all-query.md) in this parameter to match all documents. However, matching all documents can significantly increase search latency.
    ::::

    ```console
    POST product-index/_search
    {
      "query": {
        "script_score": {
          "query" : {
            "bool" : {
              "filter" : {
                "range" : {
                  "price" : {
                    "gte": 1000
                  }
                }
              }
            }
          },
          "script": {
            "source": "cosineSimilarity(params.queryVector, 'product-vector') + 1.0",
            "params": {
              "queryVector": [-0.5, 90.0, -10, 14.8, -156.0]
            }
          }
        }
      }
    }
    ```

A *k-nearest neighbor* (kNN) search finds the *k* nearest vectors to a query vector, as measured by a similarity metric.

Common use cases for kNN include:

* Relevance ranking based on natural language processing (NLP) algorithms
* Product recommendations and recommendation engines
* Similarity search for images or videos

::::{tip}
Check out our [hands-on tutorial](../bring-own-vectors.md) to learn how to ingest dense vector embeddings into Elasticsearch.
::::
