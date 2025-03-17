---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Elastic Inference Service (EIS)
---

# Elastic {{infer-cap}} Service [elastic-inference-service-eis]

The Elastic {{infer-cap}} Service (EIS) enables you to leverage AI-powered search as a service without deploying a model in your cluster.
With EIS, you don't need to manage the infrastructure and resources required for {{ml}} {{infer}} by adding, configuring, and scaling {{ml}} nodes.
Instead, you can use {{ml}} models for ingest, search and chat independently of your {{es}} infrastructure.

% TO DO: Link to the EIS inference endpoint reference docs when it's added to the OpenAPI spec. (Comming soon) %

## Available task types

EIS offers the following {{infer}} task types to perform:

* `chat_completion`

## AI features powered by EIS [ai-features-powered-by-eis]

Your Elastic deployment or project comes with a default `Elastic LLM` connector. This connector is used in the AI Assistant, Attack Discovery, Automatic Import and Search Playground.

% TO DO: Link to the EIS inference endpoint reference docs when it's added to the OpenAPI spec. (Comming soon) %

## Default EIS endpoints [default-eis-inference-endpoints]

Your {{es}} deployment includes a preconfigured EIS endpoint, making it easier to use chat completion via the {{infer}} API:

* `.rainbow-sprinkles-elastic`

::::{note}

* This endpoint is used by the `Elastic LLM` AI connector, which in turn powers the AI Assistant, Attack Discovery, Automatic Import, and the Search Playground.

::::

% TO DO: Link to the AI assistant documentation in the different solutions and possibly connector docs. %

## Regions [eis-regions]

All EIS requests are handled by one of these AWS regions:

* `us-east-1`
* `us-west-2`

For more details on AWS regions, refer to the [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/).

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

The request returns the following response as a stream:

```json
(...)
{
  "role" : "assistant",
  "content": "Yes",
  "model" : "rainbow-sprinkles",
  "usage" : {
    "completion_tokens" : 4,
    "prompt_tokens" : 13,
    "total_tokens" : 17
  }
}
(...)
```
