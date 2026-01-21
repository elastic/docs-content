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
4. Fill in the required fields:
  * **Tool ID**: Create a unique identifier for the tool.
  * **Description**: Ensure the description clearly explains *when* the agent should use this tool. 
5. Click **Save**.

### Invoke the tool in chat
Once you assign this tool to an agent, the agent can trigger the workflow autonomously.
1. Navigate to **Agents > More > View all agents** and add the tool to the selected agent.
2. In the **Agent chat**, and ask a question that triggers the workflow.
3. The agent will extract the necessary parameters from the conversation, execute the workflow, and return the workflow's final output to the chat.

:::{image} images/agent-builder-worflow-tool.png
:screenshot:
:width: 500px
:alt: Screenshot of the JSON raw response modal
:::

## Use agents in workflows
You can incorporate AI agents into your automated workflows using the `ai.agent` step type. This allows you to treat an agent as a "reasoning engine" that takes data from previous steps, processes it, and returns a human-readable summary or decision.

### Add an AI Step
When authoring a workflow, use the `ai.agent` type to invoke an agent.

1. Navigate to **Workflows**.
2. Select **Create a new workflow** as the tool type.
3. Add workflow step calling the agent or something

#### Example: AI Analysis Step
This step calls a specific agent to analyze data retrieved in previous steps.

```yaml
name: list_agents
enabled: true
triggers:
  - type: manual
steps:
  - name: ai_analysis
    type: ai.agent
    with:
      agent_id: "agent_security_analyst" <1>
      message: | <2>
        Analyze the following error logs and determine if they indicate a security breach:
        {{ steps.get_error_logs.output }}
```
1. **agent_id**: The ID of the agent you want to call (must exist in Agent Builder).
2. **message**: The prompt sent to the agent. You can use template variables (like {{ steps.step_name.output }}) to inject data dynamically.

### Call Agent Builder APIs
For advanced use cases, workflows can interact with {{agent-builder}} programmatically using the generic kibana.request step. This allows you to perform management actions that aren't covered by the `ai.agent` step, such as listing available agents.

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