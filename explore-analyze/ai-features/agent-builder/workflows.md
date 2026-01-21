---
navigation_title: "Workflows"
applies_to:
  stack: preview =9.3
  serverless: preview
---

# Workflows in {{agent-builder}}

{{agent-builder}} integrates bi-directionally with [Elastic Workflows](TODO-LINK-TO-WORKFLOWS). This integration bridges the gap between conversational reasoning and automated execution:

1. **Agents trigger Workflows:** Agents can be equipped with **Workflow tools**. This allows an agent to recognize when a specific automated process is needed (like "triage this alert" or "restart the service") and execute a predefined workflow to handle it.
2. **Workflows call Agents:** Workflows can include **AI Steps**. These steps invoke an agent to handle complex reasoning tasks—such as summarizing logs, classifying security events, or making decisions—within the middle of a deterministic workflow.

## Prerequisites

Before using these features, ensure that:
* The **Workflows** feature is enabled in your deployment.
* You have appropriate permissions to create and execute workflows.

## Use workflows as tools
You can wrap an existing workflow into a tool that your agent can call. This is ideal for tasks that require a strict, repeatable sequence of actions.

:::{image} images/create-new-tool-workflows.png
:screenshot:
:width: 900px
:alt: Screenshot of the JSON raw response modal
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
3. The agent will extract the necessary parameters from the conversation, execute the workflow, and return the workflow's final output to the chat.

:::{image} images/agent-builder-worflow-tool.png
:screenshot:
:width: 500px
:alt: Screenshot of the JSON raw response modal
:::

## Use agents in workflows
You can incorporate AI agents into your automated workflows using the `ai.agent` step type. This allows you to treat an agent as a "reasoning engine" that takes data from previous steps, processes it, and returns a human-readable summary.

### Add an AI Step
When authoring a workflow, use the `ai.agent` type to invoke an agent.

1. Navigate to **Workflows**.
2. Select **Create a new workflow**
3. Add workflow step calling the selected AI agent.

#### Example: Analyze Flight Delays
This workflow searches the sample flight data for delays and asks the **Elastic AI Agent** to summarize the most impacted airlines.

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
      agent_id: "elastic-ai-agent"
      message: |
        Review the following flight delay records and summarize which airlines are most affected and the average delay time:
        {{ steps.get_delayed_flights.output }}

  # Step 3: Print the agent's summary
  - name: print_summary
    type: console
    with:
      message: "{{ steps.summarize_delays.output }}"
```
1. **agent_id**: The ID of the agent you want to call (must exist in Agent Builder).
2. **message**: The prompt sent to the agent. You can use template variables (like {{ steps.step_name.output }}) to inject data dynamically.

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
* [Tools overview](tools.md)
* [Workflows](TODO-LINK-TO-WORKFLOWS)