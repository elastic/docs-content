---
navigation_title: Elastic Inference Service (EIS)
applies_to:
  stack: ga 9.0
  serverless: ga
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your cluster.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search and chat independently of your {{es}} infrastructure.

## AI features powered by EIS [ai-features-powered-by-eis]

* Your Elastic deployment or project comes with a default [`Elastic Managed LLM` connector](https://www.elastic.co/docs/reference/kibana/connectors-kibana/elastic-managed-llm). This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground.

* {applies_to}`stack preview 9.1` You can use [ELSER](/explore-analyze/machine-learning/nlp/ml-nlp-elser.md) to perform semantic search as a service (ELSER on EIS).

## ELSER via Elastic {{infer-cap}} Service (ELSER on EIS)

{applies_to}`stack preview 9.1`
{applies_to}`serverless preview`

ELSER on EIS enables you to use the ELSER model without using ML nodes in your infrastructure.

### Limitations

#### Access

This feature is being gradually rolled out to Serverless and Cloud Hosted customers.
It may not be available to all users at launch.

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
