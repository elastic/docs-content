---
applies_to:
  stack: ga 9.4+
  serverless:
products:
  - id: kibana
---
# External {{infer}}

You can use your own API keys to integrate with third-party model providers like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

## Manage your models

{{kib}} provides interfaces for managing external {{infer}} models and endpoints.

:::::{applies-switch}
::::{applies-item} { stack: ga 9.4+, serverless: ga }
Go to the **External {{infer}}** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/kibana-inference-external-ui.png
:alt: External inference UI
:screenshot:
:::

:::{tip}
To access **External {{infer}}**, you need the `Inference Endpoints: all` and `Advanced Settings: read` {{kib}} privileges.
:::
::::
::::{applies-item} stack: ga 9.0-9.3
Go to the **{{infer-cap}} endpoints** page by using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /explore-analyze/images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:screenshot:
:::
::::
:::::

Available actions include:

- Add endpoints
- View endpoint details
- Copy the inference endpoint ID
- Delete endpoints

Alternatively, you can use [{{infer}} APIs]({{es-apis}}group/endpoint-inference).

## Add new {{infer}} endpoint [add-inference-endpoints]

1. Select the **Add endpoint** button.
1. Select a service from the drop down menu.
1. Provide the required configuration details.

   For service-specific information, refer to the relevant API documentation.
   For example, [create a JinaAI inference endpoint]({{es-apis}}operation/operation-inference-put-jinaai).
1. Select **Save** to create the endpoint.

