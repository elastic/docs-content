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
- **GenAI Settings**: Open the global GenAI settings page to configure default connectors and other AI settings. Refer to [](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

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

### Track conversation status

The chat history panel shows the status of each conversation at a glance, so you can keep track of what your agents are doing across conversations:

| Icon | Status | Meaning |
|------|--------|---------|
| ![In progress spinner](images/agent-builder-status-in-progress.svg "=20x20") | **In progress** | The agent is generating a response. |
| ![Awaiting your input icon](images/agent-builder-status-awaiting.svg "=20x20") | **Awaiting your input** | The agent paused and needs you to respond before it can continue, for example to answer a [human-in-the-loop prompt](#human-in-the-loop-prompts). |
| ![Unread icon](images/agent-builder-status-unread.svg "=20x20") | **Unread** | The agent finished responding in a conversation you weren't viewing. |
| ![Error icon](images/agent-builder-status-error.svg "=20x20") | **Error** | The agent stopped because of an error. |

For example, the following chat history panel shows one conversation in progress and another with unread activity:

:::{image} images/agent-builder-conversation-status.png
:screenshot:
:alt: Chat history panel showing conversation status indicators, including In progress and Unread
:width: 450px
:::

Conversations run independently, so you can work in several at the same time: start an agent in one conversation, switch to another while the first keeps working, and come back later without interrupting either one. New conversations appear in the panel as soon as you start them, before the agent finishes its first response.

### Inspect tool calls and reasoning

::::{note}
:applies_to: stack: ga 9.5+, serverless: ga

Inline reasoning events replace the [Reasoning panel](glossary.md#reasoning-panel).
::::

Agent responses show reasoning, tool calls, tool results, and the final response inline as a single sequence. Events appear in the order they happen, so you can follow how the agent handles your request in context. The agent runs tools in a loop until it achieves its goal or [exceeds the maximum conversation length](limitations-known-issues.md#conversation-length-exceeded).

:::{image} images/reasoning-steps.png
:screenshot:
:alt: Inline reasoning events showing tool calls and execution steps in Agent Chat
:width: 650px
:::

Tool call events show whether a tool is still running or has returned a response. Expand a tool call to inspect **Parameters sent** and **Response returned**. Some results render inline; other results provide **View JSON** or **View execution** links for more detail.

After the agent finishes responding, use the response metadata menu to view timing and token usage details or select **View response JSON** to inspect the raw response data. For more information, refer to [Monitor token usage](monitor-usage.md).

### View traces for a conversation round
```{applies_to}
stack: ga 9.5+
serverless: ga
```

Each conversation round can record OpenTelemetry traces of how the agent ran. To inspect them, select the **View Trace** icon ({icon}`apm_trace`) on the round. A **Trace** flyout opens with a waterfall of the round's spans, including model calls and tool calls.

The **View Trace** icon appears only when trace collection is enabled and the conversation round has a trace. If trace collection is off, or the round produced no trace, the icon does not appear.

To learn how traces are collected, configured, and secured, refer to [Collect agent traces](collect-traces.md).

### Human-in-the-loop prompts
```{applies_to}
stack: ga 9.4+
```

At certain points an agent pauses and hands control back to you before it continues. This pattern is known as human-in-the-loop (HITL). While a conversation is paused this way, it shows an **Awaiting your input** status in the [chat history panel](#track-conversation-status).

{{agent-builder}} uses different prompts depending on why the agent needs your input:

| Prompt | When it appears | Available responses |
| --- | --- | --- |
| Tool confirmation | An Elastic-built tool or skill requires approval before it performs an action | Confirm the action or deny it |
| Connector authorization {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | An external connector needs access to continue | Authorize access or deny it |
| Clarifying question {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | The agent needs more information to continue | Answer or skip the question |

HITL prompts do not replace role-based access control or grant additional privileges. Actions still run with your existing permissions.

#### Confirm a change

Some Elastic-built tools and skills pause for confirmation before performing consequential actions. When confirmation is required, the chat presents a preview before the action takes effect. The preview format and available responses depend on the tool or skill. Review the preview, then confirm the action to proceed or deny it to cancel.

For example, when an agent updates a workflow, it shows the proposed change as a diff and waits for you to review it before applying:

:::{image} images/agent-builder-preview-changes.png
:screenshot:
:alt: Preview panel showing proposed changes from an agent action before they are applied.
:width: 700px
:::

The Streams management skill also previews the proposed configuration when it creates a stream:

:::{image} images/agent-builder-confirm-create-stream.png
:screenshot:
:alt: Confirmation prompt previewing a new logs.otel.checkout stream and its routing condition
:width: 700px
:::

For irreversible actions, the prompt highlights the consequences before you proceed:

:::{image} images/agent-builder-confirm-delete-stream.png
:screenshot:
:alt: Confirmation prompt warning that the logs.otel.checkout stream and its data will be permanently deleted
:width: 700px
:::

#### Authorize a connector
```{applies_to}
stack: preview 9.5+
serverless: preview
```

When an agent uses a [connector](connectors.md) to reach an external service that requires authorization, the chat pauses so you can grant access. Select **Authorize** to complete the sign-in flow for the connector, or **Deny** to decline. After you authorize, the agent retries the tool call and continues.

For example, an agent that needs to read your Notion workspace pauses until you authorize the connector:

:::{image} images/agent-builder-authorization-prompt.png
:screenshot:
:alt: Authorization prompt with Authorize and Deny buttons
:width: 650px
:::

#### Answer a clarifying question
```{applies_to}
stack: preview 9.5+
serverless: preview
```

When your request is ambiguous, an agent can pause and ask you up to five multiple-choice questions instead of guessing. For each question, select one of the options, or choose the custom option and type your own answer. Some questions let you select more than one option. To move on without answering, select **Skip question**.

When there's more than one question, use **Back** and **Continue** to move between them, then select **Submit** on the last question. After you respond, the agent resumes. The agent's questions and your answers stay in the conversation, so you can revisit what was asked and how you responded.

For example, before creating a dashboard the agent might ask which sample data set to use:

:::{image} images/agent-builder-clarifying-question.png
:screenshot:
:alt: Clarifying question prompt showing multiple-choice options, a custom answer field, and a Skip question button
:width: 650px
:::

## Create skills and workflows in chat [create-skills-and-workflows-directly-from-chat]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

In addition to answering questions and analyzing data, agents can help you create reusable skills and Elastic Workflows without leaving the conversation. Describe what you want to build in natural language:

- **Skills**: For example, "Create a skill that triages production alerts using our incident runbook."
- **Workflows**: For example, "Create a workflow that checks for failed payments every five minutes and sends a Slack notification."

Creating a resource from chat is a [human-in-the-loop](#human-in-the-loop-prompts) process:

1. The agent gathers the requirements from your request. If important information is missing or ambiguous, it pauses to ask [clarifying questions](#answer-a-clarifying-question).
2. The agent generates a draft and presents it in the conversation. You can review the configuration and ask for changes in natural language.
3. When the draft is ready, use the action on the preview to confirm creation. The resource is not created until you explicitly confirm the change.

When you create a workflow, include details such as its trigger, inputs, data sources, conditions, and connectors. The agent asks for any missing information, generates and validates the workflow YAML, and shows the proposed changes for you to review. You can continue refining the draft in the conversation before you confirm creation.

For example, the following preview shows a skill draft that you can review before selecting **Create skill**:

:::{image} images/create-skill-from-chat.png
:screenshot:
:alt: Skill draft in Agent Chat showing its description, instructions preview, associated tool references, and a Create skill button
:width: 750px
:::

You need the same privileges that are required to create the resource in its management UI. For resource-specific fields, limitations, and alternative creation methods, refer to:

- [Create and manage custom skills](custom-skills.md#create-a-skill-from-chat)
- [Create and manage workflows](/explore-analyze/workflows.md)

## Customize your agent [customize-your-agent]

```{applies_to}
stack: ga 9.4+
```

The **Customize** accordion in the left sidebar provides agent-scoped configuration for the currently selected agent. Expand it to access the following pages:

**Overview**
:   Displays a summary of the selected agent, including the total count of assigned skills and tools. Use the quick links to edit the agent's instructions or settings.

**Skills**
:   Lists the skills assigned to the current agent. Click a skill to open a read-only detail panel on the right side. To assign new skills, click **Add skill**. To view and manage all skills across the deployment, click **Manage all skills**. Skills you import into the library must be turned on with their toggle in this list before the agent can use them. For how skills work and how to manage them, refer to [Skills in {{agent-builder}}](skills.md).

**Plugins** {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   Lists the plugins assigned to the current agent. Each plugin bundles a set of related skills that install together. To assign a plugin, click **Add plugins**. To view and manage all plugins, click **Manage all plugins**. 

:::{note}
The **Plugins** option is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}.
:::

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

**Plugins** {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   View and install plugins across the deployment. Install a plugin from a URL or by uploading a ZIP file. Each plugin bundles related skills that you can assign to agents.

:::{note}
The **Plugins** option is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}.
:::

**Connectors** {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   View and manage the agent builder connectors library, which gives agents access to external data sources and systems. 

:::{note}
The **Connectors** option is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}.
:::

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

For the complete API reference, refer to the [{{kib}} API reference]({{kib-apis}}operation/operation-get-agent-builder-conversations).
