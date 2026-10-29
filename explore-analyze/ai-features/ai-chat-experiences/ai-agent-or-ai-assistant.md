---
navigation_title: Migrate to Agent Builder
description: Switch from the deprecated AI Assistant chat experience to Agent Builder, and find Agent Builder equivalents for AI Assistant features.
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
::::

[{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) is the chat experience that replaces AI Assistant. It includes built-in agents and [tools](/explore-analyze/ai-features/agent-builder/tools.md) for common use cases, and lets you create custom agents, tools, and [skills](/explore-analyze/ai-features/agent-builder/skills.md) for your needs.

- {applies_to}`stack: deprecated 9.4+` {applies_to}`serverless: deprecated` The {{obs-ai-assistant}} is deprecated.
- {applies_to}`stack: deprecated 9.6+` {applies_to}`serverless: deprecated` AI Assistant for Security is deprecated.

Both assistants still work, but they won't get new features. Use this page to switch to {{agent-builder}} and find Agent Builder equivalents for the AI Assistant features you rely on.

There is no chat history migration path. Agent Builder cannot access your chats, prompts, or knowledge base entries from AI Assistant. That data remains available if you switch back.

## Switch to Agent Builder [switch-between-chat-experiences]

Each {{kib}} space uses one chat experience for all of its users: **AI Agent** (Agent Builder) or **Classic AI Assistant**.

- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Agent Builder is the default chat experience for all solutions.
- {applies_to}`stack: preview =9.2, ga =9.3` Agent Builder is the default for {{es}} solution users. {{product.observability}} and {{product.security}} solution users can switch to Agent Builder to opt in.

{{kib}} might prompt you to switch to Agent Builder when your deployment supports it and you have sufficient privileges. You can also switch at any time:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).
2. Under **Chat experience**, select **AI Agent** or **Classic AI Assistant**.
3. Select **Save changes**.

:::{tip}
For connectors and tested models, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
:::

To learn more about the chat UI modes, refer to [](/explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md).

## Find AI Assistant features in Agent Builder [feature-differences-between-agent-builder-and-ai-assistant]

Use the tables below to find an Agent Builder equivalent for each AI Assistant feature. Availability varies by version. Features marked with an earlier version badge aren't available in that version of Agent Builder.

Agent Builder also adds capabilities that AI Assistant doesn't have, including [use-case specific skills](/explore-analyze/ai-features/agent-builder/skills.md), [custom agents](/explore-analyze/ai-features/agent-builder/custom-agents.md), [custom tools](/explore-analyze/ai-features/agent-builder/tools/custom-tools.md), and [integration with Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md).

::::{tab-set}
:group: chat-migration-group

:::{tab-item} {{elastic-sec}}
:sync: tab1

| AI Assistant feature | In Agent Builder |
| :--- | :--- |
| **Knowledge base** | Partial. Refer to [Replace knowledge base content](#replace-knowledge-base-content). |
| **Data anonymization** | {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` Available as a technical preview. Configure it in **Stack Management** → **AI** → **Anonymization**. |
| **Time awareness** | {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Available. |
| **Chat sharing** | {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [Share a conversation](/explore-analyze/ai-features/agent-builder/chat.md#share-a-conversation) with specific users or make it public. Members can continue the conversation, ask their own questions, and see answers to each other's questions. In AI Assistant for Security, recipients could only read a shared conversation. |
| **Chat duplication** | Not needed. Members can continue a shared conversation directly. |
| **Citations** | {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Available. |
| **Audit logging** | {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Available. Agent Builder writes audit events for creating, updating, and deleting agents, tools, and skills, and for creating conversations. |
| **Quick prompts** | Partial. Use [skills](/explore-analyze/ai-features/agent-builder/skills.md) and slash commands that invoke a skill directly (for example, `/threat-hunting`). |
| **In-chat previews of attached data** | Not available. |
| **AI insights** | Available. |

:::

:::{tab-item} Elastic {{observability}} and Search
:sync: tab2

| AI Assistant feature | In Agent Builder |
| :--- | :--- |
| **Knowledge base** | Partial. Refer to [Replace knowledge base content](#replace-knowledge-base-content). |
| **Data anonymization** | {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` Available as a technical preview. Configure it in **Stack Management** → **AI** → **Anonymization**. |
| **Chat sharing** | {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [Share a conversation](/explore-analyze/ai-features/agent-builder/chat.md#share-a-conversation) with specific users or make it public. Members can continue the conversation, ask their own questions, and see answers to each other's questions. |
| **Chat duplication** | Not available. Members of a shared conversation can continue it directly, so duplication isn't needed for collaboration. |
| **Chat archiving** | Not available. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [Pin conversations](/explore-analyze/ai-features/agent-builder/chat.md) instead. |
| **Alerting rule connector action** | Partial. Use an action policy in Universal Alerting to run a workflow that calls an agent with the [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) step. |
| **AI insights** | Available. |

:::

::::

### Replace knowledge base content [replace-knowledge-base-content]

Agent Builder has no dedicated knowledge base UI. Use the following equivalents for the knowledge you previously stored in AI Assistant:

| AI Assistant knowledge base feature | In Agent Builder |
| :--- | :--- |
| Elastic product documentation | Install **Elastic documentation** from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation). {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` {{kib}} installs it automatically when [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) is available and **Use AI features** is turned on. |
| Security Labs articles | Install **Security labs** from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#give-agent-builder-access-to-elastic-documentation). |
| Indices as knowledge sources | Create an [index search tool](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md) for the index and assign it to your agent. |
| Content connector indices | Create an [index search tool](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md) for those indices and assign it to your agent. |
| Markdown entries created in the settings UI | Index the content yourself, then create an [index search tool](/explore-analyze/ai-features/agent-builder/tools/index-search-tools.md). There's no dedicated UI for markdown knowledge entries. |
| "Remember this" in chat | Context Engine memories are experimental in 9.6. |
| Required knowledge (always included in the prompt) | Add the content to your [custom agent's instructions](/explore-analyze/ai-features/agent-builder/custom-agents.md). |
| Retrieval on every prompt | The agent decides when to call a tool. Include guidance in the agent's instructions if you want it to search specific knowledge regularly. |

## API differences between Agent Builder and AI Assistant

Each AI chat experience has different APIs. To learn which actions each option supports, refer to:

- [Agent Builder]({{kib-apis}}group/endpoint-agent-builder)
- [AI Assistant for Security]({{kib-apis}}group/endpoint-security-ai-assistant-api)
- [AI Assistant for Observability]({{kib-apis}}group/endpoint-observability_ai_assistant)
