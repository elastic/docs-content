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

# Large language model performance matrix for {{elastic-sec}} [llm-performance-matrix]

This page summarizes internal test results comparing large language models (LLMs) across {{elastic-sec}} [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) and AI-powered feature use cases. These ratings apply equally whether you're using [AI Assistant](/solutions/security/ai/ai-assistant.md) or [Agent Builder](/solutions/security/ai/agent-builder/agent-builder.md). To learn more about these use cases, refer to [AI-powered features](/explore-analyze/ai-features.md#security-features).

::::{important}
Higher scores indicate better performance, on a scale of 1 to 10. A score of 10 on a capability means the model met or exceeded all task-specific benchmarks for that capability.

**Any model that scores 5 or below for a capability is not recommended for that task.**
::::


## How the scores are calculated [_how_scores_are_calculated]

The matrix uses three top-line capability scores — **Agent Builder**, **Attack Discovery**, and **Automatic Migration** — that roll up into a single **Overall Score**. You can read the table top-down, from "how does this model perform across our AI features?" to "how good is it at the specific job I care about?"

* **Overall Agent Builder Score** is the average of the seven Agent Builder sub-capabilities (Alert Analysis, Entity Analytics, Threat Hunting, Detection Rules, Workflow Authoring, Triggering Workflows, and Multi-Step Executions). It summarizes how well a model handles agentic Security work end to end.
* **Overall Score** is the average of the Agent Builder, Attack Discovery, and Automatic Migration scores. It reflects how a model performs across the breadth of our AI features rather than any single workflow, and is the default sort for the tables below.

### What each Agent Builder sub-capability measures [_agent_builder_sub_capabilities]

* **Alert Analysis** — Triage an alert, reach the correct disposition, pull related alerts, and enrich with threat intel.
* **Entity Analytics** — Investigate hosts and users using purpose-built entity lookups and risk context.
* **Threat Hunting** — Generate and run queries against process, file, and network telemetry to find specific hunt artifacts.
* **Detection Rules** — Author a working detection rule, grounded in research where requested.
* **Workflow Authoring** — Produce a valid, executable automation workflow (verified by actually creating, enabling, and running it).
* **Triggering Workflows** — Call the correct backed action for the task (for example, a hash lookup, an on-call schedule, or case creation).
* **Multi-Step Executions** — Chain several steps in the right order, carrying findings forward, without skipping or fabricating steps.


## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

| **Model** | Agent Builder: Alert Analysis | Agent Builder: Entity Analytics | Agent Builder: Threat Hunting | Agent Builder: Detection Rules | Agent Builder: Workflow Authoring | Agent Builder: Triggering Workflows | Agent Builder: Multi-Step Executions | **Overall Agent Builder Score** | **Attack Discovery** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Anthropic Claude Opus 4.7** | 9.00 | 8.00 | 8.00 | 8.00 | 9.00 | 8.00 | 8.00 | 8.29 | 9.70 | 9.70 | **9.23** |
| **Anthropic Claude Sonnet 4.5** | 9.00 | 7.00 | 7.00 | 7.00 | 9.00 | 8.00 | 8.00 | 7.86 | 9.10 | 10.00 | **8.99** |
| **Anthropic Claude Sonnet 4.6** | 9.00 | 7.00 | 7.00 | 7.00 | 9.00 | 8.00 | 8.00 | 7.86 | 9.10 | 10.00 | **8.99** |
| **OpenAI GPT-5.2** | 8.00 | 6.00 | 6.00 | 7.00 | 8.00 | 8.00 | 8.00 | 7.43 | 8.30 | 10.00 | **8.58** |
| **Anthropic Claude Opus 4.6** | 9.00 | 8.00 | 7.00 | 8.00 | 9.00 | 8.00 | 8.00 | 8.14 | 7.50 | 10.00 | **8.55** |
| **Google Gemini 2.5 Flash** | 5.00 | 6.00 | 6.00 | 5.00 | 8.00 | 7.00 | 6.00 | 5.86 | 9.50 | 9.81 | **8.39** |
| **Anthropic Claude Opus 4.5** | 9.00 | 7.00 | 7.00 | 8.00 | 9.00 | 8.00 | 8.00 | 8.00 | 9.20 | 7.30 | **8.17** |
| **Anthropic Claude Haiku 4.5** | 6.00 | 7.00 | 7.00 | 5.00 | 9.00 | 8.00 | 8.00 | 6.71 | 6.50 | 10.00 | **7.74** |
| **Google Gemini 3.1 Flash Lite** | 7.00 | 7.00 | 7.00 | 7.00 | 8.00 | 8.00 | 8.00 | 7.57 | 3.20 | 9.90 | **6.89** |
| **Google Gemini 3.0 Flash** | 8.00 | 8.00 | 7.00 | 8.00 | 9.00 | 8.00 | 6.00 | 7.71 | 3.20 | 9.70 | **6.87** |
| **OpenAI GPT-5.4 Mini** | 7.00 | 7.00 | 7.00 | 7.00 | 8.00 | 8.00 | 6.00 | 7.14 | 3.50 | 9.80 | **6.81** |
| **Google Gemini 3.5 Flash** | 8.00 | 7.00 | 7.00 | 8.00 | 9.00 | 8.00 | 6.00 | 8.00 | 5.60 | 6.60 | **6.73** |
| **Google Gemini 3.1 Pro (Preview)** | 8.00 | 7.00 | 7.00 | 8.00 | 8.00 | 8.00 | 6.00 | 7.86 | 4.20 | 8.10 | **6.72** |
| **OpenAI GPT-4.1** | 5.00 | 6.00 | 6.00 | 7.00 | 8.00 | 8.00 | 6.00 | 6.29 | 3.60 | 9.60 | **6.50** |
| **OpenAI GPT-5.4** | 7.00 | 7.00 | 8.00 | 8.00 | 9.00 | 8.00 | 6.00 | 7.86 | 5.30 | 5.90 | **6.35** |
| **OpenAI GPT-5.4 Nano** | 5.00 | 3.00 | 5.00 | 7.00 | 8.00 | 8.00 | 6.00 | 5.57 | 1.00 | 9.90 | **5.49** |
| **Google Gemini 2.5 Pro** | 7.00 | 7.00 | 5.00 | 7.00 | 8.00 | 8.00 | 6.00 | 6.86 | 0.00 | 6.70 | **4.52** |
| **Google Gemini 2.5 Flash Lite** | 4.00 | 6.00 | 3.00 | 3.00 | 2.00 | 5.00 | 6.00 | 4.14 | 0.00 | 7.30 | **3.81** |
| **OpenAI GPT-4.1 Mini** | 6.00 | 3.00 | 6.00 | 5.00 | 9.00 | 7.00 | 3.00 | 5.57 | 4.20 | 0.00 | **3.26** |

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

| **Model** | Agent Builder: Alert Analysis | Agent Builder: Entity Analytics | Agent Builder: Threat Hunting | Agent Builder: Detection Rules | Agent Builder: Workflow Authoring | Agent Builder: Triggering Workflows | Agent Builder: Multi-Step Executions | **Overall Agent Builder Score** | **Attack Discovery** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI GPT-OSS 120B** | 5.00 | 4.00 | 6.00 | 7.00 | 5.00 | 8.00 | 7.00 | 5.14 | 3.00 | 9.40 | **5.85** |
| **Gemma 4 31B IT** | 6.00 | 6.00 | 7.00 | 6.00 | 8.00 | 8.00 | 7.00 | 7.00 | 2.80 | 7.50 | **5.77** |
| **DeepSeek V4 Pro** | 5.00 | 6.00 | 6.00 | 6.00 | 9.00 | 8.00 | 7.00 | 5.86 | 8.30 | 3.10 | **5.75** |
| **OpenAI GPT-OSS 20B** | 4.00 | 5.00 | 5.00 | 7.00 | 5.00 | 8.00 | 4.00 | 5.43 | 2.60 | 4.00 | **4.01** |
| **Qwen 3.6 27B** | 5.00 | 7.00 | 7.00 | 8.00 | 9.00 | 8.00 | 6.00 | 7.14 | 0.00 | 4.10 | **3.75** |
| **Kimi K2.6** | 0.00 | 6.00 | 0.00 | 0.00 | 9.00 | 6.00 | 7.00 | 4.00 | 0.00 | 3.10 | **2.37** |
