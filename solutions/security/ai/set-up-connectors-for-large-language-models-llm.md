---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/llm-connector-guides.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-connector-guides.html
applies_to:
  stack: all
  serverless:
    security: all
---

# Enable large language model (LLM) access

{{elastic-sec}} uses large language models (LLMs) for some of its advanced analytics features. To enable these features, you can connect to Elastic LLM, a third-party LLM provider, or a custom local LLM.

:::{important}
Different LLMs have varying performance when used to power different features and use-cases. For more information about how various models perform on different tasks in {{elastic-sec}}, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
:::


## Connect to Elastic LLM

Elastic LLM is enabled by default for any user with the necessary Elastic license or subscription. To use it:

1. Navigate to a feature that uses an LLM, such as AI Assistant.
2. Use the model selection menu to select the Elastic LLM*.

## Connect to a third-party LLM

Follow these guides to connect to one or more third-party LLM providers:

* [Azure OpenAI](/solutions/security/ai/connect-to-azure-openai.md)
* [Amazon Bedrock](/solutions/security/ai/connect-to-amazon-bedrock.md)
* [OpenAI](/solutions/security/ai/connect-to-openai.md)
* [Google Vertex](/solutions/security/ai/connect-to-google-vertex.md)

## Connect to a custom local LLM

You can [connect to LM Studio](/solutions/security/ai/connect-to-own-local-llm.md) to use a custom LLM deployed and managed by you.







