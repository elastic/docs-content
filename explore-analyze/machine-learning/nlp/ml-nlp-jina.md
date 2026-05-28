---
navigation_title: Jina
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Jina models [ml-nlp-jina]

:::{note}
Jina models are currently available only through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) or [external {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) providers. Since these models rely on external connectivity, they cannot currently be deployed on [{{ml}} nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#ml-node-role) and are not compatible with fully air-gapped environments.
:::

This page collects all Jina models you can use as part of the {{stack}}.

Currently, the following models are available as built-in models:

**Embedding models**

* [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small): multimodal (text, image, audio, video, PDF)
* [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano): multimodal (text, image, audio, video, PDF)
* [`jina-embeddings-v5-text-small`](#jina-embeddings-v5-text-small): text-only
* [`jina-embeddings-v5-text-nano`](#jina-embeddings-v5-text-nano): text-only
* [`jina-embeddings-v3`](#jina-embeddings-v3): text-only

**Rerankers**

* [`jina-reranker-v3`](#jina-reranker-v3)
* [`jina-reranker-v2`](#jina-reranker-v2)

:::{note}
Jina model availability varies by {{stack}} version. Refer to the [Elastic {{infer-cap}} Service supported models: embedding models](/explore-analyze/elastic-inference/eis-supported-models.md#embedding-models) table for details.
:::

## Embedding models

Embedding models convert text into vector embeddings, which are fixed-length numerical representations that capture semantic meaning.
Texts with similar meaning are mapped to nearby points in vector space, so you can retrieve relevant documents with vector similarity search.

When you send text to an EIS {{infer}} endpoint that uses an embedding model, the model returns a vector of floating-point numbers (for example, 1024 values). {{es}} stores these vectors in [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) fields or through the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field and uses vector similarity search to retrieve the most relevant documents for a given query. Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, these models produce compact dense vectors that are well suited for multilingual and cross-domain use cases. Multimodal models embed text, images, video, audio, and documents such as PDF into the same vector space so you can index and query across media types together.

### Jina v5 omni embedding models [jina-embeddings-v5-omni]

{applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga`

::::{note}
The Jina v5 omni models availability and the support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type depend on your {{stack}} version:

- {applies_to}`stack: ga 9.3+` In {{stack}} 9.3 and later, you can create endpoints and run multimodal `embedding` {{infer}} requests. You cannot use these models with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type.
- {applies_to}`stack: ga 9.4+` In {{stack}} 9.4 and later, you can use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) mappings for text-only embeddings at ingest and search time.
- {applies_to}`stack: ga 9.5+` In {{stack}} 9.5 and later, the `semantic_field` field type supports all modalities, such as text, images, video, audio, and documents.
::::

The Jina v5 omni embedding models are multimodal dense vector embedding models available through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md). They turn text, images, video, audio, and documents such as PDF into vectors in one shared space. There are two Jina v5 omni embedding models available:

$$$jina-embeddings-v5-omni-small$$$ `jina-embeddings-v5-omni-small`
:   Has 700M parameters, supports a 32768 token input context window, and produces 1024-dimension embeddings.

$$$jina-embeddings-v5-omni-nano$$$ `jina-embeddings-v5-omni-nano`
:   Has 266M parameters, supports up to an 8192-token text context window, and produces 768-dimensional vectors.

For more information, refer to the [Elastic blog post](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index), the [model card](https://huggingface.co/jinaai/jina-embeddings-v5-omni-small) on Hugging Face, or the [model collection](https://huggingface.co/collections/jinaai/jina-embeddings-v5-omni).

#### Requirements [jina-embeddings-v5-omni-small-req]

To use `jina-embeddings-v5-omni-small` and `jina-embeddings-v5-omni-nano`, you must have the [appropriate subscription]({{subscriptions}}) level or the trial period activated.

#### Performance considerations [jina-omni-performance]

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

- Use short video clips instead of long videos. Embeddings created from long videos are often less accurate for search because they try to represent too much content at once. Splitting videos into short clips or scenes improves retrieval quality.
- Image, video, and audio {{infer}} is typically more expensive than text alone. Batch and chunk content to control latency and cost.
- For long text fields: the model accepts up to a 32768 token context window, but splitting very large passages into chunks often improves latency and per-chunk quality.

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

- Use short video clips instead of long videos. Embeddings created from long videos are often less accurate for search because they try to represent too much content at once. Splitting videos into short clips or scenes improves retrieval quality.
- Image, video, and audio {{infer}} is typically more expensive than text alone. Batch and chunk content to control latency and cost.
- `jina-embeddings-v5-omni-nano` works best on small, medium or large sized fields that contain natural language. For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
- Although the model supports an 8192 token context window, consider chunking very large fields to control latency and cost.
- Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
- The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

:::

::::

#### Getting started with Jina v5 omni embedding models through Elastic {{infer-cap}} Service [jina-omni-getting-started]

This request creates a new {{infer}} endpoint. The URL path uses the `embedding` task type and ends with the `inference_id` you want to use.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-small"
  }
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-nano"
  }
}
```

:::

::::

Reference the `inference_id` in `embedding` {{infer}} requests or search queries on any supported version.

Below are examples of ingesting different types of content and generating vector embeddings for text, images, audio, video, and PDF documents using the `inference_id` created in the earlier request.

##### Text as a JSON array

Pass one or more plain text strings in the `input` array.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    "A small blue square"
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    "A small blue square"
  ]
}
```

:::

::::

##### Text and image fused into one embedding

List both a `text` entry and a base64 `image` entry inside `content` so the model produces one embedding that represents the combined multimodal input.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        {
          "type": "text",
          "value": "A small blue square"
        },
        {
          "type": "image",
          "format": "base64",
          "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
        }
      ]
    }
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    {
      "content": [
        {
          "type": "text",
          "value": "A small blue square"
        },
        {
          "type": "image",
          "format": "base64",
          "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
        }
      ]
    }
  ]
}
```

:::

::::

##### Image only (base64-encoded image bytes)

Use a single `image` block when the input contains only image data.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        {
          "type": "image",
          "format": "base64",
          "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
        }
      ]
    }
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    {
      "content": [
        {
          "type": "image",
          "format": "base64",
          "value": "data:image/png;base64,<BASE64_IMAGE_DATA>"
        }
      ]
    }
  ]
}
```

:::

::::

##### Video only (base64-encoded video bytes)

Encode a short video clip as base64. Short video clips usually produce more accurate embeddings for search than creating a single embedding from a longer video.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        {
          "type": "video",
          "format": "base64",
          "value": "data:video/mp4;base64,<BASE64_VIDEO_DATA>"
        }
      ]
    }
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    {
      "content": [
        {
          "type": "video",
          "format": "base64",
          "value": "data:video/mp4;base64,<BASE64_VIDEO_DATA>"
        }
      ]
    }
  ]
}
```

:::

::::

##### Audio only (base64-encoded audio bytes)

Use this pattern for speech, music, or other audio you have already read and base64-encoded.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        {
          "type": "audio",
          "format": "base64",
          "value": "data:audio/wav;base64,<BASE64_AUDIO_DATA>"
        }
      ]
    }
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    {
      "content": [
        {
          "type": "audio",
          "format": "base64",
          "value": "data:audio/wav;base64,<BASE64_AUDIO_DATA>"
        }
      ]
    }
  ]
}
```

:::

::::

##### PDF or other supported documents (base64-encoded file bytes)

Use the document block with base64-encoded files, such as PDFs, to create document embeddings.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "input": [
    {
      "content": [
        {
          "type": "pdf",
          "format": "base64",
          "value": "data:application/pdf;base64,<BASE64_PDF_DATA>"
        }
      ]
    }
  ]
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
POST _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "input": [
    {
      "content": [
        {
          "type": "pdf",
          "format": "base64",
          "value": "data:application/pdf;base64,<BASE64_PDF_DATA>"
        }
      ]
    }
  ]
}
```

:::

::::

##### Custom endpoint with truncated embedding dimensions (Matryoshka-style output size)

You can create another endpoint with a smaller `dimensions` value if you want shorter vectors from the same model. Smaller vectors, such as 32 dimensions, can reduce storage usage and improve search speed.

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

```console
PUT _inference/embedding/jina-omni-small-32d
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-small",
    "dimensions": 32
  }
}
```

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

```console
PUT _inference/embedding/jina-omni-nano-32d
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-nano",
    "dimensions": 32
  }
}
```

:::

::::

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

[`jina-reranker-v2`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) is a multilingual cross-encoder model that helps you to improve search relevance across over 100 languages and various data types. The model significantly improves information retrieval in multilingual environments. `jina-reranker-v2` is available out-of-the-box and supports Elastic deployments using the {{es}} {{infer-cap}} API. You can use the model to improve existing search applications like hybrid semantic search, retrieval augmented generation (RAG), and more. You can use the model through Elastic {{infer-cap}} Service (EIS), Elastic's own infrastructure, without the need of managing infrastructure and model resources.

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
Larger documents take longer to process, and {{infer}} time also increases the more documents are present in the reranking request.

## Further reading

The following blog posts provide additional background and context:

* [jina-embeddings-v5-text: Compact state-of-the-art text embeddings for search and intelligent applications](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text)
* [One index, all media: Introducing jina-embeddings-v5-omni](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index)
* [Jina rerankers bring fast, multilingual reranking to Elastic {{infer-cap}} Service (EIS)](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service)
* [jina-embeddings-v3 is now available on Elastic {{infer-cap}} Service](https://www.elastic.co/search-labs/blog/jina-embeddings-v3-elastic-inference-service)