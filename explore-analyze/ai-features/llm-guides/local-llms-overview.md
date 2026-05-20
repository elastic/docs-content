---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: security
  - id: observability
---

# Self-managed custom LLMs

You can set up connectors for self-managed LLMs to maintain more control of your data, operate in an air-gapped environment, or use specific open-source models of your choosing.

For model performance on {{elastic-sec}} and {{observability}} AI tasks, refer to the [LLM performance matrix for {{observability}}](/solutions/observability/ai/llm-performance-matrix.md) and the [LLM performance matrix for {{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md).

The following guides describe how to set up self-managed LLMs for {{elastic-sec}} and {{observability}}.

**Self-managed LLMs for {{elastic-sec}}:**

- For production environments or air-gapped environments, you can [connect to vLLM](/explore-analyze/ai-features/llm-guides/connect-to-vLLM.md).
- For test environments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-security.md).

**Self-managed LLMs for {{observability}}:**

- {applies_to}`stack: ga 9.2+` For production, test, or air-gapped environments, you can [connect to LM Studio](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-observability.md).