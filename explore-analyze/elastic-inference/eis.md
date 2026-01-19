---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: ga
    ece: ga
    eck: ga
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your environment.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with a default [`Elastic Managed LLM` connector](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm). This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground.

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview 9.1, ga 9.2` {applies_to}`serverless: ga`

## EIS for self-managed clusters [eis-self-managed]

```{applies_to}
stack: ga 9.3
deployment:
  self: ga
  ece: ga
  eck: ga
```

Use EIS with your self-managed cluster through Cloud Connect to run AI-powered search without deploying models in your environment. For details, refer to [EIS for self-managed clusters](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).

## Region and hosting [eis-regions]

Elastic {{infer-cap}} Service is currently available in a single region: {{aws}} `us-east-1`. All {{infer}} requests sent through EIS are routed to this region, regardless of where your {{es}} deployment or serverless project is hosted.

:::{note}
You may encounter different {{infer}} service URLs that appear to be region- or cloud-specific, such as `https://inference.europe-west3.gcp.svc.elastic.cloud`. These URLs are used for request routing within {{ecloud}}. Regardless of which {{infer}} service URL is configured, all EIS requests are ultimately routed to {{aws}} `us-east-1`.
:::

Depending on the model being used, request processing may involve Elastic {{infer}} infrastructure and, in some cases, trusted third-party model providers. For example, ELSER requests are processed entirely within Elastic {{infer}} infrastructure in {{aws}} `us-east-1`. Other models, such as large language models or third-party embedding models, may involve additional processing by their respective model providers, which can operate in different cloud platforms or regions.



## ELSER via Elastic {{infer-cap}} Service (ELSER on EIS) [elser-on-eis]

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

## Pricing 

All models on EIS incur a charge per million tokens. The pricing details are at our [Pricing page](https://www.elastic.co/pricing/serverless-search) for the Elastic Managed LLM and ELSER.

Note that this pricing models differs from the existing [Machine Learning Nodes](https://www.elastic.co/docs/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models), which is billed via VCUs consumed.

### Token-based billing

EIS is billed per million tokens used:

- For **chat** models, input and output tokens are billed. Longer conversations with extensive context or detailed responses will consume more tokens.
- For **embeddings** models, only input tokens are billed.

Tokens are the fundamental units that language models process for both input and output. Tokenizers convert text into numerical data by segmenting it into subword units. A token may be a complete word, part of a word, or a punctuation mark, depending on the model's trained tokenizer and the frequency patterns in its training data.

For example, the sentence "It was the best of times, it was the worst of times." contains 52 characters but would tokenize into approximately 14 tokens with a typical word-based approach, though the exact count varies by tokenizer.

### Monitor your token usage

To track your token consumption:

1. Navigate to [**Billing and subscriptions > Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} Console
2. Look for line items where the **Billing dimension** is set to "Inference"

## Rate limits

The service enforces rate limits on an ongoing basis. Exceeding a limit will result in HTTP 429 responses from the server until the sliding window moves on further and parts of the limit resets.

### Elastic Managed LLM

- 50 requests per minute
- No rate limit on tokens

### ELSER (Sparse Embeddings)

We limit on both requests per minute and tokens per minute (whichever limit is reached first).

#### Ingest 

- 6,000 request per minute
- 6,000,000 tokens per minute

#### Search

- 6,000 requests per minute
- 600,000 tokens per minute
