---
navigation_title: Jina
description: Use Jina embedding, reranker, and reader models through Elastic Inference Service, Jina on-prem, or the Jina AI API.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Jina models [ml-nlp-jina]

Jina models are pretrained models for search and retrieval workflows. Use them to create embeddings for semantic and multimodal similarity search, rerank candidate results in hybrid search and retrieval-augmented generation (RAG), and extract structured content from HTML and complex documents before indexing.

You can use Jina models in the following ways:

* [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md): Elastic hosts Jina models and serves them through managed {{infer}} endpoints in your cluster. Use EIS for {{ech}}, {{serverless-short}}, or self-managed clusters with [Cloud Connect](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md) when you want managed inference without deploying or operating model infrastructure yourself.
* [Jina on-prem](ml-nlp-jina-on-prem.md): You run Jina models in Docker containers on your network using [jina-on-prem](https://github.com/jina-ai/jina-on-prem), and {{es}} connects to them through {{infer}} endpoints. Use on-prem when model inference must run on your own infrastructure, such as in restricted networks or environments with data residency requirements.
* [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md): {{es}} connects to the [Jina AI API](https://jina.ai/) through {{infer}} endpoints. Use this option for self-managed clusters that cannot use EIS or on-prem but have outbound network access to the Jina AI API, or when you are evaluating Jina models with a Jina API key before choosing a production deployment path.

## Model overview [jina-model-overview]

Jina models are organized by category. For model specifications and release history, refer to the [Jina model catalog](https://jina.ai/models#catalog).

Model availability varies by {{stack}} version. For models available through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) and version requirements, refer to [Elastic {{infer-cap}} Service supported models](/explore-analyze/elastic-inference/eis-supported-models.md). All models listed below are available through [Jina on-prem](ml-nlp-jina-on-prem.md).

**Text**

* [`jina-embeddings-v5-text-small`](#jina-embeddings-v5-text-small): Multilingual text embeddings with task-specific adapters. Text in, 1024-dimensional vectors out, 32K input token length.
* [`jina-embeddings-v5-text-nano`](#jina-embeddings-v5-text-nano): Multilingual embeddings for edge deployment. Text in, 768-dimensional vectors out, 8K input token length.
* [`jina-colbert-v2`](#jina-colbert-v2): Multilingual ColBERT for embedding and reranking. Text in, multi-vector embeddings out, 8K input token length.
* [`jina-embeddings-v3`](#jina-embeddings-v3): Multilingual text embeddings. Text in, 1024-dimensional vectors out, 8K input token length.

**Multimodal**

* [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small): Multimodal embeddings for text, image, audio, video, and PDF. Returns 1024-dimensional vectors, 32K input token length.
* [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano): Compact multimodal embeddings for edge deployment. Returns 768-dimensional vectors, 8K input token length.
* [`jina-clip-v2`](#jina-clip-v2): Multilingual multimodal embeddings for text and image. Text and image in, 1024-dimensional vectors out, 8K input token length.
* [`jina-vlm`](#jina-vlm): Vision-language model for visual question answering. Image and text in, text out, 32K input token length.

**Code**

* [`jina-code-embeddings-1.5b`](#jina-code-embeddings-1-5b): Code embeddings for semantic code search. Code text in, 1536-dimensional vectors out, 32K input token length.
* [`jina-code-embeddings-0.5b`](#jina-code-embeddings-0-5b): Compact code embeddings for edge deployment. Code text in, 896-dimensional vectors out, 32K input token length.

**Reader**

* [`ReaderLM-v2`](#readerlm-v2): Converts raw HTML into Markdown or JSON. HTML in, Markdown or JSON text out, 512K input token length.

**Reranker**

* [`jina-reranker-v3`](#jina-reranker-v3): Listwise reranker for multilingual document retrieval. Text queries and documents in, relevance rankings out, 131K input token length.
* [`jina-reranker-m0`](#jina-reranker-m0): Multimodal reranker for visual documents. Text or image queries and documents in, relevance rankings out, 10K input token length.
* [`jina-reranker-v2`](#jina-reranker-v2): Cross-encoder reranker for multilingual search. Text queries and documents in, relevance rankings out, 1K input token length.

## Multimodal embedding models [jina-multimodal-embeddings]

Multimodal embedding models convert text, images, video, audio, and documents such as PDF into vector embeddings in a shared vector space. {{es}} stores these vectors in [`dense_vector`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md) fields or through the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field and uses vector similarity search to retrieve the most relevant documents for a given query.

### Jina v5 omni embedding models [jina-embeddings-v5-omni]

{applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga`

The Jina v5 omni embedding models are multimodal dense vector embedding models. They turn text, images, video, audio, and documents such as PDF into vectors in one shared space. There are two Jina v5 omni embedding models available:

$$$jina-embeddings-v5-omni-small$$$ `jina-embeddings-v5-omni-small`
:   Multimodal embeddings for text, image, audio, video, and PDF. Accepts text, image, audio, video, and PDF input and returns 1024-dimensional vectors. Supports an input token length of 32K.
    For additional model specifications, refer to the [jina-embeddings-v5-omni-small model page](https://jina.ai/models/jina-embeddings-v5-omni-small/) in the Jina model catalog.

$$$jina-embeddings-v5-omni-nano$$$ `jina-embeddings-v5-omni-nano`
:   Compact multimodal embeddings for edge deployment. Accepts text, image, audio, video, and PDF input and returns 768-dimensional vectors. Supports an input token length of 8K.
    For additional model specifications, refer to the [jina-embeddings-v5-omni-nano model page](https://jina.ai/models/jina-embeddings-v5-omni-nano/) in the Jina model catalog.

#### Performance considerations [jina-omni-performance]

::::{tab-set}
:group: jina-omni

:::{tab-item} jina-embeddings-v5-omni-small
:sync: omni-small

- Use short video clips instead of long videos. Embeddings created from long videos are often less accurate for search because they try to represent too much content at once. Splitting videos into short clips or scenes improves retrieval quality.
- Image, video, and audio {{infer}} is typically more expensive than text alone. Batch and chunk content to control latency and cost.
- For long text fields: the model supports an input token length of 32K, but splitting very large passages into chunks often improves latency and per-chunk quality.

:::

:::{tab-item} jina-embeddings-v5-omni-nano
:sync: omni-nano

- Use short video clips instead of long videos. Embeddings created from long videos are often less accurate for search because they try to represent too much content at once. Splitting videos into short clips or scenes improves retrieval quality.
- Image, video, and audio {{infer}} is typically more expensive than text alone. Batch and chunk content to control latency and cost.
- `jina-embeddings-v5-omni-nano` works best on small, medium or large sized fields that contain natural language. For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
- Although the model supports an input token length of 8K, consider chunking very large fields to control latency and cost.
- Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
- The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

:::

::::

::::{note}
The Jina v5 omni models availability and the support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type depend on your {{stack}} version:

- {applies_to}`stack: ga 9.3+` In {{stack}} 9.3 and later, you can create endpoints and run multimodal `embedding` {{infer}} requests. You cannot use these models with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type.
- {applies_to}`stack: ga 9.4+` In {{stack}} 9.4 and later, you can use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) mappings for text-only embeddings at ingest and search time.
- {applies_to}`stack: ga 9.5+` In {{stack}} 9.5 and later, the `semantic_field` field type supports all modalities, such as text, images, video, audio, and documents.
::::

In the following examples, you can learn how to get started with Jina v5 omni embedding models on Elastic {{infer-cap}} Service (EIS).

Like all Jina models, these models are also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

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

### `jina-clip-v2` [jina-clip-v2]

[`jina-clip-v2`](https://jina.ai/models/jina-clip-v2/) provides multilingual multimodal embeddings for text and image. It accepts text and image input and returns 1024-dimensional vectors. It supports an input token length of 8K.

For additional model specifications, refer to the [jina-clip-v2 model page](https://jina.ai/models/jina-clip-v2/) in the Jina model catalog.

#### Getting started with `jina-clip-v2` through Elastic {{infer-cap}} Service

Create an {{infer}} endpoint that references the `jina-clip-v2` model in the `model_id` field.

```console
PUT _inference/text_embedding/eis-jina-clip-v2
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-clip-v2"
  }
}
```

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

### `jina-vlm` [jina-vlm]

[`jina-vlm`](https://jina.ai/models/jina-vlm/) is a multilingual vision-language model for visual question answering. It accepts image and text input and returns text output. It supports an input token length of 32K.

For additional model specifications, refer to the [jina-vlm model page](https://jina.ai/models/jina-vlm/) in the Jina model catalog.

#### Getting started with `jina-vlm` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

## Text embedding models [jina-text-embeddings]

Text embedding models convert text into vector embeddings, which are fixed-length numerical representations that capture semantic meaning. Texts with similar meaning are mapped to nearby points in vector space, so you can retrieve relevant documents with vector similarity search.

When you send text to an {{infer}} endpoint that uses an embedding model, the model returns a vector of floating-point numbers (for example, 1024 values). Unlike [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md), which expands text into sparse token-weight vectors, these models produce compact dense vectors that are well suited for multilingual and cross-domain use cases.

### `jina-embeddings-v5-text-small` [jina-embeddings-v5-text-small]

The [`jina-embeddings-v5-text-small`](https://jina.ai/models/jina-embeddings-v5-text-small/) model provides multilingual text embeddings with task-specific adapters. It accepts text input and returns 1024-dimensional vectors. It supports an input token length of 32K.

For additional model specifications, refer to the [jina-embeddings-v5-text-small model page](https://jina.ai/models/jina-embeddings-v5-text-small/) in the Jina model catalog.

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

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

#### Performance considerations [jina-embeddings-v5-text-small-performance]

* `jina-embeddings-v5-text-small` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports an input token length of 32K, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

### `jina-embeddings-v5-text-nano` [jina-embeddings-v5-text-nano]

The [`jina-embeddings-v5-text-nano`](https://jina.ai/models/jina-embeddings-v5-text-nano/) model provides multilingual embeddings for edge deployment. It accepts text input and returns 768-dimensional vectors. It supports an input token length of 8K.

For additional model specifications, refer to the [jina-embeddings-v5-text-nano model page](https://jina.ai/models/jina-embeddings-v5-text-nano/) in the Jina model catalog.

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

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

#### Performance considerations [jina-embeddings-v5-text-nano-performance]

* `jina-embeddings-v5-text-nano` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although the model supports an input token length of 8K, consider chunking very large fields to control latency and cost.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

### `jina-embeddings-v3` [jina-embeddings-v3]

The [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) model provides multilingual text embeddings. It accepts text input and returns 1024-dimensional vectors. It supports an input token length of 8K.

For additional model specifications, refer to the [jina-embeddings-v3 model page](https://jina.ai/models/jina-embeddings-v3/) in the Jina model catalog.

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

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

#### Performance considerations [jina-embeddings-v3-performance]

* `jina-embeddings-v3` works best on small, medium or large sized fields that contain natural language.
For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
Although `jina-embeddings-v3` supports an input token length of 8K, it's best to limit the input to 2048-4096 tokens for optimal performance.
For larger fields that exceed this limit - for example, `body_content` on web crawler documents - consider chunking the content into multiple values, where each chunk can be under 4096 tokens.
* Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
* The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

### `jina-colbert-v2` [jina-colbert-v2]

[`jina-colbert-v2`](https://jina.ai/models/jina-colbert-v2/) is a multilingual ColBERT model for embedding and reranking. It accepts text input and returns multi-vector embeddings (128 dimensions). It supports an input token length of 8K.

For additional model specifications, refer to the [jina-colbert-v2 model page](https://jina.ai/models/jina-colbert-v2/) in the Jina model catalog.

#### Getting started with `jina-colbert-v2` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

## Code embedding models [jina-code-embeddings]

Code embedding models convert source code and technical text into dense vectors optimized for code search, technical Q&A, and repository retrieval workflows.

### `jina-code-embeddings-1.5b` [jina-code-embeddings-1-5b]

[`jina-code-embeddings-1.5b`](https://jina.ai/models/jina-code-embeddings-1.5b/) provides code embeddings from code generation models. It accepts code text input and returns 1536-dimensional vectors. It supports an input token length of 32K.

For additional model specifications, refer to the [jina-code-embeddings-1.5b model page](https://jina.ai/models/jina-code-embeddings-1.5b/) in the Jina model catalog.

#### Getting started with `jina-code-embeddings-1.5b` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

### `jina-code-embeddings-0.5b` [jina-code-embeddings-0-5b]

[`jina-code-embeddings-0.5b`](https://jina.ai/models/jina-code-embeddings-0.5b/) provides compact code embeddings for edge deployment. It accepts code text input and returns 896-dimensional vectors. It supports an input token length of 32K.

For additional model specifications, refer to the [jina-code-embeddings-0.5b model page](https://jina.ai/models/jina-code-embeddings-0.5b/) in the Jina model catalog.

#### Getting started with `jina-code-embeddings-0.5b` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

## Reader models [jina-reader-models]

Reader models extract clean, structured content from HTML and complex documents. Use them to prepare web pages, PDFs, and other sources for indexing and RAG pipelines.

### `ReaderLM-v2` [readerlm-v2]

[`ReaderLM-v2`](https://jina.ai/models/ReaderLM-v2/) converts raw HTML into Markdown or JSON. It accepts HTML text input and returns Markdown or JSON text output. It supports an input token length of 512K.

For additional model specifications, refer to the [ReaderLM-v2 model page](https://jina.ai/models/ReaderLM-v2/) in the Jina model catalog.

#### Getting started with `ReaderLM-v2` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

## Rerankers [jina-rerankers]

Reranker models take a query and an already retrieved set of candidate documents, then reorders those candidates by predicted relevance.
Rerankers improve precision for the top query results.

### `jina-reranker-v3` [jina-reranker-v3]

[`jina-reranker-v3`](https://jina.ai/models/jina-reranker-v3/) is a listwise reranker for multilingual document retrieval. It accepts text queries and documents and returns relevance rankings. It supports an input token length of 131K.

:::{note}
`jina-reranker-v3.5` will replace `jina-reranker-v3` as the recommended reranker model. After the release, update your {{infer}} endpoints and on-prem deployments to use `jina-reranker-v3.5`.
:::

For additional model specifications, refer to the [jina-reranker-v3 model page](https://jina.ai/models/jina-reranker-v3/) in the Jina model catalog.

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

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

#### Performance considerations [jina-reranker-v3-performance]

`jina-reranker-v3` is designed for top-k reranking in hybrid search and RAG workflows.
For larger candidate sets, rerank the most relevant results returned by your first-stage retrieval.

### `jina-reranker-m0` [jina-reranker-m0]

[`jina-reranker-m0`](https://jina.ai/models/jina-reranker-m0/) is a multilingual multimodal reranker for ranking visual documents. It accepts text or image queries and text or image documents and returns relevance rankings. It supports an input token length of 10K.

For additional model specifications, refer to the [jina-reranker-m0 model page](https://jina.ai/models/jina-reranker-m0/) in the Jina model catalog.

#### Getting started with `jina-reranker-m0` on-prem

Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

### `jina-reranker-v2` [jina-reranker-v2]

[`jina-reranker-v2`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) is a cross-encoder reranker with multilingual, function calling, and code search support. It accepts text queries and documents and returns relevance rankings. It supports an input token length of 1K.

For additional model specifications, refer to the [jina-reranker-v2 model page](https://jina.ai/models/jina-reranker-v2-base-multilingual/) in the Jina model catalog.

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

Like all Jina models, this model is also available on-prem. Refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md) for deployment steps.

#### Performance considerations [jina-reranker-v2-performance]

`jina-reranker-v2` works best on small, medium or large sized fields that contain natural language.
This aligns best with fields like title, description, summary, or abstract.
The model supports an input token length of 1K and automatically chunks larger content.
Larger documents take longer to process, and {{infer}} time also increases the more documents are present in the reranking request.

## Pricing and licensing [jina-pricing-licensing]

How you are charged depends on how you deploy Jina models.

### Elastic Inference Service (EIS) [jina-pricing-eis]

Models used through EIS are billed per million tokens. For details, refer to [Pricing](/explore-analyze/elastic-inference/eis.md#pricing) and the [Elasticsearch Serverless pricing page](https://www.elastic.co/pricing/serverless-search).

To use Jina models on EIS, you must have the [appropriate subscription]({{subscriptions}}) level or the trial period activated.

### Jina on-prem [jina-pricing-on-prem]

Jina on-prem is a commercial offering. Pricing is based on a commercial license for self-hosted deployment, not on token usage through EIS. You run the models on your own infrastructure using Docker containers from jina-on-prem.

Many Jina models are licensed under CC-BY-NC-4.0. Commercial use in production requires an appropriate license from Elastic. For pricing and licensing details, contact your Elastic representative or refer to [Elastic subscriptions]({{subscriptions}}). For deployment steps, refer to [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md).

### External inference [jina-pricing-external]

If you use the Jina AI API, billing is handled by Jina AI.

## Further reading

The following blog posts provide additional background and context:

* [jina-embeddings-v5-text: Compact state-of-the-art text embeddings for search and intelligent applications](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text)
* [One index, all media: Introducing jina-embeddings-v5-omni](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index)
* [Jina rerankers bring fast, multilingual reranking to Elastic {{infer-cap}} Service (EIS)](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service)
* [jina-embeddings-v3 is now available on Elastic {{infer-cap}} Service](https://www.elastic.co/search-labs/blog/jina-embeddings-v3-elastic-inference-service)
* [Deploy Jina models on-prem](ml-nlp-jina-on-prem.md)
* [jina-on-prem Quick Start](https://github.com/jina-ai/jina-on-prem/wiki/Quick-Start)
* [Jina model catalog](https://jina.ai/models#catalog)