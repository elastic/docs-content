---
navigation_title: "Use workflows"
description: "Learn how to trigger Elastic Workflows from Elastic Agent Builder and invoke your agents within workflow steps."
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

# Integrate workflows with {{agent-builder}}

Workflows and {{agent-builder}} are built to work together:
% (/explore-analyze/workflows.md)

* Assign agents workflow tools to trigger workflows from your chats.
* Add `ai.agent` steps to invoke agents in your workflows.

Agents chat with your data by retrieving, summarizing, and reasoning. Workflows execute reliably with business-grade guardrails. Together, they combine flexible reasoning with deterministic execution.

## Before you begin

Before using these features, ensure that:

* **Workflows are set up:** The feature must be enabled and you need specific privileges to create and run workflows. For details, see Set up workflows
% (/explore-analyze/workflows/setup.md).
* (Optional) If using the example below, ensure the [{{kib}} sample flight data](https://www.elastic.co/docs/extend/kibana/sample-data) is installed.

## Trigger a workflow from an agent
Follow these steps to wrap an existing workflow into a tool that your agent can call. This is ideal for tasks that require a strict, repeatable sequence of actions.

:::{image} ../images/create-new-tool-workflows.png
:screenshot:
:width: 900px
:alt: Screenshot of creating a new workflow tool.
:::

### Create a workflow tool
1. Navigate to **Agents > More > View all tools > New tool**.
2. Select **Workflow** as the tool type.
3. Select the specific workflow you want to wrap from the drop down list.

    :::{note}
    The UI will automatically detect the `inputs` defined in your workflow YAML and map them to tool parameters.
    :::

4. Fill in the required fields:
  * **Tool ID**: Create a unique identifier for the tool.
  * **Description**: Ensure the description clearly explains *when* the agent should use this tool. 
5. Click **Save**.

### Invoke the tool in chat
Once you assign this tool to an agent, the agent can trigger the workflow autonomously.

1. Navigate to **Agents**, select your agent, and click **Add tool** to assign the workflow tool you just created.
2. Open the **Agent chat** and ask a question that triggers the workflow.
3. The agent extracts the necessary parameters from the conversation, runs the workflow, and returns the workflow's final output to the chat.

:::{image} ../images/agent-builder-workflow-tool.png
:screenshot:
:width: 500px
:alt: Screenshot of reasoning steps of agent builder.
:::

## Call an agent from a workflow
Follow these steps to invoke an AI agent as a step within a workflow. This allows you to use the agent's reasoning capabilities to process data and return a summary.

1.  Open the **Workflows** editor and create or edit a workflow.
2.  Add a new step with the type `ai.agent`.
3.  Configure the step with the following parameters:
    * **`agent_id`**: The ID of the agent to call.
    * **`message`**: The prompt to send to the agent.

#### Example: Analyze flight delays
The following example demonstrates a workflow that searches for flight delays and uses the **Elastic AI Agent** to summarize the impact.

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
    with:
      agent_id: "elastic-ai-agent" <1>
      message: | <2>
        Review the following flight delay records and summarize which airlines are most affected and the average delay time:
        {{ steps.get_delayed_flights.output }}

  # Step 3: Print the agent's summary
  - name: print_summary
    type: console
    with:
      message: "{{ steps.summarize_delays.output }}"
```
1. **agent_id**: The ID of the agent you want to call (must exist in Agent Builder).
2. **message**: The prompt sent to the agent. You can use template variables (like `{{ steps.step_name.output }}`) to inject data dynamically.

### Call Agent Builder APIs
For advanced use cases, workflows can interact with {{agent-builder}} programmatically using the generic `kibana.request` step. This allows you to perform management actions that aren't covered by the `ai.agent` step, such as listing available agents.

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

## Related pages
* [Tools overview](../tools.md)
% * [Workflows](/explore-analyze/workflows.md)