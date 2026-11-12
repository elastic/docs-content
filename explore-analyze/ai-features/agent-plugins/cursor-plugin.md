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
The plugin is listed in the Cursor Marketplace, and its source is in the [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) repository.
You install the plugin in Cursor, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Use cases

### Work with {{es}} and {{kib}} from Cursor

The plugin contains agent skills that are synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository.
Refer to [AI agent skills for Elastic](../agent-skills.md) for more about how skills work.

After you install the plugin, these skills give the Cursor agent the procedural knowledge to perform common Elastic tasks without leaving your editor:

- Write and run {{esql}} queries against a live cluster.
- Build and manage {{kib}} dashboards, alerting rules, and workflows.
- Onboard a service into {{observability}} using {{edot}}.
- Triage {{elastic-sec}} alerts and manage cases.
- Provision Elastic Cloud resources and manage user access.

The Cursor agent loads a skill automatically when your request matches it.
You can also run a skill directly by typing `/` followed by the skill name in the chat, for example `/elasticsearch-esql`.

### Access Elastic documentation in Cursor

The plugin registers the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets the Cursor agent search and retrieve Elastic documentation as part of any conversation.
The agent can look up configuration options, API references, and feature guides without leaving the editor.

::::{note}
The Elastic Docs MCP server only gives the Cursor agent access to Elastic documentation, not to your data.
To let the agent work with the data in your deployment or project, also connect Cursor to the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md).
::::

## Install the plugin

To install the plugin from Cursor:

1. Open **Customize** in the Cursor sidebar.
2. Search for **Elastic** and select the Elastic plugin.
3. Select **Install**, then choose whether to install the plugin for the current project or for your user.

You can also open the [Elastic plugin page in the Cursor Marketplace](https://cursor.com/marketplace/elastic) and install it from there.

After installation, the plugin's skills and the Elastic Docs MCP server appear in **Customize**, where you can turn them on or off.
For more about installing and managing plugins, including distributing plugins to a team, refer to the [Cursor plugins documentation](https://cursor.com/docs/plugins).

## Next steps

- [AI agent skills for Elastic](../agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md): Connect Cursor to the data in your deployment or project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server that the plugin registers.
- [elastic/cursor-plugins on GitHub](https://github.com/elastic/cursor-plugins): Source code and release history.
