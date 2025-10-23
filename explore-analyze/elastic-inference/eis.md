---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: unavailable
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your environment.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with a default [`Elastic Managed LLM` connector](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm). This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground.

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview 9.1, ga 9.2` {applies_to}`serverless: ga`

## Region and hosting [eis-regions]

Requests through the `Elastic Managed LLM` are currently proxying to AWS Bedrock in AWS US regions, beginning with `us-east-1`.
The request routing does not restrict the location of your deployments.


ELSER requests are managed by Elastic's own EIS infrastructure and are also hosted in AWS US regions, beginning with `us-east-1`. All Elastic Cloud hosted deployments and serverless projects in any CSP and region can access the endpoint. As we expand the service to Azure and GCP and more regions, we will automatically route requests to the same CSP and closest region the Elaticsearch cluster is hosted on. 

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
This is particularly relevant when using the [_bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-bulk) for data ingestion.

## Pricing 

All models on EIS incur a charge per million tokens. The pricing details are at our [Pricing page](https://www.elastic.co/pricing/serverless-search) for the Elastic Managed LLM and ELSER. 

## Rate Limits

The service enforces rate limits on an ongoing basis. Exceeding a limit will result in HTTP 429 responses from the server until the limit time is reached and the limit resets.

### Elastic Managed LLM

- 50 requests per minute
- No rate limit on tokens

### ELSER (Sparse Embedding)

We limit on both requests per minute and tokens per minute (whichever limit is reached first).

#### Ingest 

- 6,000 request per minute
- 6,000,000 tokens per minute

#### Search

- 6,000 requests per minute
- 600,000 tokens per minute
