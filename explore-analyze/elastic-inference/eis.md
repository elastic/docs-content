---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: unavailable
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your environment.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with an [`Elastic Managed LLM` connector](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm) with a default `General Purpose LLM`. This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground. For the list of available models, refer to the documentiation.

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview 9.1, ga 9.2` {applies_to}`serverless: ga`

* You can use the [`jina-embeddings-v3`](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-embeddings-v3) multilingual dense vector embedding model to perform semantic search through the Elastic {{infer-cap}} Service. {applies_to}`stack: preview 9.3` {applies_to}`serverless: preview`

## Region and hosting [eis-regions]

Requests through the `Elastic Managed LLM` are currently proxying to AWS Bedrock in AWS US regions, beginning with `us-east-1`.
The request routing does not restrict the location of your deployments.

ELSER requests are managed by Elastic's own EIS infrastructure and are also hosted in AWS US regions, beginning with `us-east-1`. All Elastic Cloud hosted deployments and serverless projects in any CSP and region can access the endpoint. As we expand the service to Azure and GCP and more regions, we will automatically route requests to the same CSP and closest region the Elaticsearch cluster is hosted on.

## ELSER through Elastic {{infer-cap}} Service (ELSER on EIS) [elser-on-eis]

```{applies_to}
stack: preview 9.1, ga 9.2
serverless: ga
```

ELSER on EIS enables you to use the ELSER model on GPUs, without having to manage your own ML nodes. We expect better performance for ingest throughput than ML nodes and equivalent performance for search latency. We will continue to benchmark, remove limitations and address concerns.

### Using the ELSER on EIS endpoint

You can now use `semantic_text` with the new ELSER endpoint on EIS. To learn how to use the `.elser-2-elastic` inference endpoint, refer to [Using ELSER on EIS](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#using-elser-on-eis).

#### Get started with semantic search with ELSER on EIS

[Semantic Search with `semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) has a detailed tutorial on using the `semantic_text` field and using the ELSER endpoint on EIS instead of the default endpoint. This is a great way to get started and try the new endpoint.

### Limitations

#### Batch size

Batches are limited to a maximum of 16 documents.
This is particularly relevant when using the [_bulk API]({{es-apis}}operation/operation-bulk) for data ingestion.

## `jina-embeddings-v3` through Elastic {{infer-cap}} Service [jina-embeddings-on-eis]

```{applies_to}
stack: preview 9.3
serverless: preview
```

You can use the `jina-embeddings-v3` model through Elastic {{infer-cap}} Service. Running the model on EIS means that the you use the model on GPUs, without the need of managing infrastrucuture and model resources. We expect better performance for ingest throughput than ML nodes and equivalent performance for search latency.

### Get started with `jina-embeddings-v3` on EIS

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

## Rate limits

The service enforces rate limits on an ongoing basis. Exceeding a limit results in HTTP 429 responses from the server until the sliding window moves on further and parts of the limit resets.

| Model                 | Request/minute  | Tokens/minute (ingest)  | Tokens/minute (search)  | Notes                    |
|-----------------------|-----------------|-------------------------|-------------------------|--------------------------|
| General Purpose LLM   | 50              | -                       | -                       | No rete limit on tokens  |
| ELSER                 | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| `jina-embeddings-v3`  | 500             | 3,000,000               | 500,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |

## Pricing

All models on EIS incur a charge per million tokens. The pricing details are at our [Pricing page](https://www.elastic.co/pricing/serverless-search).

This pricing models differs from the existing [Machine Learning Nodes](https://www.elastic.co/docs/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models), which is billed via VCUs consumed.

### Token-based billing

EIS is billed per million tokens used:

* For **chat** models, input and output tokens are billed. Longer conversations with extensive context or detailed responses will consume more tokens.
* For **embeddings** models, only input tokens are billed.

Tokens are the fundamental units that language models process for both input and output. Tokenizers convert text into numerical data by segmenting it into subword units. A token can be a complete word, part of a word, or a punctuation mark, depending on the model's trained tokenizer and the frequency patterns in its training data.

For example, the sentence "It was the best of times, it was the worst of times." contains 52 characters but would tokenize into approximately 14 tokens with a typical word-based approach, though the exact count varies by tokenizer.

### Monitor your token usage

To track your token consumption:

1. Navigate to [**Billing and subscriptions > Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} Console
2. Look for line items where the **Billing dimension** is set to "Inference"
