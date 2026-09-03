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

    Go to **Agents > More > View all tools > New tool**.

   ::::
   
   :::::

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

  **Require user confirmation** (Optional) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
  :   Controls whether the agent asks you to approve a tool call before it runs. Select **Never** to run without a prompt, **Once** to prompt the first time the agent calls the tool in a conversation, or **Always** to prompt on every call. The default is **Never**.
  :   With **Once**, your response applies to every later call to the tool in the same conversation, whether you confirmed or denied the action. This includes retries after a failed call.
  :   Confirmation applies only when an agent calls the tool. Refer to [Human-in-the-loop prompts](../chat.md#human-in-the-loop-prompts).


<!-- [TODO-CHECK] SCOPE DECISION, pre-existing gap found during B1. The form has a field group the Configuration list above does not mention. Strings re-verified verbatim at kibana HEAD 056473990ad7 on 2026-09-03 (form/i18n.ts, workflow key): group label "Workflow execution", checkbox label "Wait until the workflow completes", help text "If checked, the tool waits until the workflow completes (up to 120s) and returns the results. If unchecked, the workflow runs in the background and you can ask the agent to check the execution status." The 120s matches WAIT_FOR_COMPLETION_TIMEOUT_SEC = 120 in agent-builder-common/tools/types/workflow.ts. Out of scope for #1610 -- decide whether to fold it in or open a separate issue. If folded in, the entry would sit between Inputs and Require user confirmation to match form order. -->

<!-- [TODO-CHECK] FIELD ORDER, low priority, decide with the item above. Form order re-verified at kibana HEAD 056473990ad7 on 2026-09-03 (workflow_configuration_fields.tsx renders WorkflowPicker, then the wait-for-completion checkbox, then ConfirmationPolicySelect), so Require user confirmation IS the last field of the Configuration block. The list above places it last too, but after Labels, and the list was already not in form order before this PR. Consistency question for review rather than an error. -->

## Call workflows from chat

Once you've created a workflow tool, you must assign it to an agent to make it available in chat.

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
3. Select **More > Edit Agent > Tools**.
4. Assign the workflow tool by selecting the checkbox.
5. Click **Save**.

::::

:::::

### Trigger a workflow

To test your workflow tool, open the [Agent chat UI](../chat.md#agent-chat-gui) and ask a question that triggers the workflow.

The agent:
- extracts the necessary parameters from the conversation
- runs the workflow
- returns the workflow's final output to the chat

Review the [inline reasoning events](../chat.md#inspect-tool-calls-and-reasoning) to trace the execution steps and inspect the raw workflow output.

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
