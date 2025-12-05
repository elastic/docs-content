---
navigation_title: Jina
applies_to:
  stack: preview 9.3 
  serverless: preview
products:
  - id: machine-learning
---

# Jina models [ml-nlp-jina]

This page collects all Jina models you can use as part of the {{stack}}.
Currently, the following models are available as built-in models:

* [`jina-embeddings-v3`](#jina-embeddings-v3)
* [`jina-reranker-v2`](#jina-reranker-v2)

## `jina-embeddings-v3` [jina-embeddings-v3]

The [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) is a multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It provides long-context embeddings across a wide range of languages without requiring you to configure, download, or deploy any model artifacts yourself.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embedings-v3` model supports input lengths of up to 8192 tokens and produces 1024-dimension embeddings by default. It uses task-specific adapters to optimize embeddings for different use cases (such as retrieval or classification), and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.

For more information about the model, refer to the [model card](https://huggingface.co/jinaai/jina-embeddings-v3) on Hugging Face.

### Dense vector embeddings

Dense vector embeddings are fixed-length numerical representations of text. When you send text to an EIS {{infer}} endpoint that uses `jina-embeddings-v3`, the model returns a vector of floating-point numbers (for example, 1024 values). Texts that are semantically similar have embeddings that are close to each other in this vector space. {{es}} stores these vectors in [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) fields or through the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) type and uses vector similarity search to retrieve the most relevant documents for a given query. Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, this model produces compact dense vectors that are well suited for multilingual and cross-domain use cases.

### Requirements [jina-embeddings-v3-req]

To use `jina-embeddings-v3`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

### Getting started with `jina-embeddings-v3` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-embeddings-v3` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-embeddings-v3
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v3"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in `text_embedding` {{infer}} tasks or search queries.
For example, the following API request ingests the input text and produce embeddings.

```console
POST _inference/text_embedding/eis-jina-embeddings-v3
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

### Performance considerations [jina-embeddings-v3-performance]

* `jina-embeddings-v3` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although `jina-embeddings-v3` has a context window of 8192 tokens, it's best to limit the input to 2048-4096 tokens for optimal performance.
For larger fields that exceed this limit - for example, `body_content` on web crawler documents - consider chunking the content into multiple values, where each chunk can be under 4096 tokens.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

## `jina-reranker-v2` [jina-reranker-v2]

[`jina-reranker-v2`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) is a multilingual cross-encoder model helps you to improve search releavence across over 100 languages and various data types. The model significantly improve information retrieval in multilingual environments. `jina-reranker-v2` is available out-of-the-box in supporting Elastic deployments using the {{es}} Inference API. You can use the model to improve existing search applications like hybrid semantic search, retrieval augmented generation (RAG), and more. You can use the model through Elastic {{infer-cap}} Service (EIS), Elastic's own infrastructure, without the need of managing infrastructure and model resources.

For more information about the model, refer to the [model card](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) on Hugging Face.

### Requirements [jina-reranker-v2-req]

To use `jina-reranker-v2`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

### Getting started with `jina-reranker-v2` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-reranker-v2` model in the `model_id` field.

```console
PUT _inference/rerank/eis-jina-reranker-v2
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-reranker-v2"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in `rerank` {{infer}} tasks.
For example, the following API request ingests the input text and rank them by relevance:

```console
POST _inference/rerank/eis-jina-reranker-v2
{
  "input": ["luke", "like", "leia", "chewy","r2d2", "star", "wars"],
  "query": "star wars main character"
}
```
