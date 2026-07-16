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

Jina models are pretrained models for search and retrieval workflows. You can use them to create embeddings for semantic and multimodal similarity search, rerank candidate results in hybrid search and retrieval-augmented generation (RAG), and extract structured content from HTML and complex documents before indexing.

You can deploy Jina models in the following ways:

* [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md): Elastic hosts Jina models and serves them through managed {{infer}} endpoints in your cluster, so you can run inference without deploying or managing model infrastructure.
* [Jina on-prem](#jina-on-prem): You run Jina models in Docker containers on your network using [Jina on-prem](https://github.com/jina-ai/jina-on-prem), and {{es}} connects to them through {{infer}} endpoints. Using on-prem means you do not send data to a third-party API, inference makes no outbound network calls, and models run on your own infrastructure.
* [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md): {{es}} connects to the [Jina AI API](https://jina.ai/) through {{infer}} endpoints, so you can call models hosted by Jina with your own API key. 

## Model overview [jina-model-overview]

The following tables list the available Jina models, provide a brief description of each model, and show the supported deployment types. Select a deployment type to view the corresponding setup and usage instructions.

::::{note}
For models accessed through [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), availability may vary by Stack version. For supported models and version requirements, refer to [Elastic {{infer-cap}} Service supported models](/explore-analyze/elastic-inference/eis-supported-models.md).
::::

### Text embedding models [jina-text-embeddings]

Text embedding models convert text into vector embeddings for semantic similarity search. 

| Model | Description | Deployment |
| --- | --- | --- |
| [`jina-embeddings-v5-text-small`](https://jina.ai/models/jina-embeddings-v5-text-small/) | Multilingual text embeddings with task-specific adapters. Accepts text input and produces 1024-dimensional vector embeddings. Supports input lengths up to 32K tokens. | [EIS](#jina-eis-text-embedding), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-embeddings-v5-text-nano`](https://jina.ai/models/jina-embeddings-v5-text-nano/) | Multilingual embeddings for edge deployment. Accepts text input and produces 768-dimensional vector embeddings. Supports input lengths up to 8K tokens. | [EIS](#jina-eis-text-embedding), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-embeddings-v3`](https://jina.ai/models/jina-embeddings-v3/) | Multilingual text embeddings. Accepts text input and produces 1024-dimensional vector embeddings. Supports input lengths up to 8K tokens. | [EIS](#jina-eis-text-embedding), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-colbert-v2`](https://jina.ai/models/jina-colbert-v2/) | Multilingual ColBERT model for embedding and reranking. Accepts text input and produces 128-dimensional multi-vector embeddings. Supports input lengths up to 8K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |

### Multimodal embedding models [jina-multimodal-embeddings]

Multimodal embedding models convert text, images, video, audio, and documents such as PDF into vector embeddings in a shared vector space. 

| Model | Description | Deployment |
| --- | --- | --- |
| [`jina-embeddings-v5-omni-small`](https://jina.ai/models/jina-embeddings-v5-omni-small/) | Multimodal embeddings for text, image, audio, video, and PDF. Accepts multimodal input and produces 1024-dimensional vector embeddings. Supports input lengths up to 32K tokens. | [EIS](#jina-omni-getting-started), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-embeddings-v5-omni-nano`](https://jina.ai/models/jina-embeddings-v5-omni-nano/) | Compact multimodal embeddings for edge deployment. Accepts multimodal input and produces 768-dimensional vector embeddings. Supports input lengths up to 8K tokens. | [EIS](#jina-omni-getting-started), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-clip-v2`](https://jina.ai/models/jina-clip-v2/) | Multilingual multimodal embeddings for text and image retrieval. Accepts text and image input and produces 1024-dimensional vector embeddings. Supports input lengths up to 8K tokens. | [EIS](#jina-omni-getting-started), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-embeddings-v4`](https://jina.ai/models/jina-embeddings-v4/) | Universal multimodal embeddings for text, image, and PDF retrieval. Accepts text, image, and PDF input and produces 2048-dimensional vector embeddings. Supports input lengths up to 32K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-vlm`](https://jina.ai/models/jina-vlm/) | Vision-language model for visual question answering. Accepts image and text input and generates text output. Supports input lengths up to 32K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |

### Code embedding models [jina-code-embeddings]

Code embedding models convert source code and technical text into dense vectors for code search, technical Q&A, and repository retrieval.

| Model | Description | Deployment |
| --- | --- | --- |
| [`jina-code-embeddings-1.5b`](https://jina.ai/models/jina-code-embeddings-1.5b/) | Code embeddings built on code generation models. Accepts source code and technical text and produces 1536-dimensional vector embeddings. Supports input lengths up to 32K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-code-embeddings-0.5b`](https://jina.ai/models/jina-code-embeddings-0.5b/) | Compact code embeddings for edge deployment. Accepts source code and technical text and produces 896-dimensional vector embeddings. Supports input lengths up to 32K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |

### Reader models [jina-reader-models]

Reader models extract clean, structured content from HTML and complex documents for indexing and RAG pipelines.

| Model | Description | Deployment |
| --- | --- | --- |
| [`ReaderLM-v2`](https://jina.ai/models/ReaderLM-v2/) | Converts raw HTML into Markdown or JSON. Accepts HTML input and generates Markdown or JSON output. Supports input lengths up to 512K tokens. | [On-prem](#jina-on-prem) |

### Rerankers [jina-rerankers]

Reranker models reorder candidate documents by predicted relevance to improve top query results.

| Model | Description | Deployment |
| --- | --- | --- |
| [`jina-reranker-v3`](https://jina.ai/models/jina-reranker-v3/) | Listwise reranker for multilingual document retrieval. Accepts text queries and documents and returns relevance rankings. Supports input lengths up to 131K tokens. | [EIS](#jina-eis-rerank), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-reranker-m0`](https://jina.ai/models/jina-reranker-m0/) | Multimodal reranker for visual documents. Accepts text or image queries and documents and returns relevance rankings. Supports input lengths up to 10K tokens. | [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |
| [`jina-reranker-v2-base-multilingual`](https://jina.ai/models/jina-reranker-v2-base-multilingual/) | Cross-encoder reranker for multilingual search. Accepts text queries and documents and returns relevance rankings. Supports input lengths up to 1K tokens. | [EIS](#jina-eis-rerank), [On-prem](#jina-on-prem), [External {{infer}}](docs-content://explore-analyze/elastic-inference/external.md) |

## Use models with Elastic {{infer-cap}} Service (EIS) [jina-eis-getting-started]

With [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md), Elastic hosts Jina models and serves them through managed {{infer}} endpoints in your cluster. Use this option when you want GPU-accelerated inference without deploying or managing model infrastructure.

To use a model through EIS, create an {{infer}} endpoint with `"service": "elastic"` and set `model_id` to the name of the model you want to use.

### Text embedding models [jina-eis-text-embedding]

The following examples use the `text_embedding` task type. Create an {{infer}} endpoint and reference the `inference_id` in `text_embedding` {{infer}} tasks or search queries:

::::{tab-set}
:group: jina-text-embeddings

:::{tab-item} jina-embeddings-v5-text-small
:sync: text-small

```console
PUT _inference/text_embedding/eis-jina-embeddings-v5-text-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-text-small"
  }
}
```

```console
POST _inference/text_embedding/eis-jina-embeddings-v5-text-small
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

:::

:::{tab-item} jina-embeddings-v5-text-nano
:sync: text-nano

```console
PUT _inference/text_embedding/eis-jina-embeddings-v5-text-nano
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-text-nano"
  }
}
```

```console
POST _inference/text_embedding/eis-jina-embeddings-v5-text-nano
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

:::

:::{tab-item} jina-embeddings-v3
:sync: text-v3

```console
PUT _inference/text_embedding/eis-jina-embeddings-v3
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v3"
  }
}
```

```console
POST _inference/text_embedding/eis-jina-embeddings-v3
{
  "input": "The sky above the port was the color of television tuned to a dead channel.",
  "input_type": "ingest"
}
```

:::

::::

### Multimodal embedding models [jina-omni-getting-started]

{applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga`

The following examples use the `embedding` task type.

Create an {{infer}} endpoint. The URL path uses the `embedding` task type and ends with the `inference_id` you want to use:

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

:::{tab-item} jina-clip-v2
:sync: clip-v2

```console
PUT _inference/embedding/eis-jina-clip-v2
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-clip-v2"
  }
}
```

:::

::::

Reference the `inference_id` in `embedding` {{infer}} requests or search queries.

Below are examples of ingesting different types of content and generating vector embeddings using the `inference_id` created in the earlier request. The omni models support text, images, audio, video, and PDF documents. `jina-clip-v2` supports text and image input only.

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

:::{tab-item} jina-clip-v2
:sync: clip-v2

```console
POST _inference/embedding/eis-jina-clip-v2
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

:::{tab-item} jina-clip-v2
:sync: clip-v2

```console
POST _inference/embedding/eis-jina-clip-v2
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

::::{note}
The Jina v5 omni models availability and the support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type depend on your {{stack}} version:

- {applies_to}`stack: ga 9.3+` In {{stack}} 9.3 and later, you can create endpoints and run multimodal `embedding` {{infer}} requests. You cannot use these models with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type.
- {applies_to}`stack: ga 9.4+` In {{stack}} 9.4 and later, you can use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) mappings for text-only embeddings at ingest and search time.
- {applies_to}`stack: ga 9.5+` In {{stack}} 9.5 and later, the `semantic_field` field type supports all modalities, such as text, images, video, audio, and documents.
::::

### Reranker models [jina-eis-rerank]

The following examples use the `rerank` task type. Create an {{infer}} endpoint and reference the `inference_id` in `rerank` {{infer}} tasks:

::::{tab-set}
:group: jina-rerankers

:::{tab-item} jina-reranker-v3
:sync: reranker-v3

```console
PUT _inference/rerank/eis-jina-reranker-v3
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-reranker-v3"
  }
}
```

```console
POST _inference/rerank/eis-jina-reranker-v3
{
  "input": ["The Swiss Alps", "a steep hill", "a pebble", "a glacier"],
  "query": "mountain range"
}
```

:::

:::{tab-item} jina-reranker-v2-base-multilingual
:sync: reranker-v2

```console
PUT _inference/rerank/jina-reranker-v2-base-multilingual
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-reranker-v2-base-multilingual"
  }
}
```

```console
POST _inference/rerank/jina-reranker-v2-base-multilingual
{
  "input": ["luke", "like", "leia", "chewy", "r2d2", "star", "wars"],
  "query": "star wars main character"
}
```

:::

::::

## Deploy Jina models on-prem [jina-on-prem]

With [Jina on-prem](https://github.com/jina-ai/jina-on-prem), you run Jina models in Docker containers on your own infrastructure. Use this option when data cannot leave your network, when inference must work without outbound connectivity, or when compliance and data residency require self-hosted model deployment.

To pull, transfer, and run a prebuilt Docker image, refer to the [Jina on-prem Quick Start](https://github.com/jina-ai/jina-on-prem/wiki/Quick-Start).

To connect {{es}} to a local Jina on-prem server, create {{infer}} endpoints that call the APIs exposed by the container. 

For an embedding model, create a `text_embedding` endpoint:

```console
PUT _inference/text_embedding/jina-embed
{
  "service": "openai", <1>
  "service_settings": {
    "url": "http://embed-host:8080/v1/embeddings", <2>
    "model_id": "jina-embeddings-v5-text-small", <3>
    "api_key": "not-needed" <4>
  }
}
```

1. Use the `openai` service type so {{es}} sends OpenAI-compatible `text_embedding` requests. 
2. Point `url` to the `/v1/embeddings` endpoint on your Jina on-prem host.
3. Set `model_id` to the embedding model running in the container.
4. This field is required by the {{es}} {{infer}} API but is not used by Jina on-prem. Specify any placeholder string, such as not-needed.

For a reranker model, create a `rerank` endpoint:

```console
PUT _inference/rerank/jina-rerank
{
  "service": "cohere", <1>
  "service_settings": {
    "url": "http://rerank-host:8081/v1/rerank", <2>
    "model_id": "jina-reranker-v3", <3>
    "api_key": "not-needed" <4>
  }
}
```

1. Use the `cohere` service type so {{es}} sends Cohere-compatible rerank requests. Jina on-prem exposes this schema locally. Requests do not go to Cohere.
2. Point `url` to the `/v1/rerank` endpoint on your Jina on-prem host.
3. Set `model_id` to the reranker model running in the container.
4. This field is required by the {{es}} {{infer}} API but is not used by Jina on-prem. Specify any placeholder string, such as not-needed.

You can reference the `inference_id` of these endpoints in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, {{infer}} processors, or search queries.

For more endpoint configuration examples, refer to the [Jina on-prem API reference](https://github.com/jina-ai/jina-on-prem/wiki/API-Reference#elasticsearch-integration).

## Performance considerations [jina-performance]

### Text embedding models [jina-text-embeddings-performance]

::::{tab-set}
:group: jina-text-embeddings

:::{tab-item} jina-embeddings-v5-text-small
:sync: text-small

- `jina-embeddings-v5-text-small` works best on small, medium or large sized fields that contain natural language. For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
- Although the model supports an input token length of 32K, consider chunking very large fields to control latency and cost.
- Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
- The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

:::

:::{tab-item} jina-embeddings-v5-text-nano
:sync: text-nano

- `jina-embeddings-v5-text-nano` works best on small, medium or large sized fields that contain natural language. For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
- Although the model supports an input token length of 8K, consider chunking very large fields to control latency and cost.
- Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
- The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

:::

:::{tab-item} jina-embeddings-v3
:sync: text-v3

- `jina-embeddings-v3` works best on small, medium or large sized fields that contain natural language. For connector or web crawler use cases, this aligns best with fields like title, description, summary, or abstract.
- Although `jina-embeddings-v3` supports an input token length of 8K, it's best to limit the input to 2048-4096 tokens for optimal performance. For larger fields that exceed this limit - for example, `body_content` on web crawler documents - consider chunking the content into multiple values, where each chunk can be under 4096 tokens.
- Larger documents take longer at ingestion time, and {{infer}} time per document also increases the more fields in a document that need to be processed.
- The more fields your pipeline has to perform {{infer}} on, the longer it takes per document to ingest.

:::

::::

### Multimodal embedding models [jina-omni-performance]

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

### Reranker models [jina-rerankers-performance]

::::{tab-set}
:group: jina-rerankers

:::{tab-item} jina-reranker-v3
:sync: reranker-v3

- `jina-reranker-v3` is designed for top-k reranking in hybrid search and RAG workflows.
- For larger candidate sets, rerank the most relevant results returned by your first-stage retrieval.

:::

:::{tab-item} jina-reranker-v2-base-multilingual
:sync: reranker-v2

- `jina-reranker-v2-base-multilingual` works best on small, medium or large sized fields that contain natural language. This aligns best with fields like title, description, summary, or abstract.
- The model supports an input token length of 1K and automatically chunks larger content.
- Larger documents take longer to process, and {{infer}} time also increases the more documents are present in the reranking request.

:::

::::

## Pricing and licensing [jina-pricing-licensing]

How you are charged depends on how you deploy Jina models.

- Models used through EIS are billed per million tokens. For details, refer to [Pricing](/explore-analyze/elastic-inference/eis.md#pricing) and the [Elasticsearch Serverless pricing page](https://www.elastic.co/pricing/serverless-search). To use Jina models on EIS, you must have the [appropriate subscription]({{subscriptions}}) level or the trial period activated.

- Jina on-prem is a commercial offering. Pricing is based on a commercial license for self-hosted deployment, not on token usage. Commercial use in production requires an appropriate license from Elastic. For pricing and licensing details, refer to [Elastic subscriptions]({{subscriptions}}). 


## Further reading

For more background and related resources:

* [jina-embeddings-v5-text](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-text): Introduces the compact multilingual text embedding models (`small` and `nano`) and how to use them on EIS.
* [jina-embeddings-v5-omni](https://www.elastic.co/search-labs/blog/jina-embeddings-v5-omni-all-media-one-index): Explains how to embed text, images, video, and audio into a single Elasticsearch index.
* [Jina rerankers on EIS](https://www.elastic.co/search-labs/blog/jina-rerankers-elastic-inference-service): Covers `jina-reranker-v2-base-multilingual` and `jina-reranker-v3` for multilingual reranking in retrieval and RAG workflows.
* [jina-embeddings-v3 on EIS](https://www.elastic.co/search-labs/blog/jina-embeddings-v3-elastic-inference-service): Introduces multilingual dense retrieval with `jina-embeddings-v3` on EIS.
* [Jina model catalog](https://jina.ai/models#catalog): Browse the full set of Jina Search Foundation models and their capabilities.