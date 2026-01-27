---
navigation_title: "Models"
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Using different models in {{agent-builder}}

{{agent-builder}} uses large language models (LLMs) to power agent reasoning and decision-making.

For {{serverless-full}} projects and {{ech}} deployments, {{agent-builder}} uses the Preconfigured AI connector to interface with models running on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md). This managed service requires zero setup.

## Default model configuration

:::::{applies-switch}

:::{applies-item} { ess:, serverless: }

You can get started with zero setup using the Preconfigured AI connector.
{{agent-builder}} uses this connector to interface with models running on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md). This managed service requires no additional API key management.

::::{note}
Learn more about the [Preconfigured AI connector](kibana://reference/connectors-kibana/elastic-managed-llm.md) and [pricing](https://www.elastic.co/pricing).
::::

:::{applies-item} {ece:, eck, self: preview =9.2, ga 9.3+}

These deployments do not include a preconfigured connector. You must [configure a connector](#change-the-default-model) to use {{agent-builder}}.

% To access models on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md) from self-managed deployments, use [Cloud Connect](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).

:::

:::::

## Switch models in the UI

Use the model selector in the chat interface to switch between available models. The selector displays all configured models, including preconfigured models (on {{ech}} and {{serverless-full}}) and any custom connectors you set up.

To learn more, refer to [select a different model](/explore-analyze/ai-features/agent-builder/chat.md#select-a-different-model).

:::{image} images/model-selector.png
:alt: Model selector dropdown in the chat interface
:width: 550px
:screenshot:
:::

## Change the default model

To change which model is used by default:

1. Search for **GenAI Settings** in the global search field
2. Select your preferred connector from the **Default AI Connector** dropdown
3. Save your changes

## Use additional models

To use additional models that aren't preconfigured, create a connector for your model provider.

### Create a connector in the UI

To create a new connector:

1. Find connectors under **Alerts and Insights / Connectors** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md)
2. Select **Create Connector** and select your model provider
3. Configure the connector with your API credentials and preferred model
4. Expand **Additional settings** and select `chat_completion` as the task type
   :::{image} images/additional-settings-chat-completion-task-type.png
   :alt: Additional settings expanded showing chat_completion task type selected
   :width: 450px
   :screenshot:
   :::

:::{tip}
For detailed instructions on creating connectors, refer to [Connectors](/deploy-manage/manage-connectors.md).

To learn about preconfigured connectors, refer to [preconfigured connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md).
:::

### Create connectors with the API

To create connectors programmatically, refer to the [Connectors API documentation]({{kib-apis}}/operation/operation-post-actions-connector-id).

### Connect a local LLM

You can connect a locally hosted LLM to Elastic using the OpenAI connector. This requires your local LLM to be compatible with the OpenAI API format.


For detailed setup instructions, refer to the [OpenAI connector documentation](kibana://reference/connectors-kibana/openai-action-type.md).

## Model requirements

{{agent-builder}} requires models with strong reasoning and tool-calling capabilities. State-of-the-art models perform significantly better than smaller or older models.

Agent Builder relies on advanced LLM capabilities including:

- **Function calling**: Models must accurately select appropriate tools and construct valid parameters from natural language requests
- **Multi-step reasoning**: Agents need to plan, execute, and adapt based on tool results across multiple iterations
- **Structured output**: Models must produce properly formatted responses that the agent framework can parse

While Elastic offers LLM [connectors](kibana://reference/connectors-kibana.md) for many different vendors and models, not all LLMs are robust enough to be used with {{agent-builder}}.

### Recommended models

The following models are known to work well with {{agent-builder}}. These categories represent a spectrum from maximum reasoning capability to maximum throughput. Choose based on your latency, cost, and complexity requirements.

| Category | Model examples | Use cases | Trade-offs |
|---|---|---|---|
| Extended reasoning | - Gemini 3 Pro <br>- Claude 4.5 Opus | Open-ended exploration, multi-step planning, and complex analysis | Higher latency and cost; best for latency-insensitive, batch, or async workflows |
| Balanced performance | - GPT-5.2 <br>- Claude 4.5 Sonnet | General-purpose agents requiring reliable tool orchestration and data retrieval and synthesis | Moderate cost; suitable for real-time and interactive use |
| High throughput | GPT-OSS-120B | Latency-sensitive pipelines and high-concurrency scenarios with well-scoped tasks | Lower reasoning depth; smaller context window. Ideal for air-gapped deployments |

:::{tip}
For agents working with large documents or conversation histories, consider models with extended context windows. For example, Claude 4.5 Sonnet and Gemini 3 Pro support up to 1M tokens. Check your model provider's documentation for specific context limits.
:::

### Incompatible models

Smaller or less capable models may produce errors like:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

While any chat-completion-compatible connector can technically be configured, we strongly recommend using state-of-the-art models for reliable agent performance.

:::{note}
Smaller or "mini" model variants are not recommended for {{agent-builder}} as they lack the necessary capabilities for reliable agent workflows.
:::

## Related pages

- [Limitations and known issues](limitations-known-issues.md): Current limitations around model selection
- [Get started](get-started.md): Initial setup and configuration
- [Connectors](/deploy-manage/manage-connectors.md): Detailed connector configuration guide
