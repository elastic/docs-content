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

# Inference integrations

{{es}} provides a machine learning [inference API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-inference-get-1) to create and manage inference endpoints that integrate with services such as Elasticsearch (for built-in NLP models like [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) and [E5](/explore-analyze/machine-learning/nlp/ml-nlp-e5.md)), as well as  popular third-party services like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

You can create a new inference endpoint:

- using the [Create an inference endpoint API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-inference-put-1)
- through the [Inference endpoints UI](#add-inference-endpoints).

## Inference endpoints UI [inference-endpoints]

You can manage inference endpoints using the UI.

The **Inference endpoints** page provides an interface for managing inference endpoints.

:::{image} /explore-analyze/images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:screenshot:
:::

Available actions:

* Add new endpoint
* View endpoint details
* Copy the inference endpoint ID
* Delete endpoints

## Add new inference endpoint [add-inference-endpoints]

To add a new interference endpoint using the UI:

1. Select the **Add endpoint** button.
1. Select a service from the drop down menu.
1. Provide the required configuration details.
1. Select **Save** to create the endpoint.

If your inference endpoint uses a model deployed in Elastic’s infrastructure, such as ELSER, E5, or a model uploaded through Eland, you can configure [adaptive allocations](#adaptive-allocations) to dynamically adjust resource usage based on the current demand.

## Adaptive allocations [adaptive-allocations]

Adaptive allocations allow inference services to dynamically adjust the number of model allocations based on the current load.
This feature is only supported for models deployed in Elastic’s infrastructure, such as ELSER, E5, or models uploaded through Eland. It is not available for third-party services like Alibaba Cloud, Cohere, or OpenAI, because those models are hosted externally and not deployed within your Elasticsearch cluster.

When adaptive allocations are enabled:

* The number of allocations scales up automatically when the load increases.
* Allocations scale down to a minimum of 0 when the load decreases, saving resources.

### Allocation scaling behavior

The behavior of allocations depends on several factors:

- Platform (Elastic Cloud Hosted, Elastic Cloud Enterprise, or Serverless)
- Usage level (low, medium, or high)
- Optimization type (ingest or search)

The tables below apply when adaptive resource settings are [configured through the UI](/deploy-manage/autoscaling/trained-model-autoscaling.md#enabling-autoscaling-in-kibana-adaptive-resources).

#### Adaptive resources enabled

::::{tab-set}

:::{tab-item} ECH, ECE
| Usage level | Optimization | Allocations |
|-------------|--------------|-------------------------------|
| Low         | Ingest       | 0 to 2 if available, dynamically |
| Medium      | Ingest       | 1 to 32 dynamically |
| High        | Ingest       | 1 to limit set in the Cloud console*, dynamically |
| Low         | Search       | 1 |
| Medium      | Search       | 1 to 2 (if threads=16), dynamically |
| High        | Search       | 1 to limit set in the Cloud console*, dynamically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::


:::{tab-item} Serverless
| Usage level | Optimization | Allocations |
|-------------|--------------|-------------------------------|
| Low         | Ingest       | 0 to 2 dynamically |
| Medium      | Ingest       | 1 to 32 dynamically |
| High        | Ingest       | 1 to 512 for Search<br>1 to 128 for Security and Observability |
| Low         | Search       | 0 to 1 dynamically |
| Medium      | Search       | 1 to 2 (if threads=16), dynamically |
| High        | Search       | 1 to 32 (if threads=16), dynamically<br>1 to 128 for Security and Observability |
:::

::::

#### Adaptive resources disabled

::::{tab-set}

:::{tab-item} ECH, ECE
| Usage level | Optimization | Allocations |
|-------------|--------------|-------------------------------|
| Low         | Ingest       | 2 if available, otherwise 1, statically |
| Medium      | Ingest       | The smaller of 32 or the limit set in the Cloud console*, statically |
| High        | Ingest       | Maximum available set in the Cloud console*, statically |
| Low         | Search       | 1 if available, statically |
| Medium      | Search       | 2 (if threads=16) statically |
| High        | Search       | Maximum available set in the Cloud console*, statically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::

:::{tab-item} Serverless
| Usage level | Optimization | Allocations |
|-------------|--------------|-------------------------------|
| Low         | Ingest       | Exactly 32 |
| Medium      | Ingest       | 1 to 32 dynamically |
| High        | Ingest       | 512 for Search<br>No static allocations for Security and Observability |
| Low         | Search       | 1 statically |
| Medium      | Search       | 2 statically (if threads=16) |
| High        | Search       | 32 statically (if threads=16) for Search<br>No static allocations for Security and Observability |
:::

::::

You can also configure adaptive allocations via the API using parameters like `num_allocations`, `min_number_of_allocations`, and `threads_per_allocation`. Refer to [Enable autoscaling through APIs](/deploy-manage/autoscaling/trained-model-autoscaling.md#enabling-autoscaling-through-apis-adaptive-allocations) for details.

::::{warning}
If you don't use adaptive allocations, the deployment will always consume a fixed amount of resources, regardless of actual usage. This can lead to inefficient resource utilization and higher costs.
::::

For more information about adaptive allocations and resources, refer to the [trained model autoscaling](/deploy-manage/autoscaling/trained-model-autoscaling.md) documentation.

## Default {{infer}} endpoints [default-enpoints]

Your {{es}} deployment contains preconfigured {{infer}} endpoints which makes them easier to use when defining `semantic_text` fields or using {{infer}} processors. The following list contains the default {{infer}} endpoints listed by `inference_id`:

* `.elser-2-elasticsearch`: uses the [ELSER](../../explore-analyze/machine-learning/nlp/ml-nlp-elser.md) built-in trained model for `sparse_embedding` tasks (recommended for English language tex). The `model_id` is `.elser_model_2_linux-x86_64`.
* `.multilingual-e5-small-elasticsearch`: uses the [E5](../../explore-analyze/machine-learning/nlp/ml-nlp-e5.md) built-in trained model for `text_embedding` tasks (recommended for non-English language texts). The `model_id` is `.e5_model_2_linux-x86_64`.

Use the `inference_id` of the endpoint in a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field definition or when creating an [{{infer}} processor](elasticsearch://reference/enrich-processor/inference-processor.md). The API call will automatically download and deploy the model which might take a couple of minutes. Default {{infer}} enpoints have adaptive allocations enabled. For these models, the minimum number of allocations is `0`. If there is no {{infer}} activity that uses the endpoint, the number of allocations will scale down to `0` automatically after 15 minutes.

## Configuring chunking [infer-chunking-config]

{{infer-cap}} endpoints have a limit on the amount of text they can process at once, determined by the model's input capacity. Chunking is the process of splitting the input text into pieces that remain within these limits.
It occurs when ingesting documents into [`semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md). Chunking also helps produce sections that are digestible for humans. Returning a long document in search results is less useful than providing the most relevant chunk of text.

Each chunk will include the text subpassage and the corresponding embedding generated from it.

By default, documents are split into sentences and grouped in sections up to 250 words with 1 sentence overlap so that each chunk shares a sentence with the previous chunk. Overlapping ensures continuity and prevents vital contextual information in the input text from being lost by a hard break.

{{es}} uses the [ICU4J](https://unicode-org.github.io/icu-docs/) library to detect word and sentence boundaries for chunking. [Word boundaries](https://unicode-org.github.io/icu/userguide/boundaryanalysis/#word-boundary) are identified by following a series of rules, not just the presence of a whitespace character. For written languages that do use whitespace such as Chinese or Japanese dictionary lookups are used to detect word boundaries.

### Chunking strategies

Two strategies are available for chunking: `sentence` and `word`.

The `sentence` strategy splits the input text at sentence boundaries. Each chunk contains one or more complete sentences ensuring that the integrity of sentence-level context is preserved, except when a sentence causes a chunk to exceed a word count of `max_chunk_size`, in which case it will be split across chunks. The `sentence_overlap` option defines the number of sentences from the previous chunk to include in the current chunk which is either `0` or `1`.

The `word` strategy splits the input text on individual words up to the `max_chunk_size` limit. The `overlap` option is the number of words from the previous chunk to include in the current chunk.

The default chunking strategy is `sentence`.

#### Example of configuring the chunking behavior

The following example creates an {{infer}} endpoint with the `elasticsearch` service that deploys the ELSER model by default and configures the chunking behavior.

```console
PUT _inference/sparse_embedding/small_chunk_size
{
  "service": "elasticsearch",
  "service_settings": {
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
