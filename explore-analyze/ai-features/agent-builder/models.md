---
navigation_title: "Models"
description: "Learn how to configure LLMs in Agent Builder, including Elastic Managed LLMs using EIS and inference endpoints for providers such as OpenAI, Claude, and Gemini."
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
- [Configure your own model](#use-additional-models) using an {{infer}} endpoint, or a Generative AI connector {applies_to}`stack: deprecated 9.5` {applies_to}`serverless: deprecated`

:::

:::::

## Switch models in the UI

Use the model selector in the chat interface to switch between available models. The selector displays all configured models, including preconfigured models (on {{ech}} and {{serverless-full}}) and any custom {{infer}} endpoints or connectors you set up.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` The selector groups models as follows:

- **Recommended**: the models {{agent-builder}} recommends by default. Refer to [Models recommended by default](#recommended-by-default).
- **Other**: the other preconfigured models.
- **Custom**: your own {{infer}} endpoints and connectors.

To learn more, refer to [select a different model](/explore-analyze/ai-features/agent-builder/chat.md#select-a-different-model).

The following screenshot shows the model selector in {{serverless-full}}. The recommended models depend on your version.

:::{image} images/model-selector.png
:alt: Model selector menu in the chat interface listing recommended models under Recommended and other models under Other, with a Manage button at the bottom
:width: 550px
:screenshot:
:::

## Select a model for a single request

```{applies_to}
stack: ga 9.4+
serverless: ga
```

When you call an agent through the [Converse API](kibana-api.md#chat-and-conversations), you can override the model used for that request. Pass one of the following in the request body:

* `inference_id`: the ID of an [{{infer}} endpoint](#add-an-inference-endpoint). Use this parameter for new integrations.
* `connector_id`: the ID of a [connector](#configure-a-connector). Generative AI connectors are deprecated.

Both parameters route the request to the same underlying model and are mutually exclusive. If you send both, the request fails with a `400` error. If you omit both, the request uses the default model for {{agent-builder}}, as set on the **Feature settings** page.

For an example request, refer to [Route a request to a specific model](kibana-api.md#chat-and-conversations).

## Change the default model

::::{applies-switch}

:::{applies-item} { ess: ga 9.5+, serverless: ga }
To change which model is used by default:

1. Search for **Model Management / Feature Settings** in the global search field.
2. From the **Global model** menu, select your preferred model.
3. Select **Save settings**.
:::

:::{applies-item} { ess: ga =9.4 }
To change which model is used by default:

1. Search for **Model Management / Feature Settings** in the global search field.
2. From the **Default model** menu, select your preferred model.
3. Select **Save settings**.
:::

:::{applies-item} { ess: ga =9.3 }
To change which model is used by default:

1. Search for **GenAI Settings** in the global search field.
2. From the **Default AI Connector** menu, select your preferred connector.
3. Save your changes.
:::

::::

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` The **Feature settings** page also provides per-feature model configuration, allowing you to assign specific models to individual AI capabilities across your deployment. This enables more granular control over model selection.

For more information about these settings, refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

## Fast model routing [fast-model]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

To give you faster responses at a lower token cost, {{agent-builder}} automatically routes some low-effort, latency-sensitive operations to a fast model instead of your default model. A fast model is a smaller, high-throughput model that returns results more quickly than a frontier reasoning model.

This routing is automatic and cannot be turned off. You do not need to configure anything to benefit from it. Your default model still handles agent reasoning, tool selection, and response synthesis.

### When the fast model is used

{{agent-builder}} uses the fast model for well-scoped tasks that do not need deep reasoning, such as:

- {{esql}} query generation
- Conversation title generation

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` The fast model also selects the [skills](skills.md#how-skills-are-invoked) that are relevant to each message, but only when both of the following are true:

- The `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) is turned on.
- A fast model is available that's different from the model the conversation uses.

Otherwise, the agent receives its full list of skills.

### Fast model availability by deployment type

:::::{applies-switch}

:::{applies-item} { ess: ga, serverless: ga }
The fast model is preconfigured through Elastic Managed LLMs on the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md), with no setup. For the built-in order, refer to [Choose the fast model](#choose-the-fast-model).
:::

:::{applies-item} { ece: ga, eck: ga, self: ga }
There is no preconfigured fast model. To get one, [connect to EIS through Cloud Connect](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md). Without that connection, fast model routing uses your default model, as described in [Fallback behavior](#fallback-behavior).
:::

:::::

### Choose the fast model [choose-the-fast-model]

{{agent-builder}} uses the first model in the fast list. The built-in order depends on your version:

:::::{applies-switch}

:::{applies-item} { stack: ga 9.5.0!-9.5.2! }
1. Claude Haiku 4.5
2. Gemini 3.0 Flash
:::

:::{applies-item} { stack: ga 9.5.3!-9.6 }
1. Gemini 3.5 Flash-Lite
2. Claude Haiku 4.5
:::

:::{applies-item} { stack: ga 9.7+, serverless: ga }
1. Gemini 3.5 Flash-Lite
2. Claude Haiku 4.5
3. GPT-6 Luna
:::

:::::

{applies_to}`stack: ga =9.6` EIS can replace the built-in lists for **Fast models** and **Main models** when it provides model capability and family metadata. Without that metadata, the built-in lists are used. While **Use recommended defaults** is on, **Fast models** shows the order in use.

{applies_to}`stack: ga 9.7+` {applies_to}`serverless: ga` EIS doesn't change the built-in lists.

The following screenshot shows the **Main models** and **Fast models** lists on 9.7 and {{serverless-full}}, with **Use recommended defaults** turned on for both.

:::{image} images/agent-builder-fast-models-feature-settings.png
:alt: Main models and Fast models cards in the Agent Builder section of the Feature settings page, each with Use recommended defaults turned on and a list of assigned models
:width: 600px
:screenshot:
:::

#### Change the fast model list

How you change the fast model list depends on your version:

:::::{applies-switch}

:::{applies-item} { stack: ga 9.6+, serverless: ga }
To prefer a specific model:

1. Open **Feature Settings** and go to **Agent Builder**.
2. Under **Fast models**, turn off **Use recommended defaults**.
3. Confirm by selecting **Turn off recommended defaults**.
4. Put the preferred model first.
5. Select **Save settings**.
:::

:::{applies-item} { stack: ga =9.5 }
The built-in order is used while **Use recommended defaults** is on for **Fast models**. If you turn off **Use recommended defaults**, change the **Fast models** list, and select **Save settings**, fast routing uses your default model.
:::

:::::

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

```{applies_to}
stack: ga 9.3-9.4, deprecated 9.5
serverless: deprecated
```

::::{important}
:applies_to: {"stack": "deprecated 9.5", "serverless": "deprecated"}
Generative AI connectors are deprecated. Existing connectors and their rule actions continue to work, and you can still create and edit connectors through the API.

In 9.6 and later, deprecated connector types are hidden from the **Create connector** UI. For new models, [add an {{infer}} endpoint](#add-an-inference-endpoint) instead.
::::

To use additional models that aren't preconfigured, create a connector for your model provider.

1. Find connectors under **Alerts and Insights / Connectors** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create connector** and select your model provider.
3. Configure the connector with your API credentials and preferred model.
4. Expand **Additional settings** and select `chat_completion` as the task type.

   The following screenshot shows the **Additional settings** section with `chat_completion` selected as the task type.

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
- Create a connector with the [Connectors API]({{kib-apis}}/operation/operation-post-actions-connector-id). Works on all deployments. {applies_to}`stack: deprecated 9.5` {applies_to}`serverless: deprecated`

### Connect a local LLM

You can connect a locally hosted LLM to Elastic. This requires your local LLM to be compatible with the OpenAI API format.

[Add an {{infer}} endpoint](#add-an-inference-endpoint) that uses the `openai` service and points at your local LLM. For an example request, refer to [Using OpenAI compatible models with the {{infer-cap}} API](/solutions/search/semantic-search/using-openai-compatible-models.md).

{applies_to}`{ deployment: { self: ga, ece: ga, eck: ga } }` If your LLM is served over HTTPS with a certificate signed by a private or internal certificate authority, refer to [Trust a private certificate authority for external {{infer}} endpoints](/explore-analyze/elastic-inference/external-inference-private-ca.md).

:::{note}
:applies_to: {"stack": "deprecated 9.5", "serverless": "deprecated"}
Earlier versions used the OpenAI connector for this. That connector is deprecated. For setup instructions, refer to the [OpenAI connector documentation](kibana://reference/connectors-kibana/openai-action-type.md).
:::

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
| Extended reasoning | - Gemini 3.1 Pro <br>- Claude Opus 4.6 <br>- Claude Opus 5 <br>- Claude Opus 5.5 | Open-ended exploration, multi-step planning, complex analysis, and {{esql}}-heavy dashboard generation | Higher latency and cost. Best for latency-insensitive, batch, async, or dashboard workflows that need fewer corrections. |
| Balanced performance | - GPT-5.2 <br>- Claude Sonnet 4.6 <br>- Claude Sonnet 5 <br>- Claude Sonnet 5.5 <br>- GPT-5.6 Sol <br>- GPT-6 Sol | General-purpose agents requiring reliable tool orchestration and data retrieval and synthesis | Moderate cost. Suitable for real-time and interactive use. For {{esql}}-heavy dashboard generation, use an extended reasoning model. |
| High throughput | - Claude Haiku 4.5 <br>- Gemini 3.0 Flash <br>- Gemini 3.5 Flash-Lite <br>- GPT-6 Luna | Latency-sensitive pipelines and high-concurrency scenarios with well-scoped tasks | Lower reasoning depth. Ideal for high-volume workloads with well-defined tasks. |

:::{note}
{{agent-builder}} automatically routes some low-effort tasks to a high-throughput model. Refer to [Fast model routing](#fast-model).
:::

#### Models recommended by default [recommended-by-default]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

{{agent-builder}} recommends a set of main models by default. They appear in **Main models** on the **Feature settings** page and under **Recommended** in the model selector. This list can differ from the models in the [Recommended models](#recommended-models) table, which are known to work well but aren't all recommended by default.

The default main models depend on your version:

:::::{applies-switch}

:::{applies-item} { stack: ga 9.5.0!-9.5.2! }
- Claude Sonnet 4.6
- Claude Opus 4.6
- GPT-5.2
:::

:::{applies-item} { stack: ga 9.5.3!-9.6 }
- Claude Sonnet 5
- Claude Opus 5
- GPT-5.6 Sol
:::

:::{applies-item} { stack: ga 9.7+, serverless: ga }
- Claude Opus 5.5
- Claude Sonnet 5.5
- GPT-6 Sol
:::

:::::

:::{tip}
For agents working with large documents or conversation histories, consider models with extended context windows. For example, Claude Sonnet 4.6 and Gemini 3.1 Pro support up to 1M tokens. Check your model provider's documentation for specific context limits.
:::

:::{note}
For [dashboards and visualizations](agent-builder-dashboards-and-visualizations.md), choose a higher-tier model when the workflow depends on complex {{esql}} generation. Current testing shows Claude Opus 4.6 generates more reliable dashboard {{esql}} than Claude Sonnet 4.6.
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
- [LLM performance matrix for the {{observability}} AI Assistant](/solutions/observability/ai/llm-performance-matrix.md)
- [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md)
- [Limitations and known issues](limitations-known-issues.md)
- [Get started](get-started.md)
- [Connectors](/deploy-manage/manage-connectors.md)
