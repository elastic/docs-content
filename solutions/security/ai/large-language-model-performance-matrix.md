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
| **Anthropic Claude Opus 5** | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.10** | 9.50 | 9.13 | **9.24** |
| **Anthropic Claude Sonnet 4.5** | 9.00 | 9.00 | 9.00 | 9.00 | 7.00 | 10.00 | 9.00 | **8.90** | 9.30 | 9.52 | **9.24** |
| **Anthropic Claude Opus 4.7** | 9.00 | 9.00 | 9.00 | 9.00 | 6.00 | 10.00 | 7.00 | **8.40** | 9.20 | 9.81 | **9.14** |
| **Anthropic Claude Sonnet 4.6** | 9.00 | 9.00 | 9.00 | 9.00 | 7.00 | 10.00 | 9.00 | **8.90** | 8.40 | 9.62 | **8.97** |
| **Anthropic Claude Opus 4.8** | 7.00 | 9.00 | 9.00 | 9.00 | 8.00 | 10.00 | 9.00 | **8.70** | 8.30 | 9.90 | **8.97** |
| **Anthropic Claude Opus 4.6** | 9.00 | 9.00 | 9.00 | 9.00 | 5.00 | 10.00 | 9.00 | **8.60** | 8.50 | 9.52 | **8.87** |
| **Anthropic Claude Sonnet 5.5** | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.10** | 7.80 | 9.33 | **8.74** |
| **Google Gemini 3.7 Flash** | 9.00 | 8.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.00** | 6.80 | 9.90 | **8.57** |
| **Anthropic Claude Opus 4.5** | 9.00 | 9.00 | 9.00 | 9.00 | 6.00 | 10.00 | 9.00 | **8.70** | 7.80 | 9.04 | **8.51** |
| **Google Gemini 4 Argon (Vertex)** | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.10** | 6.80 | 9.52 | **8.47** |
| **Google Gemini 3.8 Flash** | 9.00 | 8.00 | 9.00 | 9.00 | 7.00 | 10.00 | 9.00 | **8.70** | 7.00 | 9.71 | **8.47** |
| **Google Gemini 3.6 Flash** | 9.00 | 7.00 | 9.00 | 9.00 | 8.00 | 10.00 | 9.00 | **8.70** | 6.80 | 9.33 | **8.28** |
| **Google Gemini 3.0 Flash** | 9.00 | 7.00 | 9.00 | 9.00 | 5.00 | 9.00 | 9.00 | **8.10** | 7.00 | 9.62 | **8.24** |
| **Google Gemini 3.5 Flash Lite** | 8.00 | 3.00 | 8.00 | 5.00 | 7.00 | 9.00 | 8.00 | **6.90** | 8.00 | 9.81 | **8.24** |
| **OpenAI GPT-5.6 Terra** | 7.00 | 8.00 | 9.00 | 9.00 | 9.00 | 10.00 | 7.00 | **8.40** | 6.00 | 9.23 | **7.88** |
| **OpenAI GPT-5.2** | 4.00 | 9.00 | 9.00 | 9.00 | 8.00 | 10.00 | 9.00 | **8.30** | 6.00 | 9.33 | **7.88** |
| **OpenAI GPT-5.5** | 8.00 | 8.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.70** | 6.00 | 8.75 | **7.82** |
| **Google Gemini 3.1 Pro (Preview)** | 8.00 | 7.00 | 8.00 | 8.00 | 5.00 | 10.00 | 8.00 | **7.70** | 6.50 | 9.23 | **7.81** |
| **Anthropic Claude Sonnet 5** | 7.00 | 7.00 | 9.00 | 9.00 | 8.00 | 10.00 | 7.00 | **8.10** | 6.00 | 9.33 | **7.81** |
| **Google Gemini 3.5 Flash** | 9.00 | 7.00 | 9.00 | 9.00 | 10.00 | 9.00 | 9.00 | **8.90** | 4.50 | 9.81 | **7.74** |
| **OpenAI GPT-5.4** | 6.00 | 8.00 | 9.00 | 8.00 | 6.00 | 10.00 | 9.00 | **8.00** | 5.80 | 9.33 | **7.71** |
| **OpenAI GPT-5.6 Terra Pro** | 4.00 | 9.00 | 9.00 | 9.00 | 8.00 | 9.00 | 9.00 | **8.10** | 5.30 | 9.04 | **7.48** |
| **OpenAI GPT-5.6 Sol** | 6.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.60** | 6.50 | 7.21 | **7.44** |
| **OpenAI GPT-6 Sol** | 4.00 | 8.00 | 9.00 | 9.00 | 9.00 | 9.00 | 8.00 | **8.00** | 6.00 | 8.17 | **7.39** |
| **OpenAI GPT-5.6 Luna** | 7.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.70** | 5.30 | 7.98 | **7.33** |
| **Anthropic Claude Opus 5.5** | 7.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.90** | 6.30 | 6.54 | **7.25** |
| **OpenAI GPT-5.6 Sol Pro** | 6.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.60** | 6.50 | 6.63 | **7.24** |
| **OpenAI GPT-6 Sol Pro** | 4.00 | 8.00 | 9.00 | 8.00 | 9.00 | 9.00 | 6.00 | **7.60** | 5.80 | 8.08 | **7.16** |
| **OpenAI GPT-6 Astra** | 4.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 6.00 | **7.90** | 7.30 | 6.15 | **7.12** |
| **OpenAI GPT-6 Luna Pro** | 6.00 | 9.00 | 8.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.40** | 5.80 | 7.02 | **7.07** |
| **OpenAI GPT-6 Astra Pro** | 4.00 | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 6.00 | **7.70** | 7.30 | 6.15 | **7.05** |
| **OpenAI GPT-5.6 Luna Pro** | 5.00 | 9.00 | 9.00 | 9.00 | 10.00 | 10.00 | 9.00 | **8.70** | 4.00 | 7.69 | **6.80** |
| **OpenAI GPT-6 Luna** | 6.00 | 9.00 | 9.00 | 9.00 | 8.00 | 9.00 | 9.00 | **8.40** | 5.50 | 6.44 | **6.78** |
| **Google Gemini 3.1 Flash Lite** | 7.00 | 7.00 | 8.00 | 8.00 | 6.00 | 8.00 | 8.00 | **7.60** | 2.50 | 9.62 | **6.57** |
| **OpenAI GPT-5.4 Nano** | 4.00 | 7.00 | 9.00 | 5.00 | 6.00 | 10.00 | 7.00 | **6.90** | 2.50 | 9.52 | **6.31** |
| **OpenAI GPT-5.4 Mini** | 5.00 | 8.00 | 9.00 | 5.00 | 6.00 | 10.00 | 8.00 | **7.30** | 1.80 | 9.71 | **6.27** |
| **Google Gemini 3.8 Flash Cyber (Vertex)** | 9.00 | 8.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.90** | 0.00 | 9.04 | **5.98** |
| **Anthropic Claude Haiku 4.5** | 5.00 | 9.00 | 9.00 | 5.00 | 7.00 | 10.00 | 7.00 | **7.40** | 0.00 | 9.81 | **5.74** |
| **Anthropic Claude Fable 5.1** | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.10** | 0.00 | 7.50 | **5.53** |
| **Anthropic Claude Fable 5** | 7.00 | 9.00 | 9.00 | 9.00 | 7.00 | 10.00 | 9.00 | **8.60** | 0.00 | 7.02 | **5.21** |

:::

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md), ranked by overall score.

_Last measured in November 2026._

:::{table}
:matrix:

| **Model** | Agent Builder: Alert Analysis | Agent Builder: Entity Analytics | Agent Builder: Threat Hunting | Agent Builder: Detection Rules | Agent Builder: Workflow Authoring | Agent Builder: Triggering Workflows | Agent Builder: Multi-Step Executions | **Overall Agent Builder Score** | **Attack Discovery** | **Automatic Migration** | **Overall Score** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Z.ai GLM 5.2** | 9.00 | 7.00 | 9.00 | 9.00 | 10.00 | 9.00 | 9.00 | **8.90** | 8.60 | 8.85 | **8.78** |
| **Moonshot AI Kimi K3** | 9.00 | 9.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **9.10** | 7.50 | 9.52 | **8.71** |
| **NVIDIA Nemotron 3 Ultra** | 4.00 | 8.00 | 9.00 | 7.00 | 8.00 | 9.00 | 8.00 | **7.40** | 7.20 | 9.42 | **8.01** |
| **NVIDIA Nemotron 3.5 Super VL** | 9.00 | 7.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.90** | 4.80 | 10.00 | **7.90** |
| **Moonshot AI Kimi K2.6** | 7.00 | 7.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.60** | 5.50 | 6.63 | **6.91** |
| **Google Gemma 4 31B IT** | 8.00 | 7.00 | 8.00 | 8.00 | 4.00 | 10.00 | 9.00 | **7.70** | 3.00 | 9.90 | **6.87** |
| **Z.ai GLM 5.3** | 9.00 | 9.00 | 7.00 | 9.00 | 9.00 | 9.00 | 9.00 | **8.70** | 5.50 | 6.15 | **6.78** |
| **OpenAI GPT-OSS 120B** | 5.00 | 6.00 | 8.00 | 8.00 | 9.00 | 8.00 | 5.00 | **7.00** | 2.00 | 9.62 | **6.21** |
| **Mistral Large 4** | 9.00 | 8.00 | 9.00 | 9.00 | 10.00 | 9.00 | 9.00 | **9.00** | 8.70 | 0.00 | **5.90** |
| **DeepSeek V4 Pro** | 8.00 | 5.00 | 9.00 | 9.00 | 8.00 | 9.00 | 9.00 | **8.10** | 6.00 | 3.20 | **5.77** |
| **OpenAI GPT-OSS 20B** | 5.00 | 4.00 | 9.00 | 5.00 | 5.00 | 7.00 | 8.00 | **6.10** | 1.20 | 9.23 | **5.51** |
| **NVIDIA Nemotron 3.5 Lightning** | 5.00 | 6.00 | 8.00 | 5.00 | 6.00 | 10.00 | 5.00 | **6.40** | 2.50 | 6.83 | **5.24** |
| **Alibaba Qwen 3.6 27B** | 7.00 | 8.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.60** | 0.00 | 6.73 | **5.11** |
| **Alibaba Qwen 3.8 2.4T A95B** | 9.00 | 8.00 | 9.00 | 9.00 | 9.00 | 10.00 | 9.00 | **8.90** | 0.00 | 5.48 | **4.79** |
| **NVIDIA Nemotron 3 Nano** | 3.00 | 4.00 | 7.00 | 6.00 | 6.00 | 1.00 | 1.00 | **4.00** | 1.00 | 9.23 | **4.74** |

:::
