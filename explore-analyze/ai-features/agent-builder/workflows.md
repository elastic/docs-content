---
navigation_title: "Workflows"
applies_to:
  stack: preview =9.3
  serverless: preview
---

# Workflows in {{agent-builder}}

{{agent-builder}} integrates bi-directionally with [Elastic Workflows](https://www.elastic.co/docs/workflows). This integration allows you to:
1.  **Agents trigger Workflows:** This allows an agent to recognize when a specific automated process is needed (like "triage this alert" or "restart the service") and execute a predefined workflow to handle it.
2.  **Workflows call Agents:** Workflows can include **AI Steps**. These steps invoke an agent to handle complex reasoning tasks—such as summarizing logs, classifying security events, or making decisions—within the middle of a deterministic workflow.

## Prerequisites

Before using these features, ensure that:
* The Workflows feature enabled in your deployment.
* Appropriate permissions to create and execute workflows.

## Use workflows as tools
You can wrap an existing workflow into a tool that your agent can call. This is ideal for tasks that require a strict, repeatable sequence of actions.

### Create a workflow tool
TODO

### Invoke the tool in chat
Once assigned to an agent, the agent will use this tool whenever a user's request matches the workflow's purpose. The agent will extract the necessary parameters from the conversation and trigger the workflow execution.

## Use agents in workflows
You can incorporate AI agents into your automated workflows using **AI Steps**. This effectively treats an agent as a function that takes context as input and returns a reasoned decision or summary.

### Add an AI Step
When building a workflow you can add an **Agentic Step**.
TODO

### Call Agent Builder APIs
Workflows can interact with {{agent-builder}} programmatically.
TODO

## Related pages
* [Tools overview](tools.md)