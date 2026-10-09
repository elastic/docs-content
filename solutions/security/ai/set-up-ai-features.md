---
navigation_title: Set up AI features
description: Set up what Elastic Security AI features need, including an LLM connector, access controls, the chat experience, the Knowledge Base, and advanced settings.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up AI features [set-up-ai-features]

Before you use {{elastic-sec}} AI features, connect them to a large language model (LLM), control who can use them, and turn on any advanced settings they need. Most features share these steps, and each step links to the requirements for specific features.

## Connect to an LLM [set-up-ai-llm]

AI features need at least one LLM connector. If your subscription or project includes [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md), one might already be available with no setup required. Otherwise, refer to [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md) to add one.

Model performance varies by task. To compare models, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).

## Control access to AI features [set-up-ai-access]

```{applies_to}
serverless: ga
stack: ga 9.2
```

Use the [GenAI and Feature Settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md) pages to manage which connectors and models are available, and to turn AI features on or off.

Each feature also needs its own privileges. For details, refer to the requirements in [AI Assistant for Security](/solutions/security/ai/ai-assistant.md) and to [Attack Discovery privileges](/solutions/security/ai/attack-discovery/grant-access.md).

## Select a chat experience [set-up-ai-chat]

{{elastic-sec}} offers two chat experiences: [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) and [AI Assistant for Security](/solutions/security/ai/ai-assistant.md).

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` {{agent-builder}} is the default. To use AI Assistant instead, switch chat experiences in **GenAI Settings**.
- {applies_to}`stack: preview =9.3` To use {{agent-builder}}, you must [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).

For the differences and switching steps, refer to [Compare Agent Builder and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

## Set up the Knowledge Base [set-up-ai-knowledge-base]

AI Assistant's Knowledge Base gives it extra context, such as internal documentation or threat research. You enable it once in each {{kib}} space, and it requires {{ml}} with a minimum {{ml}} node size of 4 GB. To enable it and add knowledge, refer to [AI Assistant Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

## Turn on advanced settings for Attack Discovery [set-up-ai-advanced-settings]

Some Attack Discovery capabilities need an advanced setting:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [`securitySolution:enableAttackDiscoveryWorkflows`](kibana://reference/advanced-settings.md#kibana-siem-settings): Required to run Attack Discovery from a workflow or from {{agent-builder}}, and to configure alert retrieval, generation, and validation in the **Attacks** view. When you turn it on, users also need [Workflows privileges](/solutions/security/ai/attack-discovery/grant-access.md#attack-discovery-workflows-privileges).
- {applies_to}`stack: preview =9.4` [`securitySolution:enableAlertsAndAttacksAlignment`](kibana://reference/advanced-settings.md#kibana-siem-settings): Required to use the **Attacks** view.

## Feature-specific setup [set-up-ai-feature-specific]

- {applies_to}`serverless: preview` [Elastic AI SOC Engine](/solutions/security/ai/ease/ease-intro.md) is a separate {{sec-serverless}} project type with its own setup steps.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4` To use the [Security MCP App](/solutions/security/mcp-app/elastic-security-mcp-app.md), install it on your own machine.
