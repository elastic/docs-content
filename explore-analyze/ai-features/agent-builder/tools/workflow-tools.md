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
This page explains how to trigger a workflow in an agent conversation. If you want to use an agent within a workflow step, refer to [Call agents from workflows](../agents-and-workflows.md).
:::

## Prerequisites

Before you begin:

* Familiarize yourself with the core concepts of [Elastic Workflows](/explore-analyze/workflows.md).
* [Set up workflows](/explore-analyze/workflows/setup.md): Enable the Workflows feature and ensure you have the correct privileges to create and run workflows.
* Create at least one workflow.

## Add a Workflow tool

Follow these steps to configure a workflow tool:

1. Navigate to **Agents > More > View all tools > New tool**.

  :::{image} ../images/create-new-tool-workflows.png
  :screenshot:
  :width: 900px
  :alt: Screenshot of creating a new workflow tool.
  :::

2. Select **Workflow** as the tool type.
3. Select a workflow from the drop down list.
4. Fill in the [configuration fields](#configuration).
5. Click **Save**.

## Configuration

The Workflow tools have the following configuration settings:

  **Tool ID**
  :   A unique identifier for the tool.
  
  **Description**
  :   A natural language explanation of what the tool does. The agent uses this description to decide *when* to call the tool.
  :   *Example:* "Use this tool when the user asks to investigate an alert regarding the payment service."
  
  **Workflow**
  :   The specific Elastic Workflow to execute. Selecting a workflow automatically pulls its definition into the tool configuration.
  
  **Inputs**
  :   The parameters required by the workflow. These are automatically detected from the `inputs` section of the selected workflow's YAML definition. The agent will attempt to extract values for these inputs from the user's chat message.
  
  **Labels** (Optional)
  :   Tags used to organize and filter tools within the {{agent-builder}} UI.

## Call workflows from chat

Once you've created a workflow tool, you must assign it to an agent to make it available in chat.

### Assign tool to agent

To assign a tool to an agent:
1. Navigate to **Agents**.
2. Select your agent.
3. Select **More > Edit Agent > Tools**
4. Assign the workflow tool by selecting the checkbox.
5. Click **Save**.

### Trigger a workflow

To test your workflow tool, open the [Agent chat UI](../chat.md#agent-chat-gui) and ask a question that triggers the workflow.

The agent:
- extracts the necessary parameters from the conversation
- runs the workflow
- returns the workflow's final output to the chat

Expand the **Completed reasoning** section to trace the execution steps and inspect the raw workflow output.

:::{image} ../images/agent-builder-workflow-tool.png
:screenshot:
:width: 500px
:alt: Screenshot of reasoning steps of agent builder.
:::

## Examples

The [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows) contains more than 50 examples you can use as a starting point.

## Related pages
* [Tools overview](../tools.md)
* [Call agents from workflows](../agents-and-workflows.md)
* [Workflows](/explore-analyze/workflows.md)
