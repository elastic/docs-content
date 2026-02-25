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

* [`jina-embeddings-v5-text-small`](#jina-embeddings-v5-text-small)
* [`jina-embeddings-v5-text-nano`](#jina-embeddings-v5-text-nano)
* [`jina-embeddings-v3`](#jina-embeddings-v3)
* [`jina-reranker-v3`](#jina-reranker-v3)
* [`jina-reranker-v2`](#jina-reranker-v2)

## `jina-embeddings-v5-text-small` [jina-embeddings-v5-text-small]

The [`jina-embeddings-v5-text-small`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) model is a compact, multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It is optimized for retrieval, text matching, clustering, and classification with task-specific adapters and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v5-text-small` model has 677M parameters, supports a 32768 token input context window, and produces 1024-dimension embeddings by default.

For more information about the model family, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) or the [model collection](https://huggingface.co/collections/jinaai/jina-embeddings-v5-text) on Hugging Face.

### Dense vector embeddings

Dense vector embeddings are fixed-length numerical representations of text. When you send text to an EIS {{infer}} endpoint that uses `jina-embeddings-v5-text-small`, the model returns a vector of floating-point numbers (for example, 1024 values). Texts that are semantically similar have embeddings that are close to each other in this vector space. {{es}} stores these vectors in [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) fields or through the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) type and uses vector similarity search to retrieve the most relevant documents for a given query. Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, this model produces compact dense vectors that are well suited for multilingual and cross-domain use cases.

### Requirements [jina-embeddings-v5-text-small-req]

To use `jina-embeddings-v5-text-small`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

### Getting started with `jina-embeddings-v5-text-small` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-embeddings-v5-text-small` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-embeddings-v5-text-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-text-small"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in `text_embedding` {{infer}} tasks or search queries.
For example, the following API request ingests the input text and produce embeddings.

```console
POST _inference/text_embedding/eis-jina-embeddings-v5-text-small
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

### Performance considerations [jina-embeddings-v5-text-small-performance]

* `jina-embeddings-v5-text-small` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports a 32768 token context window, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

## `jina-embeddings-v5-text-nano` [jina-embeddings-v5-text-nano]

The [`jina-embeddings-v5-text-nano`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) model is a compact, multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It is optimized for retrieval, text matching, clustering, and classification with task-specific adapters and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v5-text-nano` model has 239M parameters, supports an 8192 token input context window, and produces 768-dimension embeddings by default.

For more information about the model family, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) or the [model collection](https://huggingface.co/collections/jinaai/jina-embeddings-v5-text) on Hugging Face.

### Requirements [jina-embeddings-v5-text-nano-req]

To use `jina-embeddings-v5-text-nano`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

### Getting started with `jina-embeddings-v5-text-nano` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-embeddings-v5-text-nano` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-embeddings-v5-text-nano
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-text-nano"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in `text_embedding` {{infer}} tasks or search queries.
For example, the following API request ingests the input text and produce embeddings.

```console
POST _inference/text_embedding/eis-jina-embeddings-v5-text-nano
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

### Performance considerations [jina-embeddings-v5-text-nano-performance]

* `jina-embeddings-v5-text-nano` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports an 8192 token context window, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

## `jina-embeddings-v3` [jina-embeddings-v3]

The [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) is a multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It provides long-context embeddings across a wide range of languages without requiring you to configure, download, or deploy any model artifacts yourself.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v3` model supports input lengths of up to 8192 tokens and produces 1024-dimension embeddings by default. It uses task-specific adapters to optimize embeddings for different use cases (such as retrieval or classification), and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.

For more information about the model, refer to the [model card](https://huggingface.co/jinaai/jina-embeddings-v3) on Hugging Face.

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

## `jina-reranker-v3` [jina-reranker-v3]

[`jina-reranker-v3`](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service) is a multilingual listwise reranking model that improves search relevance by reordering candidate results using cross-document context.
It is available out-of-the-box through Elastic {{infer-cap}} Service (EIS), so you can apply reranking without managing infrastructure or model resources.

The model reranks up to 64 documents together in a single inference call, which makes it a good fit for high-precision top-k reranking in hybrid search and RAG workflows.

For more information about the model, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service) or the [model announcement](https://jina.ai/news/jina-reranker-v3-0-6b-listwise-reranker-for-sota-multilingual-retrieval/).

### Requirements [jina-reranker-v3-req]

To use `jina-reranker-v3`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

### Getting started with `jina-reranker-v3` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-reranker-v3` model in the `model_id` field.

```console
PUT _inference/rerank/eis-jina-reranker-v3
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-reranker-v3"
  }
}
```

The created {{infer}} endpoint uses the model for {{infer}} operations on Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in `rerank` {{infer}} tasks.
For example, the following API request ingests the input strings and ranks them by relevance:

```console
POST _inference/rerank/eis-jina-reranker-v3
{
  "input": ["The Swiss Alps", "a steep hill", "a pebble", "a glacier"],
  "query": "mountain range"
}
```

### Performance considerations

`jina-reranker-v3` is designed for top-k reranking and processes up to 64 candidates at a time.
For larger candidate sets, rerank the most relevant results returned by your first-stage retrieval and keep your candidate list within the model's listwise limit.

## `jina-reranker-v2` [jina-reranker-v2]

[`jina-reranker-v2`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) is a multilingual cross-encoder model that helps you to improve search relevance across over 100 languages and various data types. The model significantly improves information retrieval in multilingual environments. `jina-reranker-v2` is available out-of-the-box and supports Elastic deployments using the {{es}} Inference API. You can use the model to improve existing search applications like hybrid semantic search, retrieval augmented generation (RAG), and more. You can use the model through Elastic {{infer-cap}} Service (EIS), Elastic's own infrastructure, without the need of managing infrastructure and model resources.

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
For example, the following API request ingests the input strings and ranks them by relevance:

```console
POST _inference/rerank/eis-jina-reranker-v2
{
  "input": ["luke", "like", "leia", "chewy","r2d2", "star", "wars"],
  "query": "star wars main character"
}
```

### Performance considerations

`jina-reranker-v2` works best on small, medium or large sized fields that contain natural language.
This aligns best with fields like title, description, summary, or abstract.
The model uses a context window of 1024 tokens and automatically chunks larger content.
Larger documents take longer to process, and inference time also increases the more documents are present in the reranking request.

## Further reading
The following blog posts provide additional background and context:

* [jina-embeddings-v5-text: Compact state-of-the-art text embeddings for search and intelligent applications](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text)
* [Jina rerankers bring fast, multilingual reranking to Elastic Inference Service (EIS)](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service)
* [jina-embeddings-v3 is now available on Elastic Inference Service](https://www.elastic.co/search-labs/blog/jina-embeddings-v3-elastic-inference-service)