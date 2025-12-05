---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Enable large language model (LLM) access

{{elastic-sec}} uses large language model (LLM) connectors to power it's [AI features](/explore-analyze/ai-features/ai-features.md#ai-powered-features-in-elastic-sec). To use these features, you can use Elastic Managed LLM, configure a third-party LLM connector, or a custom local LLM.

:::{important}
Different LLMs have varying performance when used to power different features and use-cases. For more information about how various models perform on different tasks in {{elastic-sec}}, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
:::

## Elastic Managed LLM

:::{include} ../../_snippets/elastic-managed-llm.md
:::

## Connect to a third-party LLM

Follow these guides to connect to one or more third-party LLM providers:

* [Azure OpenAI](/explore-analyze/ai-features/llm-guides/connect-to-azure-openai.md)
* [Amazon Bedrock](/explore-analyze/ai-features/llm-guides/connect-to-amazon-bedrock.md)
* [OpenAI](/explore-analyze/ai-features/llm-guides/connect-to-openai.md)
* [Google Vertex](/explore-analyze/ai-features/llm-guides/connect-to-google-vertex.md)

## Connect to a self-managed LLM

The following guides describe how to connect to a custom LLM deployed and managed by you:

- For production environments or air-gapped environments, you can [connect to vLLM](/solutions/security/ai/connect-to-vLLM.md).
- For experimental deployments, you can [connect to LM Studio](/solutions/security/ai/connect-to-own-local-llm.md).

## Preconfigured connectors

```{applies_to}
stack: ga 9.0
serverless: unavailable
```

You can use [preconfigured connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md) to set up a third-party LLM connector. 

If you use a preconfigured connector for your LLM connector we recommend you add the `exposeConfig: true` parameter within the `xpack.actions.preconfigured` section of the `kibana.yml` config file. This parameter makes debugging easier by adding configuration information to the debug logs, including which large language model the connector uses.





