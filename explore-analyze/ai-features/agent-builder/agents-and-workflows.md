---
navigation_title: "Call agents from workflows"
description: "Learn how to connect Agent Builder agents and Elastic Workflows, including workflow tools, pre-execution workflows, and the `ai.agent` step."
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

# Call {{agent-builder}} agents from Elastic Workflows

Elastic Workflows and {{agent-builder}} allow you to combine deterministic automation with conversational reasoning. By invoking an AI agent directly within a workflow execution, you can treat the agent as a "reasoning engine" that summarizes data, classifies events, or makes decisions before passing the results to the next step in your automation.

:::{note}
This guide explains how to call an agent from a workflow. If you want to trigger a workflow in an agent conversation, you need to create a custom [workflow tool](./tools/workflow-tools.md). For workflows that run before the agent makes any LLM calls in response to a user message, refer to [Pre-execution workflows](#pre-execution-workflows).
:::

## Approaches

There are three ways to integrate agents and workflows:

* **The `ai.agent` step:** A simplified shorthand step for common operations. Use this when you want to send a prompt to an agent and receive a text response without complex configuration.
* **The `kibana.request` step:** A generic step that provides full access to the {{agent-builder}} APIs. Use this for advanced use cases, such as listing available agents or managing agent sessions programmatically.
* **Pre-execution workflows:** Workflows assigned to an agent that run once after each user message, before the agent makes any LLM calls in response. Use this when you want deterministic setup or validation before the LLM starts.

## Prerequisites

Before you begin:

* Familiarize yourself with the core concepts of [Elastic Workflows](/explore-analyze/workflows.md).
* Enable the Workflows feature in **Advanced settings**.
* Ensure you have the correct privileges to create and run workflows.
* For details, refer to [Set up workflows](/explore-analyze/workflows/get-started/setup.md).
* Create at least one workflow.

## Pre-execution workflows [pre-execution-workflows]

Pre-execution workflows run after each user message, before the agent makes any LLM calls in response. They let you use Elastic Workflows for deterministic preparation or control before the agent begins its reasoning loop.

A pre-execution workflow runs once for each user message. It does not run before every LLM call or tool call within the agent's response.

Pre-execution workflows can:

* Add or rewrite prompt context before the agent starts.
* Cancel the agent run when a workflow detects that the request should not continue.
* Run multiple workflows in sequence when more than one workflow is assigned.

To configure pre-execution workflows:

1. Select **Manage components** at the bottom of the left sidebar, then select **Agents**.
2. Select an agent, then go to **Settings**.
3. In **Pre-execution workflow**, select **Workflows**.
4. Select one or more workflows to run after each user message and before the agent makes any LLM calls in response.
5. Save the agent.

:::{image} images/pre-execution-workflows.png
:screenshot:
:width: 900px
:alt: Edit agent settings flyout showing the Pre-execution workflow section with a workflow selector
:::

Only administrators can configure pre-execution workflows. The Workflows feature must also be enabled in **Advanced settings**.

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
* [Workflows](/explore-analyze/workflows.md)
* [Agent Builder API]({{kib-apis}}group/endpoint-agent-builder)