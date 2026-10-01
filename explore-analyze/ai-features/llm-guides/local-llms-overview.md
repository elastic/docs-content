---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: security
  - id: observability
---

# Self-managed custom LLMs

You can connect self-managed LLMs to maintain more control of your data, operate in an air-gapped environment, or use specific open-source models of your choosing.

:::{note}
:applies_to: { serverless: deprecated, stack: deprecated 9.5+ }

The guides on this page use Generative AI connectors, which are deprecated. For new setups, [add an {{infer}} endpoint](/explore-analyze/ai-features/agent-builder/models.md#add-an-inference-endpoint) that uses the `openai` service and points at your local LLM.
:::

For model performance on {{elastic-sec}} and {{observability}} AI tasks, refer to the [LLM performance matrix for {{observability}}](/solutions/observability/ai/llm-performance-matrix.md) and the [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md).

:::{warning}
Self-managed LLMs work well for {{elastic-sec}}'s [AI Assistant](/solutions/security/ai/ai-assistant.md). For [Attack Discovery](/solutions/security/ai/attack-discovery/index.md), we recommend using one of the models in the [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md).
:::

The following guides describe how to set up self-managed LLMs for {{elastic-sec}} and {{observability}}.

**Self-managed LLMs for {{elastic-sec}}:**

- For production environments or air-gapped environments, you can [connect to vLLM](/explore-analyze/ai-features/llm-guides/connect-to-vLLM.md).
- For test environments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-security.md).

**Self-managed LLMs for {{observability}}:**

- {applies_to}`stack: ga 9.2+` For production, test, or air-gapped environments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-observability.md).