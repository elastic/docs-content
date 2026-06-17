---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Use Elastic Inference Service (EIS) to run inference for search, embeddings, and chat without deploying models in your environment.
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your environment.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

{applies_to}`stack: ga 9.3` You can use EIS with your [self-managed](/deploy-manage/deploy/self-managed.md) cluster through Cloud Connect. For details, refer to [EIS for self-managed clusters](connect-self-managed-cluster-to-eis.md).

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with [Elastic Managed LLMs](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm) by default. These can be used in Agent Builder, the AI Assistant, Attack Discovery, Automatic Import and Search Playground. For the list of available models, refer to [Supported models](/explore-analyze/elastic-inference/eis-supported-models.md).

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview =9.1, ga 9.2+` {applies_to}`serverless: ga`

* You can use the [`jina-embeddings-v3`](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-embeddings-v3) multilingual dense vector embedding model to perform semantic search through the Elastic {{infer-cap}} Service. {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`

## Manage your models [manage-models]

{{kib}} provides interfaces for managing EIS models and endpoints.

:::::{applies-switch}
::::{applies-item} { stack: ga 9.4+, serverless: ga }
Go to the **Elastic inference** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/eis-ui.png
:alt: Elastic Inference UI
:screenshot:
:::

:::{tip}
To access **Elastic {{infer}}**, you need the `Inference Endpoints: all` and `Advanced Settings: read` {{kib}} privileges.
:::
::::
::::{applies-item} stack: ga 9.0-9.3
Go to the **{{infer-cap}} endpoints** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:screenshot:
:::
::::
:::::

Available actions include:

- Add endpoints
- View endpoint details
- Copy the inference endpoint ID
- Delete endpoints

## Add endpoints [add-endpoint]

Your deployment includes default {{infer}} endpoints which are preconfigured and ready to use.
In most cases, you should use these default endpoints.
However, you can choose to create custom EIS endpoints if you need to instantiate a specific model version or configuration that is not covered by the defaults.

:::::{applies-switch}
::::{applies-item} { stack: ga 9.4+, serverless: ga }

1. Go to the **Elastic inference** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the model you want the new endpoint to use.
1. Click **Add endpoint**.
1. Enter a unique **Model ID**. For a complete list of valid Model IDs and their corresponding task types, refer to the [Supported models](/explore-analyze/elastic-inference/eis-supported-models.md).
1. Select **Save**.
::::
::::{applies-item} stack: ga 9.0-9.3
1. Go to the **{{infer-cap}} endpoints** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. In the **Service** dropdown, select **Elastic Inference Service**.
1. In the **Settings** section, enter the specific **Model ID**. For a complete list of valid Model IDs and their corresponding task types, refer to the [Elastic {{infer-cap}} Service supported models](/explore-analyze/elastic-inference/eis-supported-models.md).
1. (Optional) Under **More options**, set the **Maximum Input Tokens**. This limits the number of tokens processed per request. If left blank, the model's default limit is used.
1. Expand **Additional settings** and select the **Task type** that corresponds to your model.
1. Select **Save**.
::::
:::::

Alternatively, you can use [{{infer}} APIs]({{es-apis}}group/endpoint-inference), as described in the following section.

## Get started with models on EIS

The following sections describe how to get started with specific models available through Elastic {{infer-cap}} Service, including creating {{infer}} endpoints and using them for search and ingest.

### Jina v5 omni embedding models [jina-embeddings-v5-omni]

```{applies_to}
stack: ga 9.3+
serverless: ga
```

::::{important}
The Jina v5 omni models availability and the support for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type depend on your {{stack}} version:

- {applies_to}`stack: ga 9.3+` In {{stack}} 9.3 and later, you can create endpoints and run multimodal `embedding` {{infer}} requests. You cannot use these models with the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type.
- {applies_to}`stack: ga 9.4+` In {{stack}} 9.4 and later, you can use [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) mappings for text-only embeddings at ingest and search time.
- {applies_to}`stack: ga 9.5+` In {{stack}} 9.5 and later, the `semantic_field` field type supports all modalities, such as text, images, video, audio, and documents.
::::

There are two Jina v5 omni embedding models available through Elastic {{infer-cap}} Service, [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small-on-eis) and [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano-on-eis). Both models support multimodal embeddings for text, images, video, audio, and documents such as PDF in one shared vector space.

- Use [`jina-embeddings-v5-omni-small`](#jina-embeddings-v5-omni-small-on-eis) for larger context windows and higher-capacity retrieval workloads. 
- Use [`jina-embeddings-v5-omni-nano`](#jina-embeddings-v5-omni-nano-on-eis) for lower cost and lower resource usage.

#### `jina-embeddings-v5-omni-small` on EIS [jina-embeddings-v5-omni-small-on-eis]

Create an {{infer}} endpoint that references the `jina-embeddings-v5-omni-small` model in the `model_id` field. Use the `embedding` task type so the endpoint can accept multimodal input.

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-small
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-small"
  }
}
```

You can reference the `inference_id` in `embedding` {{infer}} tasks and search queries on any supported version. 

For examples of ingesting different media types and generating embeddings for text, images, audio, and video, refer to [Getting started with Jina v5 omni embedding models through Elastic {{infer-cap}} Service](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started). Select the jina-embeddings-v5-omni-small tab in each example.

#### `jina-embeddings-v5-omni-nano` on EIS [jina-embeddings-v5-omni-nano-on-eis]

Create an {{infer}} endpoint that references the `jina-embeddings-v5-omni-nano` model in the `model_id` field. Use the `embedding` task type so the endpoint can accept multimodal input.

```console
PUT _inference/embedding/eis-jina-embeddings-v5-omni-nano
{
  "service": "elastic",
  "service_settings": {
    "model_id": "jina-embeddings-v5-omni-nano"
  }
}
```

You can reference the `inference_id` in `embedding` {{infer}} tasks and search queries on any supported version. 

For examples of ingesting different media types and generating embeddings for text, images, audio, and video, refer to [Getting started with Jina v5 omni embedding models through Elastic {{infer-cap}} Service](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-omni-getting-started). Select the jina-embeddings-v5-omni-nano tab in each example.

### `jina-embeddings-v5-text-small` on EIS [jina-embeddings-v5-on-eis]

```{applies_to}
stack: preview 9.4
serverless: preview
```

You can use the `jina-embeddings-v5-text-small` model through Elastic {{infer-cap}} Service. Running the model on EIS means that you use the model on GPUs, without the need of managing infrastructure and model resources.

#### Get started with `jina-embeddings-v5-text-small` on EIS

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

The created {{infer}} endpoint uses the model for {{infer}} operations on the Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, `text_embedding` {{infer}} tasks, or search queries.

### `jina-embeddings-v3` on EIS [jina-embeddings-on-eis]

```{applies_to}
stack: preview 9.3
serverless: preview
```

You can use the `jina-embeddings-v3` model through Elastic {{infer-cap}} Service. Running the model on EIS means that you use the model on GPUs, without the need of managing infrastructure and model resources.

#### Get started with `jina-embeddings-v3` on EIS

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

The created {{infer}} endpoint uses the model for {{infer}} operations on the Elastic {{infer-cap}} Service. You can reference the `inference_id` of the endpoint in index mappings for the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field type, text_embedding {{infer}} tasks, or search queries.

### ELSER through Elastic {{infer-cap}} Service (ELSER on EIS) [elser-on-eis]

```{applies_to}
stack: preview =9.1, ga 9.2+
serverless: ga
```

ELSER on EIS enables you to use the ELSER model on GPUs, without having to manage your own ML nodes. We expect better performance for ingest throughput than ML nodes and equivalent performance for search latency. We will continue to benchmark, remove limitations and address concerns.

#### Using the ELSER on EIS endpoint

You can now use `semantic_text` with the new ELSER endpoint on EIS. To learn how to use the `.elser-2-elastic` inference endpoint, refer to [Using ELSER on EIS](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#using-elser-on-eis).

##### Get started with semantic search with ELSER on EIS

[Semantic Search with `semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) has a detailed tutorial on using the `semantic_text` field and using the ELSER endpoint on EIS instead of the default endpoint. This is a great way to get started and try the new endpoint.

## Pricing [pricing]

All models on EIS incur a charge per million tokens. Certain LLM providers charge different prices depending on the prompt size. The pricing details are available on our [Pricing page](https://www.elastic.co/pricing/serverless-search).

This pricing model differs from the existing [Machine Learning Nodes](https://www.elastic.co/docs/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models), which is billed through VCUs consumed.

### Token-based billing

EIS is billed per million tokens used:

* For **chat** models, input and output tokens are billed. Longer conversations with extensive context or detailed responses will consume more tokens.
* For **embeddings** models, only input tokens are billed.

Tokens are the fundamental units that language models process for both input and output. Tokenizers convert text into numerical data by segmenting it into subword units. A token can be a complete word, part of a word, or a punctuation mark, depending on the model's trained tokenizer and the frequency patterns in its training data.

For example, the sentence `It was the best of times, it was the worst of times.` contains 52 characters but would tokenize into approximately 14 tokens with a typical word-based approach, though the exact count varies by tokenizer.

### Monitor your token usage [monitor-your-token-usage]

To track your token consumption:

1. Navigate to [**Billing > Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} Console.
2. Look for line items where the **Billing dimension** is set to "Inference".
