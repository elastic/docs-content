---
navigation_title: Set up AI features
description: Set up the LLM access and privileges that Elastic Security AI features need, plus optional settings such as the chat experience, the Knowledge Base, and Agent Builder documentation.
applies_to:
  serverless:
    security: all
  stack: all
products:
  - id: security
  - id: cloud-serverless
---

# Set up AI features [set-up-ai-features]

This page explains how to set up {{elastic-sec}} AI features. It covers the required setup, optional setup that control which models and chat experience are available, and setup that applies only to specific features.

## Required setup [set-up-ai-required]

{{elastic-sec}} AI features require a connection to a large language model (LLM), and users need privileges for the features they use.
### Connect to an LLM [set-up-ai-llm]

If your subscription or project feature tier includes [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md), they're available by default with no setup required. To connect a different LLM, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

Model performance varies by task. To compare models, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md).

### Grant privileges [set-up-ai-privileges]

For the privileges that each feature needs, refer to:

- AI Assistant: [AI Assistant for Security requirements](/solutions/security/ai/ai-assistant.md)
- Attack Discovery: [Attack Discovery privileges](/solutions/security/ai/attack-discovery/grant-access.md)
- {{agent-builder}}: [Permissions and access control in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/permissions.md)

## Optional setup [set-up-ai-optional]

AI features work with their default settings. Change them to control which models and features are available, or which chat experience each space uses.

### Manage available models and features [set-up-ai-access]

```{applies_to}
serverless: ga
stack: ga 9.2+
```

To limit which connectors and models AI features can use, or to turn AI features off, go to **Feature Settings** or **GenAI Settings** (depending on your {{stack}} version). For details, refer to [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

### Switch chat experiences [set-up-ai-chat]

```{applies_to}
serverless: ga
stack: preview =9.3, ga 9.4+
```

Each space uses one of two chat experiences for all its users, either [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) or [AI Assistant for Security](/solutions/security/ai/ai-assistant.md). The other experience isn't available in that space. To change which experience a space uses, switch chat experiences in **GenAI Settings**. For the default experience in each version and the feature differences, refer to [Compare Agent Builder and AI Assistant](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).

## Feature-specific setup [set-up-ai-by-feature]

The following sections apply to specific features. Only use them if you plan to set up the feature it covers.

### Install documentation for {{agent-builder}} [set-up-ai-agent-builder-docs]

```{applies_to}
serverless: ga
stack: preview =9.3, ga 9.4+
```

To give {{agent-builder}} more context for its answers, install Elastic documentation and Security Labs content. Installed content is available in every space.

To check whether the content is already installed, or to install it, refer to [Give {{agent-builder}} access to Elastic documentation](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation).

### Set up the Knowledge Base [set-up-ai-knowledge-base]

The Knowledge Base gives AI Assistant more context, such as your internal documentation or threat research. {{agent-builder}} doesn't use the Knowledge Base.

The Knowledge Base requires a {{ml}} node of at least 4 GB. If {{agent-builder}} is the chat experience in the space, [switch to AI Assistant](#set-up-ai-chat) first, because AI Assistant settings aren't available until you do. Then enable the Knowledge Base in each {{kib}} space where you want to use it. For steps to enable it and add knowledge, refer to [AI Assistant Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md#enable-knowledge-base).

### Turn on Attack Discovery workflows [set-up-ai-advanced-settings]

```{applies_to}
serverless: ga
stack: ga 9.5+
```

To run Attack Discovery from a workflow or from {{agent-builder}}, turn on the [`securitySolution:enableAttackDiscoveryWorkflows`](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting. This setting also lets you configure alert retrieval, generation, and validation in the **Attacks** view. After you turn it on, users also need [Workflows privileges](/solutions/security/ai/attack-discovery/grant-access.md#attack-discovery-workflows-privileges).

### Features with their own setup [set-up-ai-feature-specific]

Some features need a separate project or a local install:

- {applies_to}`serverless: preview` To use [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md), create an EASE project, which is a separate {{sec-serverless}} project type.
- To use the [Security MCP App](/solutions/security/mcp-app/elastic-security-mcp-app.md), install it on your own machine.
