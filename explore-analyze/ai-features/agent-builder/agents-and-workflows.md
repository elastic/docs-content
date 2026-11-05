---
navigation_title: "Connect agents and workflows"
description: "Learn how Agent Builder works with Elastic Workflows, including creating workflows from chat, workflow tools, pre-execution workflows, and the `ai.agent` step."
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

Elastic Workflows and {{agent-builder}} combine deterministic automation with conversational reasoning. You can create workflows conversationally, make workflows available to agents, and invoke agents from workflows.

## Approaches

There are three ways to use {{agent-builder}} and workflows together:

* **Create workflows from Agent Chat**: {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Create and edit workflows by describing what you want [in plain language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md). {{kib}} generates and updates the workflow YAML for you, so you can quickly build without memorizing step types or Liquid syntax. 
* **Use workflows from agents:** Trigger an existing workflow from a conversation with a [workflow tool](./tools/workflow-tools.md) {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`, or assign [pre-execution workflows](#pre-execution-workflows) that run before the agent starts reasoning.
* **Use agents from workflows:** Invoke an agent from a workflow with the [`ai.agent` step](#use-ai-agent-workflow-step). To add context to a conversation without triggering an agent response, use the [conversation steps](#add-conversation-context-workflow) {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`. For advanced API operations, use the [`kibana.request` step](#use-kibana-request-workflow-step).

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
Configuring an agent's pre-execution workflows requires a role that grants wildcard (`*`) {{kib}} privileges, such as the built-in `superuser` role. You can't grant this from the {{kib}} role management UI.

Changing the space setting works differently: it requires the `manage_advanced_settings` privilege, which you can grant through the **Advanced Settings** [feature privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
:::

A pre-execution workflow runs before the agent calls the model. It doesn't run before every LLM call or tool call inside that response. When the agent resumes after a [human-in-the-loop prompt](chat.md#human-in-the-loop-prompts), the workflow runs again for that same user message. {{agent-builder}} waits up to 120 seconds for each workflow to finish. If the workflow fails, or {{agent-builder}} can't find the execution after that wait, the agent run stops. A workflow that is still running after 120 seconds, or that pauses for input with `waitForInput` or `waitForApproval`, doesn't hold the agent back: {{agent-builder}} ignores its output and continues the run. Don't use pausing steps in a pre-execution workflow.

By default, each pre-execution workflow runs as the user who sent the message, so its steps can do only what that user's privileges allow. If the workflow is private, that user must own it or have **Executor** or **Editor** access to it. Otherwise the workflow fails and the agent run stops.

Pre-execution workflows can:

* Add or rewrite prompt context before the agent starts.
* Cancel the agent run when a workflow detects that the request should not continue.
* Run multiple workflows in sequence when more than one workflow is assigned.

You can assign pre-execution workflows to a single agent or to every agent in a space. If you do both, the agent runs the workflows from both settings. Workflows assigned to the space run first, then workflows assigned to the agent.

A pre-execution workflow receives details about the run as [inputs](#pre-execution-workflow-inputs), and its [output](#pre-execution-workflow-outputs) can rewrite the user message, stop the run, or add context for the model.

### Assign workflows to an agent [assign-pre-execution-workflows-to-an-agent]

1. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list.
2. Select an agent, then select **Settings** → **Pre-execution workflow**.
3. Open the **Workflows** selector.
4. Select one or more workflows. They run after each user message, before the agent makes any LLM calls in response.
5. Save the agent.

To confirm the setup, send a message to the agent, then check that the run appears in the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history).

The following screenshot shows the **Pre-execution workflow** setting in the agent **Settings** view.

:::::{applies-switch}

::::{applies-item} { stack: ga 9.6+, serverless: ga }
:::{image} images/pre-execution-workflows.png
:screenshot:
:width: 900px
:alt: Agent Settings tab showing the Pre-execution workflow and Post-execution workflow sections, each with one workflow selected
:::
::::

::::{applies-item} stack: ga 9.4-9.5
:::{image} images/pre-execution-workflows-9-4.png
:screenshot:
:width: 900px
:alt: Agent Settings tab showing the Pre-execution workflow section with an empty Workflows selector
:::
::::

:::::

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

### Workflow inputs [pre-execution-workflow-inputs]

Declare the inputs you want the workflow to receive under its manual trigger, not at the workflow root. {{agent-builder}} doesn't detect `inputs` declared at the root of a workflow saved in 9.5 or later. Refer to [`inputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs). Inside the workflow, reference an input as `{{ inputs.prompt }}`.

{{agent-builder}} can send these inputs:

| Input | Type | Contains |
|---|---|---|
| `prompt` | `string` | The user message for this run, or an empty string when there's none, such as when a resumed run only answers a human-in-the-loop prompt. |
| `conversation_id` {applies_to}`stack: ga 9.6+` | `string` | The conversation ID. If the run doesn't save the conversation, the ID might not match a saved conversation. |
| `agent_id` {applies_to}`stack: ga 9.6+` | `string` | The agent ID. Omitted when the run has no agent ID. |
| `round_execution_index` {applies_to}`stack: ga 9.6+` | `integer` | `0` the first time the agent runs for a user message. Greater than `0` each time the agent resumes after a human-in-the-loop prompt. |

{{agent-builder}} always sends `prompt`, and sends `conversation_id` whenever the run has one, even if the workflow doesn't declare it. It sends `agent_id` and `round_execution_index` only when the workflow declares them under its manual trigger.

If the workflow declares its inputs with `additionalProperties: false`, declare every input that {{agent-builder}} sends. Otherwise input validation fails, the workflow execution fails, and the agent run stops.

:::{important}
:applies_to: stack: ga 9.6+
Starting in 9.6, {{agent-builder}} also sends `conversation_id`. Before you upgrade, add `conversation_id` to any pre-execution workflow that sets `additionalProperties: false`. Otherwise every message to the agents that use the workflow fails.
:::

{applies_to}`stack: ga 9.6+` When {{agent-builder}} starts the workflow, [`execution.triggeredBy`](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution) is `agent-builder-hook`. To reject runs that someone started directly, check that value in the workflow. This is useful when the workflow uses `settings.run_as` to run with a service account's privileges. In earlier versions, the value is `manual`.

### Workflow outputs [pre-execution-workflow-outputs]

{{agent-builder}} reads the output of the last top-level step that ran, including a top-level step with an `if` condition. It doesn't merge outputs from multiple steps or loops. To return output fields reliably, end the workflow with a top-level [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) step or a top-level [`workflow.output`](/explore-analyze/workflows/steps/composition.md#workflow-output) step {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`.

The output can include these fields:

| Output | Effect |
|---|---|
| `new_prompt` | A non-empty value replaces the user message that the agent receives. Later workflows receive this text as `prompt`. |
| `abort` | `true` stops the agent run. |
| `abort_message` | Any non-empty value stops the agent run, even when `abort` is `false`. The conversation shows the message in a **Conversation Aborted** notice. Without a message, the notice says that the workflow stopped the run. |
| `model_context` {applies_to}`stack: ga 9.6+` | Text that the model receives as a separate message after the user message. The chat UI doesn't display it, though {{agent-builder}} stores it on the conversation record. |
| `workflow_context` {applies_to}`stack: ga 9.6+` | Data for the agent's post-execution workflows. The model never receives it, but {{agent-builder}} stores it on the conversation record. |

Each user message and the agent's response to it form a round. {{agent-builder}} stores `model_context` with the round, so the model keeps receiving it later in the conversation. When {{agent-builder}} summarizes older rounds to shorten a long conversation, the summary leaves `model_context` out.

Because {{agent-builder}} stores both values on the conversation record, anyone who can read the conversation can read them through the API. Don't put secrets in either one.

A workflow assigned under **Post-execution workflow** in the agent's **Settings** receives the stored `workflow_context` when it declares a `workflow_context` input.

#### Context limits [pre-execution-workflow-context-limits]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

{{agent-builder}} ignores a `model_context` or `workflow_context` value that breaks these rules. The agent run continues without it.

`model_context` rules:

* The value must be a string. {{agent-builder}} removes leading and trailing whitespace and ignores a string that is empty after that.
* {{agent-builder}} keeps the first 100,000 characters and drops the rest.
* When more than one workflow returns `model_context`, {{agent-builder}} joins the texts in run order, separated by a blank line, and keeps the first 100,000 characters of the result.

`workflow_context` rules:

* The value is an object keyed by namespace, a name you choose to group your data, such as `support.policy`. Each namespace has a `version` and a `data` object.
  * `version` is a positive integer.
  * `data` is a JSON object. Nested objects and arrays can go eight levels deep, counting `data` as the first level.
* A namespace name can be 1 to 256 characters long.
* The whole `workflow_context` JSON, including namespaces from earlier workflows, can contain at most 16 namespaces and be at most 65,536 bytes.
* If any namespace breaks a rule, {{agent-builder}} ignores that workflow's whole `workflow_context`. Namespaces that earlier workflows stored stay in place.

When more than one workflow returns `workflow_context`, a later workflow replaces a namespace with the same name and keeps the other namespaces. If the combined object would exceed a limit, {{agent-builder}} ignores the later workflow's `workflow_context` and keeps the earlier one.

#### When the agent resumes [pre-execution-workflow-resume]

When the agent resumes after a [human-in-the-loop prompt](chat.md#human-in-the-loop-prompts), pre-execution workflows run again:

* The workflow can still stop the agent run with `abort` or `abort_message`.
* {applies_to}`stack: ga 9.6+` {{agent-builder}} keeps `model_context` and `workflow_context` from the first run of the round (`round_execution_index: 0`) and ignores any that a later run returns. To skip steps that only prepare initial context, declare `round_execution_index` and add `if: "inputs.round_execution_index : 0"` to those steps.
* {applies_to}`stack: ga 9.6+` A `new_prompt` doesn't change the message the agent answers, which stays the original user message.

### Example: Add flight delay context before the agent answers [pre-execution-workflow-example]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

The following workflow searches the [{{kib}} sample flight data](/manage-data/ingest/sample-data.md#add-sample-data-sets) for delayed flights. It gives the model the current count, and stores the count for the agent's post-execution workflows.

```yaml
version: "1"
name: add_flight_delay_context
description: Adds the current number of delayed flights before the agent answers.
enabled: true
triggers:
  - type: manual
    inputs:
      properties:
        round_execution_index: <1>
          type: integer
steps:
  - name: find_delays
    type: elasticsearch.search
    if: "inputs.round_execution_index : 0" <2>
    with:
      index: "kibana_sample_data_flights"
      query:
        range:
          FlightDelayMin:
            gt: 60
      size: 0
  - name: return_context <3>
    type: data.set
    if: "inputs.round_execution_index : 0"
    with:
      model_context: | <4>
        There are currently {{ steps.find_delays.output.hits.total.value }} flights delayed by more than an hour in kibana_sample_data_flights.
        Use this number when the user asks about delays.
      workflow_context:
        flights.delays: <5>
          version: 1
          data:
            index: "kibana_sample_data_flights"
            delayed_flights: "{{ steps.find_delays.output.hits.total.value }}"
```
1. Declares `round_execution_index` so {{agent-builder}} sends it. Because the trigger doesn't set `additionalProperties: false`, {{agent-builder}} can still send `prompt` and `conversation_id` without failing validation.
2. Runs the search only on the first execution for the user message, and skips it when the agent resumes after a human-in-the-loop prompt.
3. `data.set` is the last top-level step that runs, so {{agent-builder}} reads its output. You can also use `workflow.output`.
4. The model receives this text as a separate message. The chat UI doesn't display it.
5. A namespace you choose. Post-execution workflows read this data from their `workflow_context` input.

## Use the `ai.agent` step [use-ai-agent-workflow-step]

Follow these steps to invoke an `ai.agent` as a step within a workflow.

1.  Open the **Workflows** editor and create or edit a workflow.
2.  Add a new step with the type `ai.agent`.
3.  Set the **`agent-id`** parameter at the top level of the step to the unique identifier of the target agent. If you omit it, the step uses the built-in Elastic AI Agent.
4.  In the **`with`** block, set the **`message`** parameter to your natural language prompt.
5.  Optionally, in the **`with`** block, set the **`schema`** parameter to a JSON Schema object to receive structured output from the agent instead of free-text.
6.  Optionally, route the step to a specific model by setting **`connector-id`** or **`inference-id`** at the top level of the step. These parameters are mutually exclusive.

### Example: Analyze flight delays
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

### Parameters

Set `agent-id` and other configuration keys at the top level of the step. Set inputs like `message` in the `with` block.

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `agent-id` | Top level | string | No | The unique identifier of the target agent (must exist in {{agent-builder}}). Defaults to the built-in Elastic AI Agent. |
| `connector-id` | Top level | string | No | The Generative AI connector to use for model routing. Mutually exclusive with `inference-id`. Generative AI connectors are deprecated, so use `inference-id` for new workflows. |
| `inference-id` | Top level | string | No | The {{infer}} endpoint ID to use for model routing. Mutually exclusive with `connector-id`. |
| `create-conversation` | Top level | boolean | No | When `true`, persists the conversation so that follow-up steps or later requests can continue it. |
| `public-conversation` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | Top level | boolean | No | When `true`, makes the conversation this step creates public. Any user who can access the agent can read and continue the conversation and see it in their conversation list. Only applies when `create-conversation` is `true`. Defaults to `false` (private). Refer to [Conversation access control](/explore-analyze/ai-features/agent-builder/permissions.md#conversation-access-control). |
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

### Example: List available agents
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

## Examples

The [`elastic/workflows` GitHub repo](https://github.com/elastic/workflows) contains more than 50 examples you can use as a starting point.

## Related pages
* [Tools overview](./tools.md)
* [Workflow tools](../agent-builder/tools/workflow-tools.md)
* [Author workflows with natural language](/explore-analyze/workflows/authoring-techniques/use-natural-language.md)
* [Agent Builder API]({{kib-apis}}group/endpoint-agent-builder)
