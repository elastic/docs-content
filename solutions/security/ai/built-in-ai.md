---
navigation_title: Built-in AI
description: AI features built into Elastic Security, including Elastic AI SOC Engine, Agent Builder, AI Assistant, and Attack Discovery, plus guided use cases.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Built-in AI features in {{elastic-sec}} [built-in-ai]

These AI features run inside {{elastic-sec}} and work directly with your security data. Most of them require at least one working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md). For an introduction to each feature and help choosing a starting point, refer to [AI for security](/solutions/security/ai.md).

| Feature | What it does |
|---|---|
| [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) | An {{sec-serverless}} project type that combines Attack Discovery, AI Assistant, and agentless data ingestion to augment your existing SIEM and EDR/XDR platforms. |
| [{{agent-builder}} for {{elastic-sec}}](/solutions/security/ai/agent-builder/agent-builder.md) | An LLM-powered chat experience for alert investigation, incident response, and {{esql}} query generation, extensible with custom skills. |
| [AI Assistant for Security](/solutions/security/ai/ai-assistant.md) | An LLM-powered chat experience for alert investigation, incident response, and {{esql}} query generation, with a Knowledge Base you can add custom context to. |
| [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) | Analyzes alerts in your environment to surface potential attacks, maps activity to the MITRE ATT&CK matrix, and can run on a schedule. |
| [AI use cases](/solutions/security/ai/use-cases.md) | Guided workflows that show how AI Assistant and Attack Discovery work individually and together. |
| [Value report](/solutions/security/ai/ease/ease-value-report.md) | Summarizes key security metrics to help you measure the impact of your AI-powered SOC. |

To compare how different models perform across these features, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md). To use {{elastic-sec}} from an AI tool outside {{kib}}, refer to [External AI access](/solutions/security/ai/external-ai-access.md).
