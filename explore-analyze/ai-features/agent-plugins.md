---
navigation_title: Agent plugins
description: "Official Elastic plugins bring Elastic agent skills, Elastic documentation access, and other Elastic extensions to AI agent ecosystems in a single install from each tool's plugin marketplace."
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

# Elastic plugins for AI agents [elastic-agent-plugins]

Elastic publishes official, open-source plugins for AI agent tools.
A plugin packages Elastic components, such as [Elastic agent skills](agent-skills.md) and a connection to the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), so you can add them to your agent in one step from the tool's own plugin marketplace.
You install a plugin in the AI tool, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Available plugins

| Plugin | Install from | Source |
| --- | --- | --- |
| [Elastic plugin for Claude](agent-plugins/claude-plugin.md) | Claude **Settings** → **Plugins** | [elastic/claude-plugin](https://github.com/elastic/claude-plugin) |
| [Elastic plugin for Cursor](agent-plugins/cursor-plugin.md) | [Cursor Marketplace](https://cursor.com/marketplace/elastic) | [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) |

## What a plugin can include

Each AI tool defines what its plugins can contain. Depending on the tool, a plugin can bundle components such as agent skills, MCP server connections, hooks, commands, and subagents.
The contents of each Elastic plugin can differ by tool and change between releases. Each plugin's page describes what it currently provides.

Elastic plugins are built from these common components:

Agent skills
:   Skill packages synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository. Skills give the agent procedural knowledge for common Elastic tasks, such as writing {{esql}} queries, building {{kib}} dashboards, onboarding services into {{observability}}, and triaging {{elastic-sec}} alerts.

Elastic Docs MCP server
:   A connection to the public [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets the agent search and retrieve Elastic documentation during a conversation.

The plugins don't include credentials or a connection to your deployment or project.
To let the agent work with your data, install and configure the [Elastic CLI](cli://index.md). Most skills that act on a cluster or on {{ecloud}} run their operations through it.

## Plugins compared to installing skills directly

The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository is the authoritative source for Elastic agent skills.
You can [install skills directly](agent-skills.md#installation) from that repository into any compatible AI agent, and choose which skills to install.

Use a plugin when your agent supports one. A plugin installs all Elastic skills, together with the plugin's other components, in one step from the agent's plugin marketplace.

## Next steps

- [AI agent skills for Elastic](agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [Elastic CLI](cli://index.md): Install and configure the CLI that most skills use to work with your deployment or project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server that the plugins register.
