---
navigation_title: Migrate to Agent Builder
description: Switch from the AI Assistant to Agent Builder and find where AI Assistant features live in Agent Builder.
applies_to:
  stack: ga 9.4+, preview 9.3
  serverless: ga
products:
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Migrate from AI Assistant to Agent Builder

::::{admonition} Requirements
These features require the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).

To change the chat experience, you need the {{kib}} privileges listed in [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#requirements).

The chat experience switch appears when you have access to at least one classic AI assistant and either the **Agent Builder: All** privilege or, {applies_to}`stack: ga 9.4+`, **Agent Builder: Read** plus **Create and edit agents**. For details, refer to [{{agent-builder}} permissions](/explore-analyze/ai-features/agent-builder/permissions.md).
::::

[{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) replaces AI Assistant. The {{obs-ai-assistant}} is deprecated from {{stack}} 9.4. AI Assistant for Security is generally available through 9.5 and deprecated from 9.6. In {{serverless-short}}, both are deprecated.

Switching changes the chat experience only. It doesn't migrate your AI Assistant conversations, prompts, or knowledge base entries, and {{agent-builder}} can't access them. Use the [feature replacements](#feature-differences-between-agent-builder-and-ai-assistant) to re-create what you need.

## Switch to Agent Builder [switch-between-chat-experiences]

- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Agent Builder is the default chat experience for all solutions.
- {applies_to}`stack: ga =9.3` Agent Builder is the default for {{es}} solution users. {{product.observability}} and {{product.security}} solution users can switch to Agent Builder to opt in.

{{kib}} might prompt you to switch when your deployment supports it and you have sufficient privileges. You can also switch at any time:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).
2. Under **Chat Experience**, select **AI Agent**.
3. Select **Save changes**.

{applies_to}`stack: preview =9.3, ga 9.4+` {applies_to}`serverless: ga` When the switch succeeds, the **AI Agent** button in the {{kib}} header opens {{agent-builder}} instead of AI Assistant. To start using it, refer to [Get started with {{agent-builder}}](/explore-analyze/ai-features/agent-builder/get-started.md).

:::{tip}
For connectors and tested models, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md). To learn about the chat UI modes, refer to [](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md).
:::

## Find AI Assistant features in Agent Builder [feature-differences-between-agent-builder-and-ai-assistant]

Most AI Assistant features have an {{agent-builder}} equivalent. Availability varies by version. Features labeled {{elastic-sec}} or {{observability}} exist only in that solution's AI Assistant.

| AI Assistant feature | In Agent Builder |
| :--- | :--- |
| **Chat sharing and duplication** | {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Only the owner of a conversation can [share it](/explore-analyze/ai-features/agent-builder/chat.md#share-a-conversation), with specific users or publicly. Members can continue a shared conversation. Duplication isn't available. |
| **Chat archiving**<br>({{observability}}) | Not available. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [Pin conversations](/explore-analyze/ai-features/agent-builder/chat.md#pin-conversations) instead. |
| **Data anonymization** | {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` Open **Stack Management**, then select **Anonymization** in the **AI** section. This page requires an [Enterprise](https://www.elastic.co/pricing) license, **Advanced Settings: All**, and **Actions and Connectors** access. For details, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-management). Anonymization doesn't mask data that you send directly to a connector. |
| **Knowledge base** | Partial. Refer to [Replace knowledge base content](#replace-knowledge-base-content). |
| **Alerting rule connector action**<br>({{observability}}) | {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Partial. Use an [action policy to run a workflow](/explore-analyze/alerting/esql/workflows-alerting.md) that calls an agent with the [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) step. |
| **Audit logging** | {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Partial. {{kib}} records audit events when agents, tools, and skills are created, updated, or deleted. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` {{kib}} also records when a conversation is created. |
| **Citations**<br>({{elastic-sec}}) | {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Available. |
| **In-chat previews of attached data**<br>({{elastic-sec}}) | Not available. |
| **Quick prompts**<br>({{elastic-sec}}) | {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Partial. Use [skills](/explore-analyze/ai-features/agent-builder/skills.md) and invoke them with slash commands. |

{{agent-builder}} also adds [custom agents](/explore-analyze/ai-features/agent-builder/custom-agents.md), [custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md), and [integration with Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md).

### Replace knowledge base content [replace-knowledge-base-content]

{{agent-builder}} has no dedicated knowledge base UI. Use these equivalents for what you stored in AI Assistant:

| AI Assistant knowledge base feature | In Agent Builder |
| :--- | :--- |
| Elastic product documentation | Install **Elastic documentation** from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation). {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` {{kib}} installs it automatically when [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) is available and **Use AI features** is turned on. |
| Security Labs articles<br>({{elastic-sec}}) | Install **Security labs** from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation). |
| Indices and content connector indices | Create an [index search tool](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md) for the index and assign it to your agent. |
| Markdown entries created in the settings UI | Index the content yourself, then create an [index search tool](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md). |
| "Remember this" in chat | {applies_to}`stack: experimental 9.6` {applies_to}`serverless: experimental` Not a direct replacement. [{{context-engine}} memories](/explore-analyze/ai-features/context-engine/save-and-retrieve-memories.md) need {{context-engine}} turned on and a memory-enabled AI index assigned to your agent. |
| Required knowledge and retrieval on every prompt | Add the knowledge to your [custom agent's instructions](/explore-analyze/ai-features/agent-builder/custom-agents.md). The agent decides when to call a tool, so include guidance if it should search specific knowledge regularly. |

## API differences between Agent Builder and AI Assistant

Each AI chat experience has different APIs. To learn which actions each option supports, refer to:

- [Agent Builder]({{kib-apis}}group/endpoint-agent-builder)
- [AI Assistant for Security]({{kib-apis}}group/endpoint-security-ai-assistant-api)
- [AI Assistant for Observability]({{kib-apis}}group/endpoint-observability_ai_assistant)
