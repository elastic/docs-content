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

### Elastic deployment awareness

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Agents tailor their guidance on features, navigation, and terminology to the Elastic deployment they run in, and they can answer questions about that deployment directly. To make this possible, {{agent-builder}} adds details about the deployment to the instructions of every agent, built-in or custom. The details depend on the deployment type:

- {applies_to}`stack: ga 9.6+` **{{ech}}, {{ece}}, and self-managed**: The environment, the {{stack}} version, and, when available, the space's solution view and the license type and status. If {{kib}} is configured as air-gapped, the details also say so.
- {applies_to}`serverless: ga` **{{serverless-full}}**: The environment, the project type, and the product tier, when the project has one.

{{agent-builder}} adds these details automatically, and you can't turn them off. Agents can share these details with anyone who chats with them, even though they don't disclose their other instructions.

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
    - **Built-in agents**: You can **chat** or **clone** built-in agents. They cannot be edited or deleted. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` If you have the privilege to create and edit agents, you can also set a built-in agent as the space default.
    - **Custom agents**: You can **chat**, **edit**, **clone**, or **delete** custom agents.

      The actions menu for a custom agent also includes **Manage access** {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` if you can change the agent's access. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` It also includes **Set as space default**.

      The menu looks like this:

      :::{image} images/chat-edit-clone-delete.png
      :screenshot:
      :alt: Actions menu for a custom agent showing Chat, Edit, Clone, Manage access, Set as space default, and Delete
      :width: 130px
      :::
- {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Set an agent as the [space default agent](#space-default-agent)

### Set a default agent for a space [space-default-agent]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

You can make one agent the default agent for a {{kib}} space. Users in that space who can't manage agents can then chat only with that agent in the {{agent-builder}} UI. For example, give a team one agent that's configured for their data and tasks.

To set or remove the space default agent, you need the **Agent Builder > Management: Create and edit agents** privilege. **Agent Builder: All** also includes it. For details, refer to [](permissions.md#kib-privileges).

#### Set or remove the space default agent

To set the space default agent:

1. Go to the **Agents** page.
2. From the actions menu for the agent, select **Set as space default**.

The agent shows a **Space default** badge. Each space has at most one space default agent, so setting a new one replaces the previous one.

In the **Agents** list, the badge appears next to the name of the space default agent:

:::{image} images/space-default-agent-badge.png
:screenshot:
:alt: Agents list with a Space default badge next to the Team Agent name
:width: 500px
:::

To remove the space default agent:

1. Go to the **Agents** page.
2. From the actions menu for the space default agent, select **Remove as space default**.

#### Which agents can be the space default

These agents can be the space default:

- **Public** and **Shared** custom agents.
- Built-in agents, such as the Elastic AI Agent.

% TODO: After #9180 (hidden agents) merges, add a note that hidden agents can't be the space default. The **Set as space default** action isn't available for them.

A **Private** agent can't be the space default. If you try, {{kib}} shows an error. To use one, first change its [access control level](custom-agents.md#access-control-settings) to **Public** or **Shared**.

#### What users see

| Users | Experience |
| --- | --- |
| Without the privilege to create and edit agents | {{agent-builder}} opens with the space default agent selected. The agent selector lists only that agent, and links to other agents open the space default agent instead. In [sidebar mode](standalone-and-flyout-modes.md#sidebar-mode) {applies_to}`serverless: preview`, the chat also uses the space default agent. |
| With the privilege to create and edit agents | They can still use all the agents they have access to. {{agent-builder}} opens on the agent they last used in that browser and space. If they haven't used an agent yet, or their last agent is no longer available, it opens on the space default agent. In sidebar mode, the chat opens on the Elastic AI Agent unless the page that opens it specifies another agent. |

For users without the privilege, the agent selector lists only the space default agent, and **New agent** and **Manage agents** are disabled:

:::{image} images/space-default-agent-selector.png
:screenshot:
:alt: Agent selector open for a user without the privilege, listing only Team Agent, with New agent and Manage agents disabled
:width: 400px
:::

While the space default agent applies to them, users without the privilege can't open conversations with other agents in the {{agent-builder}} UI, including conversations that are shared with them. The conversations aren't deleted. They're available again when you remove the space default agent, or when it no longer applies to those users.

#### Special cases

Deleted or not visible
:   If the space default agent is deleted or isn't visible to a user, that user isn't restricted to it. {{agent-builder}} opens on the agent they last used in that browser and space, or on the Elastic AI Agent.

Changed to **Private**
:   Changing the space default agent to **Private** doesn't remove the setting. Users who can still see the agent remain restricted to it, and everyone else falls back as described in the previous case. To stop restricting users, select **Remove as space default**.

APIs
:   The space default agent only affects the {{agent-builder}} UI. It doesn't restrict which agents users can call through the [{{agent-builder}} APIs](kibana-api.md). To control who can use an agent, use its [access control settings](custom-agents.md#access-control-settings).


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

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The toggle doesn't affect the [HTTP API tools](tools/builtin-tools-reference.md#http-api-tools), which every agent has.

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` This toggle doesn't assign [connectors](connectors.md), but it includes the `connector-discovery` skill that agents need to find their assigned connectors. You assign connectors to each agent separately, and agents start with none, including the built-in **Elastic AI Agent**. For details, refer to [Assign connectors to an agent](connectors.md#assign-connectors-to-an-agent).

### Default settings

- **Built-in agents**: Elastic capabilities are **enabled** by default. Disable if you want to limit the agent to the tools and skills you assign. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The agent keeps the HTTP API tools.
- **Custom agents**: Elastic capabilities are **disabled** by default. Enable if you want the agent to have access to all current and future Elastic-built tools, skills, and plugins.

To review which tools and skills are active, open the agent's **Tools** or **Skills** tab after enabling the toggle. Elastic-provided items are marked with a lock icon.

## Subagents [subagents]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

An agent can delegate tasks to subagents. A subagent is another agent that works on a task separately and returns the result. The agent can also delegate to a copy of itself. In the UI, that copy is labeled **This agent (self-fork)**, and it has the same custom instructions, tools, and skills as the agent. Use subagents to split a complex request into focused tasks, or to hand part of the work to an agent with specialized instructions and tools.

### How subagents run

The agent decides when to delegate a task and writes the task instructions for the subagent. The subagent doesn't see the conversation, only those instructions.

The agent can wait for a subagent to finish, or let the subagent run in the background while it continues working. Background subagents are available only in saved conversations.

In a saved conversation, the agent can also start a named subagent and send it follow-up tasks later in that conversation with the `send_message_to_agent` tool. The named subagent keeps the history of those tasks. If you approve APIs for the first task, that approval does not apply to the follow-up tasks.

The subagent returns its result to the agent, not to you, and the agent uses it in its response. To review what a subagent did, select the `run_subagent` tool call in the conversation, then select the **Sub-agent execution** link.

#### Limits and safeguards

- A subagent can't delegate tasks to its own subagents.
- The agent can only delegate to agents that you can access. The UI and the API accept only those agents. When the agent runs, it skips agents in the **Delegable subagents** list that you can't access or that were deleted.
- Before it delegates a task that can modify or delete data, the agent might ask you to approve the APIs the subagent can call. If you select **Deny**, the subagent runs without access to those APIs.
- Subagents can't show you confirmation prompts. For details, refer to [Human-in-the-loop prompts require an interactive conversation](limitations-known-issues.md#human-in-the-loop-prompts-require-an-interactive-conversation).

### Configure subagents

New custom agents have subagents turned off. By default, the Elastic AI Agent can delegate to a copy of itself. If the Elastic AI Agent existed in a space before subagents were available, for example after an upgrade, it keeps its configuration without subagents.

To change an agent's subagents, you need permission to edit the agent.

1. Edit the agent and go to the **Subagents** section of the **Settings** tab. You can also select **Edit agent settings** on the agent's **Overview** page.
2. Select **Enable subagents**. **This agent (self-fork)** appears under **Delegable subagents**.
3. Under **Delegable subagents**, select the other agents this agent can delegate to. To stop the agent from delegating to a copy of itself, remove **This agent (self-fork)**.
4. Select **Save**.

The following example shows an agent that can delegate tasks to a copy of itself and to one custom agent:

:::{image} images/agent-subagents-settings.png
:screenshot:
:alt: The Subagents section of the agent Settings tab, with Enable subagents selected and This agent (self-fork) and a custom agent selected under Delegable subagents.
:width: 700px
:::

#### Configure subagents with the API

To configure subagents with the Agents API, set `configuration.subagent_ids` when you [create]({{kib-apis}}operation/operation-post-agent-builder-agents) or [update]({{kib-apis}}operation/operation-put-agent-builder-agents-id) an agent:

- The list takes up to 50 unique agent IDs.
- To let the agent delegate to a copy of itself, use `_self`. You can't use the agent's own ID.
- An empty list turns subagents off.
- If you omit `subagent_ids` when you update an agent, the agent keeps its current list.

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