---
navigation_title: Elastic Claude plugin
description: "Install the official Elastic plugin for Claude to give the Claude AI assistant specialized skills, MCP server access, and Elastic Stack knowledge in any Claude environment."
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

# Elastic plugin for Claude [elastic-claude-plugin]

The [Elastic plugin for Claude](https://github.com/elastic/claude-plugin) is an official, open-source [Claude plugin](https://docs.claude.com/en/docs/claude-code/plugins) that bundles Elastic agent skills and an Elastic Docs MCP server connection into a single installable unit.
It gives Claude specialized knowledge of the {{stack}} so it can perform Elastic tasks more accurately and efficiently.
The plugin is compatible with Claude Code and Cowork, and has been tested on the desktop and web apps.
You install the plugin in Claude, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Use cases

### Work with {{es}} and {{kib}} from a Claude environment

The plugin contains agent skills that are synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository.
Refer to [AI agent skills for Elastic](../agent-skills.md) for how skills work and the areas they cover.

After you install the plugin, these skills give Claude the procedural knowledge to perform common Elastic tasks without leaving your editor or terminal:

:::{include} _snippets/plugin-skill-tasks.md
:::

### Access Elastic documentation in conversations

The plugin registers the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets Claude search and retrieve Elastic documentation as part of any conversation.
Claude can look up configuration options, API references, and feature guides without leaving the chat session.

::::{note}
The Elastic Docs MCP server only gives Claude access to Elastic documentation, not to your data.
To let Claude work with your data, install and configure the [Elastic CLI](cli://index.md).
For an {{serverless-full}} project, you can also add the [Elastic Cloud Serverless connector for Claude](../claude-connector.md).
::::

## Install the plugin

In Claude on the web or in the desktop app, open **Settings** → **Plugins** → **Discover**, search for **Elastic**, and click **Add**.

:::{image} ../images/claude-code-discover-elastic-plugin.png
:screenshot:
:alt: The Claude settings panel with Plugins selected in the sidebar, showing the Discover tab with a search for Elastic. The Elastic plugin appears as the top result with an Add button.
:width: 700px
:::

::::{note}
Plugins installed via the Claude web app are synced to Claude Code, but with some nuances.
See the official [Claude documentation on synced plugins](https://code.claude.com/docs/en/plugins/loading#synced-plugins) for more details.
::::

## Next steps

- [AI agent skills for Elastic](../agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [Elastic CLI](cli://index.md): Install and configure the CLI that most skills use to work with your deployment or project.
- [Elastic Cloud Serverless connector for Claude](../claude-connector.md): Connect Claude to the data in your {{serverless-short}} project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server the plugin registers.
- [elastic/claude-plugin on GitHub](https://github.com/elastic/claude-plugin): Source code, changelog, and contribution guide.
