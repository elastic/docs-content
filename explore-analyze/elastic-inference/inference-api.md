---
navigation_title: Inference integrations
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/inference-endpoints.html
applies_to:
  stack:
  serverless:
products:
  - id: kibana
---

# {{infer-cap}} integrations

{{es}} provides a machine learning [{{infer}} API]({{es-apis}}group/endpoint-inference) to create and manage {{infer}} endpoints that integrate with services such as {{es}} (for built-in NLP models like [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) and [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md)), as well as  popular third-party services like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

You can use the default {{infer}} endpoints your deployment contains or create a new {{infer}} endpoint:

- using the [Create an inference endpoint API]({{es-apis}}operation/operation-inference-put)
- through the [Inference endpoints UI](#add-inference-endpoints).

## Default {{infer}} endpoints [default-enpoints]

Your {{es}} deployment contains preconfigured {{infer}} endpoints, which makes them easier to use when defining `semantic_text` fields or using {{infer}} processors. These endpoints come in two forms:

- **Elastic Inference Service (EIS) endpoints**, which provide {{infer}} as a managed service and do not consume resources from your own nodes.

- **ML node-based endpoints**, which run on your dedicated {{ml}} nodes.

The following section lists the default {{infer}} endpoints, identified by their `inference_id`, grouped by whether they are EIS- or ML node–based.

### Default endpoints for Elastic {{infer-cap}} Service (EIS)

- `.elser-2-elastic`: uses the [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) trained model as an Elastic {{infer-cap}} Service for `sparse_embedding` tasks (recommended for English language text). The `model_id` is `.elser_model_2`. {applies_to}`stack: preview 9.1` {applies_to}`self: unavailable` {applies_to}`serverless: preview`

### Default endpoints used on ML-nodes

- `.elser-2-elasticsearch`: uses the [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) built-in trained model for `sparse_embedding` tasks (recommended for English language text). The `model_id` is `.elser_model_2_linux-x86_64`.
- `.multilingual-e5-small-elasticsearch`: uses the [E5](../../explore-analyze/machine-learning/nlp/ml-nlp-e5.md) built-in trained model for `text_embedding` tasks (recommended for non-English language texts). The `model_id` is `.e5_model_2_linux-x86_64`.

Use the `inference_id` of the endpoint in a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field definition or when creating an [{{infer}} processor](elasticsearch://reference/enrich-processor/inference-processor.md). The API call will automatically download and deploy the model which might take a couple of minutes. Default {{infer}} enpoints have adaptive allocations enabled. For these models, the minimum number of allocations is `0`. If there is no {{infer}} activity that uses the endpoint, the number of allocations will scale down to `0` automatically after 15 minutes.

## {{infer-cap}} endpoints UI [inference-endpoints]

The **{{infer-cap}} endpoints** page provides an interface for managing {{infer}} endpoints.

:::{image} /explore-analyze/images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:screenshot:
:::

Available actions:

- Add new endpoint
- View endpoint details
- Copy the inference endpoint ID
- Delete endpoints

## Add new {{infer}} endpoint [add-inference-endpoints]

To add a new {{infer}} endpoint using the UI:

1. Select the **Add endpoint** button.
1. Select a service from the drop down menu.
1. Provide the required configuration details.
1. Select **Save** to create the endpoint.

If your {{infer}} endpoint uses a model deployed in Elastic’s infrastructure, such as ELSER, E5, or a model uploaded through Eland, you can configure [adaptive allocations](#adaptive-allocations) to dynamically adjust resource usage based on the current demand.

## Adaptive allocations [adaptive-allocations]

Adaptive allocations allow {{infer}} services to dynamically adjust the number of model allocations based on the current load.
This feature is only supported for models deployed in Elastic’s infrastructure, such as ELSER, E5, or models uploaded through Eland. It is not available for models used through the Elastic {{infer-cap}} Service (EIS) and third-party services (for example, Alibaba Cloud, Cohere, or OpenAI), because those models are not deployed within your Elasticsearch cluster.

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

{{infer-cap}} endpoints have a limit on the amount of text they can process at once, determined by the model's input capacity. Chunking is the process of splitting the input text into pieces that remain within these limits.
It occurs when ingesting documents into [`semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md). Chunking also helps produce sections that are digestible for humans. Returning a long document in search results is less useful than providing the most relevant chunk of text.

Each chunk will include the text subpassage and the corresponding embedding generated from it.

By default, documents are split into sentences and grouped in sections up to 250 words with 1 sentence overlap so that each chunk shares a sentence with the previous chunk. Overlapping ensures continuity and prevents vital contextual information in the input text from being lost by a hard break.

{{es}} uses the [ICU4J](https://unicode-org.github.io/icu-docs/) library to detect word and sentence boundaries for chunking. [Word boundaries](https://unicode-org.github.io/icu/userguide/boundaryanalysis/#word-boundary) are identified by following a series of rules, not just the presence of a whitespace character. For written languages that do use whitespace such as Chinese or Japanese dictionary lookups are used to detect word boundaries.

### Chunking strategies

Several strategies are available for chunking:

#### `sentence`

The `sentence` strategy splits the input text at sentence boundaries. Each chunk contains one or more complete sentences ensuring that the integrity of sentence-level context is preserved, except when a sentence causes a chunk to exceed a word count of `max_chunk_size`, in which case it will be split across chunks. The `sentence_overlap` option defines the number of sentences from the previous chunk to include in the current chunk which is either `0` or `1`.

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
- [Predefined separator groups](#separator-groups): [`plaintext`](#plaintext) or [`markdown`](#markdown)
- [Custom separators](#custom-separators): Define your own regular expression patterns

##### Predefined separator groups [separator-groups]

Predefined separator groups provide optimized patterns for common text formats: [`plaintext`](#plaintext) works for simple line-structured text without markup, and [`markdown`](#markdown) works for Markdown-formatted content.

###### `plaintext`

The `plaintext` separator group splits text at paragraph boundaries, first attempting to split on double newlines (paragraph breaks), then falling back to single newlines when chunks are still too large.

:::{dropdown} Regular expression patterns for the `plaintext` separator group

1. `(?<!\\n)\\n\\n(?!\\n)`: Splits on consecutive newlines that indicate paragraph breaks.
2. `(?<!\\n)\\n(?!\\n)`: Splits on single newlines when double newlines don't produce small enough chunks.

:::

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

If the [predefined separator groups](#separator-groups) don't meet your needs, you can define custom separators using regular expressions. The following example configures chunking with the `recursive` strategy using a custom list of separators to split text into chunks of up to 180 words.

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


