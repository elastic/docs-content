---
applies_to:
  stack: ga 9.4+
  serverless:
products:
  - id: kibana
---
# External {{infer}}

You can use your own API keys to integrate with third-party model providers like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

The **External {{infer}}** app provides an interface for managing external {{infer}} models and endpoints.

<!--
:::{image} /explore-analyze/images/kibana-external-endpoints-ui.png
:alt: External inference UI
:screenshot:
:::
-->

Available actions include:

- Add new endpoint
- View endpoint details
- Copy the inference endpoint ID
- Delete endpoints

Alternatively, you can use [{{infer}} APIs]({{es-apis}}group/endpoint-inference).

## Add new {{infer}} endpoint [add-inference-endpoints]

1. Go to the **External {{infer}}** model management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Add endpoint** button.
1. Select a service from the drop down menu.
1. Provide the required configuration details.

   For service-specific information, refer to the relevant API documentation.
   For example, [create a JinaAI inference endpoint]({{es-apis}}operation/operation-inference-put-jinaai).
1. Select **Save** to create the endpoint.
