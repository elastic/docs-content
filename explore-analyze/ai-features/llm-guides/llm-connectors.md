---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/llm-connector-guides.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-connector-guides.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: elasticsearch
  - id: security
  - id: cloud-serverless
---

# Configure access to LLMs

Elastic's [AI features](/explore-analyze/ai-features.md) work with the out-of-the-box Elastic Managed LLMs or with third-party LLMs configured using one of the available connectors.

## Elastic Managed LLMs

:::{include} ../../../solutions/_snippets/elastic-managed-llm.md
:::

## Connect to a third-party LLM

Follow these guides to connect to one or more third-party LLM providers:

* [Azure OpenAI](/explore-analyze/ai-features/llm-guides/connect-to-azure-openai.md)
* [Amazon Bedrock](/explore-analyze/ai-features/llm-guides/connect-to-amazon-bedrock.md)
* [OpenAI](/explore-analyze/ai-features/llm-guides/connect-to-openai.md)
* [Google Vertex](/explore-analyze/ai-features/llm-guides/connect-to-google-vertex.md)

## Connect to a self-managed LLM

For {{elastic-sec}} and {{observability}}, you can also connect to a custom LLM deployed and managed by you.

Self-managed LLMs for {{elastic-sec}}: 

-- For production environments or air-gapped environments, you can [connect to vLLM](/explore-analyze/ai-features/llm-guides/connect-to-vllm.md).
-- For experimental deployments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/solutions/security/ai/connect-to-lmstudio-security.md).

Self-managed LLMs for {{observability}}:

-- For experimental deployments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-observability.md).

## Preconfigured connectors

```{applies_to}
stack: ga
serverless: unavailable
```

You can also use [preconfigured connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md) to set up third-party LLM connectors by editing the `kibana.yml` file. This allows you enable a connector for multiple spaces at once, without performing set up in the {{kib}} UI for each space. 

If you use a preconfigured connector for your LLM connector, we recommend adding the `exposeConfig: true` parameter to the `xpack.actions.preconfigured` section of the `kibana.yml` config file. This parameter makes debugging easier by adding configuration information to the debug logs, including which LLM the connector uses.





