---
navigation_title: "Workflows"
applies_to:
  stack: preview =9.3
  serverless: preview
---

# Workflows in {{agent-builder}}

{{agent-builder}} integrates bi-directionally with [Elastic Workflows](https://www.elastic.co/docs/workflows). This integration allows you to:
1.  **Trigger workflows from chat:** Give your agents the ability to execute complex automation sequences (like remediating an alert or restarting a service) by equipping them with **Workflow tools**.
2.  **Call agents from workflows:** Use the reasoning capabilities of an agent as a step within a larger automation workflow.
TODO

## Prerequisites

Before using these features, ensure that:
* You have the **Workflows** feature enabled and configured.
* You have appropriate permissions to create and execute workflows.
TODO

## Use workflows as tools
You can wrap an existing workflow into a tool that your agent can call. This allows the agent to trigger defined processes based on user requests.
TODO

### Create a workflow tool
TODO

### Invoke the tool in chat
Once the tool is assigned to an agent, the agent can trigger it when the conversation context requires it.
TODO

## Use agents in workflows
You can incorporate AI agents into your automated workflows to handle tasks that require natural language processing or decision-making.
TODO

### Call Agent Builder APIs
Workflows can interact with {{agent-builder}} programmatically.
TODO

## Related pages
TODO
