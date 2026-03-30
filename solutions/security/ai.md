---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ai-for-security.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-for-security.html
navigation_title: AI for security
description: Learn how Elastic Security uses AI to automate alert triage, accelerate threat investigation, and augment SOC analyst workflows with Attack Discovery, AI Assistant, and Agent Builder.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# AI for security [ai-for-security]

{{elastic-sec}} provides AI-powered tools that help security analysts automate alert triage, accelerate threat investigation, and streamline SOC operations. These tools use large language models (LLMs) to analyze your security data, identify attacks, generate queries, and assist with incident response—reducing mean time to respond and helping your team manage growing alert volumes.

These security-specific AI capabilities build on Elastic's [platform-level AI infrastructure](/explore-analyze/ai-features.md), including [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md) and [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md). This page introduces each security AI tool and helps you find the right starting point for your goals.

## Where to start [where-to-start]

| Your goal | Start here |
|---|---|
| Automatically discover attacks across alerts | [Attack Discovery](/solutions/security/ai/attack-discovery.md) |
| Get AI help with investigation, queries, and incident response | [AI Assistant](/solutions/security/ai/ai-assistant.md) or [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) |
| Deploy an AI-powered SOC on {{sec-serverless}} | [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) |
| Compare LLM performance for security tasks | [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) |
| Walk through AI-driven security workflows end-to-end | [AI use case guides](#ai-use-case-guides) |
| Connect to an LLM provider | [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md) |

## Interactive AI tools [interactive-ai-tools]

The following tools provide interactive, LLM-driven capabilities for security analysts. Each requires at least one working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

### Attack Discovery [attack-discovery-overview]

[Attack Discovery](/solutions/security/ai/attack-discovery.md) uses LLMs to automatically analyze alerts in your environment and surface potential attacks. Rather than requiring you to review alerts individually, Attack Discovery identifies relationships among multiple alerts, maps activity to the MITRE ATT&CK matrix, and suggests which threat actors might be responsible. You can schedule Attack Discovery to run automatically and send notifications through connectors such as Slack, Microsoft Teams, PagerDuty, or email.

### AI chat [ai-chat-overview]

{{elastic-sec}} offers two AI chat experiences: [Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) and [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md). Both provide an LLM-powered chat interface that helps you with alert investigation, incident response, and {{esql}} query generation throughout {{elastic-sec}}, and both provide contextual insights that explain errors and suggest remediation steps.

However, there are several important differences in their capabilities. To learn more and choose which to use, refer to [AI Agent or AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

## Elastic AI SOC Engine [ease-overview]

```{applies_to}
serverless:
  security: preview
```

[Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) is an {{sec-serverless}} project type that provides AI-powered tools to augment your existing SIEM and EDR/XDR platforms. EASE combines Attack Discovery, AI Assistant, and agentless data ingestion in a serverless deployment that you can start using in minutes. It's designed for teams that want to get value from AI-driven security operations quickly, without managing infrastructure.

EASE also offers a [Value report](/solutions/security/ai/ease/ease-value-report.md) that summarizes key security metrics and helps you measure the impact of your AI-powered SOC.

## AI-powered workflow tools [ai-workflow-tools]

In addition to the interactive tools described on this page, {{elastic-sec}} provides several AI-powered tools that automate specific workflows:

- [Automatic Import](/solutions/security/get-started/automatic-import.md): Uses AI to ingest data from sources that don't have prebuilt Elastic integrations, by creating custom integrations with ECS mappings.
- [Automatic Migration](/solutions/security/get-started/automatic-migration.md): Uses AI to translate rules and dashboards from third-party SIEMs into {{elastic-sec}}'s native format, accelerating SIEM migration.
- [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md): Uses AI to identify issues that could prevent {{elastic-defend}} from working as intended, including policy response failures and third-party antivirus conflicts.

## Choose the right LLM [choose-llm]

Most security AI features require at least one working LLM connector. You can use Elastic Managed LLMs, which are available by default with a supported license, or [connect to third-party providers](/explore-analyze/ai-features/llm-guides/llm-connectors.md) such as OpenAI, Amazon Bedrock, Azure OpenAI, or Google Vertex AI. To compare how different models perform across security AI use cases, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).

## AI use case guides [ai-use-case-guides]

The following guides walk you through example workflows that demonstrate how AI Assistant and Attack Discovery work individually and together:

- [Triage alerts](/solutions/security/ai/triage-alerts.md): Use AI Assistant to analyze and triage alerts, including generating investigation reports.
- [Identify, investigate, and document threats](/solutions/security/ai/identify-investigate-document-threats.md): Use Attack Discovery and AI Assistant together to find, investigate, and document potential threats.
- [Generate, customize, and learn about {{esql}} queries](/solutions/security/ai/generate-customize-learn-about-esorql-queries.md): Use AI Assistant to write and understand {{esql}} queries.
- [Use AI Assistant's Knowledge Base to improve response quality](/solutions/security/ai/usecase-knowledge-base-walkthrough.md): Add custom knowledge to AI Assistant to improve the quality and relevance of its responses.

## Related capabilities [related-capabilities]

Several other Elastic capabilities complement the security AI tools described on this page:

- [AI-powered features](/explore-analyze/ai-features.md) provides a complete view of AI capabilities across the Elastic platform, including features for {{observability}} and {{es}}.
- [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md) describes how to control which AI features and connectors are available in your environment.
- [LLM connectors and Elastic Managed LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md) explains how to set up the LLM connections that security AI tools require.
- [Investigation tools](/solutions/security/investigate.md) covers the full range of {{elastic-sec}} investigation tools, many of which integrate with AI chat.
