---
navigation_title: Set up AI features
description: Set up the LLM access and privileges that Elastic Security AI features need, plus optional settings such as the chat experience, the Knowledge Base, and Agent Builder documentation.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up AI features [set-up-ai-features]

{{elastic-sec}} AI features need access to a large language model (LLM), and users need privileges for the features they use. Complete this required setup first. The rest of the page is optional or applies only to specific features, so do only the steps for the features you plan to use.

## Required setup [set-up-ai-required]

### Connect to an LLM [set-up-ai-llm]

AI features need access to at least one LLM. If your subscription or project includes [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md), one might already be available with no setup required. Otherwise, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md) to connect one.

Model performance varies by task. To compare models, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).

### Grant privileges [set-up-ai-privileges]

Each user needs privileges for the AI features they use. For the privileges that each feature needs, refer to:

- AI Assistant: [AI Assistant for Security requirements](/solutions/security/ai/ai-assistant.md)
- Attack Discovery: [Attack Discovery privileges](/solutions/security/ai/attack-discovery/grant-access.md)
- {{agent-builder}}: [Permissions and access control in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/permissions.md)

## Optional and feature-specific setup [set-up-ai-optional]

### Manage available models and features [set-up-ai-access]

```{applies_to}
serverless: ga
stack: ga 9.2+
```

This step is optional, because AI features work with the default settings. Use the [GenAI and Feature Settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md) pages to manage which connectors and models are available, and to turn AI features on or off.

### Select a chat experience [set-up-ai-chat]

```{applies_to}
serverless: ga
stack: preview =9.3, ga 9.4+
```

Skip this step unless you want to use a chat experience other than the default. {{elastic-sec}} offers two chat experiences: [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) and [AI Assistant for Security](/solutions/security/ai/ai-assistant.md). You select one for each space in **GenAI Settings**, and the other one isn't available in that space.

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` {{agent-builder}} is the default. To use AI Assistant instead, switch chat experiences in **GenAI Settings**.
- {applies_to}`stack: preview =9.3` AI Assistant is the default. To use {{agent-builder}}, you must [opt in](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md#switch-between-chat-experiences).

For the differences and switching steps, refer to [Compare Agent Builder and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

### Install documentation for {{agent-builder}} [set-up-ai-agent-builder-docs]

```{applies_to}
serverless: ga
stack: preview =9.3, ga 9.4+
```

This step is optional and applies only to {{agent-builder}}. Elastic documentation and Security Labs content give {{agent-builder}} more context for its answers, and installed content is available in every space. To check whether the content is installed, or to install it, refer to [Give {{agent-builder}} access to Elastic documentation](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation).

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` {{kib}} can install this content automatically, so it might already be installed.

### Set up the Knowledge Base [set-up-ai-knowledge-base]

This step is optional and applies only to AI Assistant. The Knowledge Base gives AI Assistant extra context, such as internal documentation or threat research. {{agent-builder}} doesn't use the Knowledge Base. To give {{agent-builder}} more context, [install documentation](#set-up-ai-agent-builder-docs) instead.

You enable the Knowledge Base once in each {{kib}} space, and it requires {{ml}} with a minimum {{ml}} node size of 4 GB. If {{agent-builder}} is the chat experience in the space, [switch to AI Assistant](#set-up-ai-chat) first, because AI Assistant's settings aren't available until you do. To enable the Knowledge Base and add knowledge, refer to [AI Assistant Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

### Turn on advanced settings for Attack Discovery [set-up-ai-advanced-settings]

Skip this step unless you use one of the following Attack Discovery capabilities, which each need an advanced setting:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` [`securitySolution:enableAttackDiscoveryWorkflows`](kibana://reference/advanced-settings.md#kibana-siem-settings): Required to run Attack Discovery from a workflow or from {{agent-builder}}, and to configure alert retrieval, generation, and validation in the **Attacks** view. When you turn it on, users also need [Workflows privileges](/solutions/security/ai/attack-discovery/grant-access.md#attack-discovery-workflows-privileges).
- {applies_to}`stack: preview =9.4` [`securitySolution:enableAlertsAndAttacksAlignment`](kibana://reference/advanced-settings.md#kibana-siem-settings): Required to use the **Attacks** view.

### Features with their own setup [set-up-ai-feature-specific]

- {applies_to}`serverless: preview` [Elastic AI SOC Engine](/solutions/security/ai/ease/ease-intro.md) is a separate {{sec-serverless}} project type with its own setup steps.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4` To use the [Security MCP App](/solutions/security/mcp-app/elastic-security-mcp-app.md), install it on your own machine.
