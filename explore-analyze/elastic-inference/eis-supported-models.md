---
navigation_title: Supported models
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Identify the models that are supported by Elastic Inference Service (EIS).
---

# Elastic {{infer-cap}} Service supported models

The following tables list the models supported by Elastic {{infer-cap}} Service by model type.

The corresponding {{kib}} connectors and {{infer}} endpoints for these models are created automatically. To customize the configuration, you can create [your own connectors](kibana://reference/connectors-kibana.md#creating-new-connector) or [{{infer}} endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

::::{note}
The **{{infer-cap}} Regions** column shows the regions where {{infer}} requests are processed and where data is sent.
::::

### LLM chat models

:::{csv-include} chat-models.csv
:caption: Scroll horizontally to view more information.
:::

### Embedding models

:::{csv-include} embedding-models.csv
:caption: Scroll horizontally to view more information.
:::

### Rerankers

:::{csv-include} reranker-models.csv
:caption: Scroll horizontally to view more information.
:::

::::{important}

* The applicable terms of use, uptime, and performance for each of the AI models available with EIS are each described in the applicable AI model's Provider Terms and Model Card.
* Prior to using the AI model with EIS, Customers are responsible for reviewing and agreeing to the chosen AI model's Provider Terms to understand the availability and data practices of the AI model's provider.
* After the listed end-of-life (EOL) date, the model is no longer available for {{infer}} use and requests will fail. You need to actively transition to another model before the EOL date, there is no automated migration.
* Elastic makes every effort to use third party providers who do not use inputs to train models, and do not retain any data (zero data retention). Browse the tables on this page to double-check the status of a specific model.
::::

## Region and hosting [eis-regions]

Elastic {{infer-cap}} Service is currently available in these regions:

**AWS:**

* `us-east-1` (Virginia)

**GCP:**

* `asia-southeast1` (Singapore)
* `europe-west1` (Belgium)
* `us-east4` (Virginia)

All {{infer}} requests sent through EIS are routed to the nearest region, regardless of where your {{es}} deployment or {{serverless-short}} project is hosted.

Depending on the model being used, request processing may involve Elastic {{infer}} infrastructure and, in some cases, trusted third-party model providers. For example, ELSER and Jina requests are processed entirely within Elastic {{infer}} infrastructure. Other models, such as large language models or third-party embedding models, may involve additional processing by their respective model providers, which can operate in different cloud platforms or regions.

## Rate limits

The service enforces rate limits on an ongoing basis. Exceeding a limit results in HTTP 429 responses from the server until the sliding window moves on further and parts of the limit resets.

| Model                                             | Request/minute  | Tokens/minute (ingest)  | Tokens/minute (search)  | Notes                    |
|---------------------------------------------------|-----------------|-------------------------|-------------------------|--------------------------|
| Elastic Managed LLMs {applies_to}`stack: ga 9.3+` | 2000            | -                       | -                       | No rate limit on tokens  |
| ELSER {applies_to}`stack: ga 9.0+`                | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 Nano {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 Small {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v3 {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 (Small) {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Embeddings v5 (Nano) {applies_to}`stack: ga 9.3+`   | 6,000           | 6,000,000               | 600,000                 | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Reranker v2 {applies_to}`stack: ga 9.3+`     | 600             | -                       | 6,000,000               | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |
| Jina Reranker v3 {applies_to}`stack: ga 9.3+`     | 600             | -                       | 6,000,000               | Limits are applied to both requests per minute and tokens per minute, whichever limit is reached first.  |

## Pricing

All models on EIS incur a charge per million tokens. Certain LLM providers charge different prices depending on the prompt size. The pricing details are available on our [Pricing page](https://www.elastic.co/pricing/serverless-search).

This pricing model differs from the existing [Machine Learning Nodes](https://www.elastic.co/docs/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models), which is billed through VCUs consumed.

### Token-based billing

EIS is billed per million tokens used:

* For **chat** models, input and output tokens are billed. Longer conversations with extensive context or detailed responses will consume more tokens.
* For **embeddings** models, only input tokens are billed.

Tokens are the fundamental units that language models process for both input and output. Tokenizers convert text into numerical data by segmenting it into subword units. A token can be a complete word, part of a word, or a punctuation mark, depending on the model's trained tokenizer and the frequency patterns in its training data.

For example, the sentence `It was the best of times, it was the worst of times.` contains 52 characters but would tokenize into approximately 14 tokens with a typical word-based approach, though the exact count varies by tokenizer.

### Monitor your token usage

To track your token consumption:

1. Navigate to [**Billing > Usage**](https://cloud.elastic.co/billing/usage) in the {{ecloud}} Console.
2. Look for line items where the **Billing dimension** is set to "Inference".
