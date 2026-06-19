---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/observability-llm-performance-matrix.html
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: observability
---

# Large language model performance matrix for {{observability}} [llm-performance-matrix]

This page summarizes internal test results comparing large language models (LLMs) across {{observability}} [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) use cases. These ratings only apply if you're using [AI Assistant](/solutions/observability/ai/observability-ai-assistant.md). For Agent Builder, refer to [recommended models](/explore-analyze/ai-features/agent-builder/models.md#recommended-models).

:::{warning}
:applies_to: {"stack": "ga 9.4", "serverless": "ga"}
The {{obs-ai-assistant}} is deprecated. The [Elastic AI Agent](/explore-analyze/ai-features/elastic-agent-builder.md) is now the default chat experience in {{observability}}. To switch back to the AI Assistant, go to **GenAI settings**.
:::

**Rating legend**

For each category, the evaluation framework produces a score between 0–100 based on the criteria defined. This score is then converted to a rating using the following legend:

| Score | Rating |
| --- | --- |
| 84%–100% | **Excellent**: Highly accurate and reliable for the use case. |
| 75%–83% | **Great**: Strong performance with minor limitations. |
| 45%–74% | **Good**: Possibly adequate for many use cases but with noticeable tradeoffs. |
| 0%–44% | **Poor**: Significant issues; not recommended for production for the use case. |

Recommended models are those rated **Excellent** or **Great** for the particular use case.

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon Bedrock | **Claude Sonnet 3.5** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Good | Excellent |
| Amazon Bedrock | **Claude Sonnet 3.7** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Amazon Bedrock | **Claude Sonnet 4**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Amazon Bedrock | **Claude Sonnet 4.5**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Good | Excellent |
| Google Gemini    | **Gemini 2.0 Flash**    | Excellent | Good | Excellent | Excellent | Excellent | Good | Good | Excellent |
| Google Gemini    | **Gemini 2.5 Flash**    | Excellent | Good | Excellent | Excellent | Excellent | Great | Good | Excellent |
| Google Gemini    | **Gemini 2.5 Pro**    | Excellent | Great | Excellent | Excellent | Excellent | Great | Good | Excellent |
| OpenAI    | **GPT-4.1**           | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Good | Excellent |
| OpenAI    | **GPT-4.1 Mini**      | Excellent | Great | Excellent | Excellent | Excellent | Great | Good | Excellent |
| OpenAI    | **GPT-5**           | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Good | Excellent |
| OpenAI    | **GPT-5.2**         | Excellent | Great | Excellent | Excellent | Excellent | Great | Good | Excellent |


## Open-source models [_open_source_models]

```{applies_to}
stack: preview 9.2
serverless: preview
```

Models you can [deploy and manage yourself](/explore-analyze/ai-features/llm-guides/connect-to-lmstudio-observability.md).

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek | **DeepSeek-V3.1** | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Great | Excellent |
| Google DeepMind    | **Gemma-3-27b-it**    | Excellent | Good | Great | Great | Excellent | Good | Great | Excellent |
| OpenAI | **gpt-oss-20b** | Poor | Poor | Great | Poor | Good | Poor | Good | Good |
| OpenAI | **gpt-oss-120b** | Excellent | Poor | Great | Great | Excellent | Good | Good | Excellent |
| Meta | **Llama-3.3-70B-Instruct** | Excellent | Good | Great | Excellent | Excellent | Good | Good | Excellent |
| Meta | **Llama-4-Maverick-17B-128E-Instruct** | Great | Good | Great | Excellent | Excellent | Good | Good | Great |
| Mistral | **Mistral-Small-3.2-24B-Instruct-2506** | Excellent | Poor | Great | Great | Excellent | Good | Good | Excellent |
| Alibaba Cloud | **Qwen2.5-72b-Instruct** | Excellent | Good | Great | Excellent | Excellent | Good | Good | Excellent |

::::{note}
`Llama-3.3-70B-Instruct` and `Qwen2.5-72b-Instruct` were tested with simulated function calling.
::::

## Evaluate your own model

You can run the {{observability}} AI evaluation framework against any model, and use it to benchmark a custom or self-hosted model against the use cases in the matrix. Refer to the [evaluation framework README](https://github.com/elastic/kibana/blob/main/x-pack/solutions/observability/plugins/observability_ai_assistant_app/scripts/evaluation/README.md) for setup and usage details.

For consistency, all ratings in this matrix were generated using `Gemini 2.5 Pro` as the judge model (specified through the `--evaluateWith` flag). Use the same judge when evaluating your own model to ensure comparable results.
