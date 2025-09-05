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

_Last updated: 4 September 2025_

This page summarizes internal test results comparing large language models (LLMs) across {{obs-ai-assistant}} use cases. To learn more about these use cases, refer to [AI Assistant](/solutions/observability/observability-ai-assistant.md).

::::{important}
Rating legend

**Excellent** – Highly accurate and reliable for the use case.<br>
**Great** – Strong performance with minor limitations.<br>
**Good** – Possibly adequate for many use cases but with noticeable tradeoffs.<br>
**Poor** – Significant issues; not recommended for production for the use case.

Recommended models are those rated **Excellent** or **Great** for the paticular use case.
::::

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon Bedrock | **Claude Sonnet 3.5** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Amazon Bedrock | **Claude Sonnet 3.7** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Amazon Bedrock | **Claude Sonnet 4**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| OpenAI    | **GPT-4.1**           | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Great | Excellent |
| Google Gemini    | **Gemini 2.0 Flash**  | Excellent | Good | Great | Excellent | Excellent | Great | Great | Excellent |
| Google Gemini    | **Gemini 2.5 Flash**  | Excellent | Great | Excellent | Excellent | Excellent | Great | Great | Excellent |
| Google Gemini    | **Gemini 2.5 Pro**    | Excellent | Excellent | Excellent | Excellent | Great | Great | Excellent | Excellent |


## Open-source models [_open_source_models]

Models you can [deploy and manage yourself](/solutions/observability/connect-to-own-local-llm.md).

| Provider | Model | **Alert questions** | **APM questions** | **Contextual insights** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Execute connector** | **Knowledge retrieval** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meta | **Llama-3.3-70B-Instruct** | Excellent | Good | Great | Excellent | Excellent | Great | Great | Excellent |
| Mistral | **Mistral-Small-3.2-24B-Instruct-2506** | Excellent | Good | Great | Excellent | Excellent | Poor | Great | Excellent |

::::{note}
`Llama-3.3-70B-Instruct` is currently supported with simulated function calling.
::::

## Evaluate your own model

You can run the {{obs-ai-assistant}} evaluation framework against any model of choice. See the [evaluation framework README](https://github.com/elastic/kibana/blob/main/x-pack/solutions/observability/plugins/observability_ai_assistant_app/scripts/evaluation/README.md) for setup and usage details.

You can use it to benchmark a custom or self-hosted model against the use cases in this matrix, then compare your results with the ratings above.
