---
navigation_title: "Agents and Elastic Workflows"
description: "Learn how to invoke AI agents directly within Elastic Workflows."
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

# Work with AI agents in Elastic Workflows

Elastic Workflows and {{agent-builder}} allow you to combine deterministic automation with conversational reasoning. By invoking an AI agent directly within a workflow execution, you can treat the agent as a "reasoning engine" that summarizes data, classifies events, or makes decisions before passing the results to the next step in your automation.

:::{note}
This guide explains how to call an agent from a workflow. If you want to trigger a workflow in an agent conversation, you need to create a custom [workflow tool](./tools/workflow-tools.md).
:::

## Approaches

There are two ways to integrate agents into your workflows:

* **The `ai.agent` step:** A simplified shorthand step for common operations. Use this when you want to send a prompt to an agent and receive a text response without complex configuration.
* **The `kibana.request` step:** A generic step that provides full access to the {{agent-builder}} APIs. Use this for advanced use cases, such as listing available agents or managing agent sessions programmatically.

## Prerequisites

Before you begin:

* Familiarize yourself with the core concepts of Elastic Workflows.
% (/explore-analyze/workflows.md)
* Enable the Workflows feature in **Advanced settings**.
* Ensure you have the correct privileges to create and run workflows.
% For details, refer to Set up workflows (/explore-analyze/workflows/setup.md).
* Create at least one workflow.

## Use the `ai.agent` step

Follow these steps to invoke an `ai.agent` as a step within a workflow.

1.  Open the **Workflows** editor and create or edit a workflow.
2.  Add a new step with the type `ai.agent`.
3.  Configure the **`agent_id`** parameter with the unique identifier of the target agent.
4.  Configure the **`message`** parameter with your natural language prompt.

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


## Use `kibana.request` step
Use the generic `kibana.request` step to interact with {{agent-builder}} APIs programmatically.

1. Add a new step with the type `kibana.request`.
2. Set the method (for example: `GET`, `POST`).
3. Set the `path` to the specific [Agent Builder API endpoint](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder).

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
% * [Workflows](/explore-analyze/workflows.md)
* [Agent Builder API]((https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder))