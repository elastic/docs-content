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

This page describes the performance of various large language models (LLMs) for different use cases in {{elastic-sec}}, based on our internal testing. To learn more about these use cases, refer to [AI-Powered features](/explore-analyze/ai-features.md#security-features).

::::{important}
Higher scores indicate better performance. A score of 10 on a task means the model met or exceeded all task-specific benchmarks. 

Models with a score of "Not recommended" failed testing. This could be due to various issues, including context window constraints.
::::


## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| **Model** | **Alerts** | **Security Knowledge** | **{{esql}} Query Generation** | **Knowledge Base Retrieval** | **Attack Discovery** | **Automatic Migration** | **Average Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Opus 4.6** | 8.9 | 9.5 | 8.5 | 8.42 | 8.7 | 10 | **9** |
| **Sonnet 4.5** | 8.6 | 7.6 | 7.7 | 7.23 | 8 | 10 | **8.19** |
| **Opus 4.5** | 9 | 8.2 | 7.5 | 7.94 | 8.5 | 7.3 | **8.07** |
| **GPT 5.2** | 8.6 | 6.6 | 8 | 6 | 8.5 | 10 | **7.95** |
| **Sonnet 4** | 7.5 | 7.4 | 8 | 7.85 | 7 | 7.5 | **7.54** |
| **Sonnet 4.6** | 9.3 | 9.5 | 8.4 | 7.45 | Not recommended | 10 | **7.44** |
| **Sonnet 3.7** | 7.4 | 6.9 | 6.1 | 7.04 | 7 | 9.7 | **7.36** |
| **GPT 5.1** | 9.3 | 4.3 | 7.2 | 6 | 6.5 | 9.8 | **7.18** |
| **GPT 4.1 Mini** | 6.5 | 6.4 | 6 | 6.96 | 4.5 | 9.9 | **6.71** |
| **Gemini 2.5 Flash** | 7.8 | 6.2 | 4.4 | 5.71 | 6 | 9.81 | **6.65** |
| **Gemini 2.5 Pro** | 8 | 5.6 | 1.9 | 5.3 | 8.7 | 6.3 | **5.97** |
| **GPT 4.1** | 7.4 | 5.7 | 4.4 | 5.85 | 8 | 3.1 | **5.74** |

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

| **Model** | **Alerts** | **Security Knowledge** | **{{esql}} Query Generation** | **Knowledge Base Retrieval** | **Attack Discovery** | **Automatic Migration** | **Average Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT OSS 120B** | 7.6 | 3.7 | 5.5 | 6 | 3.5 | 9.7 | **6** |
| **GPT OSS 20b** | 8.2 | 1.5 | 2.5 | Not recommended | Not recommended | Not recommended | **2.03** |
