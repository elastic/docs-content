---
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Query vector builders [query-vector-builders]

A *query vector builder* generates a query vector at search time, so you don't need to compute the vector outside of {{es}} before running a kNN search.

Query vector builders are used inside the `query_vector_builder` object, which is supported by:

- The [`knn` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-knn-query.md)
- The [`knn` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/knn-retriever.md)
- The [`knn` option in the search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-knn)

{{es}} provides three query vector builders:

| Builder | Description |
| --- | --- |
| [`text_embedding`](#text-embedding-query-vector-builder) | Generates a query vector from text using a deployed {{ml}} text embedding model |
| [`embedding`](#embedding-query-vector-builder) | Generates a query vector from text or images using an inference service |
| [`lookup`](#lookup-query-vector-builder) | Retrieves a query vector stored in an existing {{es}} document |

## `text_embedding` query vector builder [text-embedding-query-vector-builder]

The `text_embedding` builder generates a query vector from a text string using a [text embedding model](../../../explore-analyze/machine-learning/nlp/ml-nlp-search-compare.md#ml-nlp-text-embedding) deployed in {{es}} Machine Learning.

Use `text_embedding` when you have a text embedding model deployed through {{es}} ML and want to perform semantic text search.

::::{important}
To use `text_embedding`:

* You need an index containing dense vector representations created by the same model.
* The text embedding NLP model deployment must be started.
::::

Reference the deployed model in the `query_vector_builder` object and provide the search text as `model_text`:

```js
(...)
{
  "knn": {
    "field": "dense-vector-field",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": { <1>
        "model_id": "my-text-embedding-model", <2>
        "model_text": "The opposite of blue" <3>
      }
    }
  }
}
(...)
```

1. The query vector builder to use.
2. The ID of the deployed text embedding model. Use the same model that produced the document embeddings in the target index. You can also provide the `deployment_id` as the `model_id` value.
3. The query text from which the model generates the dense vector representation.

For more information on how to deploy a trained model and use it to create text embeddings, refer to this [end-to-end example](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md).

## `embedding` query vector builder [embedding-query-vector-builder]

```{applies_to}
stack: ga 9.4
serverless: ga
```

The `embedding` builder generates a query vector from multimodal inputs — currently text and base64-encoded images — using an [inference service](../../../explore-analyze/elastic-inference/inference-api.md) configured with the `EMBEDDING` task type.

Use `embedding` when you want to:

- Search using both text and image inputs in the same query
- Use an externally managed inference service (such as Amazon Bedrock, Azure AI, Google Vertex AI, or a custom service) rather than an {{es}}-managed ML model
- Perform multimodal similarity search

::::{important}
The `inference_id` must refer to an inference service configured with the `EMBEDDING` task type. The target `dense_vector` field must contain embeddings produced by the same model.
::::

### Parameters [embedding-query-vector-builder-parameters]

`inference_id` (Required, string)
:   The ID of the inference endpoint to use for generating the query embedding. The endpoint must use the `EMBEDDING` task type.

`input` (Required)
:   The input to embed. Can be:

    - A **string** — a shorthand for a single text input.
    - A **single input object** with `type`, `value`, and optionally `format` fields.
    - An **array of input objects** for multimodal queries combining text and images.

    Each input object supports:

    - `type` (Required, string): `text` or `image`.
    - `value` (Required, string): The text string or the base64-encoded image data.
    - `format` (Optional, string): The encoding format of the value. Defaults to `text` for text inputs and `base64` for image inputs.

`timeout` (Optional, [time value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units))
:   Timeout for the inference request. Defaults to `30s`.

### Examples [embedding-query-vector-builder-examples]

**Text query (string shorthand):**

```js
(...)
{
  "knn": {
    "field": "content-vector",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "embedding": {
        "inference_id": "my-multimodal-endpoint", <1>
        "input": "What is the capital of France?" <2>
      }
    }
  }
}
(...)
```

1. The inference endpoint ID configured with the `EMBEDDING` task type.
2. A plain string is treated as a single text input.

**Single image input:**

```js
(...)
{
  "knn": {
    "field": "image-vector",
    "k": 5,
    "num_candidates": 50,
    "query_vector_builder": {
      "embedding": {
        "inference_id": "my-multimodal-endpoint",
        "input": {
          "type": "image", <1>
          "format": "base64", <2>
          "value": "<base64-encoded-image-data>" <3>
        }
      }
    }
  }
}
(...)
```

1. Specifies the input as an image.
2. The image data is base64-encoded.
3. The base64-encoded image bytes.

**Multimodal input (text and image combined):**

```js
(...)
{
  "knn": {
    "field": "multimodal-vector",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "embedding": {
        "inference_id": "my-multimodal-endpoint",
        "input": [ <1>
          {
            "type": "text",
            "value": "A red sports car"
          },
          {
            "type": "image",
            "format": "base64",
            "value": "<base64-encoded-image-data>"
          }
        ],
        "timeout": "60s" <2>
      }
    }
  }
}
(...)
```

1. An array of input objects combining text and image.
2. Optional custom timeout for the inference call.

## `lookup` query vector builder [lookup-query-vector-builder]

```{applies_to}
stack: ga 9.4
```

The `lookup` builder retrieves a query vector stored in an existing {{es}} document, so you can use any document's vector field directly as the query vector.

Use `lookup` when you want to:

- Find similar items for recommendations
- Retrieve related content from a seed document
- Avoid an extra client round-trip to fetch a vector before searching

The lookup source must reference a `dense_vector` field that contains a single vector value. As with any kNN search, the looked-up vector must be compatible with the target kNN field (same dimensions and same embedding model semantics).

```js
(...)
{
  "knn": {
    "field": "product-vector",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "lookup": { <1>
        "id": "product-123", <2>
        "index": "seed-products", <3>
        "path": "product-vector", <4>
        "routing": "tenant-a" <5>
      }
    }
  }
}
(...)
```

1. Use the `lookup` query vector builder to retrieve the vector from an existing document.
2. The ID of the source document that contains the vector to use for search.
3. The name of the index that stores the source document.
4. The vector field path in the source document. It must reference a `dense_vector` field containing a single vector value.
5. Optional routing value used to retrieve the source document.
