---
navigation_title: "Chat"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# {{agent-builder}}: Agent Chat

**Agent Chat** is the chat interface for natural language conversations with your [agents](agent-builder-agents.md).

The chat GUI and programmatic interfaces enable real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents.

% TODO: Uncomment once page is live.
<!-- :::{note}
The chat UI is available in both standalone and flyout modes. For more information, refer to [Chat UI modes](standalone-and-flyout-modes.md).
::: -->

## Get started

:::{tip}
Refer to the [getting started](get-started.md) guide to enable the feature and ingest some data.
:::

Once the feature is enabled, find **Agents** in the navigation menu to begin chatting.
You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

This takes you to the chat GUI:

:::{image} images/agent-builder-chat-UI-get-started.png
:screenshot:
:alt: The main Agent Chat GUI showing the chat window, message input box, and agent selection panel
:::

## Agent Chat GUI

### Chat and select agent

Use the text input area to chat with an agent in real time. By default, you chat with the built-in Elastic AI Agent.

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
:alt: Agent selector dropdown and message input field
:width: 650px
:::

#### Select a different model
```{applies_to}
stack: ga 9.3+
```

Use the model selector to switch the underlying [model](models.md) the agent uses to generate responses. Switch models to prioritize faster responses, lower costs, or more complex reasoning, depending on your use case.

:::{image} images/model-selector.png
:alt: Image description
:width: 650px
:screenshot:
:::

### Access key actions
```{applies_to}
stack: ga 9.3+
```

This menu is your hub for key management actions. You can quickly access important pages from here.

:::{image} images/more-actions.png
:screenshot:
:alt: More actions menu button
:width: 150px
:::

This opens a panel with links to key actions and management pages including agent, tool, and settings management.

:::{image} images/more-actions-menu-options.png
:screenshot:
:alt: The expanded more options menu panel
:width: 250px
:::

### Find conversation history

Use the chat history panel to access previous conversations.

:::{image} images/agent-builder-chat-history.png
:screenshot:
:alt: Chat history panel showing conversation list
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

## Agent Chat API

The Agent Chat API provides programmatic access to chat functionality through REST endpoints.

### Quick overview

For a quick overview of the REST API for conversations, refer to [Chat and conversations API](kibana-api.md#chat-and-conversations).

### API reference

For the complete API reference, refer to the [{{kib}} API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-conversations).






