---
navigation_title: Default endpoints, adaptive allocations, and chunking
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/inference-endpoints.html
applies_to:
  stack:
  serverless:
products:
  - id: kibana
---
# Default {{infer}} endpoints, adaptive allocations, and chunking

{{es}} provides a machine learning [{{infer}} API]({{es-apis}}group/endpoint-inference) to create and manage {{infer}} endpoints that integrate with services such as {{es}} (for built-in NLP models like [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) and [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md)), as well as  popular third-party services like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

You can use the default {{infer}} endpoints your deployment contains or create a new {{infer}} endpoint using the [create an {{infer}} endpoint API]({{es-apis}}operation/operation-inference-put).
Alternatively, you can use [EIS](/explore-analyze/elastic-inference/eis.md) or [External {{infer}}](/explore-analyze/elastic-inference/external.md) apps in {{kib}}.

## Default {{infer}} endpoints [default-enpoints]

Your {{es}} deployment contains preconfigured {{infer}} endpoints, which makes them easier to use when defining `semantic_text` fields or using {{infer}} processors. These endpoints come in two forms:

- **Elastic Inference Service (EIS) endpoints**, which provide {{infer}} as a managed service and do not consume resources from your own nodes.

- **ML node-based endpoints**, which run on your dedicated {{ml}} nodes.

The following section lists the default {{infer}} endpoints, identified by their `inference_id`, grouped by whether they are EIS- or ML node–based.

### Default endpoints for Elastic {{infer-cap}} Service (EIS)

- `.elser-2-elastic`: uses the [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) trained model as an Elastic {{infer-cap}} Service for `sparse_embedding` tasks (recommended for English language text). The `model_id` is `.elser_model_2`. {applies_to}`stack: preview 9.1` {applies_to}`self: unavailable` {applies_to}`serverless: preview`

For more information, refer to [](/explore-analyze/elastic-inference/eis-supported-models.md).

### Default endpoints used on ML-nodes

- `.elser-2-elasticsearch`: uses the [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) built-in trained model for `sparse_embedding` tasks (recommended for English language text). The `model_id` is `.elser_model_2_linux-x86_64`.
- `.multilingual-e5-small-elasticsearch`: uses the [E5](../../explore-analyze/machine-learning/nlp/ml-nlp-e5.md) built-in trained model for `text_embedding` tasks (recommended for non-English language texts). The `model_id` is `.e5_model_2_linux-x86_64`.

Use the `inference_id` of the endpoint in a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field definition or when creating an [{{infer}} processor](elasticsearch://reference/enrich-processor/inference-processor.md). The API call will automatically download and deploy the model which might take a couple of minutes. Default {{infer}} endpoints have adaptive allocations enabled. For these models, the minimum number of allocations is `0`. If there is no {{infer}} activity that uses the endpoint, the number of allocations will scale down to `0` automatically after 15 minutes.

For an end-to-end tutorial on using {{infer}} endpoints with `semantic_text` fields, refer to [Semantic search with `semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md).

## Adaptive allocations [adaptive-allocations]

Adaptive allocations allow {{infer}} services to dynamically adjust the number of model allocations based on the current load.
This feature is only supported for models deployed in Elastic's infrastructure, such as ELSER, E5, or models uploaded through Eland. It is not available for models used through the Elastic {{infer-cap}} Service (EIS) and third-party services (for example, Alibaba Cloud, Cohere, or OpenAI), because those models are not deployed within your Elasticsearch cluster.

When adaptive allocations are enabled:

- The number of allocations scales up automatically when the load increases.
- Allocations scale down to a minimum of 0 when the load decreases, saving resources.

### Allocation scaling behavior

The behavior of allocations depends on several factors:

- Deployment type (Elastic Cloud Hosted, Elastic Cloud Enterprise, or Serverless)
- Usage level (low, medium, or high)
- Optimization type ([ingest](/deploy-manage/autoscaling/trained-model-autoscaling.md#ingest-optimized) or [search](/deploy-manage/autoscaling/trained-model-autoscaling.md#search-optimized))

::::{important}
If you enable adaptive allocations and set the `min_number_of_allocations` to a value greater than `0`, you will be charged for the machine learning resources, even if no inference requests are sent.

However, setting the `min_number_of_allocations` to a value greater than `0` keeps the model always available without scaling delays. Choose the configuration that best fits your workload and availability needs.
::::

For more information about adaptive allocations and resources, refer to the [trained model autoscaling](/deploy-manage/autoscaling/trained-model-autoscaling.md) documentation.

## Configuring chunking [infer-chunking-config]

Chunking is the process of splitting input text into smaller pieces, which is typically required in these situations:

* When sending input text to an {{infer}} endpoint. These endpoints have a limit on the amount of text they can ingest at once, determined by the model's input capacity. Splitting text into several chunks helps meet these limits, particularly when documents are ingested into [`semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md). 
* When showing search results to a human. In general, a human is only interested in a specific piece of text that answers their search query. As such, returning a chunk containing the answer to the query is more effective compared to returning a long document.

:::{note}

All chunks always include the text subpassage to which they belong and the corresponding embedding.

:::

By default, documents are split into sentences and grouped in sections up to 250 words with 1 sentence overlap so that each chunk shares a sentence with the previous chunk. Overlapping ensures continuity and prevents vital contextual information in the input text from being lost by a hard break.

{{es}} uses the [ICU4J](https://unicode-org.github.io/icu/userguide/icu4j/) library to detect word and sentence boundaries for chunking. [Word boundaries](https://unicode-org.github.io/icu/userguide/boundaryanalysis/#word-boundary) are identified by following a series of rules, which include detecting the presence of a whitespace character. For written languages that do not use whitespace, such as Chinese or Japanese, dictionary lookups are used to detect word boundaries.

### Chunking strategies

You can use the following strategies to chunk text. For a quick reference on how these strategies differ, consult the below table.

| Strategy | How it works | When to use | When not to use |
|---|---|---|---|
| [`sentence`](#sentence) | Splits at sentence boundaries | Building RAG systems on structured text | Splitting unpunctuated text |
| [`word`](#word) | Splits on individual words | Splitting logs and/or chats | When chunks have to be shown to a human |
| [`recursive`](#recursive) + [`plaintext`](#plaintext) | Splits on paragraph breaks | Splitting plain text with clear paragraphs (e.g., books) | Splitting one-line text scraped from raw HTML |
| [`recursive`](#recursive) + [`markdown`](#markdown) | Splits at Markdown headings and other separators | Ingesting documentation and knowledge bases | Splitting non-Markdown text |
| [`recursive`](#recursive) + [custom separators](#custom-separators) | Splits on regular expression patterns you define, applied in order | Ingesting AsciiDoc | Splitting Markdown or plain text |
| [`none`](#none) | Does not split text (pre-chunking is possible) | Consuming short text, where chunking is unnecessary | Any use case when exceeding a model's input capacity is possible |


#### `sentence`

The `sentence` strategy splits the input text at sentence boundaries. Each chunk contains one or more complete sentences ensuring that the integrity of sentence-level context is preserved, except when a sentence causes a chunk to exceed a word count of `max_chunk_size`, in which case it will be split across chunks. The `sentence_overlap` option defines the number of sentences from the previous chunk to include in the current chunk which is either `0` or `1`.

::::{admonition} Example of chunking

:::{dropdown} Complete example with `max_chunk_size: 20` 

Text:

```
S1  Elasticsearch stores data in indices.        (5 words)
S2  Each index is divided into shards.           (6)
S3  Shards are distributed across nodes.         (5)
S4  This distribution enables horizontal scaling.(5)
S5  Replicas provide redundancy.                 (3)
```

With `sentence_overlap: 0`:

```
Chunk 1: S1 S2 S3          (16 words)
Chunk 2: S4 S5             (8 words)
```

With `sentence_overlap: 1`:

```
Chunk 1: S1 S2 S3          (16 words)
Chunk 2: S3 S4 S5          (13 words)
```

:::

::::

The following example creates an {{infer}} endpoint with the `elasticsearch` service that deploys the ELSER model and configures the chunking behavior with the `sentence` strategy.

```console
PUT _inference/sparse_embedding/sentence_chunks
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "sentence",
    "max_chunk_size": 100,
    "sentence_overlap": 0
  }
}
```

The default chunking strategy is `sentence`.

#### `word`

The `word` strategy splits the input text on individual words up to the `max_chunk_size` limit. The `overlap` option is the number of words from the previous chunk to include in the current chunk.

::::{admonition} Example of chunking

:::{dropdown} Complete example with `max_chunk_size: 20` 

Text:

```
1 Elasticsearch        7 index        13 are           19 enables
2 stores          8 is           14 distributed   20 horizontal
3 data            9 divided      15 across        21 scaling.
4 in             10 into         16 nodes.        22 Replicas
5 indices.       11 shards.      17 This          23 provide
6 Each           12 Shards       18 distribution  24 redundancy.
```

With `overlap: 0`:

```
Chunk 1: words 1–20   Elasticsearch stores data in indices. Each index is divided
                      into shards. Shards are distributed across nodes. This
                      distribution enables horizontal
Chunk 2: words 21–24  scaling. Replicas provide redundancy.
```

With `overlap: 5`:

```
Chunk 1: words 1–20   ...This distribution enables horizontal
Chunk 2: words 16–24  nodes. This distribution enables horizontal scaling.
                      Replicas provide redundancy.
```

:::

::::

The following example creates an {{infer}} endpoint with the `elasticsearch` service that deploys the ELSER model and configures the chunking behavior with the `word` strategy, setting a maximum of 120 words per chunk and an overlap of 40 words between chunks.

```console
PUT _inference/sparse_embedding/word_chunks
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "word",
    "max_chunk_size": 120,
    "overlap": 40
  }
}
```

#### `recursive`

```{applies_to}
stack: ga 9.1
```

The `recursive` strategy splits the input text based on a configurable list of separator patterns, such as paragraph boundaries or Markdown structural elements like headings and horizontal rules. The chunker applies these separators in order, recursively splitting any chunk that exceeds the `max_chunk_size` word limit. If no separator produces a small enough chunk, the strategy falls back to [sentence-level splitting](#sentence).

You can configure the `recursive` strategy using either:
- [Predefined separator groups](#separator-groups): [`Plaintext`](#plaintext) or [`markdown`](#markdown)
- [Custom separators](#custom-separators): Define your own regular expression patterns

##### Predefined separator groups [separator-groups]

Predefined separator groups provide optimized patterns for common text formats: [`plaintext`](#plaintext) works for simple line-structured text without markup, and [`markdown`](#markdown) works for Markdown-formatted content.

###### `plaintext`

The `plaintext` separator group splits text at paragraph boundaries, first attempting to split on double newlines (paragraph breaks), then falling back to single newlines when chunks are still too large.

:::{dropdown} Regular expression patterns for the `plaintext` separator group

1. `(?<!\\n)\\n\\n(?!\\n)`: Splits on consecutive newlines that indicate paragraph breaks.
2. `(?<!\\n)\\n(?!\\n)`: Splits on single newlines when double newlines don't produce small enough chunks.

:::

::::{admonition} Example of chunking

:::{dropdown} Complete example with `max_chunk_size: 20` 

Text:

```
Elasticsearch stores data in indices. Each index is divided into shards.      (11 words)
                                                                              ← \n\n
Shards are distributed across nodes. This distribution enables horizontal
scaling.                                                                      (10 words)
                                                                              ← \n\n
Replicas provide redundancy.                                                  (3 words)
```

Chunks:

```
Chunk 1: Elasticsearch stores data in indices. Each index is divided into shards.
Chunk 2: Shards are distributed across nodes. This distribution enables horizontal scaling.
Chunk 3: Replicas provide redundancy.
```

:::

::::

The following example configures chunking with the `recursive` strategy using the `plaintext` separator group and a maximum of 200 words per chunk.

```console
PUT _inference/sparse_embedding/recursive_plaintext_chunks
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "recursive",
    "max_chunk_size": 200,
    "separator_group": "plaintext"
  }
}
```

###### `markdown`

The `markdown` separator group splits text based on Markdown structural elements, processing separators hierarchically from highest to lowest level: H1 through H6 headings, then horizontal rules.

:::{dropdown} Regular expression patterns for the `markdown` separator group

1. `\n# `: Splits on level 1 headings (H1).
2. `\n## `: Splits on level 2 headings (H2).
3. `\n### `: Splits on level 3 headings (H3).
4. `\n#### `: Splits on level 4 headings (H4).
5. `\n##### `: Splits on level 5 headings (H5).
6. `\n###### `: Splits on level 6 headings (H6).
7. `\n^(?!\\s*$).*\\n-{1,}\\n`: Splits on horizontal rules created with hyphens.
8. `\n^(?!\\s*$).*\\n={1,}\\n`: Splits on horizontal rules created with equals signs.

:::

::::{admonition} Example of chunking

:::{dropdown} Complete example with `max_chunk_size: 20` 

Text:

```
# Elasticsearch

## Storage

Elasticsearch stores data in indices. Each index is divided into shards.

## Distribution

Shards are distributed across nodes. This distribution enables horizontal scaling.

## Redundancy

Replicas provide redundancy.
```

Chunks:

```
Chunk 1: ## Storage / Elasticsearch stores data in indices. Each index is divided into shards.
Chunk 2: ## Distribution / Shards are distributed across nodes. This distribution enables horizontal scaling.
Chunk 3: ## Redundancy / Replicas provide redundancy.
```

:::

::::

The following example configures chunking with the `recursive` strategy using the `markdown` separator group and a maximum of 200 words per chunk.

```console
PUT _inference/sparse_embedding/recursive_markdown_chunks
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "recursive",
    "max_chunk_size": 200,
    "separator_group": "markdown"
  }
}
```

##### Custom separators

If the [predefined separator groups](#separator-groups) don't meet your needs, you can define custom separators using regular expressions. 

::::{admonition} Example of chunking

:::{dropdown} Complete example with `max_chunk_size: 20`

Separators:

```json
"separators": [
  "^(#{1,6})\\s",
  "\\n\\n",
  "\\n[-*]\\s",
  "\\n\\d+\\.\\s",
  "\\n"
]
```

Text:

```
# Elasticsearch

Data is stored in indices.

## Shards

- Each index is divided into shards.
- Shards are distributed across nodes.
- This distribution enables horizontal scaling.

## Replicas

Replicas provide redundancy.
```

Chunks:

```
Chunk 1: # Elasticsearch / Data is stored in indices.               (6 words)
Chunk 2: ## Shards / - Each index... (three bullet points)          (17 words)
Chunk 3: ## Replicas / Replicas provide redundancy.                 (4 words)
```

:::

::::


The following example configures chunking with the `recursive` strategy using a custom list of separators to split text into chunks of up to 180 words.

```console
PUT _inference/sparse_embedding/recursive_custom_chunks
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "recursive",
    "max_chunk_size": 180,
    "separators": [
      "^(#{1,6})\\s",
      "\\n\\n",
      "\\n[-*]\\s",
      "\\n\\d+\\.\\s",
      "\\n"
    ]
  }
}
```

#### `none`

```{applies_to}
stack: ga 9.1
```

The `none` strategy disables chunking and processes the entire input text as a single block, without any splitting or overlap. When using this strategy, you can instead [pre-chunk](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text#auto-text-chunking) the input by providing an array of strings, where each element acts as a separate chunk to be sent directly to the inference service without further chunking.

The following example creates an {{infer}} endpoint with the `elasticsearch` service that deploys the ELSER model and disables chunking by setting the strategy to `none`.

```console
PUT _inference/sparse_embedding/none_chunking
{
  "service": "elasticsearch",
  "service_settings": {
    "model_id": ".elser_model_2",
    "num_allocations": 1,
    "num_threads": 1
  },
  "chunking_settings": {
    "strategy": "none"
  }
}
```
