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
* **Use agents from workflows:** Invoke an agent from a workflow with the [`ai.agent` step](#use-ai-agent-workflow-step). For advanced API operations, use the [`kibana.request` step](#use-kibana-request-workflow-step).

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

A pre-execution workflow runs once for each user message. It does not run before every LLM call or tool call within the agent's response.

Pre-execution workflows can:

* Add or rewrite prompt context before the agent starts.
* Cancel the agent run when a workflow detects that the request should not continue.
* Run multiple workflows in sequence when more than one workflow is assigned.

You can assign pre-execution workflows to a single agent or to every agent in a space. If you do both, the agent runs the workflows from both settings.

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
| `connector-id` | Top level | string | No | The GenAI connector to use for model routing. Mutually exclusive with `inference-id`. |
| `inference-id` | Top level | string | No | The {{infer}} endpoint ID to use for model routing. Mutually exclusive with `connector-id`. |
| `create-conversation` | Top level | boolean | No | When `true`, persists the conversation so that follow-up steps or later requests can continue it. |
| `message` | `with` | string | Yes | The natural language prompt to send to the agent. Can include template variables to reference data from previous steps. |
| `schema` | `with` | object | No | A JSON Schema object that defines the structure of the expected response. When provided, the agent returns structured data matching the schema instead of free-text. |
| `conversation_id` | `with` | string | No | Continue an existing conversation by ID. |
| `attachments` | `with` | array | No | Attachments to provide to the agent. |

For the complete step reference, refer to [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent).


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
