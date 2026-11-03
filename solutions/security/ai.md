---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ai-for-security.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-for-security.html
navigation_title: AI-assisted operations
description: Learn how Elastic Security uses AI to automate alert triage, accelerate threat investigation, and augment SOC analyst workflows with Agent Builder and Attack Discovery.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# AI-assisted operations [ai-for-security]

{{elastic-sec}} provides AI-powered tools that help security analysts automate alert triage, accelerate threat investigation, and streamline SOC operations. These tools use large language models (LLMs) to analyze your security data, identify attacks, generate queries, and assist with incident response—reducing mean time to respond and helping your team manage growing alert volumes.

These security-specific AI capabilities build on Elastic's [platform-level AI infrastructure](/explore-analyze/ai-features.md), including [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md) and [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md). This page introduces each security AI tool and helps you find the right starting point for your goals.

## Where to start [where-to-start]

| Your goal | Start here |
|---|---|
| Set up AI features for the first time | [Set up AI features](/solutions/security/ai/set-up-ai-features.md) |
| Automatically discover attacks across alerts | [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) |
| Get AI help with investigation, queries, and incident response | {applies_to}`stack: preview =9.3, ga 9.4+` {applies_to}`serverless: ga` [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) |
| Deploy an AI-powered SOC on {{sec-serverless}} | [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) |
| Compare LLM performance for security tasks | [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) |
| Walk through AI-driven security workflows end-to-end | [AI use case guides](#ai-use-case-guides) |
| Connect to an LLM provider | [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md) |
| Install the Security MCP App to open interactive {{elastic-sec}} dashboards in Claude, Cursor, or another AI tool | [Security MCP App](/solutions/security/mcp-app/elastic-security-mcp-app.md) |

## Interactive AI tools [interactive-ai-tools]

The following tools provide interactive, LLM-driven capabilities for security analysts. Each requires at least one working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

### Attack Discovery [attack-discovery-overview]

[Attack Discovery](/solutions/security/ai/attack-discovery/index.md) uses LLMs to automatically analyze alerts in your environment and surface potential attacks. Rather than requiring you to review alerts individually, Attack Discovery identifies relationships among multiple alerts, maps activity to the MITRE ATT&CK matrix, and suggests which threat actors might be responsible. You can schedule Attack Discovery to run automatically and send notifications through connectors such as Slack, Microsoft Teams, PagerDuty, or email.

### AI chat [ai-chat-overview]

{{elastic-sec}} provides an LLM-powered chat interface for alert investigation, incident response, and {{esql}} query generation.

#### {{agent-builder}} [ai-chat-agent-builder]

```{applies_to}
stack: preview =9.3, ga 9.4+
serverless:
  security: ga
```

[{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) is the recommended AI chat experience for {{elastic-sec}}. It adds custom agents, tools, and skills to chat. To move from AI Assistant, follow [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

#### AI Assistant [ai-chat-ai-assistant]

```{applies_to}
stack: ga 9.0-9.5, deprecated 9.6+
serverless:
  security: deprecated
```

The [AI Assistant for Security](/solutions/security/ai/ai-assistant.md) is deprecated and has been replaced by {{agent-builder}}.

## Elastic AI SOC Engine [ease-overview]

```{applies_to}
serverless:
  security: preview
```

[Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) is an {{sec-serverless}} project type that provides AI-powered tools to augment your existing SIEM and EDR/XDR platforms. EASE combines Attack Discovery, {{agent-builder}}, and agentless data ingestion in a serverless deployment that you can start using in minutes. It's designed for teams that want to get value from AI-driven security operations quickly, without managing infrastructure.

EASE also offers a [Value report](/solutions/security/ai/ease/ease-value-report.md) that summarizes key security metrics and helps you measure the impact of your AI-powered SOC.

## AI-powered workflow tools [ai-workflow-tools]

In addition to the interactive tools described on this page, {{elastic-sec}} provides several AI-powered tools that automate specific workflows:

- [Automatic Import](/explore-analyze/ai-features/automatic-import.md): Uses AI to ingest data from sources that don't have prebuilt Elastic integrations, by creating custom integrations with ECS mappings.
- [Automatic Migration](/solutions/security/get-started/automatic-migration.md): Uses AI to translate rules and dashboards from third-party SIEMs into {{elastic-sec}}'s native format, accelerating SIEM migration.
- [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md): Uses AI to identify issues that could prevent {{elastic-defend}} from working as intended, including policy response failures and third-party antivirus conflicts.

## Choose the right LLM [choose-llm]

Most security AI features require at least one working LLM connector. You can use Elastic Managed LLMs, which are available by default with a supported license, or [connect to third-party providers](/explore-analyze/ai-features/llm-guides/llm-connectors.md) such as OpenAI, Amazon Bedrock, Azure OpenAI, or Google Vertex AI. To compare how different models perform across security AI use cases, refer to the [LLM performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md). For the other setup steps, refer to [Set up AI features](/solutions/security/ai/set-up-ai-features.md).

## AI use case guides [ai-use-case-guides]

The following guides walk you through example workflows that demonstrate how AI chat and Attack Discovery work individually and together.

- [Triage alerts](/solutions/security/ai/triage-alerts.md): Use AI chat to analyze and triage alerts, including generating investigation reports.
- [Identify, investigate, and document threats](/solutions/security/ai/identify-investigate-document-threats.md): Use Attack Discovery and AI chat together to find, investigate, and document potential threats.
- [Generate, customize, and learn about {{esql}} queries](/solutions/security/ai/generate-customize-learn-about-esorql-queries.md): Use AI chat to write, run, and understand {{esql}} queries.
- {applies_to}`stack: preview =9.3, ga 9.4+` {applies_to}`serverless: ga` [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md): Example prompts for each built-in Security skill.
- {applies_to}`stack: preview =9.3, ga 9.4+` {applies_to}`serverless: ga` [Replace knowledge base content](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#replace-knowledge-base-content): Give {{agent-builder}} the context that you would keep in an AI Assistant Knowledge Base.

## Related capabilities [related-capabilities]

Several other Elastic capabilities complement the security AI tools described on this page:

- [AI-powered features](/explore-analyze/ai-features.md) provides a complete view of AI capabilities across the Elastic platform, including features for {{observability}} and {{es}}.
- [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md) describes how to control which AI features and connectors are available in your environment.
- [LLM connectors and Elastic Managed LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md) explains how to set up the LLM connections that security AI tools require.
- [Investigation tools](/solutions/security/investigate.md) covers the full range of {{elastic-sec}} investigation tools, many of which integrate with AI chat.
