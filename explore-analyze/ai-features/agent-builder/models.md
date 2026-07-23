---
navigation_title: "Models"
description: "Learn how to configure LLMs in Agent Builder, including Elastic Managed LLMs using EIS and custom connectors for OpenAI, Claude, and Gemini."
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

# Model configuration in {{agent-builder}}

{{agent-builder}} uses large language models (LLMs) to power agent reasoning and decision-making.

For model performance for {{observability}} and {{elastic-sec}}, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md). The [Recommended models](#recommended-models) section focuses on {{agent-builder}}.

For {{serverless-full}} projects and {{ech}} deployments, {{agent-builder}} uses Elastic Managed LLMs running on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md). This managed service requires zero setup.

## Default model configuration

:::::{applies-switch}

:::{applies-item} { ess:, serverless: }

You can get started with zero setup using Elastic Managed LLMs. These are built-in LLMs running on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md). This managed service requires no additional API key management.

::::{note}
Learn more about [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md) and [pricing](https://www.elastic.co/pricing).
::::

:::

:::{applies-item} {ece:, eck, self: preview =9.2, ga 9.3+}

These deployments do not include a preconfigured model. To use {{agent-builder}}, you have two options:

- [Connect to the Elastic {{infer-cap}} Service (EIS) using Cloud Connect](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md) (recommended) {applies_to}`stack: ga 9.3+`
- [Configure your own model](#use-additional-models) using an {{infer}} endpoint or a Generative AI connector

:::

:::::

## Switch models in the UI

Use the model selector in the chat interface to switch between available models. The selector displays all configured models, including preconfigured models (on {{ech}} and {{serverless-full}}) and any custom {{infer}} endpoints or connectors you set up.

To learn more, refer to [select a different model](/explore-analyze/ai-features/agent-builder/chat.md#select-a-different-model).

:::{image} images/model-selector.png
:alt: Model selector dropdown in the chat interface
:width: 550px
:screenshot:
:::

## Select a model for a single request

```{applies_to}
stack: ga 9.4+
serverless: ga
```

When you call an agent through the [Converse API](kibana-api.md#chat-and-conversations), you can override the agent's configured model for that request. Pass one of the following in the request body:

* `inference_id`: the ID of an [{{infer}} endpoint](#add-an-inference-endpoint).
* `connector_id`: the ID of a [connector](#configure-a-connector).

Both parameters route the request to the same underlying model and are mutually exclusive. If you send both, the request fails with a `400` error. If you omit both, the agent uses its default model.

For an example request, refer to [Route a request to a specific model](kibana-api.md#chat-and-conversations).

## Change the default model

::::{applies-switch}

:::{applies-item} { ess: ga 9.4+, serverless: ga }
To change which model is used by default:

1. Search for **Model management / Feature settings** in the global search field.
2. Select your preferred model from the **Default model** dropdown.
3. Save your changes.

The **Feature settings** page also provides per-feature model configuration, allowing you to assign specific models to individual AI capabilities across your deployment. This enables more granular control over model selection.

:::

:::{applies-item} { ess: ga =9.3 }
To change which model is used by default:

1. Search for **GenAI Settings** in the global search field.
2. Select your preferred connector from the **Default AI Connector** dropdown.
3. Save your changes.
:::

::::

For more information about these settings, refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

## Fast model routing [fast-model]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

To reduce latency, {{agent-builder}} automatically routes some low-effort, latency-sensitive operations to a fast model instead of your default model. A fast model is a smaller, high-throughput model that returns results more quickly than a frontier reasoning model.

This routing is automatic and cannot be turned off. You do not need to configure anything to benefit from it. Your default model still handles agent reasoning, tool selection, and response synthesis.

### When the fast model is used

{{agent-builder}} uses the fast model for well-scoped tasks that do not need deep reasoning, such as {{esql}} query generation and conversation title generation.

### Fast model availability by deployment type

On {{serverless-full}} projects and {{ech}} deployments, the fast model is preconfigured through Elastic Managed LLMs on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md), with no setup. Claude Haiku 4.5 is one example. The latency improvement is most noticeable on {{serverless-full}}.

On {{ece}}, {{eck}}, and self-managed deployments, there is no preconfigured fast model unless you [connect to EIS through Cloud Connect](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md). Without it, fast model routing falls back to your default model.

### Choose the fast model

{{agent-builder}} uses a recommended Elastic Managed LLM for fast routing. When more than one recommended fast model is available, such as Claude Haiku 4.5 and Google Gemini Flash, it uses the first one. To prefer a specific model, open the **Feature settings** page, go to the **Agent Builder** section, and order the models under **Fast models** so your preferred one is at the top. To find this page, refer to [Change the default model](#change-the-default-model).

In 9.5, only recommended Elastic Managed LLMs are used for fast routing. Assigning a custom or non-recommended model has no effect on the fast model.

:::{image} images/agent-builder-fast-models-feature-settings.png
:alt: Main models and Fast models cards in the Agent Builder section of the Feature settings page
:width: 600px
:screenshot:
:::

<!-- TODO(verify before merge): confirm the exact Fast models ordering UI in Feature settings and that this screenshot still matches the flow (check with Joe/Sid or on a 9.5 cluster). Custom-assignment support is tracked in search-team#15449 (not in 9.5). -->

### Fallback behavior

If no fast model is available, {{agent-builder}} uses your default model instead. Fast model routing is an optimization, so a missing fast model reduces the latency benefit but does not cause errors.

## Use additional models

You can configure additional models for {{agent-builder}} in two ways:

### Add an {{infer}} endpoint [add-an-inference-endpoint]

```{applies_to}
stack: ga 9.4+
serverless: ga
```

Configure an {{infer}} endpoint for your model provider. The endpoint must support the `chat_completion` task type.

Choose based on how the model is hosted:

- **Elastic-managed models**: Add an endpoint in [**Elastic {{infer}}**](/explore-analyze/elastic-inference/eis.md).
- **Third-party providers** (such as OpenAI, Anthropic, or Amazon Bedrock): Add an endpoint in [**External {{infer}}**](/explore-analyze/elastic-inference/external.md).

If you prefer not to use the UI, you can also create endpoints with the {{infer}} APIs. See [Create models programmatically](#create-models-programmatically).

### Configure a connector

To use additional models that aren't preconfigured, create a connector for your model provider.

1. Find connectors under **Alerts and Insights / Connectors** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create Connector** and select your model provider.
3. Configure the connector with your API credentials and preferred model.
4. Expand **Additional settings** and select `chat_completion` as the task type.

   :::{image} images/additional-settings-chat-completion-task-type.png
   :alt: Additional settings expanded showing chat_completion task type selected
   :width: 450px
   :screenshot:
   :::

:::{tip}
For detailed instructions on creating connectors, refer to [Connectors](/deploy-manage/manage-connectors.md).

To learn about preconfigured connectors, refer to [preconfigured connectors](kibana://reference/connectors-kibana/pre-configured-connectors.md).
:::

### Create models programmatically

You can create either an {{infer}} endpoint or a connector through the API:

- Create an {{infer}} endpoint with the [{{infer}} APIs]({{es-apis}}group/endpoint-inference).
- Create a connector with the [Connectors API]({{kib-apis}}/operation/operation-post-actions-connector-id). Works on all deployments.

### Connect a local LLM

You can connect a locally hosted LLM to Elastic using the OpenAI connector. This requires your local LLM to be compatible with the OpenAI API format.


For detailed setup instructions, refer to the [OpenAI connector documentation](kibana://reference/connectors-kibana/openai-action-type.md).

## Model requirements

{{agent-builder}} requires models with strong reasoning and tool-calling capabilities. State-of-the-art models perform significantly better than smaller or older models.

Agent Builder relies on advanced LLM capabilities including:

- **Function calling**: Models must accurately select appropriate tools and construct valid parameters from natural language requests.
- **Multi-step reasoning**: Agents need to plan, execute, and adapt based on tool results across multiple iterations.
- **Structured output**: Models must produce properly formatted responses that the agent framework can parse.

While {{agent-builder}} can be configured to use LLMs from many different vendors, not all LLMs are robust enough for reliable agent workflows.

### Recommended models

The following models are known to work well with {{agent-builder}}. These categories represent a spectrum from maximum reasoning capability to maximum throughput. Choose based on your latency, cost, and complexity requirements.

| Category | Model examples | Use cases | Trade-offs |
|---|---|---|---|
| Extended reasoning | - Gemini 3.1 Pro <br>- Claude 4.6 Opus | Open-ended exploration, multi-step planning, complex analysis, and {{esql}}-heavy dashboard generation | Higher latency and cost. Best for latency-insensitive, batch, async, or dashboard workflows that need fewer corrections. |
| Balanced performance | - GPT-5.2 <br>- Claude 4.6 Sonnet | General-purpose agents requiring reliable tool orchestration and data retrieval and synthesis | Moderate cost. Suitable for real-time and interactive use. For {{esql}}-heavy dashboard generation, use an extended reasoning model. |
| High throughput | - Claude 4.5 Haiku <br>- Gemini 3.0 Flash | Latency-sensitive pipelines and high-concurrency scenarios with well-scoped tasks | Lower reasoning depth. Ideal for high-volume workloads with well-defined tasks. |

:::{note}
{{agent-builder}} automatically routes some low-effort tasks to a high-throughput model. Refer to [Fast model for low-effort tasks](#fast-model).
:::

:::{tip}
For agents working with large documents or conversation histories, consider models with extended context windows. For example, Claude 4.6 Sonnet and Gemini 3.1 Pro support up to 1M tokens. Check your model provider's documentation for specific context limits.
:::

:::{note}
For [dashboards and visualizations](agent-builder-dashboards-and-visualizations.md), choose a higher-tier model when the workflow depends on complex {{esql}} generation. Current testing shows Claude 4.6 Opus generates more reliable dashboard {{esql}} than Claude 4.6 Sonnet.
:::

### Incompatible models

Smaller or less capable models may produce errors like:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

Although any chat-completion-compatible model can technically be configured, use state-of-the-art models for reliable agent performance.

:::{note}
Smaller or "mini" model variants are not recommended for {{agent-builder}} as they lack the necessary capabilities for reliable agent workflows.
:::

## Related pages

- [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md)
- [External {{infer}}](/explore-analyze/elastic-inference/external.md)
- [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md)
- [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md)
- [LLM performance matrix for {{observability}}](/solutions/observability/ai/llm-performance-matrix.md)
- [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md)
- [Limitations and known issues](limitations-known-issues.md)
- [Get started](get-started.md)
- [Connectors](/deploy-manage/manage-connectors.md)
