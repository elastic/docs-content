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

## `jina-embeddings-v3` [jina-embeddings-v3]
```{applies_to}
stack: preview 9.3
serverless: preview
```

The [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) is a multilingual dense vector embedding model that you can use through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It provides long-context embeddings across a wide range of languages without requiring you to configure, download, or deploy any model artifacts yourself.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embedings-v3` model supports input lengths of up to 8192 tokens and produces 1024-dimension embeddings by default. It uses task-specific adapters to optimize embeddings for different use cases (such as retrieval or classification), and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.

### Dense vector embeddings

Dense vector embeddings are fixed-length numerical representations of text. When you send text to an EIS {{infer}} endpoint that uses `jina-embeddings-v3`, the model returns a vector of floating-point numbers (for example, 1024 values). Texts that are semantically similar have embeddings that are close to each other in this vector space. {{es}} stores these vectors in `dense_vector` fields or through the `semantic_text` type and uses vector similarity search to retrieve the most relevant documents for a given query. Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, this model produces compact dense vectors that are well suited for multilingual and cross-domain use cases.

### Requirements [jina-embeddings-v3-req]

To use `jina-embeddings-v3`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level for semantic search or the trial period activated.

### Getting started with `jina-embeddings-v3` via the Elastic {{infer-cap}} Service

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

The created {{infer}} endpoint uses the model for {{infer}} operations on the Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in text_embedding {{infer}} tasks or search queries.
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
Although `jina-embeddings-v3` has a context window of 8192 tokens, for optimal performance it's best to limit the input to 2048-4096 tokens.
For larger fields that exceed this limit - for example, body_content on web crawler documents - consider "chunking" the content into multiple values, where each chunk can be under 4096 tokens.
* Larger documents take longer at ingestion time, and inference time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform inference on, the longer it takes per document to ingest.

To learn more about `jina-embeddings-v3` performance, refer to the Benchmark information.

