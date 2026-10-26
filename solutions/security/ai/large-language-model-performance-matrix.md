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

This page summarizes internal test results comparing large language models (LLMs) across {{elastic-sec}} [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) and AI-powered feature use cases. The matrix tests each model across [Agent Builder](/solutions/security/ai/agent-builder/agent-builder.md), [Attack Discovery](/solutions/security/ai/attack-discovery/index.md), and [Automatic Migration](/solutions/security/get-started/automatic-migration.md). To learn more about these use cases, refer to [AI-powered features](/explore-analyze/ai-features.md#security-features). To learn how these scores are produced, refer to [Benchmarking the Agentic SOC](https://www.elastic.co/security-labs/llm-benchmarking-agentic-soc) on Elastic Security Labs.

::::{important}
Higher scores indicate better performance, on a scale of 1 to 10. A score of 10 on a capability means the model met or exceeded all task-specific benchmarks for that capability.

**Any model that scores 5 or below for a capability is not recommended for that task.**
::::


## How the scores are calculated [_how_scores_are_calculated]

The matrix uses three top-line capability scores — **Agent Builder**, **Attack Discovery**, and **Automatic Migration** — that roll up into a single **Overall Score**. You can read the table top-down, from "how does this model perform across our AI features?" to "how good is it at the specific job I care about?"

* **Overall Agent Builder Score** is the average of the seven Agent Builder [sub-capabilities](#_agent_builder_sub_capabilities). It summarizes how well a model handles agentic Security work end to end.
* **Overall Score** is the average of the Agent Builder, Attack Discovery, and Automatic Migration scores. It reflects how a model performs across the breadth of Elastic's AI features rather than any single workflow, and is the default sort for the tables below.

For a full walkthrough of the evaluation framework behind these scores — the synthetic intrusion, deterministic ground truth, trace-level grading, and blind judging — refer to [Benchmarking the Agentic SOC](https://www.elastic.co/security-labs/llm-benchmarking-agentic-soc) on Elastic Security Labs.

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

:::{table}
:matrix:

| **Model** | Agent Builder: Alert Analysis | Agent Builder: Entity Analytics | Agent Builder: Threat Hunting | Agent Builder: Detection Rules | Agent Builder: Workflow Authoring | Agent Builder: Triggering Workflows | Agent Builder: Multi-Step Executions | **Overall Agent Builder Score** | **Attack Discovery** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Anthropic Claude Sonnet 4.5** | 9.00 | 8.00 | 7.00 | 8.00 | 4.00 | 9.00 | 8.00 | **7.57** | 9.40 | 9.61 | **8.86** |
| **Anthropic Claude Opus 4.7** | 5.00 | 8.00 | 8.00 | 8.00 | 6.00 | 9.00 | 8.00 | **7.43** | 9.10 | 9.90 | **8.81** |
| **Anthropic Claude Opus 4.6** | 9.00 | 8.00 | 8.00 | 8.00 | 4.00 | 8.00 | 8.00 | **7.57** | 9.20 | 9.61 | **8.79** |
| **Anthropic Claude Sonnet 4.6** | 9.00 | 8.00 | 8.00 | 8.00 | 6.00 | 9.00 | 8.00 | **8.00** | 9.00 | 9.23 | **8.74** |
| **Anthropic Claude Opus 5** | 6.00 | 8.00 | 8.00 | 8.00 | 9.00 | 9.00 | 6.00 | **7.71** | 9.60 | 8.75 | **8.69** |
| **Anthropic Claude Opus 4.8** | 7.00 | 7.00 | 8.00 | 8.00 | 7.00 | 9.00 | 6.00 | **7.43** | 8.00 | 10.00 | **8.48** |
| **Anthropic Claude Sonnet 5** | 8.00 | 8.00 | 7.00 | 8.00 | 7.00 | 9.00 | 5.00 | **7.43** | 9.00 | 8.84 | **8.42** |
| **OpenAI GPT-5.2** | 6.00 | 7.00 | 8.00 | 8.00 | 6.00 | 8.00 | 8.00 | **7.29** | 8.00 | 9.60 | **8.30** |
| **OpenAI GPT-5.5** | 8.00 | 8.00 | 7.00 | 8.00 | 9.00 | 8.00 | 8.00 | **8.00** | 8.20 | 8.55 | **8.25** |
| **Anthropic Claude Opus 4.5** | 8.00 | 8.00 | 8.00 | 8.00 | 6.00 | 9.00 | 8.00 | **7.86** | 8.70 | 8.17 | **8.24** |
| **Google Gemini 2.5 Pro** | 5.00 | 5.00 | 7.00 | 6.00 | 6.00 | 9.00 | 8.00 | **6.57** | 8.70 | 9.32 | **8.20** |
| **OpenAI GPT-5.6 Terra** | 7.00 | 7.00 | 7.00 | 8.00 | 5.00 | 8.00 | 8.00 | **7.14** | 6.50 | 9.61 | **7.75** |
| **OpenAI GPT-5.4** | 7.00 | 7.00 | 8.00 | 7.00 | 7.00 | 9.00 | 8.00 | **7.57** | 5.30 | 9.84 | **7.57** |
| **Google Gemini 3.6 Flash** | 8.00 | 5.00 | 7.00 | 8.00 | 7.00 | 8.00 | 8.00 | **7.29** | 8.20 | 7.21 | **7.57** |
| **OpenAI GPT-5.6 Sol** | 6.00 | 8.00 | 7.00 | 8.00 | 9.00 | 8.00 | 6.00 | **7.43** | 8.00 | 7.21 | **7.55** |
| **Anthropic Claude Haiku 4.5** | 3.00 | 8.00 | 7.00 | 6.00 | 7.00 | 9.00 | 8.00 | **6.86** | 7.00 | 8.65 | **7.50** |
| **Google Gemini 3.0 Flash** | 7.00 | 6.00 | 7.00 | 8.00 | 3.00 | 8.00 | 8.00 | **6.71** | 6.00 | 9.71 | **7.47** |
| **OpenAI GPT-5.6 Luna** | 8.00 | 7.00 | 6.00 | 8.00 | 9.00 | 8.00 | 8.00 | **7.71** | 6.30 | 7.88 | **7.30** |
| **Google Gemini 2.5 Flash** | 3.00 | 4.00 | 5.00 | 3.00 | 3.00 | 6.00 | 6.00 | **4.29** | 6.80 | 9.61 | **6.90** |
| **Google Gemini 3.5 Flash** | 8.00 | 6.00 | 7.00 | 7.00 | 9.00 | 8.00 | 8.00 | **7.57** | 6.30 | 6.73 | **6.87** |
| **Google Gemini 3.1 Flash Lite** | 8.00 | 7.00 | 7.00 | 8.00 | 9.00 | 8.00 | 6.00 | **7.57** | 2.50 | 9.51 | **6.53** |
| **OpenAI GPT-5.4 Nano** | 4.00 | 4.00 | 5.00 | 4.00 | 9.00 | 7.00 | 6.00 | **5.57** | 3.50 | 8.75 | **5.94** |
| **Google Gemini 3.1 Pro (Preview)** | 8.00 | 5.00 | 7.00 | 8.00 | 7.00 | 9.00 | 7.00 | **7.29** | 3.20 | 6.44 | **5.64** |
| **OpenAI GPT-5.4 Mini** | 4.00 | 6.00 | 6.00 | 5.00 | 6.00 | 9.00 | 8.00 | **6.29** | 1.00 | 9.51 | **5.60** |
| **Google Gemini 3.5 Flash Lite** | 5.00 | 3.00 | 6.00 | 7.00 | 7.00 | 8.00 | 7.00 | **6.14** | 0.00 | 9.81 | **5.32** |
| **Google Gemini 2.5 Flash Lite** | 5.00 | 2.00 | 1.00 | 2.00 | 0.00 | 8.00 | 5.00 | **3.29** | 0.00 | 6.15 | **3.15** |

:::

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md), ranked by overall score.

_Last measured in September 2026._

:::{table}
:matrix:

| **Model** | Agent Builder: Alert Analysis | Agent Builder: Entity Analytics | Agent Builder: Threat Hunting | Agent Builder: Detection Rules | Agent Builder: Workflow Authoring | Agent Builder: Triggering Workflows | Agent Builder: Multi-Step Executions | **Overall Agent Builder Score** | **Attack Discovery** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Z.ai GLM 5.3** | 8.00 | 7.00 | 7.00 | 8.00 | 9.00 | 9.00 | 8.00 | **8.00** | 8.00 | 7.30 | **7.77** |
| **Gemma 4 31B IT** | 6.00 | 7.00 | 7.00 | 8.00 | 3.00 | 9.00 | 8.00 | **6.86** | 4.30 | 9.61 | **6.92** |
| **Kimi K2.6** | 8.00 | 6.00 | 7.00 | 8.00 | 9.00 | 9.00 | 8.00 | **7.86** | 8.00 | 2.31 | **6.05** |
| **DeepSeek V4 Pro** | 6.00 | 8.00 | 7.00 | 8.00 | 9.00 | 7.00 | 8.00 | **7.57** | 3.50 | 6.25 | **5.77** |
| **Qwen 3.8 2.4T A95B** | 8.00 | 7.00 | 7.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.29** | 0.00 | 7.88 | **5.39** |
| **OpenAI GPT-OSS 120B** | 1.00 | 1.00 | 1.00 | 3.00 | 5.00 | 8.00 | 1.00 | **2.86** | 2.00 | 9.51 | **4.79** |
| **Qwen 3.6 27B** | 6.00 | 7.00 | 8.00 | 7.00 | 7.00 | 9.00 | 8.00 | **7.43** | 0.00 | 5.67 | **4.37** |
| **OpenAI GPT-OSS 20B** | 2.00 | 2.00 | 2.00 | 5.00 | 4.00 | 7.00 | 5.00 | **3.86** | 1.00 | 6.05 | **3.64** |

:::
