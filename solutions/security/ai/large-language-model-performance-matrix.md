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

This page describes the performance of various large language models (LLMs) for different use cases in {{elastic-sec}}, based on our internal testing. To learn more about these use cases, refer to [AI-Powered features](/explore-analyze/ai-features.md#security-features)

::::{important}
Higher scores indicate better performance. A score of 100 on a task means the model met or exceeded all task-specific benchmarks.
::::


## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| **Model** | **Alerts** | **{{esql}} Query Generation** | **Knowledge Base Retrieval** | **Attack Discovery** | **General Security** | **Automatic Migration - Translated Rules** | **Average Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT 5 Chat** | 91 | 92 | 100 | 85 | 92 | 51.50 | 92 |
| **Gemini 2.5 Pro** | 89 | 86 | 100 | 87 | 90 | 32.50 | 90 |
| **Sonnet 4.5** | 90 | 90 | 100 | 80 | 90 | 52.00 | 90 |
| **GPT 5.1** | 93 | 95 | 100 | 95 | 65 | 51.00 | 90 |
| **Opus 4.5** | 86 | 86 | 100 | 85 | 90 | 38.00 | 89 |
| **Opus 4.1** | 92 | 93 | 100 | 70 | 90 | 36.50 | 89 |
| **GPT 4.1** | 87 | 88 | 100 | 80 | 88 | 16.00 | 89 |
| **Sonnet 4** | 89 | 92 | 100 | 70 | 88 | 39.00 | 88 |
| **Elastic Managed LLM** | 89 | 90 | 100 | 70 | 90 | 50.50 | 88 |
| **Gemini 2.5 Flash** | 87 | 90 | Not recommended | Not recommended | 90 | Not recommended | N/A |
| **Haiku 4.5** | 84 | 80 | Not recommended | Not recommended | 88 | Not recommended | N/A |

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

| **Model** | **Alerts** | **ES\|QL Query Generation** | **Knowledge Base Retrieval** | **Attack Discovery** | **General Security** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **GPT OSS 20b** | 82 | 25 | Not recommended | Not recommended | 10 | Not recommended | N/A |