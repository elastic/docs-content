---
navigation_title: "Agents"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

# {{agent-builder}}: Agents

Agents engage in natural language conversations with users and interact with your {{es}} data through tools.
Fundamentally, an agent is defined by its custom instructions and the set of tools it's assigned.

Each agent manages the conversation flow, interprets user requests, and provides responses based on its configured tools, instructions, and behavior settings.

## How agents work

When you ask a question to an agent, it analyzes your request, selects the most appropriate tool, and determines the right arguments to use. After receiving results, the agent evaluates the information and decides whether to use additional tools or formulate a response. This iterative process of tool selection, execution, and analysis continues until the agent can provide a complete answer.

{{agent-builder}} includes a default agent (named `Elastic AI Agent`) with access to all built-in tools. You can create specialized agents with custom instructions and selected tools to address specific use cases or workflows.

## Manage your agents

The **Agents** page provides a centralized view of all your agents. From this page you can:

- View all your agents with their names and labels
- Search for specific agents using the search bar
- Filter agents by labels using the **Labels** dropdown
- Create new agents using the **+ New agent** button
- Start chatting with an agent or perform other actions
    - **Elastic AI Agent**: you can **chat** or **clone** the default agent using the chat or clone buttons.
      :::{image} images/chat-and-clone-buttons.png
      :alt: Chat with agent and clone agent buttons
      :width: 120px
      :::
    - **Custom agents**: You can **chat**, **edit**, **clone**, or **delete** an agent from the management overview.
      :::{image} images/chat-edit-clone-delete.png
      :alt: Agent context menu showing Chat, Edit, Clone, and Delete options
      :width: 130px
      :::

## How to create a new agent

Follow these steps to create a new agent:

:::::{stepper}
::::{step} Navigate to the Agents page

Navigate to the **Agents** page to access the agent management interface.

::::

::::{step} Create a new agent

Click the **New agent** button to start creating a new agent.

:::{image} images/new-agent-button.png
:alt: Click the New agent button to create a new agent
:width: 150px
:::


::::

::::{step} Configure essential settings

Configure the essential agent settings in the **settings** tab:

1. Enter an **Agent ID**, a unique identifier for reference in code.
1. Add **Custom instructions**.<br><br>Custom instructions define the agent's personality and determine how it will interact with users and perform tasks.

    :::{note}
    Your custom instructions are added to the system prompt to define the agent's behavior. The system prompt enables core features like visualization and citations.
    :::
1. Set the **Display name** that users will see.
1. Add a **Display description** to explain the agent's purpose

::::

::::{step} Assign tools

Switch to the **Tools** tab to assign [tools](tools.md) to your agent.

Select the combination of built-in and custom tools available to the agent, based on your use case.

::::

::::{step} Customize appearance (optional)

Optionally customize the agent's appearance and organization:

- Add **Labels** to organize your agents
- Choose an **Avatar color** and **Avatar symbol** to help visually distinguish the agent

::::

::::{step} Save your changes

Click **Save** to create your agent, or **Save and chat** to create the agent and immediately start a conversation with it.

:::{image} images/save-and-chat-buttons.png
:alt: Save and Save and chat buttons
:width: 270px
:::

::::
:::::