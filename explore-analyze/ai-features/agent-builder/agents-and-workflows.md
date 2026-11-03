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

A pre-execution workflow runs before the agent calls the model. It does not run before every LLM call or tool call inside that response. When the agent resumes after a [human-in-the-loop prompt](chat.md#human-in-the-loop-prompts), the workflow runs again for that same user message.

Pre-execution workflows can:

* Add or rewrite prompt context before the agent starts.
* Cancel the agent run when a workflow detects that the request should not continue.
* Run multiple workflows in sequence when more than one workflow is assigned.

You can assign pre-execution workflows to a single agent or to every agent in a space. If you do both, the agent runs the workflows from both settings.

### Inputs and outputs [pre-execution-workflow-inputs-and-outputs]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

A pre-execution workflow can read details about the current run and return context for the model and for workflows that run after the agent responds.

Declare inputs under the workflow's manual trigger. Refer to [`inputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs). Inside the workflow, reference an input as `{{ inputs.prompt }}`.

The Sent column shows when {{agent-builder}} sends each input:

| Input | Sent | Contains |
|---|---|---|
| `prompt` | Always | The user message for this run. An empty string when the run has no user message, such as a resume that only answers a [human-in-the-loop prompt](chat.md#human-in-the-loop-prompts). If an earlier workflow in the sequence returns `new_prompt`, later workflows receive that text as `prompt`. |
| `conversation_id` | When the run has one, even if not declared | The conversation ID. When the run doesn't save a conversation, such as an [`ai.agent` step](#use-ai-agent-workflow-step) without a conversation ID, this ID doesn't match a saved conversation. |
| `agent_id` | Only when declared | The agent ID. Omitted when the run has no agent ID. |
| `round_execution_index` | Only when declared | `0` the first time the agent runs for this user message. `1` or higher when the agent resumes after a human-in-the-loop prompt. |

To keep `agent_id` or `round_execution_index` out of the workflow, leave it out of the manual trigger. You can't omit `prompt`. You also can't omit `conversation_id` when the run has one.

If the workflow sets `additionalProperties: false`, declare every input {{agent-builder}} sends, including `conversation_id`. Otherwise input validation fails, the workflow execution is marked failed in its [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history), and the agent run stops.

On the workflow execution, `execution.triggeredBy` is `agent-builder-hook`. A workflow can check that value and skip runs that someone started directly. Refer to [`execution.triggeredBy`](/explore-analyze/workflows/reference/context-variables.md#workflows-ctx-execution).

{{agent-builder}} reads the output of the workflow's last step. That output can include `new_prompt`, `abort`, and `abort_message`. It can also include these fields:

| Output | Effect |
|---|---|
| `model_context` | Text that {{agent-builder}} sends to the model as a separate message after the user message. The conversation doesn't show this message. It stays on the round, so the model still receives it when the conversation continues. |
| `workflow_context` | Data for a workflow assigned under **Post-execution workflow**. The model never receives it. |

`model_context` must be a string. {{agent-builder}} ignores any other type, and the agent run continues. It removes leading and trailing whitespace, and it ignores a blank string. It keeps at most 100,000 characters. Workflows from the space setting run first, then workflows assigned to the agent. When more than one workflow returns `model_context`, {{agent-builder}} joins the texts with a blank line in that order, and then keeps the first 100,000 characters of the combined text.

`workflow_context` is an object keyed by namespace. Each namespace name can be at most 256 characters, and the object can contain at most 16 namespaces. Each namespace has a `version` and a `data` object:

* `version` is a positive integer.
* `data` is a JSON object. Nested objects and arrays can go eight levels deep, counting `data` as the first level.
* The combined JSON is at most 65,536 bytes.

If a workflow returns a `workflow_context` with a different shape, or one that doesn't match these limits, {{agent-builder}} ignores that value and continues. Namespaces already stored for the round stay in place. When two workflows use the same namespace, the later workflow replaces that namespace. Other namespaces are kept. If the combined value would exceed the limits, {{agent-builder}} ignores the later value and keeps the earlier one.

{{agent-builder}} stores `model_context` and `workflow_context` only from the first run of the round. The workflow still runs when the agent resumes after a human-in-the-loop prompt. That later run can stop the agent. The model keeps the original user message. Any `model_context` or `workflow_context` from that later run is ignored. A `new_prompt` from that run is still passed to later workflows in the sequence as `prompt`.

A workflow assigned under **Post-execution workflow** can receive the stored object. {{agent-builder}} passes it as that workflow's `workflow_context` input when the workflow declares the input.

The following workflow declares every input and returns both context fields. It uses [`workflow.output`](/explore-analyze/workflows/steps/composition.md#workflow-output) as its last step. That step is in technical preview. Put it at the top level of `steps`.

```yaml
version: "1"
name: add_support_context
description: Adds support policy context before the agent answers.
enabled: true
triggers:
  - type: manual
    inputs:
      properties:
        prompt:
          type: string
        conversation_id:
          type: string
        agent_id:
          type: string
        round_execution_index:
          type: number
      additionalProperties: false
steps:
  - name: return_context
    type: workflow.output
    with:
      model_context: |
        Apply the support policy before you answer.
        The user message is: {{ inputs.prompt }}
      workflow_context:
        support.policy:
          version: 1
          data:
            policy: "answer from the published support policy"
```

### Assign workflows to an agent [assign-pre-execution-workflows-to-an-agent]

1. Select **Manage components** at the bottom of the left sidebar to open the **Agents** list.
2. Select an agent, then select **Settings** → **Pre-execution workflow**.
3. Open the **Workflows** selector.
4. Select one or more workflows. They run after each user message, before the agent makes any LLM calls in response.
5. Save the agent.

To confirm the setup, send a message to the agent, then check that the run appears in the workflow's [execution history](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md#workflows-execution-history).

The following screenshot shows the **Pre-execution workflow** setting in the agent **Settings** view.

:::{image} images/pre-execution-workflows.png
:screenshot:
:width: 900px
:alt: Edit agent settings flyout showing the Pre-execution workflow section with a workflow selector
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
