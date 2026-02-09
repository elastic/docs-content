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

# {{agent-builder}} Agents overview

Agents are AI models (LLMs) defined with custom instructions and a set of assigned [tools](tools.md). Users [chat](chat.md) with agents using natural language, in the Agent Builder UI or programmatically.

An agent parses user requests to define a goal and then runs tools in a loop to achieve that goal. The agent provides responses based on its configured tools, instructions, and behavior settings.

## How agents work

When you ask a question to an agent, it analyzes your request to define a specific goal. It selects the most appropriate tools and determines the right arguments to use. The agent evaluates the information returned after each action and decides whether to use additional tools or formulate a response. This iterative process of tool selection, execution, and analysis continues until the agent can provide a complete answer.

:::{note}
The process of tool selection, execution, and analysis consumes tokens. To understand how usage is calculated, refer to [Token usage in Elastic Agent Builder](monitor-usage.md).
:::

{{agent-builder}} includes a default agent (named `Elastic AI Agent`) with access to all built-in tools. You can [create custom agents](custom-agents.md) with custom instructions and selected tools to address specific use cases or workflows.

You can also use pre-configured [built-in agents](builtin-agents-reference.md) that are specialized for common use cases.

## Built-in agents

{{agent-builder}} includes pre-configured built-in agents optimized for common use cases:

- **[Elastic AI Agent](builtin-agents-reference.md#elastic-ai-agent)**: The default general-purpose agent with access to all platform core tools
- **[Observability Agent](builtin-agents-reference.md#observability-agent)**: Specialized for logs, metrics, and traces
- **[Threat Hunting Agent](builtin-agents-reference.md#threat-hunting-agent)**: Specialized for security alert analysis

Built-in agents cannot be modified or deleted. To customize one, you can clone it and create a custom agent.

For the complete list of built-in agents and their assigned tools, refer to [Built-in agents reference](builtin-agents-reference.md).

## Custom agents

Create custom agents tailored to your specific needs by defining custom instructions and selecting relevant tools. Custom agents give you full control over:

- Agent behavior and personality through custom instructions
- Available tools and capabilities
- Visual appearance and organization

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

## Agents API

The Agents API enables programmatic management of both built-in and custom agents.

### Quick overview

For an overview, refer to [Agents API](kibana-api.md#agents-apis).

### API reference

For the complete API reference, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-agents).

## Related pages

- [Custom agents](custom-agents.md)
- [](prompt-engineering.md)
- [Built-in agents reference](builtin-agents-reference.md)
- [Tools](tools.md)