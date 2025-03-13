---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Elastic Inference Service (EIS)
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your cluster.
With EIS, you don't need to manage the infrastructure and resources required for large language models (LLMs) by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models in high-throughput, low-latency scenarios independently of your {{es}} infrastructure.

% TO DO: Link to the EIS inference endpoint reference docs when it's added to the OpenAPI spec. (Comming soon) %

## Available task types

EIS offers the following {{infer}} task types to perform:

* Chat completion

## How to use EIS [using-eis]

Your Elastic deployment comes with default endpoints for EIS that you can use performing {{infer}} tasks.
You can either do it by calling the {{infer}} API or using the default `Elastic LLM` model in the AI Assistant, Attack Discovery UI, and Search Playground.

% TO DO: Link to the EIS inference endpoint reference docs when it's added to the OpenAPI spec. (Comming soon) %

## Default EIS endpoints [default-eis-inference-endpoints]

Your {{es}} deployment includes a preconfigured EIS endpoint, making it easier to use chat completion via the {{infer}} API:

* `rainbow-sprinkles-elastic`

::::{note}

* The model appears as `Elastic LLM` in the AI Assistant, Attack Discovery UI, preconfigured connectors list, and the Search Playground.

::::

% TO DO: Link to the AI assistant documentation in the different solutions and possibly connector docs. %

## Regions [eis-regions]

EIS runs on AWS in the following regions:

* `us-east-1`
* `us-west-2`

For more details on AWS regions, refer to the [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) and the [supported cross-region {{infer}} profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) documentation.

## Examples

The following example demonstrates how to perform a `chat_completion` task through EIS by using the `.rainbow-sprinkles-elastic` default {{infer}} endpoint.

```json
POST /_inference/chat_completion/.rainbow-sprinkles-elastic/_stream
{
    "messages": [
        {
            "role": "user",
            "content": "Say yes if it works."
        }
    ],
    "temperature": 0.7,
    "max_completion_tokens": 300
}
```

The request returns the following response:

```json
(...)
{
  "role" : "assistant",
  "content": "Yes",
  "model" : "rainbow-sprinkles",
  "object" : "chat.completion.chunk",
  "usage" : {
    "completion_tokens" : 4,
    "prompt_tokens" : 13,
    "total_tokens" : 17
  }
}
(...)
```
