---
navigation_title: "Connect agents and workflows"
description: "Learn how Agent Builder works with Elastic Workflows, including creating workflows from chat, workflow tools, pre-execution and post-execution workflows, the `ai.agent` step, and conversation triggers."
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Connect {{agent-builder}} agents and Elastic Workflows

Elastic Workflows and {{agent-builder}} combine deterministic automation with conversational reasoning. You can create workflows conversationally, make workflows available to agents, invoke agents from workflows, and start workflows from conversation events.

## Approaches

{{agent-builder}} and workflows work together in the following ways:

* **Create workflows from Agent Chat**: {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Create and edit workflows by describing what you want [in plain language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md). {{kib}} generates and updates the workflow YAML for you, so you can quickly build without memorizing step types or Liquid syntax. 
* **Use workflows from agents:**
    * {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview` Trigger an existing workflow from a conversation with a [workflow tool](./tools/workflow-tools.md).
    * {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Assign [pre-execution workflows](#pre-execution-workflows) that run before the agent starts reasoning.
    * {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Assign [post-execution workflows](#post-execution-workflows) that run after the agent finishes responding.
* **Use agents from workflows:** Invoke an agent from a workflow with the [`ai.agent` step](#use-ai-agent-workflow-step). To add context to a conversation without triggering an agent response, use the [conversation steps](#add-conversation-context-workflow) {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`. For advanced API operations, use the [`kibana.request` step](#use-kibana-request-workflow-step).
* **React to conversation activity:** {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` Run a workflow when an attachment is added, updated, or deleted, or when conversation metadata changes. For supported conversation templates, you can also run a workflow when a conversation gets new messages or other changes. Refer to [{{agent-builder}} triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md#agent-builder-triggers).

## Prerequisites [prerequisites]

Before you begin:

* Familiarize yourself with the core concepts of [Elastic Workflows](/explore-analyze/workflows.md).
* Turn on Elastic Workflows through the `workflows:ui:enabled` [advanced setting](kibana://reference/advanced-settings.md#kibana-workflows-settings), which is on by default in 9.4 and later. When this setting is off, the workflow options in {{agent-builder}} are hidden and assigned workflows don't run.
* Make sure you have the appropriate subscription. Elastic Workflows requires an [Enterprise subscription](https://www.elastic.co/subscriptions) on {{stack}} deployments, or the appropriate [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) on {{serverless-short}}.
* Make sure you have the correct privileges to create and run workflows.

For details, refer to [Set up workflows](/explore-analyze/workflows/get-started/setup.md).

## Pre-execution workflows [pre-execution-workflows]

```{applies_to}
stack: ga 9.4+
serverless: ga
```

Pre-execution workflows run after each user message, before the agent makes any calls to the large language model (LLM) in response. They let you use Elastic Workflows for deterministic preparation or control before the agent begins its reasoning loop.

:::{note}
Configuring an agent's pre-execution workflows requires a role that grants wildcard (`*`) {{kib}} privileges, such as the built-in `superuser` role or the **Admin** role in {{serverless-short}}. You can't grant this from the {{kib}} role management UI. Refer to [Users and roles](/deploy-manage/users-roles.md) for how to assign roles.

Changing the space setting works differently: it requires the `manage_advanced_settings` privilege, which you can grant through the **Advanced Settings** [feature privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
:::

A pre-execution workflow runs once for each user message. It does not run before every LLM call or tool call within the agent's response.

Pre-execution workflows can:

* Add or rewrite prompt context before the agent starts.
* Cancel the agent run when a workflow detects that the request should not continue.
* Run multiple workflows in sequence when more than one workflow is assigned.

You can assign pre-execution workflows to a single agent or to every agent in a space. If you do both, the agent runs the workflows from both settings.

### Assign workflows to an agent [assign-pre-execution-workflows-to-an-agent]

1. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list.
2. Select an agent, then select **Settings**.
3. Under **Pre-execution workflow**, select one or more workflows in **Workflows**.
4. Select **Save**.

To confirm the setup, send a message to the agent, then check that the run appears in the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history).

The following screenshot shows the **Pre-execution workflow** setting in the agent **Settings** view.

:::{image} images/pre-execution-workflows.png
:screenshot:
:width: 900px
:alt: Pre-execution workflow section of the agent Settings tab with an empty Workflows selector
:::

### Assign workflows to every agent in a space [assign-pre-execution-workflows-to-a-space]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

The [prerequisites](#prerequisites) apply here too. In addition, the **Agent Builder** section in **GenAI Settings** appears only when the [`agentBuilder:experimentalFeatures`](get-started.md#enable-experimental-features-optional) advanced setting is turned on. It's off by default.

1. Go to **{{stack-manage-app}}** → **AI** → [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).
2. In the **Agent Builder** section, find **Pre-execution workflow** and open the **Workflows** selector.
3. Select one or more workflows.
4. Select **Save changes**.

To confirm the setup, send a message to any agent in the space, then check that the run appears in the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history).

Workflows that you assign here run for every agent in the space, in addition to any workflows you assign to an individual agent. If you assign the same workflow in both places, it runs only once.

Agents keep running these workflows whenever Elastic Workflows is turned on, even if you later turn off [`agentBuilder:experimentalFeatures`](get-started.md#enable-experimental-features-optional) and the **Agent Builder** section disappears. To clear the setting when the section is hidden, use the API. Refer to [Remove the workflow from the space setting](troubleshooting/pre-execution-workflow-disabled.md#remove-from-space).

### Recover agents blocked by a disabled workflow [recover-blocked-agents]

Disabling a workflow doesn't remove it from the agents or spaces that use it. Until you remove the workflow, every message to the affected agents fails. Refer to [Disabled pre-execution workflow](troubleshooting/pre-execution-workflow-disabled.md).

## Post-execution workflows [post-execution-workflows]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Post-execution workflows run after the agent finishes each response. Use them to audit the exchange, open a ticket, notify a channel, or grade the response. They can't change the response, and {{agent-builder}} ignores their output.

You assign post-execution workflows to individual agents. Unlike pre-execution workflows, post-execution workflows have no space setting.

### Requirements [post-execution-workflows-requirements]

* The [prerequisites](#prerequisites) for using workflows with {{agent-builder}}.
* A role that grants wildcard (`*`) {{kib}} privileges, such as the `superuser` role or the **Admin** role in {{serverless-short}}. You need this role to configure an agent's post-execution workflows. Without it, the **Workflows** selector is disabled. You can't grant wildcard privileges from the {{kib}} role management UI. Refer to [Users and roles](/deploy-manage/users-roles.md) for how to assign roles.
* By default, each workflow runs as the user who sent the message, so its steps can do only what that user's privileges allow. If the workflow is private, that user must own it or have **Executor** or **Editor** access to it.

### Assign post-execution workflows to an agent [assign-post-execution-workflows-to-an-agent]

:::::{tab-set}
:group: post-execution-assign

::::{tab-item} {{kib}} UI
:sync: ui

1. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list.
2. Select an agent, then select **Settings**.
3. Under **Post-execution workflow**, select one or more workflows in **Workflows**.
4. Select **Save**.

To confirm the setup, check that **Post-execution workflows** shows **Enabled** on the agent overview. Then send a message to the agent and check that the run appears in the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history).

The following screenshot shows the **Post-execution workflow** setting in the agent **Settings** view.

:::{image} images/post-execution-workflows.png
:screenshot:
:width: 900px
:alt: Post-execution workflow section of the agent Settings tab with an empty Workflows selector
:::
::::

::::{tab-item} API
:sync: api

To assign post-execution workflows through the [Agent Builder API]({{kib-apis}}group/endpoint-agent-builder), set the agent field `configuration.post_execution_workflow_ids`. The following request assigns one workflow:

```console
PUT kbn:/api/agent_builder/agents/<agent_id>
{
  "configuration": {
    "post_execution_workflow_ids": ["<workflow_id>"]
  }
}
```

* The update replaces only the keys you send, so the agent keeps its instructions, tools, skills, and other settings.
* Without wildcard (`*`) {{kib}} privileges, a request that changes `post_execution_workflow_ids` returns a `400` error: `Only administrators can configure post-execution workflows.`
::::

:::::

### How post-execution workflows run [post-execution-workflows-run]

A post-execution workflow runs only when the agent completes its response. It doesn't run in these cases:

* The agent run fails, or the user stops it.
* A [pre-execution workflow](#pre-execution-workflows) cancels the run.
* The agent is paused on a [human-in-the-loop prompt](chat.md#human-in-the-loop-prompts). The workflow runs later, after the user answers and the agent finishes that response.
* The agent reads an existing conversation without saving to it, such as an [`ai.agent` step](#use-ai-agent-workflow-step) that sets `ephemeral: true` and a conversation ID.

When an agent has more than one post-execution workflow, they run in the order they're listed. {{agent-builder}} waits up to 120 seconds for each workflow to complete, fail, or pause for input before it starts the next. A workflow that's still running after that wait doesn't block the workflows that follow.

{{agent-builder}} sets `execution.triggeredBy` to `agent-builder-hook` for these runs, so a workflow can check that value and skip runs that someone started directly. Refer to [`execution.triggeredBy`](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution).

If a workflow fails, the agent's response stays in place. {{kib}} logs the failure and still runs any later workflows assigned to the agent. In the following cases, {{kib}} logs the failure before it records an execution, so the failure doesn't appear in [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history):

* The workflow doesn't exist, for example, because someone deleted it.
* The workflow is turned off.
* The workflow has validation errors.
* The workflow is private, and the user who sent the message doesn't have access to run it.

### Workflow inputs [post-execution-workflow-inputs]

Declare the inputs you want the workflow to receive under its manual trigger, not at the workflow root. {{agent-builder}} doesn't detect `inputs` declared at the root of a workflow saved in 9.5 or later. Refer to [`inputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs). Inside the workflow, reference an input as `{{ inputs.prompt }}`.

The following workflow logs each exchange:

```yaml
name: log_agent_exchange
enabled: true
triggers:
  - type: manual
    inputs:
      properties:
        prompt:
          type: string
        response:
          type: string
steps:
  - name: log_exchange
    type: console
    with:
      message: "User asked: {{ inputs.prompt }}. Agent answered: {{ inputs.response }}"
```

{{agent-builder}} always sends `prompt`, `response`, `round_id`, and `tool_calls`. It also sends `conversation_id` and `agent_id` when the run has them, even if the workflow doesn't declare them. It sends `round_connector_id`, `workflow_context`, and `tool_results` only when the workflow declares them. To keep one of these three out of the workflow, remove it from the manual trigger.

| Input | Description |
|---|---|
| `prompt` | The user message for this response, including any rewrite by a pre-execution workflow, or an empty string when there's no user message. |
| `response` | The agent's final answer, or an empty string when the response has no answer text. |
| `round_id` | The ID of the completed conversation round, meaning one user message and the agent's response to it. |
| `tool_calls` | One entry for each tool call, with `tool_id`, `tool_call_id`, and `params`, or an empty array when the agent called no tools. |
| `conversation_id` | The conversation ID. If the run doesn't save the conversation, no saved conversation has this ID. |
| `agent_id` | The agent ID. |
| `round_connector_id` | The connector the agent used for this response. Not sent when the connector ID isn't available. |
| `workflow_context` | Data that pre-execution workflows returned as `workflow_context` for this response, keyed by namespace. Each namespace has a numeric `version` and a `data` object. Not sent when there's none. |
| `tool_results` | One entry for each tool call that has results, with `tool_id`, `tool_call_id`, and `results`. A workflow that declares `tool_results` as an array receives an empty array when no tool call has results. {{agent-builder}} truncates this data, so it might not be complete. Refer to the limits after this table. |

The `tool_results` data is truncated and might not be the complete tool output. To limit size, {{agent-builder}} truncates `tool_results` before the workflow receives it: each string to 4,000 characters and each array to 50 items. If a result's data is still larger than 32,000 characters, {{agent-builder}} replaces it with `type: other` and `data` set to `{ "omitted": "result data exceeded 32000 characters" }`.

If the workflow sets `additionalProperties: false`, declare every input that {{agent-builder}} sends, including `conversation_id` and `agent_id`. Otherwise, the run fails input validation and appears as a failed execution in the workflow's execution history.

:::{dropdown} Example: Manual trigger that declares every input
```yaml
triggers:
  - type: manual
    inputs:
      properties:
        prompt:
          type: string
        response:
          type: string
        conversation_id:
          type: string
        round_id:
          type: string
        agent_id:
          type: string
        round_connector_id:
          type: string
        workflow_context:
          type: object
        tool_calls:
          type: array
          items:
            type: object
            additionalProperties: true
        tool_results:
          type: array
          items:
            type: object
            additionalProperties: true
      additionalProperties: false
```
:::

## Use the `ai.agent` step [use-ai-agent-workflow-step]

Follow these steps to invoke an `ai.agent` as a step within a workflow.

1.  Open the **Workflows** editor and create or edit a workflow.
2.  Add a new step with the type `ai.agent`.
3.  Set the **`agent-id`** parameter at the top level of the step to the unique identifier of the target agent. If you omit it, the step uses the built-in Elastic AI Agent.
4.  In the **`with`** block, set the **`message`** parameter to your natural language prompt.
5.  Optionally, in the **`with`** block, set the **`schema`** parameter to a JSON Schema object to receive structured output from the agent instead of free-text.
6.  Optionally, route the step to a specific model by setting **`connector-id`** or **`inference-id`** at the top level of the step. These parameters are mutually exclusive.

:::{dropdown} Example: Analyze flight delays
The following example demonstrates a workflow that searches for flight delays and uses the **Elastic AI Agent** to summarize the impact. To follow along with this example ensure that the [{{kib}} sample flight data](https://www.elastic.co/docs/extend/kibana/sample-data) is installed.

```yaml
version: "1"
name: analyze_flight_delays
description: Fetches delayed flights and uses an agent to summarize the impact.
enabled: true
triggers:
  - type: manual
steps:
  # Step 1: Get data from Elasticsearch
  - name: get_delayed_flights
    type: elasticsearch.search
    with:
      index: "kibana_sample_data_flights"
      query:
        range:
          FlightDelayMin:
            gt: 60
      size: 5

  # Step 2: Ask the agent to reason over the data
  - name: summarize_delays
    type: ai.agent
    agent-id: "elastic-ai-agent" <1>
    with:
      message: | <2>
        Review the following flight delay records and summarize which airlines are most affected and the average delay time:
        {{ steps.get_delayed_flights.output }}

  # Step 3: Print the agent's summary
  - name: print_summary
    type: console
    with:
      message: "{{ steps.summarize_delays.output }}"
```
1. **agent-id**: The ID of the agent you want to call (must exist in Agent Builder). Set it at the top level of the step, not in the `with` block.
2. **message**: The prompt sent to the agent. You can use template variables (like `{{ steps.step_name.output }}`) to inject data dynamically.
:::

### Parameters

Set `agent-id` and other configuration keys at the top level of the step. Set inputs like `message` in the `with` block.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `agent-id` | Top level | string | No | The unique identifier of the target agent (must exist in {{agent-builder}}). Defaults to the built-in Elastic AI Agent. |
| `connector-id` | Top level | string | No | The Generative AI connector to use for model routing. Mutually exclusive with `inference-id`. Generative AI connectors are deprecated, so use `inference-id` for new workflows. |
| `inference-id` | Top level | string | No | The {{infer}} endpoint ID to use for model routing. Mutually exclusive with `connector-id`. |
| `create-conversation` | Top level | boolean | No | When `true`, persists the conversation so that follow-up steps or later requests can continue it. |
| `public-conversation` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | Top level | boolean | No | When `true`, makes the conversation this step creates public. Any user who can access the agent can read and continue the conversation and see it in their conversation list. Only applies when `create-conversation` is `true`. Defaults to `false` (private). Refer to [Conversation access control](/explore-analyze/ai-features/agent-builder/permissions.md#conversation-access-control). |
| `ephemeral` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | Top level | boolean | No | When `true`, the agent reads the conversation set in `conversation_id` but doesn't change it. Defaults to `false`. Can't be combined with `create-conversation: true`. Refer to [Example: Summarize a conversation without changing it](/explore-analyze/workflows/steps/ai-steps.md#ai-agent-ephemeral). |
| `message` | `with` | string | Yes | The natural language prompt to send to the agent. Can include template variables to reference data from previous steps. |
| `schema` | `with` | object | No | A JSON Schema object that defines the structure of the expected response. When provided, the agent returns structured data matching the schema instead of free-text. |
| `conversation_id` | `with` | string | No | Continue an existing conversation by ID. |
| `attachments` | `with` | array | No | Attachments to provide to the agent. |

For the complete step reference, refer to [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent).

## Add context to a conversation without an agent response [add-conversation-context-workflow]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

A workflow can add events, such as notes, and user messages to an {{agent-builder}} conversation. The agent reads user messages and notes the next time it runs on the conversation. For example, a workflow can post incident updates as they arrive, and a later `ai.agent` step or chat request can summarize them.

Use these steps:

- [`ai.conversation.create`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-create): Create a conversation and get its ID.
- [`ai.conversation.add_event`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-add-event): Add an event, such as a note.
- [`ai.conversation.add_user_message`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-add-user-message): Add a user message.

## Use `kibana.request` step [use-kibana-request-workflow-step]

Use the generic `kibana.request` step to interact with {{agent-builder}} APIs programmatically.

1. Add a new step with the type `kibana.request`.
2. Set the method (for example: `GET`, `POST`).
3. Set the `path` to the specific [Agent Builder API endpoint]({{kib-apis}}group/endpoint-agent-builder).

:::{dropdown} Example: List available agents
This step retrieves a list of all agents currently available in Agent Builder.

```yaml
name: list_agents
enabled: true
triggers:
  - type: manual
steps:
  - name: list_agents
    type: kibana.request
    with:
      method: GET
      path: /api/agent_builder/agents
```
:::

## Examples

The [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows) contains more than 50 examples you can use as a starting point.

## Related pages
* [Tools overview](./tools.md)
* [Workflow tools](../agent-builder/tools/workflow-tools.md)
* [Author workflows with natural language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md)
* [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md#agent-builder-triggers)
* [Agent Builder API]({{kib-apis}}group/endpoint-agent-builder)
