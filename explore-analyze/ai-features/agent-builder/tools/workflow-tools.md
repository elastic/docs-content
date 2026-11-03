---
navigation_title: "Workflow tools"
description: "Create custom tools that allow agents to trigger Elastic Workflows directly from a chat conversation to perform deterministic tasks."
applies_to:
  stack: preview 9.3+
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Workflow tools in {{agent-builder}}

Workflow tools enable agents to trigger [Elastic Workflows](/explore-analyze/workflows.md) directly from a conversation and use their output. This is ideal for offloading tasks from the LLM that require a deterministic, repeatable sequence of actions.

:::{note}
This page explains how to trigger an existing workflow in an agent conversation. To create a new workflow from Agent Chat, refer to [Create skills and workflows in chat](../chat.md#create-skills-and-workflows-directly-from-chat). If you want to use an agent within a workflow step, refer to [Call agents from workflows](../agents-and-workflows.md).
:::

## Prerequisites

Before you begin:

* Familiarize yourself with the core concepts of [Elastic Workflows](/explore-analyze/workflows.md).
* [Set up workflows](/explore-analyze/workflows/get-started/setup.md): Enable the Workflows feature and ensure you have the correct privileges to create and run workflows.
* Create at least one workflow.

## Add a Workflow tool

Follow these steps to configure a workflow tool:

1. Navigate to the Tools page and create a new tool:

   :::::{applies-switch}

   ::::{applies-item} { stack: ga 9.4+, serverless: ga }

    Click **Manage components** at the bottom of the left sidebar, select **Tools**, then click **+ New tool**.
   ::::

   ::::{applies-item} { stack: ga =9.3 }

    Go to **Agents** → **More** → **View all tools** → **New tool**.

   ::::
   
   :::::

   The following screenshot shows a new workflow tool with **Require user confirmation** set to **Always**:

   :::{image} ../images/create-new-tool-workflows.png
   :screenshot:
   :width: 900px
   :alt: Create new tool form with the Workflow type, the cancel-order workflow selected, and Require user confirmation set to Always
   :::

2. Select **Workflow** as the tool type.
3. Select a workflow from the dropdown list.
4. Fill in the [configuration fields](#configuration).
5. Click **Save**.

## Configuration

Workflow tools have the following configuration settings:

  **Tool ID**
  :   A unique identifier for the tool.
  
  **Description**
  :   A natural language explanation of what the tool does. The agent uses this description to decide *when* to call the tool.
  :   *Example:* "Use this tool when the user asks to investigate an alert regarding the payment service."
  
  **Workflow**
  :   The specific Elastic Workflow to execute. Selecting a workflow automatically pulls its definition into the tool configuration.
  
  **Inputs**
  :   The parameters required by the workflow. These are automatically detected from the `inputs` section of the selected workflow's YAML definition. The agent tries to extract values for these inputs from the user's chat message.
  
  **Require user confirmation** {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`
  :   Controls whether the agent asks you to approve a call to this tool before it runs. Select **Never** (default) to run without a prompt, **Once** to prompt the first time the agent calls the tool in a conversation, or **Always** to prompt on every call. For details, refer to [Require confirmation before a tool runs](custom-tools.md#require-confirmation-before-a-tool-runs).

  **Labels** (Optional)
  :   Tags used to organize and filter tools within the {{agent-builder}} UI.

## Call workflows from chat

After you create a workflow tool, you must assign it to an agent to make it available in chat.

### Assign tool to agent

To assign a tool to an agent:

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

1. Select the agent from the agent selector in the left sidebar.
2. Expand the **Customize** accordion and select **Tools**.
3. Click **Add tool** and select the workflow tool to assign.

::::

::::{applies-item} { stack: ga =9.3 }

1. Navigate to **Agents**.
2. Select your agent.
3. Select **More** → **Edit Agent** → **Tools**.
4. Assign the workflow tool by selecting the checkbox.
5. Click **Save**.

::::

:::::

### Trigger a workflow

To test your workflow tool, open the [Agent chat UI](../chat.md#agent-chat-gui) and ask a question that triggers the workflow.

The agent:
- Extracts the necessary parameters from the conversation.
- Runs the workflow.
- Returns the workflow's final output to the chat.

Review the [inline reasoning events](../chat.md#inspect-tool-calls-and-reasoning) to trace the execution steps and inspect the raw workflow output. The following screenshot shows a workflow tool call in the reasoning events:

:::{image} ../images/agent-builder-workflow-tool.png
:screenshot:
:width: 500px
:alt: Inline reasoning events showing an Agent Builder workflow tool execution.
:::

## Examples

The [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows) contains more than 50 examples you can use as a starting point.

## Related pages
* [Tools overview](../tools.md)
* [Call agents from workflows](../agents-and-workflows.md)
* [Author workflows with natural language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md)
