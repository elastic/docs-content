---
navigation_title: "Workflow tools"
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

# Workflow tools

Workflow tools enable agents to trigger Elastic Workflows directly from a conversation. By wrapping a workflow in a tool, you allow the agent to offload complex, multi-step, or deterministic tasks to the workflow engine while maintaining a natural language interface with the user.

% (/explore-analyze/workflows.md)

## Prerequisites

Before using these features, ensure that:

* **Workflows basics**: Familiarize yourself with the core concepts of Elastic Workflows before you begin.
% (/explore-analyze/workflows.md)
* **Workflows are set up:** The feature must be enabled and you need specific privileges to create and run workflows. For details, see Set up workflows
% (/explore-analyze/workflows/setup.md).

## Add a Workflow tool

Follow these steps to configure a tool to invoke a workflow that an agent can call. This is ideal for tasks that require a strict, repeatable sequence of actions.

:::{image} ../images/create-new-tool-workflows.png
:screenshot:
:width: 900px
:alt: Screenshot of creating a new workflow tool.
:::

1. Navigate to **Agents > More > View all tools > New tool**.
2. Select **Workflow** as the tool type.
3. Select the specific workflow you want to wrap from the drop down list.
4. Fill in the required fields:

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

5. Click **Save**.

## Invoke the Workflow tool in Agent chat
Once you assign a Workflow tool to an agent, the agent can trigger the workflow autonomously.

:::{image} ../images/agent-builder-workflow-tool.png
:screenshot:
:width: 500px
:alt: Screenshot of reasoning steps of agent builder.
:::

1. Navigate to **Agents**.
2. Select your agent.
3. Select **More > Edit Agent > Tools**
4. Assign the workflow tool by selecting the checkbox.
5. Click **Save**.
6. Open the **Agent chat** and ask a question that triggers the workflow.
7. The agent extracts the necessary parameters from the conversation, runs the workflow, and returns the workflow's final output to the chat.


<!--
## Call an agent from a workflow
Follow these steps to invoke an AI agent as a step within a workflow. This allows you to use the agent's reasoning capabilities to process data and return a summary.

* (Optional) If using the example below, ensure the [{{kib}} sample flight data](https://www.elastic.co/docs/extend/kibana/sample-data) is installed.

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
-->

## Related pages
* [Tools overview](../tools.md)
% * [Workflows](/explore-analyze/workflows.md)