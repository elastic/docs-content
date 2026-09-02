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

  <!-- RESOLVED 2026-08-31. Recaptured on QA ECH 9.6.0 showing the "Require user confirmation" select. Replaced the 2026-01-28 image, which predated kibana#281896. -->
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

<!-- RESOLVED 2026-08-31 by test B1 on QA ECH 9.6.0. A workflow tool with Require user confirmation set to Always DOES prompt: card titled "Permission to call tool", body 'Agent wants to call tool "<toolId>". Do you want to proceed?', buttons Deny and Allow. This refutes Pierre Gayvallet in #agent-builder on 2026-08-26 ("the execute_workflow tool of the agent, or a user tool of type `workflow`, do not, afaik, trigger confirmation prompt no", hedged twice): https://elastic.slack.com/archives/C08LX7YSHU2/p1787768859700779 . He was also recommending workflow tools to customers as an HITL bypass, so that advice is now stale -- worth telling him separately. -->

<!-- RESOLVED 2026-09-01 by test B2 on QA ECH 9.6.0 (Kibana 9.6.0), run over the public converse API, which accepts prompts: { <promptId>: { allow: bool } }. All four sub-tests passed, so the "Once" wording stands as written. (a) Prompt on the first call, none on the second in the same conversation; the prompt ID was `tools.<toolId>.confirmation` with no toolCallId suffix, which is the `once` mechanism. (b) A DENIAL is reused: the second call got no prompt and was declined again, tool result "The user chose not to proceed with this action." both times. (c) The retry claim -- previously untested at every level in kibana -- HOLDS: one approval, then three tool calls in a single turn (original plus two retries after a forced failure), zero re-prompts. The failure was forced by repointing the tool's ES|QL query at a missing index. (d) A new conversation prompted again. Also validated: Always re-prompts on every call (distinct prompt ID per tool call, suffixed with the toolCallId) and Never never prompts. Note for reviewers: the quoted string is the tool RESULT the model receives, not literal chat text -- the user sees the model's paraphrase. We do not quote it, so nothing to change. -->


<!-- RESOLVED 2026-08-31 by test B1. UI strings confirmed character for character on QA ECH 9.6.0: label "Require user confirmation", help text "Sets the policy for when the agent should require user confirmation before executing the tool.", options Never / Once / Always. The fresh-create-form default is now confirmed too: confirmation_policy_select.tsx renders `value={value ?? 'never'}`, and on the QA 9.6.0 cluster a tool created via POST /api/agent_builder/tools with no `confirmation` field came back as { askUser: 'never' }. "The default is Never" is correct. -->

<!-- [TODO-CHECK] NOT ADDED, pre-existing gap found during B1. The form has a "Workflow execution" group containing a "Wait until the workflow completes" checkbox, help text "If checked, the tool waits until the workflow completes (up to 120s) and returns the results. If unchecked, the workflow runs in the background and you can ask the agent to check the execution status." That checkbox is absent from the Configuration list below. The 120s matches WAIT_FOR_COMPLETION_TIMEOUT_SEC = 120 in the kibana source. Out of scope for #1610 -- decide whether to fold it in or open a separate issue. -->

<!-- [TODO-CHECK] Field order, low priority. In the form, Require user confirmation is the LAST field of the Type/Configuration block, immediately above Tool ID. The list below places it last, after Labels. The existing list was already not in form order, so this is a consistency question for review rather than an error. -->

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
