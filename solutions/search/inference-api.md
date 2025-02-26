---
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/inference-endpoints.html

navigation_title: Inference integrations
applies_to:
  stack:
  serverless:
---

# Integrate with third-party services

{{es}} provides a machine learning [inference API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-inference-get-1) to create and manage inference endpoints to integrate with machine learning models provide by popular third-party services like Amazon Bedrock, Anthropic, Azure AI Studio, Cohere, Google AI, Mistral, OpenAI, Hugging Face, and more.

Learn how to integrate with specific services in the subpages of this section.

## Inference endpoints UI [inference-endpoints]

You can also manage inference endpoints using the UI.

The **Inference endpoints** page provides an interface for managing inference endpoints.

:::{image} ../../images/kibana-inference-endpoints-ui.png
:alt: Inference endpoints UI
:class: screenshot
:::

Available actions:

* Add new endpoint
* View endpoint details
* Copy the inference endpoint ID
* Delete endpoints

## Add new inference endpoint

To add a new interference endpoint using the UI:

1. Select the **Add endpoint** button.
1. Select a service from the drop down menu.
1. Provide the required configuration details.
1. Select **Save** to create the endpoint.