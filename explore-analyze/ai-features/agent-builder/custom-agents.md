---
navigation_title: "Custom agents"
description: "Learn how to create and manage custom agents in Agent Builder. Define custom instructions, assign tools, and iterate on agent behavior for specific workflows."
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

# Create and manage custom agents in {{agent-builder}}

Custom agents enable you to create specialized AI assistants tailored to your specific use cases and workflows. Unlike [built-in agents](builtin-agents-reference.md), which are pre-configured by Elastic, custom agents give you full control over instructions, tools, and behavior.

:::{note}
Built-in agents are immutable and cannot be edited. To customize agent behavior, you need to create a custom agent by cloning an agent or creating a new one from scratch. The **Elastic AI Agent** is an exception {applies_to}`stack: ga 9.4+`: as the default agent for each space, it can be edited directly.
:::

Custom agents are space-aware: they are only available in the [{{kib}} space](/deploy-manage/manage-spaces.md) where they were created. In contrast, built-in agents are available across all spaces.

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/kibana/agent-builder
:::

## Create a custom agent

Follow these steps to create a new custom agent:

::::::{stepper}
:::::{step} Navigate to the Agents page

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }

Select **Manage components** at the bottom of the left sidebar, then select **Agents**.

:::{tip}
You can also reach this page from the agent selector: open the selector in the left sidebar and select **New Agent**.
:::

:::

:::{applies-item} { stack: ga =9.3 }

Navigate to **Agents** in the main navigation.

:::

::::

:::::

:::::{step} Create a new agent

Select the **New agent** button to begin creating a new agent.

:::{image} images/new-agent-button.png
:screenshot:
:alt: Select the New agent button to create a new agent
:width: 150px
:::


:::::

:::::{step} Configure essential settings

Configure the essential agent settings in the **Settings** tab:

1. Enter an **Agent ID**, a unique identifier for reference in code.
2. Add **Custom instructions**.<br><br>Custom instructions define the agent's personality and determine how it interacts with users and performs tasks.

    :::{note}
    Agent Builder adds your custom instructions to the system prompt to define the agent's behavior. The system prompt enables core features like visualization and citations.
    :::
3. Set the **Display name** for users.
4. Add a **Display description** to explain the agent's purpose.

:::::

:::::{step} Enable Elastic capabilities (optional)
```{applies_to}
stack: ga 9.4+
```

Optionally enable the **Enable Elastic capabilities** toggle to automatically assign all Elastic-built [tools](tools/builtin-tools-reference.md), [skills](builtin-skills-reference.md), and plugins to your agent. This toggle is disabled by default for custom agents.

For more information, refer to [Elastic capabilities](agent-builder-agents.md#elastic-capabilities).

:::::

:::::{step} Configure pre-execution workflows (optional)
```{applies_to}
stack: ga 9.4+
```

Administrators can assign workflows that run once after each user message, before the agent makes any LLM calls in response. Use pre-execution workflows to prepare prompt context or stop an agent run before the LLM starts.

For details, refer to [Pre-execution workflows](agents-and-workflows.md#pre-execution-workflows).

:::::

:::::{step} Set visibility
```{applies_to}
stack: ga 9.4+
```

Configure the **Visibility** for your agent in the **Organization** section. Visibility controls who can view and edit the agent. The default setting is **Public**.

For more information, refer to [Visibility settings](#visibility-settings). You can also configure [per-agent access controls](#per-agent-access-controls) for more granular control.

:::::

:::::{step} Assign tools

Switch to the **Tools** tab to assign [tools](tools.md) to your agent.

Select the combination of built-in and custom tools available to the agent, based on your use case.

:::::

:::::{step} Assign skills (optional)
```{applies_to}
stack: ga 9.4+
```

Switch to the **Skills** tab to assign skills to your agent. Skills are reusable instruction sets that give the agent specialized expertise for particular types of tasks.

You can assign skills that already exist in your deployment's skill library—you create and manage those from [**Manage components**](chat.md#manage-components) > **Skills**—or you can create new skills inline from this tab. For an overview of skills, built-in versus custom skills, and APIs, refer to [Skills in {{agent-builder}}](skills.md).

:::::

:::::{step} Assign plugins (optional)
```{applies_to}
stack: preview 9.4+
serverless: preview
```

Switch to the **Plugins** tab to assign plugins to your agent. Each plugin bundles a set of related skills into a single install. Before you can assign a plugin, install it from the global **Plugins** page in **Manage components**.
For more information, refer to [Plugins in {{agent-builder}}](plugins.md).

:::{note}
The **Plugins** option is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}.
:::

:::::

:::::{step} Customize appearance (optional)

Optionally customize the agent's appearance and organization:

- Add **Labels** to organize your agents.
- Select an **Avatar color** and **Avatar symbol** to help visually distinguish the agent.

:::::

:::::{step} Save your changes

Select **Save** to create your agent, or **Save and chat** to create the agent and immediately begin a conversation with it.

:::{image} images/save-and-chat-buttons.png
:screenshot:
:alt: Save and Save and chat buttons
:width: 270px
:::

:::::
::::::

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
These management options apply only to custom agents and the Elastic AI Agent {applies_to}`stack: ga 9.4+`. Other built-in agents can only be chatted with or cloned, not edited or deleted.
:::

## Visibility settings

```{applies_to}
stack: ga 9.4+
```

Control who can view and edit your agent by configuring its visibility. To change visibility, edit the agent and scroll to the **Organization** section.

Every agent has one of three visibility levels:

**Public**
:   Anyone can view and edit.

**Shared**
:   Anyone can view. Only the owner or an administrator can edit.

**Private**
:   Only the owner or an administrator can view and edit.

:::{image} images/agent-visibility-levels.png
:alt: Agent visibility dropdown showing Public, Shared, and Private.
:width: 700px
:::

### Per-agent access controls

```{applies_to}
stack: ga 9.5+
serverless: ga
```

In addition to the three visibility levels, you can configure access controls for individual users on a per-agent basis. This allows you to grant specific users view or edit access to an agent, giving you more granular control over who can interact with and modify your agents.

To configure per-agent access controls:

1. Edit the agent and scroll to the **Organization** section.
2. Select a base visibility level.
3. Add individual users and assign each one a **View** or **Edit** access level.

Users you add to the access list can interact with the agent according to the access level you assign, regardless of the base visibility setting. For example, you can set an agent to **Private** and then grant specific users view or edit access.

::::{note}
Per-agent access controls only apply to **Private** and **Shared** agents. Any user in your organization can view and use a **Public** agent.
::::

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

For an overview of agent API operations, refer to [Agents API](kibana-api.md#agents-apis).

For the complete API reference, refer to the [Kibana API reference]({{kib-apis}}operation/operation-get-agent-builder-agents).

## Related pages

- [Agents overview](agent-builder-agents.md)
- [](prompt-engineering.md)
- [Built-in agents reference](builtin-agents-reference.md)
- [Tools](tools.md)
- [Skills in {{agent-builder}}](skills.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Plugins in {{agent-builder}}](plugins.md)
- [Connectors in {{agent-builder}}](connectors.md)
