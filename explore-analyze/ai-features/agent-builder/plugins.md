---
navigation_title: "Plugins"
description: "Learn about Agent Builder plugins, installable packages compatible with the Claude agent plugin specification that bundle agent capabilities such as skills."
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Plugins in {{agent-builder}}

:::{note}
:applies_to: stack: preview 9.4+, serverless: preview

The plugins library is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) in {{kib}}.
:::

Plugins are installable packages that bundle agent capabilities such as skills, and are compatible with the [Claude agent plugin specification](https://docs.claude.com/en/docs/claude-code/plugins). Use a plugin to add a set of related capabilities to an agent in a single install.

## Install a plugin

To install a plugin:

1. In the left sidebar, select **Manage components** > **Plugins**.
2. Select **Install plugin**, then choose an install method:
    - **Install from URL**: Provide the URL of a plugin package hosted remotely.
    - **Upload ZIP**: Upload a plugin packaged as a `.zip` file from your local machine.
3. Confirm the install.

Installed plugins appear in the library and can be assigned to agents in the current space. You can remove a plugin from the library at any time.

## Assign a plugin to an agent

Plugins are assigned per agent. After installing a plugin, open the agent and add the plugin from its **Plugins** tab:

1. Open the agent in edit mode, or create a new agent. Refer to [Create and manage custom agents](custom-agents.md#create-a-custom-agent).
2. Select the **Plugins** tab.
3. Select **Add plugins**, choose one or more installed plugins, and save the agent.

The assigned plugin's detail panel lists its source, the skills it includes, and its plugin ID.

:::{note}
Skills bundled in a plugin are scoped to the plugin. They do not appear as independent entries in the agent's **Skills** tab or in the Skills library.
:::

:::{tip}
You can also manage plugin assignments from the **Customize** accordion in the chat UI. Refer to [Customize your agent](chat.md#customize-your-agent).
:::

## Tools referenced by plugin skills

A skill inside a plugin can reference tools that the agent calls at runtime. A tool definition packaged in a plugin gives the agent the tool's interface — its name and parameters — but does not provide the execution backend. For the agent to actually run the tool, a matching implementation must exist in the agent's tool registry.

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Tools in {{agent-builder}}](tools.md)
- [Custom agents](custom-agents.md)
- [Connectors in {{agent-builder}}](connectors.md)
