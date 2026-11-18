---
navigation_title: Elastic Cursor plugin
description: "Install the official Elastic plugin for Cursor to give Cursor agent skills and access to documentation through the Elastic Docs MCP server."
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
sub:
  plugin-host: "Cursor"
  skill-command-example: "/elasticsearch-esql"
---

# Elastic plugin for Cursor [elastic-cursor-plugin]

The [Elastic plugin for Cursor](https://cursor.com/marketplace/elastic) is an official, open-source [Cursor plugin](https://cursor.com/docs/plugins) that bundles agent skills and an Elastic Docs MCP server connection into a single installable unit.
It gives the Cursor agent specialized knowledge of the {{stack}} so it can perform Elastic tasks more accurately and efficiently.
You install the plugin in Cursor, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Use cases

### Work with {{es}} and {{kib}} from Cursor

:::{include} _snippets/plugin-skills-use-case.md
:::

### Access Elastic documentation in Cursor

:::{include} _snippets/plugin-docs-mcp-use-case.md
:::

## Install the plugin

To install the plugin from Cursor:

1. Open **Customize** in the Cursor sidebar.
2. Find the **Elastic** plugin and select it.
3. Select **Add to Cursor**, then choose the project or user scope.

:::{image} ../images/cursor-elastic-plugin.png
:screenshot:
:alt: The Elastic plugin details page in Cursor, showing the plugin description, an Add to Cursor button, the elastic-docs MCP server, and the start of the plugin's skills list.
:width: 700px
:::

You can also open the [Elastic plugin page in the Cursor Marketplace](https://cursor.com/marketplace/elastic) and install it from there.

After installation, the plugin's skills and the Elastic Docs MCP server appear in **Customize**, where you can manage them.
For more about installing and managing plugins, including distributing plugins to a team, refer to the [Cursor plugins documentation](https://cursor.com/docs/plugins).

## Next steps

- [AI agent skills for Elastic](../agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [Elastic CLI](cli://index.md): Install and configure the CLI that most skills use to work with your deployment or project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server that the plugin registers.
- [elastic/cursor-plugins on GitHub](https://github.com/elastic/cursor-plugins): Source code and release history.
