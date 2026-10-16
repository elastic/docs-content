---
navigation_title: "Gemini 3 on Vertex AI"
description: Troubleshooting guide for Gemini 3 tool-call failures on a Google Vertex AI inference endpoint in Elastic Agent Builder.
type: troubleshooting
applies_to:
  stack: ga 9.4-9.5
  serverless: unavailable
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Gemini 3 tool calls fail on a Google Vertex AI inference endpoint

{{agent-builder}} fails when a Google Vertex AI {{infer}} endpoint uses a Gemini 3.x model and the agent calls a tool. Creating the endpoint succeeds. The failure happens on the chat completion request, because the endpoint does not preserve the thought signature (`thought_signature`) Gemini 3 requires on each function call.

Gemini 3.x models remain supported through the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md).

## Symptoms

- The agent fails when it tries to call a tool. You get no tool result.
- The error includes status `400` and `thought_signature`. For example:

    ```console-response
    Error: Received an unsuccessful status code for request from inference entity id [<inference_id>] status [400]. Function call is missing a thought_signature in functionCall parts. This is required for tools to work correctly, and missing thought_signature may lead to degraded model performance.
    ```

    `<inference_id>` is the ID of the Google Vertex AI endpoint {{agent-builder}} is using.

## Resolution

Use a Gemini 2.x model on the Google Vertex AI endpoint, or use a Gemini 3.x model through EIS.

### Use a Gemini 2.x model

The model ID of an existing endpoint cannot be changed. Create a new Google Vertex AI endpoint that uses a Gemini 2.x model.

```console
PUT _inference/chat_completion/gemini_2_5_flash <1>
{
  "service": "googlevertexai",
  "service_settings": {
    "service_account_json": "<service_account_json>", <2>
    "model_id": "gemini-2.5-flash",
    "project_id": "<project_id>", <3>
    "location": "<location>" <4>
  }
}
```

1. The endpoint ID. Use an ID that is not already in use.
2. The service account JSON key for the Google Vertex AI API.
3. The Google Cloud project ID.
4. The Google Cloud region where Vertex AI is enabled, such as `us-central1`.

Select this endpoint in the [model selector](../models.md#switch-models-in-the-ui). For the full field list, refer to [Create a Google Vertex AI inference endpoint]({{es-apis}}operation/operation-inference-put-googlevertexai).

### Use Gemini 3.x through EIS

Use a Gemini 3.x model that runs as an Elastic Managed LLM on EIS. These models are preconfigured. 

On {{serverless-full}} projects and {{ech}} deployments, the Elastic Managed LLMs are already available. On {{ece}}, {{eck}}, and self-managed deployments, [connect the cluster to EIS](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md) first.

In the [model selector](../chat.md#select-a-different-model), select **Gemini 3.0 Flash** or **Gemini 3.1 Pro** under **Recommended** or **Other**.

## Resources

- [Recommended models](../models.md#recommended-models)
- [](/explore-analyze/elastic-inference/eis.md)
- [](../troubleshooting.md)

:::{tip}
If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can [contact Elastic support](/troubleshoot/index.md#contact-us) for assistance.
:::
