---
navigation_title: "Agents"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

# {{agent-builder}}: Agents

Agents are AI models (LLMs) defined with custom instructions and a set of assigned [tools](tools.md). Users [chat](chat.md) with agents using natural language, in the Agent Builder UI or programmatically.

An agent parses user requests to define a goal and then runs tools in a loop to achieve that goal. The agent provides responses based on its configured tools, instructions, and behavior settings.

## How agents work

When you ask a question to an agent, it analyzes your request to define a specific goal. It selects the most appropriate tools and determines the right arguments to use. The agent evaluates the information returned after each action and decides whether to use additional tools or formulate a response. This iterative process of tool selection, execution, and analysis continues until the agent can provide a complete answer.

{{agent-builder}} includes a default agent (named `Elastic AI Agent`) with access to all built-in tools. You can create specialized agents with custom instructions and selected tools to address specific use cases or workflows.

:::{note}
The default `Elastic AI Agent` is immutable and cannot be edited. To customize agent behavior, you need to create a custom agent by cloning the default agent or creating a new one from scratch.
:::

## Manage your agents

The **Agents** page provides a centralized view of all your agents. From this page you can:

- View all your agents with their names and labels.
- Search for specific agents using the search bar.
- Filter agents by labels using the **Labels** dropdown.
- Create new agents using the **+ New agent** button.
- Start chatting with an agent or perform other actions:
    - **Elastic AI Agent**: you can **chat** or **clone** the default agent using the chat or clone buttons. The default agent cannot be edited directly.
      :::{image} images/chat-and-clone-buttons.png
      :alt: Chat with agent and clone agent buttons
      :width: 120px
      :::
    - **Custom agents**: You can **chat**, **edit**, **clone**, or **delete** an agent from the management overview.
      :::{image} images/chat-edit-clone-delete.png
      :alt: Agent context menu showing Chat, Edit, Clone, and Delete options
      :width: 130px
      :::

## Create a new agent in the GUI

Follow these steps to create a new agent:

:::::{stepper}
::::{step} Navigate to the Agents page

Navigate to the **Agents** page to access the agent management interface.

::::

::::{step} Create a new agent

Select the **New agent** button to being creating a new agent.

:::{image} images/new-agent-button.png
:alt: Select the New agent button to create a new agent
:width: 150px
:::


::::

::::{step} Configure essential settings

Configure the essential agent settings in the **settings** tab:

1. Enter an **Agent ID**, a unique identifier for reference in code.
2. Add **Custom instructions**.<br><br>Custom instructions define the agent's personality and determine how it interacts with users and performs tasks.

    :::{note}
    Agent Builder adds your custom instructions to the system prompt to define the agent's behavior. The system prompt enables core features like visualization and citations.
    :::
3. Set the **Display name** for users.
4. Add a **Display description** to explain the agent's purpose.

::::

::::{step} Assign tools

Switch to the **Tools** tab to assign [tools](tools.md) to your agent.

Select the combination of built-in and custom tools available to the agent, based on your use case.

::::

::::{step} Customize appearance (optional)

Optionally customize the agent's appearance and organization:

- Add **Labels** to organize your agents.
- Select an **Avatar color** and **Avatar symbol** to help visually distinguish the agent.

::::

::::{step} Save your changes

Select **Save** to create your agent, or **Save and chat** to create the agent and immediately begin a conversation with it.

:::{image} images/save-and-chat-buttons.png
:alt: Save and Save and chat buttons
:width: 270px
:::

::::
:::::

## Agents API

The Agents API enables programmatic access to agent creation and management actions.

### Quick overview

For an overview, refer to [Agents API](kibana-api.md#agents).

### Serverless API reference

For the complete API reference, refer to the [Kibana serverless API reference](https://www.elastic.co/docs/api/doc/serverless/operation/operation-get-agent-builder-agents).