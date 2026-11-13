---
navigation_title: Elastic Cursor plugin
description: "Install the official Elastic plugin for Cursor to give the Cursor agent Elastic agent skills and access to Elastic documentation through the Elastic Docs MCP server."
type: overview
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: elasticsearch
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Elastic plugin for Cursor [elastic-cursor-plugin]

The [Elastic plugin for Cursor](https://cursor.com/marketplace/elastic) is an official, open-source [Cursor plugin](https://cursor.com/docs/plugins) that bundles Elastic agent skills and an Elastic Docs MCP server connection into a single installable unit.
It gives the Cursor agent specialized knowledge of the {{stack}} so it can perform Elastic tasks more accurately and efficiently.
Its source is in the [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) repository.
You install the plugin in Cursor, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Use cases

### Work with {{es}} and {{kib}} from Cursor

The plugin contains agent skills that are synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository.
Refer to [AI agent skills for Elastic](../agent-skills.md) for how skills work and the areas they cover.

The Cursor agent decides when to use a skill based on your request.
You can also run a skill directly by typing `/` followed by the skill name in the chat, for example `/elasticsearch-esql`.

After you install the plugin, these skills give the Cursor agent the procedural knowledge to perform common Elastic tasks without leaving your editor:

:::{include} _snippets/plugin-skill-tasks.md
:::

### Access Elastic documentation in Cursor

The plugin registers the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets the Cursor agent search and retrieve Elastic documentation as part of any conversation.
The agent can look up configuration options, API references, and feature guides without leaving the editor.

::::{note}
The Elastic Docs MCP server only gives the Cursor agent access to Elastic documentation, not to your data.
To let the agent work with your data, install and configure the [Elastic CLI](cli://index.md).
::::

## Install the plugin

To install the plugin from Cursor:

1. Open **Customize** in the Cursor sidebar.
2. Find the **Elastic** plugin and select it.
3. Select **Add to Cursor**, then choose the project or user scope.

You can also open the [Elastic plugin page in the Cursor Marketplace](https://cursor.com/marketplace/elastic) and select **Add to Cursor**.

:::{image} ../images/cursor-marketplace-elastic-plugin.png
:screenshot:
:alt: The Elastic plugin page in the Cursor Marketplace, showing the plugin description, an Add to Cursor button, the elastic-docs MCP server, and the start of the plugin's skills list.
:width: 700px
:::

After installation, the plugin's skills and the Elastic Docs MCP server appear in **Customize**, where you can manage them.
For more about installing and managing plugins, including distributing plugins to a team, refer to the [Cursor plugins documentation](https://cursor.com/docs/plugins).

## Next steps

- [AI agent skills for Elastic](../agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [Elastic CLI](cli://index.md): Install and configure the CLI that most skills use to work with your deployment or project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server that the plugin registers.
- [elastic/cursor-plugins on GitHub](https://github.com/elastic/cursor-plugins): Source code and release history.
