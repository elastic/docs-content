---
navigation_title: "Agents"
description: "Learn how Agent Builder agents use tools to solve problems. Compare built-in and custom agents and understand the iterative reasoning loop."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} agents overview

Agents are AI models (LLMs) defined with custom instructions and a set of assigned [tools](tools.md). {applies_to}`stack: ga 9.4+` Agents can also be equipped with [skills](skills.md), which are reusable instruction sets that provide specialized expertise. Users [chat](chat.md) with agents using natural language, in the Agent Builder UI or programmatically.

An agent parses user requests to define a goal and then runs tools in a loop to achieve that goal. The agent provides responses based on its configured tools, instructions, and behavior settings.

## How agents work

When you ask a question to an agent, it analyzes your request to define a specific goal. It selects the most appropriate tools and determines the right arguments to use. The agent evaluates the information returned after each action and decides whether to use additional tools or formulate a response. This iterative process of tool selection, execution, and analysis continues until the agent can provide a complete answer.

:::{note}
The process of tool selection, execution, and analysis consumes tokens. To understand how usage is calculated, refer to [Token usage in Elastic Agent Builder](monitor-usage.md).
:::

{{agent-builder}} includes a default agent named `Elastic AI Agent`. You can [create custom agents](custom-agents.md) with custom instructions and selected tools to address specific use cases or workflows.

You can also use pre-configured [built-in agents](builtin-agents-reference.md) that are specialized for common use cases.

## Built-in agents

{{agent-builder}} includes a pre-configured built-in agent optimized for common use cases, which you can also customize using custom instructions, tools, and skills.

- **[Elastic AI Agent](builtin-agents-reference.md#elastic-ai-agent)**: The default general-purpose agent

:::{dropdown} Previous versions
- {applies_to}`stack: preview =9.2, ga =9.3, removed 9.4+` **[Observability Agent](builtin-agents-reference.md#observability-agent)**: Specialized for logs, metrics, and traces
- {applies_to}`stack: preview =9.2, ga =9.3, removed 9.4+` **[Threat Hunting Agent](builtin-agents-reference.md#threat-hunting-agent)**: Specialized for security alert analysis
:::

:::{note}
:applies_to: stack: ga 9.2-9.3
Built-in agents cannot be modified or deleted. To customize one, you can clone it and create a custom agent.

Built-in agents are space-agnostic and are available in all [{{kib}} spaces](/deploy-manage/manage-spaces.md).
:::

For the complete list of built-in agents and their assigned tools, refer to [Built-in agents reference](builtin-agents-reference.md).

## Custom agents

Create custom agents tailored to your specific needs by defining custom instructions and selecting relevant tools. Custom agents give you full control over:

- Agent behavior and personality through custom instructions
- Available tools and capabilities
- {applies_to}`stack: ga 9.4+` Assigned skills for specialized expertise
- {applies_to}`stack: ga 9.6+` [Subagents](#subagents) the agent can delegate tasks to
- Visual appearance and organization

Custom agents are space-aware: they are only available in the [{{kib}} space](/deploy-manage/manage-spaces.md) where they were created.

To learn how to create and manage custom agents, refer to [Custom agents](custom-agents.md).

## Managing agents in the UI

The **Agents** page provides a centralized view of all your agents. From this page you can:

- View all your agents with their names and labels
- Search for specific agents using the search bar
- Filter agents by labels using the **Labels** dropdown
- Create new agents using the **New agent** button
- Start chatting with an agent or perform other actions:
    - **Built-in agents**: You can **chat** or **clone** built-in agents. They cannot be edited or deleted.
      :::{image} images/chat-and-clone-buttons.png
      :screenshot:
      :alt: Chat with agent and clone agent buttons
      :width: 120px
      :::
    - **Custom agents**: You can **chat**, **edit**, **clone**, or **delete** custom agents.

      :::{image} images/chat-edit-clone-delete.png
      :screenshot:
      :alt: Agent context menu showing Chat, Edit, Clone, and Delete options
      :width: 130px
      :::


## Elastic capabilities [elastic-capabilities]

```{applies_to}
stack: ga 9.4+
```

The **Enable Elastic capabilities** toggle controls whether an agent is automatically assigned all current and future Elastic-built [tools](tools/builtin-tools-reference.md), [skills](builtin-skills-reference.md), and plugins. The set of assigned capabilities is dynamic and grows as Elastic adds new built-in content. Disable this toggle to manage tool, skill, and plugin assignments manually.

:::{image} images/elastic-capabilities.png
:alt: Enable Elastic Capabilities toggle ON
:width: 500px
:::

This toggle is available for all agents, both built-in and custom.

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` This toggle doesn't assign [connectors](connectors.md), but it includes the `connector-discovery` skill that agents need to find their assigned connectors. You assign connectors to each agent separately, and agents start with none, including the built-in **Elastic AI Agent**. For details, refer to [Assign connectors to an agent](connectors.md#assign-connectors-to-an-agent).

### Default settings

- **Built-in agents**: Elastic capabilities are **enabled** by default. Disable if you want to limit the agent to a specific set of tools and skills.
- **Custom agents**: Elastic capabilities are **disabled** by default. Enable if you want the agent to have access to all current and future Elastic-built tools, skills, and plugins.

To review which tools and skills are active, open the agent's **Tools** or **Skills** tab after enabling the toggle. Elastic-provided items are marked with a lock icon.

## Subagents [subagents]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

An agent can delegate tasks to subagents. A subagent is another agent, or a copy of the same agent, that works on a task separately and returns the result. Use subagents to split a complex request into focused tasks, or to hand part of the work to an agent with specialized instructions and tools.

### Turn on subagents for an agent

To change an agent's subagents, you need permission to edit the agent.

1. Edit the agent and go to the **Subagents** section of the **Settings** tab. You can also select **Edit agent settings** on the agent's **Overview** page.
2. Select **Enable subagents**. **This agent (self-fork)** is added to the list.
3. Under **Delegable subagents**, select the other agents this agent can delegate to. You can only select agents that you can access. To stop the agent from delegating to a copy of itself, remove **This agent (self-fork)**.
4. Select **Save**.

Subagents are turned off for new custom agents. When the Elastic AI Agent is first created in a space on version 9.6 or later, it can delegate to a copy of itself by default.

To configure subagents with the Agents API, set `configuration.subagent_ids` when you [create]({{kib-apis}}operation/operation-post-agent-builder-agents) or [update]({{kib-apis}}operation/operation-put-agent-builder-agents-id) an agent. The list takes up to 50 agent IDs. Use `_self` to let the agent delegate to a copy of itself, rather than the agent's own ID. An empty list turns subagents off. When you update an agent without `subagent_ids`, the current list is kept.

### How subagents run

The agent decides when to delegate a task and writes the instructions for the subagent. The subagent doesn't see the conversation, only those instructions. A copy of the agent uses the same instructions, tools, and skills as the agent.

The agent can wait for a subagent to finish, or let the subagent run in the background while it continues working. Background subagents are available only in conversations that are saved.

The subagent returns its result to the agent, not to you, and the agent uses it in its response. To review what a subagent did, select the `run_subagent` tool call in the conversation, then select the **Sub-agent execution** link.

- A subagent can't delegate tasks to its own subagents.
- The agent can only delegate to agents that the current user can access. Agents in the **Delegable subagents** list that the user can't access, or that were deleted, are skipped.
- Before it delegates a task that can modify or delete data, the agent can ask you to approve the APIs the subagent can call. If you select **Deny**, the subagent runs without access to those APIs.
- Subagents can't show confirmation prompts to the user. For details, refer to [Human-in-the-loop prompts require an interactive conversation](limitations-known-issues.md#human-in-the-loop-prompts-require-an-interactive-conversation).

## Agents API

The Agents API enables programmatic management of both built-in and custom agents.

### Quick overview

For an overview, refer to [Agents API](kibana-api.md#agents-apis).

### API reference

For the complete API reference, refer to the [Kibana API reference]({{kib-apis}}operation/operation-get-agent-builder-agents).

## Related pages

- [Custom agents](custom-agents.md)
- [](prompt-engineering.md)
- [Built-in agents reference](builtin-agents-reference.md)
- [Tools](tools.md)
- [Skills in {{agent-builder}}](skills.md)