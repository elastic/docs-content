---
navigation_title: "Chat"
description: "Learn how to chat with AI agents in Agent Builder, inspect reasoning steps, and manage conversation history through the UI or API."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Chat with {{agent-builder}} agents

**Agent Chat** is the chat interface for natural language conversations with your [agents](agent-builder-agents.md).

The chat GUI and programmatic interfaces enable real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents.

:::{note}
The chat UI is available in both standalone and flyout modes. For more information, refer to [Chat UI modes](standalone-and-flyout-modes.md).
:::

## Get started

:::{tip}
Refer to the [getting started](get-started.md) guide if you need to enable the feature and ingest some data.
:::

Find **Agents** in the navigation menu to begin chatting.
You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

This takes you to the chat GUI:

:::{image} images/agent-builder-chat-UI-get-started.png
:screenshot:
:alt: Annotated screenshot of the Agent Chat GUI with numbered callouts highlighting the chat input (1), agent selector (2), model selector (3), chats panel (4), options menu (5), customize accordion (6), and manage components link (7)
:::

1. [Chat input area](#start-a-chat-and-select-an-agent)
2. [Agent selector](#select-a-different-agent)
3. [Model selector](#select-a-different-model)
4. [Chats (conversation history)](#find-conversation-history)
5. [Options menu](#access-key-actions)
6. [Customize accordion](#customize-your-agent)
7. [Manage components link](#manage-components)

## Agent Chat GUI

### Start a chat and select an agent

Use the text input area to chat with an agent in real time. Check the agent selector to see which agent is active. To switch agents, refer to [Select a different agent](#select-a-different-agent).

:::{image} images/agent-builder-chat-input.png
:screenshot:
:alt: Text input area for chatting with agents
:width: 650px
:::

:::{note}
Conversations with agents consume tokens. To understand how usage is calculated, refer to [Token usage in Elastic Agent Builder](monitor-usage.md).
:::

#### Select a different agent

```{applies_to}
stack: ga 9.3+
```

Use the agent selector to switch agents, to navigate to the agent management section, or to create a new agent. An agent's behavior is defined by its custom instructions and available tools. Switch agents when you need different capabilities for your tasks.

:::{image} images/agent-builder-agent-selector.png
:screenshot:
:alt: Agent selector dropdown showing available agents with options to create or manage agents
:width: 650px
:::

#### Select a different model

```{applies_to}
stack: ga 9.3+
```

Use the model selector to switch the underlying [model](models.md) the agent uses to generate responses. Switch models to prioritize faster responses, lower costs, or more complex reasoning, depending on your use case.

:::{image} images/model-selector.png
:alt: Model selector dropdown showing available models
:width: 650px
:screenshot:
:::

### Options menu [access-key-actions]

```{applies_to}
stack: ga 9.3+
```

Click the three-dot menu icon in the top-right corner to access additional options.

:::{image} images/more-actions.png
:screenshot:
:alt: Three-dot menu icon for additional options
:width: 150px
:::

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

The options menu provides access to:

- **Agent details**: View information about the currently selected agent.
- **GenAI Settings**: Open the global GenAI settings page to configure default connectors and other AI settings.

:::{image} images/more-actions-menu-options-9.4.png
:screenshot:
:alt: Options menu showing Agent details and GenAI Settings
:width: 250px
:::


:::{tip}
To manage agents and tools, use the [**Manage components**](#manage-components) link at the bottom of the left sidebar, or the [**Customize**](#customize-your-agent) accordion to configure the current agent.
:::

::::

::::{applies-item} { stack: ga =9.3 }

This menu provides links to key actions and management pages, including agent management, tool management, agent editing, and duplication.

:::{image} images/more-actions-menu-options.png
:screenshot:
:alt: Options menu showing agent management, tool management, agent editing, and duplication
:width: 250px
:::

::::

:::::

### Find conversation history

Use the chat history panel to access previous conversations.

:::{image} images/agent-builder-chat-history.png
:screenshot:
:alt: Search chats panel with search field and conversation list
:width: 450px
:::

### Inspect tool calls and reasoning

Expand the **Reasoning** section to see how the agent handles your request. This provides a detailed breakdown of the agent's reasoning steps, the tool calls it makes, and the responses it receives. The agent runs tools in a loop until it achieves its goal or [exceeds the maximum conversation length](limitations-known-issues.md#conversation-length-exceeded).

:::{image} images/reasoning-steps.png
:screenshot:
:alt: Reasoning panel showing tool calls and execution steps
:width: 650px
:::

Select **Inspect response** to view detailed information about individual tool calls and responses.

Select **View JSON** to view the full raw response data. For more information, refer to [Monitor token usage](monitor-usage.md).

### Review and confirm agent changes
```{applies_to}
stack: ga 9.4+
```

You control every write operation an agent performs. Whenever an agent proposes to create, update, or delete a resource, the chat pauses and presents a preview before anything takes effect. The preview format and available actions depend on the skill the agent is using.

No changes are applied until you explicitly confirm or dismiss.

:::{image} images/agent-builder-preview-changes.png
:screenshot:
:alt: Preview panel showing proposed changes from an agent action before they are applied.
:width: 700px
:::

## Customize your agent [customize-your-agent]

```{applies_to}
stack: ga 9.4+
```

The **Customize** accordion in the left sidebar provides agent-scoped configuration for the currently selected agent. Expand it to access the following pages:

**Overview**
:   Displays a summary of the selected agent, including the total count of assigned skills and tools. Use the quick links to edit the agent's instructions or settings.

**Skills**
:   Lists the skills assigned to the current agent. Click a skill to open a read-only detail panel on the right side. To assign new skills, click **Add skill**. To view and manage all skills across the deployment, click **Manage all skills**. Skills you import into the library must be turned on with their toggle in this list before the agent can use them. For how skills work and how to manage them, refer to [Skills in {{agent-builder}}](skills.md).

**Plugins**
:   Lists the plugins assigned to the current agent. 

**Tools**
:   Lists the [tools](tools.md) assigned to the current agent. Click a tool to open a read-only detail panel. To assign new tools, click **Add tool**. To view and manage all tools, click **Manage all tools**.

:::{image} images/customize-your-agent-accordion.png
:alt: Customize accordion open
:width: 200px
:::

## Manage components [manage-components]

```{applies_to}
stack: ga 9.4+
```

The **Manage components** link at the bottom of the left sidebar exits the single-agent view. It provides an overview of all agents, skills, plugins, connectors, and tools available across the deployment.

**Agents**
:   View all agents in the deployment. The list displays each agent's name, visibility badge (**Public**, **Shared**, or **Read-only**), and any custom labels. From this page, you can create new agents, edit existing ones, or start a chat.

**Skills**
:   View and manage all skills available in the deployment. Create new skills or edit existing ones.

**Plugins**
:   View and install plugins for the deployment so you can assign their bundled skills and capabilities to agents.

**Connectors**
:   View and manage {{kib}} connectors for GenAI and related features, including LLM providers and other integrations agents and tools use.

**Tools**
:   View and manage all tools. The global Tools page includes a search bar, **Labels** filter, **Manage MCP** dropdown, **Manage agents** link, and **+ New tool** button.

:::{image} images/manage-components.png
:alt: Manage component menu
:width: 350px
:::

:::{tip}
You can also reach the global agents list from the **Manage agents** button in the [agent selector](#select-a-different-agent) dropdown.
:::

## Dashboards and visualizations

Agents can create and manage dashboards and visualizations directly in the conversation. To learn more, refer to [Dashboards and visualizations in chat](agent-builder-dashboards-and-visualizations.md).

## Agent Chat API

The Agent Chat API provides programmatic access to chat functionality through REST endpoints.

### Quick overview

For a quick overview of the REST API for conversations, refer to [Chat and conversations API](kibana-api.md#chat-and-conversations).

### API reference

For the complete API reference, refer to the [{{kib}} API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-conversations).
