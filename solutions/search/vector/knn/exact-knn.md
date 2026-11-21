---
navigation_title: Exact kNN search
description: Run exact brute-force k-nearest neighbor (kNN) vector search in Elasticsearch for small datasets or precise scoring.
applies_to:
  stack:
  serverless:
---

# Exact kNN search [exact-knn]

Exact kNN search computes similarity between the query vector and every matching document, so results are fully accurate but latency increases with corpus size. Use it for small datasets, pre-filtered subsets, or when you need precise scoring without approximate indexing. For most production workloads, prefer [Approximate kNN search](approximate-knn.md).

{{es}} supports two query methods for exact kNN search:

- Use the [`dense_vector` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-dense-vector-query.md) for standard exact vector scoring. See an [example](#exact-knn-dense-vector-query).
- Use the [`script_score` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) when you need a custom scoring calculation. See an [example](#exact-knn-script-score-query).

## Map and index vectors

First, map and index the vectors that you want to search:

1. Explicitly map one or more `dense_vector` fields. If you don't intend to use the field for approximate kNN, set the `index` mapping option to `false`. This can significantly improve indexing speed.

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

## Run an exact kNN search with the `dense_vector` query [exact-knn-dense-vector-query]
```{applies_to}
stack: ga 9.6
serverless: ga
```

Use the [search API]({{es-apis}}operation/operation-search) to run a `dense_vector` query. The query scores every document that has a value for the specified vector field. To reduce the number of vectors that it scores, combine it with a filter in a `bool` query:

```console
POST product-index/_search
{
  "query": {
    "bool": {
      "must": {
        "dense_vector": {
          "field": "product-vector",
          "query_vector": [-0.5, 90.0, -10, 14.8, -156.0]
        }
      },
      "filter": {
        "range": {
          "price": {
            "gte": 1000
          }
        }
      }
    }
  }
}
```

Because `product-vector` uses the default `float` element type and is not indexed, the query uses cosine similarity by default. You can use the `similarity_function` parameter to select a different similarity function. For indexed fields, the query uses the similarity configured in the field mapping by default.

## Run an exact kNN search with a `script_score` query [exact-knn-script-score-query]

Use a `script_score` query if the `dense_vector` query isn't available in your {{stack}} version. You can also use `script_score` when you need to customize the scoring calculation.

Specify a filter query in the `script_score.query` parameter to limit the number of matched documents passed to the vector function. If needed, you can use a [`match_all` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-all-query.md) in this parameter to match all documents. However, matching all documents can significantly increase search latency.

```console
POST product-index/_search
{
  "query": {
    "script_score": {
      "query": {
        "bool": {
          "filter": {
            "range": {
              "price": {
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

The `dense_vector` and `script_score` examples can rank documents in the same order, but they don't return the same numeric scores. The `dense_vector` query applies the built-in score transformation for the selected similarity function. A `script_score` query returns the value calculated by your script, such as the cosine similarity plus `1.0` in this example.

## Resources

- [Tune approximate kNN search](/deploy-manage/production-guidance/optimize-performance/approximate-knn-search.md): Production guidance for vector memory, node sizing, indexing, filesystem cache, and on-disk rescoring.
- [Profile kNN search](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md#profiling-knn-search): Inspect query timing and vector operation counts to diagnose slow kNN searches.
- [`dense_vector` field type](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md): API reference for vector field mapping, including `index`, `similarity`, `index_options`, and quantization parameters.
- [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md): API reference for the `knn` query, including parameters, `query_vector_builder` options, and usage with `dense_vector` and `semantic_text` fields.
