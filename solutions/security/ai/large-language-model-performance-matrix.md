---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/llm-performance-matrix.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-performance-matrix.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Large language model performance matrix

This page describes the performance of various large language models (LLMs) for different use cases in {{elastic-sec}}, based on our internal testing. To learn more about these use cases, refer to [Attack discovery](/solutions/security/ai/attack-discovery.md) or [AI Assistant](/solutions/security/ai/ai-assistant.md).

::::{important}
`Excellent` is the best rating, followed by `Great`, then by `Good`, and finally by `Poor`. Models rated `Excellent` or `Great` should produce quality results. Models rated `Good` or `Poor` are not recommended for that use case.
::::



## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| **Feature** | - | **Assistant - General** | **Assistant - {{esql}} generation** | **Assistant - Alert questions** | **Assistant - Knowledge retrieval** | **Attack Discovery** | **Automatic Migration** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Model** | **Claude Opus 4**          | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent
|           | **Claude Sonnet 4**        | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent
|           | **Claude Sonnet 3.7**      | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent
|           | **GPT-4.1**                 | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent
|           | **Gemini 2.0 Flash 001**    | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent
|           | **Gemini 2.5 Pro**          | Excellent | Excellent | Excellent | Excellent | Excellent | Excellent


## Open-source models [_open_source_models]

Models you can [deploy yourself](/solutions/security/ai/connect-to-own-local-llm.md).

| **Feature** | - | **Assistant - General** | **Assistant - {{esql}} generation** | **Assistant - Alert questions** | **Assistant - Knowledge retrieval** | **Attack Discovery** | **Automatic Migration**
| --- | --- | --- | --- | --- | --- | --- |
| **Model** | **Mistral‑Small‑3.2‑24B‑Instruct‑2506** | Excellent | Good | Excellent | Excellent | Good | N/A
|           | **Mistral-Small-3.1-24B-Instruct-2503** | Excellent | Good | Excellent | Excellent | Good | N/A
|           | **Mistral Nemo**   | Good | Good  | Great | Good | Poor | Poor |
|           | **LLama 3.2**      | Good | Poor  | Good  | Poor | Poor | Good |
|           | **LLama 3.1 405b** | Good | Great | Good  | Good | Poor | Poor |
|           | **LLama 3.1 70b**  | Good | Good  | Poor  | Poor | Poor | Good |