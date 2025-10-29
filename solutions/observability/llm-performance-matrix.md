---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/observability-llm-performance-matrix.html
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: observability
---

# Large language model performance matrix

This page summarizes internal test results comparing large language models (LLMs) across {{obs-ai-assistant}} use cases. To learn more about these use cases, refer to [AI Assistant](/solutions/observability/observability-ai-assistant.md).

::::{important}
Rating legend:

**Excellent:** Highly accurate and reliable for the use case.<br>
**Great:** Strong performance with minor limitations.<br>
**Good:** Possibly adequate for many use cases but with noticeable tradeoffs.<br>
**Poor:** Significant issues; not recommended for production for the use case.

Recommended models are those rated **Excellent** or **Great** for the particular use case.
::::

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon Bedrock | **Claude Sonnet 3.5** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Good | Excellent |
| Amazon Bedrock | **Claude Sonnet 3.7** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Amazon Bedrock | **Claude Sonnet 4**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Amazon Bedrock | **Claude Sonnet 4.5**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Good | Excellent |
| OpenAI    | **GPT-4.1**           | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Good | Excellent |
| Google Gemini    | **Gemini 2.0 Flash**    | Excellent | Good | Excellent | Excellent | Excellent | Good | Good | Excellent |
| Google Gemini    | **Gemini 2.5 Flash**    | Excellent | Good | Excellent | Excellent | Excellent | Great | Good | Excellent |
| Google Gemini    | **Gemini 2.5 Pro**    | Excellent | Great | Excellent | Excellent | Excellent | Great | Good | Excellent |


## Open-source models [_open_source_models]

```{applies_to}
stack: preview 9.2
serverless: preview
```

Models you can [deploy and manage yourself](/solutions/observability/connect-to-own-local-llm.md).

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meta | **Llama-3.3-70B-Instruct** | Excellent | Good | Great | Excellent | Excellent | Good | Good | Excellent |
| Mistral | **Mistral-Small-3.2-24B-Instruct-2506** | Excellent | Poor | Great | Great | Excellent | Good | Good | Excellent |
| Alibaba Cloud | **Qwen2.5-72b-Instruct** | Excellent | Good | Great | Excellent | Excellent | Good | Good | Excellent |

::::{note}
`Llama-3.3-70B-Instruct` and `Qwen2.5-72b-Instruct` were tested with simulated function calling.
::::

## Evaluate your own model

You can run the {{obs-ai-assistant}} evaluation framework against any model, and use it to benchmark a custom or self-hosted model against the use cases in the matrix. Refer to the [evaluation framework README](https://github.com/elastic/kibana/blob/main/x-pack/solutions/observability/plugins/observability_ai_assistant_app/scripts/evaluation/README.md) for setup and usage details.

For consistency, all ratings in this matrix were generated using `Gemini 2.5 Pro` as the judge model (specified via the `--evaluateWith` flag). Use the same judge when evaluating your own model to ensure comparable results.
