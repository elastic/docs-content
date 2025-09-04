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
Ratings (best to worst): `Excellent`, `Great`, `Good`, `Poor`. 
Models rated `Excellent` or `Great` are recommended for that use case; those rated `Good` or `Poor` are not recommended for that use case.
::::

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| Provider | Model | **Alert questions** | **APM questions** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Knowledge retrieval** | **Contextual insights** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon Bedrock | **Claude Sonnet 3.5** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Amazon Bedrock | **Claude Sonnet 3.7** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Amazon Bedrock | **Claude Sonnet 4**   | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| OpenAI    | **GPT-4.1**           | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Google Gemini    | **Gemini 2.0 Flash**  | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Google Gemini    | **Gemini 2.5 Flash**  | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |
| Google Gemini    | **Gemini 2.5 Pro**    | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |


## Open-source models [_open_source_models]

Models you can [deploy and manage yourself](/solutions/observability/connect-to-own-local-llm.md).

| Provider | Model | **Alert questions** | **APM questions** | **Documentation retrieval** | **Elasticsearch operations** | **{{esql}} generation** | **Knowledge retrieval** | **Contextual insights** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Meta | **Llama 3.3 70B** | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent |

::::{note}
`Llama 3.3` is currently supported with simulated function calling.
::::

## Evaluate your own model

You can run the {{obs-ai-assistant}} evaluation framework against any model of choice. See the [evaluation framework README](https://github.com/elastic/kibana/blob/main/x-pack/solutions/observability/plugins/observability_ai_assistant_app/scripts/evaluation/README.md) for setup and usage details.

You can use it to benchmark a custom or self-hosted model against the use cases in this matrix, then compare your results with the ratings above.
