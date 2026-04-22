---
navigation_title: "Plugins"
description: "Learn how Agent Builder plugins bundle skills and capabilities that you can install and assign to agents."
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

A plugin is an installable package that bundles a set of related [skills](skills.md) so you can add them to an agent in a single install. For individual capabilities, use skills; for callable functions and integrations, use [tools](tools.md).

## Install a plugin

To install a plugin:

1. In the left sidebar, select **Manage components** > **Plugins**.
2. Select **Add plugins**, then choose an install method:
    - **Install from URL**: Provide the URL of a plugin package hosted remotely.
    - **Upload ZIP**: Upload a plugin packaged as a `.zip` file from your local machine.
3. Confirm the install.

Installed plugins appear in the library and are available to assign to any agent in the current space.

## Assign a plugin to an agent

Plugins are assigned per agent. After installing a plugin, open the agent you want to extend and add the plugin from the **Plugins** tab:

1. Open the agent in edit mode, or create a new agent. Refer to [Create and manage custom agents](custom-agents.md#create-a-custom-agent).
2. Select the **Plugins** tab.
3. Select **Add plugins**, choose one or more installed plugins, and save the agent.

Once assigned, the plugin's bundled skills appear in the agent's **Skills** tab and are available when the agent chats.

:::{tip}
You can also manage assignments from the **Customize** accordion in the chat UI. Refer to [Customize your agent](chat.md#customize-your-agent).
:::

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Tools in {{agent-builder}}](tools.md)
- [Custom agents](custom-agents.md)
- [Connectors in {{agent-builder}}](connectors.md)
