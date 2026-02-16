---
navigation_title: "Tutorial: Manual dense and sparse workflows"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search-deployed-nlp-model.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Tutorial: Dense and sparse workflows using ingest pipelines [semantic-search-deployed-nlp-model]

::::{important}

* For the easiest way to perform semantic search in the {{stack}}, refer to the [`semantic_text`](../semantic-search/semantic-search-semantic-text.md) end-to-end tutorial.
* This tutorial predates the [{{infer}} endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) and the [`semantic_text` field type](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md). Today there are simpler, higher-level options for semantic search than the ones outlined in this tutorial. The semantic text workflow is the recommended way to perform semantic search for most use cases.
::::

This guide shows how to implement semantic search in {{es}} with deployed NLP models: from selecting a model, to configuring ingest pipelines, to running queries.

## Select an NLP model [deployed-select-nlp-model]

{{es}} supports a [wide range of NLP models](/explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md#ml-nlp-model-ref-text-embedding), including **dense** and **sparse** vector models. Choosing the right model is critical for good relevance.

While bringing your own text embedding model is possible, achieving strong results typically requires tuning and evaluation. Selecting a well-performing third-party model from our list is a good start. Training the model on your own data is essential to ensure better search results than using only BM25. However, the model training process requires a team of data scientists and ML experts, making it expensive and time-consuming.

To lower the barrier, Elastic provides [**Elastic Learned Sparse EncodeR (ELSER)**](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), a pre-trained sparse vector model (English-only) that delivers strong out-of-the-box relevance without fine-tuning. This adaptability makes it suitable for various NLP use cases out of the box. Unless you have an ML team, we recommend starting with ELSER.

Sparse vectors are mostly zeros with a small number of non-zero values. This representation is commonly used for textual data. With ELSER, both documents and queries are represented as high-dimensional sparse vectors. Each non-zero element of the vector corresponds to a term in the model vocabulary. The ELSER vocabulary contains around 30000 terms, so the sparse vectors created by ELSER contain about 30000 values, the majority of which are zero. The ELSER model replaces the terms in the original query with other terms learned from the training dataset that appear in documents matching the original search terms, and assigns weights to control their importance.

## Deploy the model in {{es}} [deployed-deploy-nlp-model]

After you choose a model, deploy it in {{es}}.

:::::::{tab-set}

::::::{tab-item} ELSER
To deploy ELSER, refer to [Download and deploy ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#download-deploy-elser).
::::::

::::::{tab-item} Dense vector models
To deploy a third-party text embedding model, refer to [Deploy a text embedding model](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md#ex-te-vs-deploy).
::::::

:::::::

## Map a field for the text embeddings [deployed-field-mappings]

Before generating embeddings, prepare your **index mapping**. The mapping depends on whether you use a **sparse** (ELSER) or **dense** model.

:::::::{tab-set}

::::::{tab-item} ELSER
ELSER outputs token-weight pairs. Use the [`sparse_vector`](elasticsearch://reference/elasticsearch/mapping-reference/sparse-vector.md) field to store them.

To create a mapping for your ELSER index, refer to the [Create the index mapping section](../semantic-search/semantic-search-elser-ingest-pipelines.md#elser-mappings) of the tutorial.
Create a mapping with a `sparse_vector` field for the tokens and a `text` field for the source content. For example:

```console
PUT my-index
{
  "mappings": {
    "properties": {
      "my_tokens": { <1>
        "type": "sparse_vector" <2>
      },
      "my_text_field": { <3>
        "type": "text" <4>
      }
    }
  }
}
```

1. The field that will contain ELSER-generated tokens.
2. The field that contains the tokens must be a `sparse_vector` field.
3. The source field used to create the sparse vector representation. In this example, the name of the field is `my_text_field`.
4. The field type is `text` in this example.
::::::

::::::{tab-item} Dense vector models
Dense vector models output numeric embeddings. Use the [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) field type for storing dense vectors that the supported third-party model you selected generates. Keep in mind that the model produces embeddings with a certain number of dimensions. The `dense_vector` field must be configured with the same number of dimensions using the `dims` option. Refer to the respective model documentation to get information about the number of dimensions of the embeddings.

To review a mapping of an index for an NLP model, refer to the mapping code snippet in the [Add the text embedding model to an ingest inference pipeline](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md#ex-text-emb-ingest) section of the related tutorial. The example shows how to create an index mapping that defines the `my_embeddings.predicted_value` field - which will contain the model output - as a `dense_vector` field.

```console
PUT my-index
{
  "mappings": {
    "properties": {
      "my_embeddings.predicted_value": { <1>
        "type": "dense_vector", <2>
        "dims": 384 <3>
      },
      "my_text_field": { <4>
        "type": "text" <5>
      }
    }
  }
}
```

1. The name of the field that will contain the embeddings generated by the model.
2. The field that contains the embeddings must be a `dense_vector` field.
3. The model produces embeddings with a certain number of dimensions. The `dense_vector` field must be configured with the same number of dimensions by the `dims` option. Refer to the respective model documentation to get information about the number of dimensions of the embeddings.
4. The source field used to create the dense vector representation. In this example, the name of the field is `my_text_field`.
5. The field type is `text` in this example.
::::::

:::::::

## Generate text embeddings [deployed-generate-embeddings]

Use an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) with an [inference processor](elasticsearch://reference/enrich-processor/inference-processor.md) to generate embeddings at ingest time. The ingest pipeline processes the input data and indexes it into the destination index. At index time, the inference ingest processor uses the trained model to infer against the data ingested through the pipeline. After you created the ingest pipeline with the inference processor, you can ingest your data through it to generate the model output.

:::::::{tab-set}

::::::{tab-item} ELSER
This is how an ingest pipeline that uses the ELSER model is created:

```console
PUT _ingest/pipeline/my-text-embeddings-pipeline
{
  "description": "Text embedding pipeline",
  "processors": [
    {
      "inference": {
        "model_id": ".elser_model_2",
        "input_output": [ <1>
          {
            "input_field": "my_text_field",
            "output_field": "my_tokens"
          }
        ]
      }
    }
  ]
}
```

1. Configuration object that defines the `input_field` for the {{infer}} process and the `output_field` that will contain the {{infer}} results.

To ingest data through the pipeline to generate tokens with ELSER, refer to the [Ingest the data through the {{infer}} ingest pipeline](/solutions/search/semantic-search/semantic-search-elser-ingest-pipelines.md#reindexing-data-elser) section of the tutorial. After you successfully ingested documents by using the pipeline, your index will contain the tokens generated by ELSER. Tokens are learned associations capturing relevance, they are not synonyms. To learn more about what tokens are, refer to [this page](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md#elser-tokens).
::::::

::::::{tab-item} Dense vector models
Example ingest pipeline using a text embedding model:

```console
PUT _ingest/pipeline/my-text-embeddings-pipeline
{
  "description": "Text embedding pipeline",
  "processors": [
    {
      "inference": {
        "model_id": "sentence-transformers__msmarco-minilm-l-12-v3", <1>
        "target_field": "my_embeddings",
        "field_map": { <2>
          "my_text_field": "text_field"
        }
      }
    }
  ]
}
```

1. The model ID of the text embedding model you want to use.
2. The `field_map` object maps the input document field name (which is `my_text_field` in this example) to the name of the field that the model expects (which is always `text_field`).

To ingest data through the pipeline to generate text embeddings with your chosen model, refer to the [Add the text embedding model to an inference ingest pipeline](/explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md#ex-text-emb-ingest) section. The example shows how to create the pipeline with the inference processor and reindex your data through the pipeline. After you successfully ingested documents by using the pipeline, your index will contain the text embeddings generated by the model.
::::::

:::::::
Now it is time to perform semantic search!

## Search the data with vector search [deployed-search]

Depending on the type of model you have deployed, you can query rank features with a [sparse vector](elasticsearch://reference/query-languages/query-dsl/query-dsl-sparse-vector-query.md) query, or dense vectors with a kNN search.

:::::::{tab-set}

::::::{tab-item} ELSER
ELSER text embeddings can be queried using a [sparse vector query](elasticsearch://reference/query-languages/query-dsl/query-dsl-sparse-vector-query.md). The sparse vector query enables you to query a [sparse vector](elasticsearch://reference/elasticsearch/mapping-reference/sparse-vector.md) field, by providing the inference ID associated with the NLP model you want to use, and the query text:

```console
GET my-index/_search
{
   "query":{
    "sparse_vector": {
        "field": "my_tokens",
        "inference_id": "my-elser-endpoint",
        "query": "the query string"
      }
   }
}
```

::::::

::::::{tab-item} Dense vector models
Text embeddings produced by dense vector models can be queried using a [kNN search](knn.md#knn-semantic-search). In the `knn` clause, provide the name of the dense vector field, and a `query_vector_builder` clause with the model ID and the query text.

```console
GET my-index/_search
{
  "knn": {
    "field": "my_embeddings.predicted_value",
    "k": 10,
    "num_candidates": 100,
    "query_vector_builder": {
      "text_embedding": {
        "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
        "model_text": "the query string"
      }
    }
  }
}
```

::::::

:::::::

## Beyond semantic search with hybrid search [deployed-hybrid-search]

In some situations, lexical search may perform better than semantic search. For example, when searching for single words or IDs, like product numbers.

Combining semantic and lexical search into one hybrid search request using [reciprocal rank fusion](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) provides the best of both worlds. Not only that, but hybrid search using reciprocal rank fusion [has been shown to perform better in general](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-hybrid).

:::::::{tab-set}

::::::{tab-item} ELSER
Hybrid search between a semantic and lexical query can be achieved by using an [`rrf` retriever](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) as part of your search request. Provide a `sparse_vector` query and a full-text query as [`standard` retrievers](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) for the `rrf` retriever. The `rrf` retriever uses [reciprocal rank fusion](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) to rank the top documents.

```console
GET my-index/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "match": {
                "my_text_field": "the query string"
              }
            }
          }
        },
        {
          "standard": {
            "query": {
             "sparse_vector": {
                "field": "my_tokens",
                "inference_id": "my-elser-endpoint",
                "query": "the query string"
              }
            }
          }
        }
      ]
    }
  }
}
```

::::::

::::::{tab-item} Dense vector models
Hybrid search between a semantic and lexical query can be achieved by providing:

* an `rrf` retriever to rank top documents using [reciprocal rank fusion](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md)
* a `standard` retriever as a child retriever with `query` clause for the full-text query
* a `knn` retriever as a child retriever with the kNN search that queries the dense vector field

```console
GET my-index/_search
{
  "retriever": {
    "rrf": {
      "retrievers": [
        {
          "standard": {
            "query": {
              "match": {
                "my_text_field": "the query string"
              }
            }
          }
        },
        {
          "knn": {
            "field": "text_embedding.predicted_value",
            "k": 10,
            "num_candidates": 100,
            "query_vector_builder": {
              "text_embedding": {
                "model_id": "sentence-transformers__msmarco-minilm-l-12-v3",
                "model_text": "the query string"
              }
            }
          }
        }
      ]
    }
  }
}
```

::::::

:::::::
