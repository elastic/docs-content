---
navigation_title: "Agent Chat UI"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

# {{agent-builder}}: Agent Chat

**Agent Chat** is the synchronous chat interface for natural language conversations with your agents.

The chat GUI and programmatic interfaces enable real-time communication where you can ask questions, request data analysis, and receive immediate responses from your configured agents.

## Get started

:::{tip}
Refer to the [getting started](get-started.md) guide to enable the feature and ingest some data.
:::

Once the feature is enabled, find **Agents** in the navigation menu to start chatting.
You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

This will take you to the chat GUI:

:::{image} images/agent-builder-chat-UI-get-started.png
:::
:alt: The main Agent Chat GUI showing the chat window, message input box, and agent selection panel

## Agent Chat GUI

### Chat and select agent

Use the text input area to chat with an agent in real time. By default, you'll be chatting with the built-in Elastic AI Agent.

:::{image} images/agent-builder-chat-input.png
:alt: Text input area for chatting with agents
:width: 850px
:::

#### Agent selector

Use the agent selector to switch agents, to navigate to the agent management section, or to create a new agent.

:::{image} images/agent-builder-agent-selector.png
:alt: Agent selector dropdown and message input field
:width: 850px
:::

### Find conversation history

The left sidebar shows your conversation history, so you can easily access all your conversations.

:::{image} images/agent-builder-chat-history.png
:alt: Chat history panel showing conversation list
:width: 250px
:::

## Agent Chat API

The Agent Chat API provides programmatic access to chat functionality through REST endpoints.

### Quick overview

For a quick overview of the programmtic interfaces for conversations, refer to [Chat and conversations API](kibana-api.md#chat-and-conversations).

### Serverless API reference

For the complete API reference, see the [Kibana serverless API reference](https://www.elastic.co/docs/api/doc/serverless/). 








