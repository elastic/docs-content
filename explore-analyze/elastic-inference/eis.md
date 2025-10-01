---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga
  serverless: ga
  deployment:
    self: unavailable
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your cluster.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search, and chat independently of your {{es}} infrastructure.

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with a default [`Elastic Managed LLM` connector](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm). This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground.

* You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS). {applies_to}`stack: preview 9.1` {applies_to}`serverless: preview`

## Region and hosting [eis-regions]

Requests through the `Elastic Managed LLM` are currently proxying to AWS Bedrock in AWS US regions, beginning with `us-east-1`.
The request routing does not restrict the location of your deployments.

ELSER requests are managed by Elastic's own EIS infrastructure and are also hosted in AWS US regions, beginning with `us-east-1`.


## ELSER via Elastic {{infer-cap}} Service (ELSER on EIS) [elser-on-eis]

```{applies_to}
stack: preview 9.1
serverless: preview
```

ELSER on EIS enables you to use the ELSER model on GPUs, without having to manage your own ML nodes. We expect significantly better performance for throughput and consistent search latency as compared to ML nodes, and will continue to benchmark, remove limitations and address concerns as we move towards General Availability.

### Usage

You can now use `semantic_text` with the new ELSER endpoint on EIS, see the [instructions to change the inference id](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/semantic-text#using-elser-on-eis) to use the `.elser-2-elastic` inference endpoint. 

### Limitations

While we do encourage experimentation, we do not recommend implementing production use cases on top of this feature while it is in Technical Preview.

#### Region Availability 

ELSER on EIS is only available in AWS `us-east-1`. Endpoints in other CSPs and regions including GovCloud regions are not yet supported. 

#### Uptime

There are no uptime guarantees during the Technical Preview.
While Elastic will address issues promptly, the feature may be unavailable for extended periods.

#### Throughput and latency

{{infer-cap}} throughput via this endpoint is expected to exceed that of {{infer}} operations on an ML node.
However, throughput and latency are not guaranteed.
Performance may vary during the Technical Preview.

#### Batch size

Batches are limited to a maximum of 16 documents.
This is particularly relevant when using the [_bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/v9/operation/operation-bulk) for data ingestion.

#### Rate limits 

Rate limit for search and ingest is currently at 500 requests per minute. This allows you to ingest approximately 8000 documents per minute at 16 documents per request.

## Pricing 

All models on EIS incur a charge per million tokens. The pricing details are at our [Pricing page](https://www.elastic.co/pricing/serverless-search) for the Elastic Managed LLM and ELSER. 
