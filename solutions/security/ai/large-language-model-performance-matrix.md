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
| **Sonnet 4.5** | 9.05 | 9.8 | 7.3 | 9 | 8 | 10 | **8.86** |
| **GPT 5.2** | 10 | 8 | 8.9 | 7.5 | 8.5 | 10 | **8.82** |
| **Opus 4.5** | 9.15 | 9.8 | 8.75 | 9.15 | 8.5 | 7.3 | **8.78** |
| **Sonnet 4** | 9.15 | 9.8 | 8.75 | 8.9 | 7 | 7.5 | **8.52** |
| **Sonnet 3.7** | 7.7 | 9.2 | 7.3 | 8.6 | 7 | 9.7 | **8.25** |
| **Gemini 2.5 Pro** | 8 | 7.3 | 4.05 | 6.75 | 8.7 | 6.3 | **6.85** |
| **GPT 5.1** | 9 | 0.8 | 7.1 | 7.7 | 6.5 | 9.8 | **6.82** |
| **GPT 4.1** | 7.25 | 6.2 | 5.7 | 6.3 | 8 | 3.1 | **6.09** |

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

| **Model** | **Alerts** | **Security Knowledge** | **{{esql}} Query Generation** | **Knowledge Base Retrieval** | **Attack Discovery** | **Automatic Migration** | **Average Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT OSS 20b** | 8.2 | 1.5 | 2.5 | Not recommended | Not recommended | Not recommended | **2.03** |