---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/llm-performance-matrix.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-performance-matrix.html
---

# Large language model performance matrix

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/llm-performance-matrix.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-llm-performance-matrix.md

This page describes the performance of various large language models (LLMs) for different use cases in {{elastic-sec}}, based on our internal testing. To learn more about these use cases, refer to [Attack discovery](/solutions/security/ai/attack-discovery.md) or [AI Assistant](/solutions/security/ai/ai-assistant.md).

::::{note}
`Excellent` is the best rating, followed by `Great`, then by `Good`, and finally by `Poor`.
::::



## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| **Feature** |  | **Assistant - General** | **Assistant - {{esql}} generation** | **Assistant - Alert questions** | **Assistant - Knowledge retrieval** | **Attack Discovery** |
| --- | --- | --- | --- | --- | --- | --- |
| **Model** | **Claude 3: Opus** | Excellent | Excellent | Excellent | Good | Great |
|  | **Claude 3.5: Sonnet v2** | Excellent | Excellent | Excellent | Excellent | Great |
|  | **Claude 3.5: Sonnet** | Excellent | Excellent | Excellent | Excellent | Excellent |
|  | **Claude 3.5: Haiku** | Excellent | Excellent | Excellent | Excellent | Poor |
|  | **Claude 3: Haiku** | Excellent | Excellent | Excellent | Excellent | Poor |
|  | **GPT-4o** | Excellent | Excellent | Excellent | Excellent | Great |
|  | **GPT-4o-mini** | Excellent | Great | Great | Great | Poor |
|  | **Gemini 1.5 Pro 002** | Excellent | Excellent | Excellent | Excellent | Excellent |
|  | **Gemini 1.5 Flash 002** | Excellent | Poor | Good | Excellent | Poor |


## Open-source models [_open_source_models]

Models you can [deploy yourself](/solutions/security/ai/connect-to-own-local-llm.md).

| **Feature** |  | **Assistant - General** | **Assistant - {{esql}} generation** | **Assistant - Alert questions** | **Assistant - Knowledge retrieval** | **Attack Discovery** |
| --- | --- | --- | --- | --- | --- | --- |
| **Model** | **Mistral Nemo** | Good | Good | Great | Good | Poor |
|  | **LLama 3.2** | Good | Poor | Good | Poor | Poor |
|  | **LLama 3.1 405b** | Good | Great | Good | Good | Poor |
|  | **LLama 3.1 70b** | Good | Good | Poor | Poor | Poor |
