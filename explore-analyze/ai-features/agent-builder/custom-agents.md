---
navigation_title: "Custom agents"
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

# Custom agents in {{agent-builder}}

Custom agents enable you to create specialized AI assistants tailored to your specific use cases and workflows. Unlike [built-in agents](builtin-agents-reference.md), which are pre-configured by Elastic, custom agents give you full control over instructions, tools, and behavior.

:::{note}
The default `Elastic AI Agent` is immutable and cannot be edited. To customize agent behavior, you need to create a custom agent by cloning the default agent or creating a new one from scratch.
:::

## Create a new agent

Follow these steps to create a new custom agent:

:::::{stepper}
::::{step} Navigate to the Agents page

Navigate to the **Agents** page to access the agent management interface.

::::

::::{step} Create a new agent

Select the **New agent** button to begin creating a new agent.

:::{image} images/new-agent-button.png
:screenshot:
:alt: Select the New agent button to create a new agent
:width: 150px
:::


::::

::::{step} Configure essential settings

Configure the essential agent settings in the **settings** tab:

1. Enter an **Agent ID**, a unique identifier for reference in code.
2. Add **Custom instructions**.<br><br>Custom instructions define the agent's personality and determine how it interacts with users and performs tasks.

    :::{note}
    Agent Builder adds your custom instructions to the system prompt to define the agent's behavior. The system prompt enables core features like visualization and citations.
    :::
3. Set the **Display name** for users.
4. Add a **Display description** to explain the agent's purpose.

::::

::::{step} Assign tools

Switch to the **Tools** tab to assign [tools](tools.md) to your agent.

Select the combination of built-in and custom tools available to the agent, based on your use case.

::::

::::{step} Customize appearance (optional)

Optionally customize the agent's appearance and organization:

- Add **Labels** to organize your agents.
- Select an **Avatar color** and **Avatar symbol** to help visually distinguish the agent.

::::

::::{step} Save your changes

Select **Save** to create your agent, or **Save and chat** to create the agent and immediately begin a conversation with it.

:::{image} images/save-and-chat-buttons.png
:screenshot:
:alt: Save and Save and chat buttons
:width: 270px
:::

::::
:::::

## Manage custom agents

From the **Agents** page, you can perform various actions on custom agents:

- **Chat**: Start a conversation with the agent.
- **Edit**: Modify the agent's settings, instructions, tools, or appearance.
- **Clone**: Create a copy of the agent as a starting point for a new agent.
- **Delete**: Remove the agent from your workspace.

:::{image} images/chat-edit-clone-delete.png
:screenshot:
:alt: Agent context menu showing Chat, Edit, Clone, and Delete options
:width: 130px
:::

:::{note}
These management options apply only to custom agents. Built-in agents like the **Elastic AI Agent** can only be chatted with or cloned, not edited or deleted.
:::

## Best practices for custom agents

When creating custom agents, follow these best practices to ensure optimal performance and usability:

### Instructions

1. **Be specific and clear**: Write instructions that clearly define the agent's role and capabilities.
2. **Define boundaries**: Specify what the agent should and shouldn't do to prevent unexpected behavior.
3. **Include examples**: Provide examples of how the agent should respond to common queries.
4. **Keep it focused**: Agents with narrow, well-defined purposes typically perform better than generalist agents.

### Tool selection

1. **Assign relevant tools only**: Limit tools to those directly related to the agent's purpose.
2. **Fewer is better**: Too many tools can confuse the agent's decision-making process.
3. **Test tool combinations**: Verify that the selected tools work well together for your use case.

### Naming and organization

1. **Use descriptive names**: Choose names that clearly convey the agent's purpose.
2. **Write meaningful descriptions**: Help users understand when to use each agent.
3. **Apply labels consistently**: Use labels to organize agents by team, use case, or department.
4. **Choose distinctive avatars**: Select unique colors and symbols to make agents easily recognizable.

### Testing and iteration

1. **Test thoroughly**: Verify the agent works correctly with various queries before deploying.
2. **Iterate based on feedback**: Refine instructions and tool assignments based on actual usage.
3. **Monitor performance**: Track how well the agent addresses user needs and adjust as necessary.

## Agents API

The Agents API enables programmatic management of custom agents.

For an overview of agent API operations, refer to [Agents API](kibana-api.md#agents).

For the complete API reference, refer to the [Kibana API reference](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-agent-builder-agents).

## Related pages

- [Agents overview](agent-builder-agents.md)
- [Built-in agents reference](builtin-agents-reference.md)
- [Tools](tools.md)
