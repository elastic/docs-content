---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/llm-connector-guides.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-connector-guides.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Enable large language model (LLM) access

{{elastic-sec}} uses large language models (LLMs) for some of its advanced analytics features. To enable these features, you can connect a third-party LLM provider or a custom local LLM.

:::{important}
Different LLMs have varying performance when used to power different features and use-cases. For more information about how various models perform on different tasks in {{elastic-sec}}, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).
:::

## Elastic Managed LLM

:::{include} ../../_snippets/elastic-managed-llm.md
:::

## Connect to a third-party LLM

To access deployment guides for each available generative third-party LLM connector, refer to [GenAI Connectors](kibana://reference/connectors-kibana/gen-ai-connectors.md). 

## Connect to a custom local LLM

You can [connect to LM Studio](/solutions/security/ai/connect-to-own-local-llm.md) to use a custom LLM deployed and managed by you.

## Preconfigured connectors

```{applies_to}
stack: ga 9.0
serverless: unavailable
```

You can use [preconfigured connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md) to set up a third-party LLM connector. 

If you use a preconfigured connector for your LLM connector we recommend you add the `exposeConfig: true` parameter within the `xpack.actions.preconfigured` section of the `kibana.yml` config file. This parameter makes debugging easier by adding configuration information to the debug logs, including which large language model the connector uses.





