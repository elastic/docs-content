---
navigation_title: "Gemini 3 on Vertex AI"
description: Troubleshooting guide for Gemini 3 tool-call failures on a Google Vertex AI inference endpoint in Elastic Agent Builder.
type: troubleshooting
applies_to:
  stack: preview =9.2, ga =9.3
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Gemini 3 tool calls fail on a Google Vertex AI inference endpoint

On Stack 9.2 and 9.3, {{agent-builder}} tool calls fail when using a Gemini 3.x model through a Google Vertex AI {{infer}} endpoint configured in [External {{infer}}](/explore-analyze/elastic-inference/external.md), even though endpoint creation succeeds.

Gemini 3.x models remain supported through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md).

## Symptoms

- The agent fails when it tries to call a tool. You get no tool result.
- The error includes status `400` and `thought_signature`. For example:

    ```console-response
    Error: Received an unsuccessful status code for request from inference entity id [<inference_id>] status [400]. Function call is missing a thought_signature in functionCall parts. This is required for tools to work correctly, and missing thought_signature may lead to degraded model performance.
    ```

    `<inference_id>` is the ID of the Google Vertex AI endpoint {{agent-builder}} is using.

## Resolution

You can choose one of the following options:

- [Upgrade](#upgrade) to Stack 9.5.6 or later.
- [Create a new endpoint that uses a Gemini 2.x model](#use-a-gemini-2.x-model).
- [Use Gemini 3.x models through EIS](#use-gemini-3.x-through-eis).

### Upgrade

Upgrade your cluster to Stack 9.5.6 or later. For instructions, refer to [Upgrade your deployment or cluster](/deploy-manage/upgrade/deployment-or-cluster.md).

### Use a Gemini 2.x model

Create a new Google Vertex AI endpoint that uses a Gemini 2.x model. The model ID of an existing endpoint cannot be changed. For example:

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

Select this endpoint in the [model selector](../models.md#switch-models-in-the-ui). For the full field list, refer to [Create a Google Vertex AI {{infer}} endpoint]({{es-apis}}operation/operation-inference-put-googlevertexai).

### Use Gemini 3.x through EIS

Gemini 3.x models are available through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md). EIS is automatically available on {{serverless-full}} projects and {{ech}} deployments. On {{ece}}, {{eck}}, and self-managed deployments, [connect the cluster to EIS](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md) first.

To use a Gemini 3.x model on EIS, select it in the [model selector](../chat.md#select-a-different-model). 

## Resources

- [Recommended models](../models.md#recommended-models)
- [](/explore-analyze/elastic-inference/eis.md)
