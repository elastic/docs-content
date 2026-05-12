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

:::{note}
Jina models are currently available only through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) or [external {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) providers. Since these models rely on external connectivity, they cannot currently be deployed on [{{ml}} nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role) and are not compatible with fully air-gapped environments.
:::

:::{tip}
If you may need to search images, audio, video, or PDFs alongside text, start with a `jina-embeddings-v5-omni-*` model. The v5 omni models share the same text embedding space as their matching v5 text models, so existing `v5-text-*` vectors can be compared with text vectors from the matching omni model without reindexing.
:::

Currently, the following models are available as built-in models:

**Embedding models**

* [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small) — multimodal (text, image, audio, video, PDF)
* [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano) — multimodal (text, image, audio, video, PDF)
* [`jina-embeddings-v5-text-small`](#jina-embeddings-v5-text-small) — text-only
* [`jina-embeddings-v5-text-nano`](#jina-embeddings-v5-text-nano) — text-only
* [`jina-embeddings-v3`](#jina-embeddings-v3) — text-only

**Rerankers**

* [`jina-reranker-v3`](#jina-reranker-v3)
* [`jina-reranker-v2`](#jina-reranker-v2)

## Embedding models

Embedding models convert text into vector embeddings, which are fixed-length numerical representations that capture semantic meaning.
Texts with similar meaning are mapped to nearby points in vector space, so you can retrieve relevant documents with vector similarity search.
When you send text to an EIS {{infer}} endpoint that uses an embedding model, the model returns a vector of floating-point numbers (for example, 1024 values). {{es}} stores these vectors in [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) fields or through the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field and uses vector similarity search to retrieve the most relevant documents for a given query. Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, these models produce compact dense vectors that are well suited for multilingual and cross-domain use cases.

### Jina v5 omni embedding models [jina-embeddings-v5-omni]

The `jina-embeddings-v5-omni-*` models accept **text, image, audio, video, and PDF** inputs and place all supported input types in a shared vector space. Use them when you need cross-modal retrieval, such as querying a text index with an image or finding videos from a text query.

The v5 omni models are available through Elastic {{infer-cap}} Service (EIS), so no {{ml}} node scaling or model deployment is required.

#### `jina-embeddings-v5-omni-small` [jina-embeddings-v5-omni-small]

```{applies_to}
stack: ga 9.5
serverless: ga
```

[`jina-embeddings-v5-omni-small`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index) is the recommended Jina embedding model for deployments that need higher-quality mixed-media search. It produces 1024-dimension embeddings by default, supports a 32768 token input context window, and uses the same text embedding space as [`jina-embeddings-v5-text-small`](#jina-embeddings-v5-text-small).

For more information about the model, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index) or the [model page](https://jina.ai/models/jina-embeddings-v5-omni-small/).

#### `jina-embeddings-v5-omni-nano` [jina-embeddings-v5-omni-nano]

```{applies_to}
stack: ga 9.5
serverless: ga
```

[`jina-embeddings-v5-omni-nano`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index) is the compact, lower-cost member of the Jina v5 omni family. It produces 768-dimension embeddings by default, supports a 32768 token input context window, and uses the same text embedding space as [`jina-embeddings-v5-text-nano`](#jina-embeddings-v5-text-nano).

For more information about the model, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index) or the [model page](https://jina.ai/models/jina-embeddings-v5-omni-nano/).

#### Requirements [jina-embeddings-v5-omni-req]

To use a v5 omni model, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level. {{ecloud}} trial accounts cannot use the v5 omni models; start a paid {{ecloud}} deployment or {{serverless-short}} project to access them.

All input types require {{stack}} 9.5 or later.

#### Getting started with v5 omni models through Elastic {{infer-cap}} Service

For text input, the recommended entry point is a `semantic_text` field that references one of the preconfigured v5 omni {{infer}} endpoints. {{es}} provisions the endpoint on first reference.

Create an index with a `semantic_text` field:

```console
PUT multimodal-semantic-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "semantic_text",
        "inference_id": ".jina-embeddings-v5-omni-small"
      }
    }
  }
}
```

Index documents normally. {{es}} generates embeddings through the {{infer}} endpoint:

```console
POST multimodal-semantic-index/_doc
{
  "content": "'Kraft Dinner' is what Canadians call macaroni and cheese when prepared from a kit."
}
```

Query the field with a `semantic` query:

```console
GET multimodal-semantic-index/_search
{
  "query": {
    "semantic": {
      "field": "content",
      "query": "Was bedeutet 'Kraft Dinner' für Kanadier?"
    }
  }
}
```

To use `jina-embeddings-v5-omni-nano`, set `inference_id` to `.jina-embeddings-v5-omni-nano` instead.

To create an explicit {{infer}} endpoint instead of using the preconfigured endpoint, use the `embedding` task type:

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-small"
  }
}
```

#### Multimodal ingestion and querying [jina-embeddings-v5-omni-multimodal]

`semantic_text` ingests text content. To embed image, audio, video, or PDF input, or to issue a cross-modal query against a text index, call the {{infer}} endpoint directly and store or compare the resulting vector against a `dense_vector` field.

The request body is a structured `input` array. Each element holds a `content` object describing one piece of media, and each request can hold up to 16 input items. Media values are base64-encoded data URIs:

```console
POST _inference/embedding/.jina-embeddings-v5-omni-small
{
  "input": [
    { "content": { "type": "image", "format": "base64", "value": "data:image/png;base64,iVBORw0KGgo..." } },
    { "content": { "type": "audio", "format": "base64", "value": "data:audio/wav;base64,UklGRiQAAAB..." } },
    { "content": { "type": "video", "format": "base64", "value": "data:video/mp4;base64,AAAAIGZ0eXA..." } },
    { "content": { "type": "pdf",   "format": "base64", "value": "data:application/pdf;base64,JVBE..." } }
  ]
}
```

To combine several media items into a single embedding, pass an array of content fields under one `input` element:

```console
POST _inference/embedding/.jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        { "type": "text",  "value": "A description of the scene" },
        { "type": "image", "format": "base64", "value": "data:image/png;base64,iVBORw0KGgo..." },
        { "type": "audio", "format": "base64", "value": "data:audio/wav;base64,UklGRiQAAAB..." }
      ]
    }
  ]
}
```

The response is shaped `{"embeddings": [{"embedding": [...]}, ...]}`. The array length matches the number of input items, except for PDF input, which produces one embedding per page.

#### Upgrading from `jina-embeddings-v5-text-*` [jina-embeddings-v5-omni-migrate]

The v5 omni models share their text embedding space with the matching v5 text models. Existing `dense_vector` data populated by `jina-embeddings-v5-text-*` remains directly comparable to vectors produced from text input by the corresponding omni model, so no reindex is required.

Use the matching pair:

* `jina-embeddings-v5-omni-small` with `jina-embeddings-v5-text-small` (1024 dimensions)
* `jina-embeddings-v5-omni-nano` with `jina-embeddings-v5-text-nano` (768 dimensions)

Do not mix across the small and nano families, because their vector spaces and dimensions differ.

For `semantic_text` mappings, set the `inference_id` to the corresponding `.jina-embeddings-v5-omni-*` endpoint on new indices. Existing indices continue to work unchanged.

For code that calls `_inference` directly, the task type changes from `text_embedding` to `embedding`, and the request body changes from a flat string `input` to an array of `content` objects. See [Multimodal ingestion and querying](#jina-embeddings-v5-omni-multimodal).

For pure text workloads, keep using `v5-text-*` endpoints. Use `v5-omni-*` when mixed media is in scope.

#### Performance considerations [jina-embeddings-v5-omni-performance]

* Use `jina-embeddings-v5-omni-small` when retrieval quality is the main priority. Use `jina-embeddings-v5-omni-nano` when ingestion volume, latency, or cost is the main constraint.
* Each {{infer}} request can contain up to 16 input items.
* Image inputs must be at least 28×28 pixels (784 pixels total).
* PDF inputs return one embedding per page.
* Video is sampled at 32 uniformly spaced frames regardless of clip length. For long videos, segment into shorter clips for finer temporal resolution.
* Although the models support a 32768 token context window, consider chunking very large text fields to control latency and cost.

### `jina-embeddings-v5-text-small` [jina-embeddings-v5-text-small]

The [`jina-embeddings-v5-text-small`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) model is a compact, multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It is optimized for retrieval, text matching, clustering, and classification with task-specific adapters and includes support for Matryoshka Representation Learning, which enables you to truncate embeddings to fewer dimensions with minimal loss in quality.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v5-text-small` model has 677M parameters, supports a 32768 token input context window, and produces 1024-dimension embeddings by default.

For more information about the model family, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) or the [model collection](https://huggingface.co/collections/jinaai/jina-embeddings-v5-text) on Hugging Face.

#### Requirements [jina-embeddings-v5-text-small-req]

To use `jina-embeddings-v5-text-small`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

#### Getting started with `jina-embeddings-v5-text-small` through Elastic {{infer-cap}} Service

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

#### Performance considerations [jina-embeddings-v5-text-small-performance]

* `jina-embeddings-v5-text-small` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports a 32768 token context window, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

### `jina-embeddings-v5-text-nano` [jina-embeddings-v5-text-nano]

The [`jina-embeddings-v5-text-nano`](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) model is a compact, multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It is optimized for retrieval, text matching, clustering, and classification with task-specific adapters and includes support for Matryoshka Representation Learning, which enables you to truncate embeddings to fewer dimensions with minimal loss in quality.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v5-text-nano` model has 239M parameters, supports an 8192 token input context window, and produces 768-dimension embeddings by default.

For more information about the model family, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text) or the [model collection](https://huggingface.co/collections/jinaai/jina-embeddings-v5-text) on Hugging Face.

#### Requirements [jina-embeddings-v5-text-nano-req]

To use `jina-embeddings-v5-text-nano`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

#### Getting started with `jina-embeddings-v5-text-nano` through Elastic {{infer-cap}} Service

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

#### Performance considerations [jina-embeddings-v5-text-nano-performance]

* `jina-embeddings-v5-text-nano` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports an 8192 token context window, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

### `jina-embeddings-v3` [jina-embeddings-v3]

The [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) is a multilingual dense vector embedding model that you can use through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).
It provides long-context embeddings across a wide range of languages without requiring you to configure, download, or deploy any model artifacts yourself.
As the model runs on EIS, Elastic's own infrastructure, no ML node scaling and configuration is required to use it.

The `jina-embeddings-v3` model supports input lengths of up to 8192 tokens and produces 1024-dimension embeddings by default. It uses task-specific adapters to optimize embeddings for different use cases (such as retrieval or classification), and includes support for Matryoshka Representation Learning, which allows you to truncate embeddings to fewer dimensions with minimal loss in quality.

For more information about the model, refer to the [model card](https://huggingface.co/jinaai/jina-embeddings-v3) on Hugging Face.

#### Requirements [jina-embeddings-v3-req]

To use `jina-embeddings-v3`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

#### Getting started with `jina-embeddings-v3` through Elastic {{infer-cap}} Service

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

#### Performance considerations [jina-embeddings-v3-performance]

* `jina-embeddings-v3` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although `jina-embeddings-v3` has a context window of 8192 tokens, it's best to limit the input to 2048-4096 tokens for optimal performance.
For larger fields that exceed this limit - for example, `body_content` on web crawler documents - consider chunking the content into multiple values, where each chunk can be under 4096 tokens.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

## Rerankers

Reranker models take a query and an already retrieved set of candidate documents, then reorders those candidates by predicted relevance.
Rerankers improve precision for the top query results.

### `jina-reranker-v3` [jina-reranker-v3]

[`jina-reranker-v3`](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service) is a multilingual listwise reranking model that improves search relevance by reordering candidate results using cross-document context.
It is available out-of-the-box through Elastic {{infer-cap}} Service (EIS), so you can apply reranking without managing infrastructure or model resources.

The model reranks up to 64 documents together in a single inference call, which makes it a good fit for high-precision top-k reranking in hybrid search and RAG workflows.

For more information about the model, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service) or the [model announcement](https://jina.ai/news/jina-reranker-v3-0-6b-listwise-reranker-for-sota-multilingual-retrieval/).

#### Requirements [jina-reranker-v3-req]

To use `jina-reranker-v3`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

#### Getting started with `jina-reranker-v3` through Elastic {{infer-cap}} Service

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

#### Performance considerations [jina-reranker-v3-performance]

`jina-reranker-v3` is designed for top-k reranking and processes up to 64 candidates at a time.
For larger candidate sets, rerank the most relevant results returned by your first-stage retrieval and keep your candidate list within the model's listwise limit.

### `jina-reranker-v2` [jina-reranker-v2]

[`jina-reranker-v2`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) is a multilingual cross-encoder model that helps you to improve search relevance across over 100 languages and various data types. The model significantly improves information retrieval in multilingual environments. `jina-reranker-v2` is available out-of-the-box and supports Elastic deployments using the {{es}} Inference API. You can use the model to improve existing search applications like hybrid semantic search, retrieval augmented generation (RAG), and more. You can use the model through Elastic {{infer-cap}} Service (EIS), Elastic's own infrastructure, without the need of managing infrastructure and model resources.

For more information about the model, refer to the [model card](https://huggingface.co/jinaai/jina-reranker-v2-base-multilingual) on Hugging Face.

#### Requirements [jina-reranker-v2-req]

To use `jina-reranker-v2`, you must have the [appropriate subscription](https://www.elastic.co/subscriptions) level or the trial period activated.

#### Getting started with `jina-reranker-v2` through Elastic {{infer-cap}} Service

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

#### Performance considerations [jina-reranker-v2-performance]

`jina-reranker-v2` works best on small, medium or large sized fields that contain natural language.
This aligns best with fields like title, description, summary, or abstract.
The model uses a context window of 1024 tokens and automatically chunks larger content.
Larger documents take longer to process, and inference time also increases the more documents are present in the reranking request.

## Further reading

The following blog posts provide additional background and context:

* [jina-embeddings-v5-omni for text, images, video, and audio](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index)
* [jina-embeddings-v5-text: Compact state-of-the-art text embeddings for search and intelligent applications](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text)
* [Jina rerankers bring fast, multilingual reranking to Elastic Inference Service (EIS)](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service)
* [jina-embeddings-v3 is now available on Elastic Inference Service](https://www.elastic.co/search-labs/blog/jina-embeddings-v3-elastic-inference-service)