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

Currently, you can perform chat completion tasks through EIS using the {{infer}} API.

% TO DO: Link to the EIS inference endpoint reference docs when it's added to the OpenAPI spec. (Comming soon) %

## Default EIS endpoints [default-eis-inference-endpoints]

Your {{es}} deployment includes a preconfigured EIS endpoint, making it easier to use chat completion via the {{infer}} API:

* `rainbow-sprinkles-elastic`: uses Anthropic's Claude Sonnet 3.5 model for chat completion {{infer}} tasks.

::::{note}

* The model appears as `Elastic LLM` in the AI Assistant, Attack Discovery UI, preconfigured connectors list, and the Search Playground.
* To fine-tune prompts sent to `rainbow-sprinkles-elastic`, optimize them for Claude Sonnet 3.5.

::::

% TO DO: Link to the AI assistant documentation in the different solutions and possibly connector docs. %

## Regions [eis-regions]

EIS runs on AWS in the following regions:

* `us-east-1`
* `us-west-2`

For more details on AWS regions, refer to the [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/regions_az/) and the [supported cross-region {{infer}} profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) documentation.

## LLM hosts [llm-hosts]

The LLM used with EIS is hosted by [Amazon Bedrock](https://aws.amazon.com/bedrock/).

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
}
```
