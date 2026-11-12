---
navigation_title: Agent plugins
description: "Official Elastic plugins for Claude and Cursor package Elastic agent skills and the Elastic Docs MCP server, so AI agents can perform Elastic tasks and look up documentation."
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

Elastic publishes official, open-source plugins for AI agent tools, currently Claude and Cursor.
Each plugin packages [Elastic agent skills](agent-skills.md) and a connection to the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server) so you can add them to your agent in one step, from the tool's own plugin marketplace.
You install a plugin in the AI tool, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Available plugins

| Plugin | Install from | Source |
| --- | --- | --- |
| [Elastic plugin for Claude](agent-plugins/claude-plugin.md) | Claude **Settings** → **Plugins** | [elastic/claude-plugin](https://github.com/elastic/claude-plugin) |
| [Elastic plugin for Cursor](agent-plugins/cursor-plugin.md) | [Cursor Marketplace](https://cursor.com/marketplace/elastic) | [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) |

## What the plugins include

Both plugins provide the same two Elastic components:

Agent skills
:   Skill packages synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository on each release. Skills give the agent procedural knowledge for common Elastic tasks, such as writing {{esql}} queries, building {{kib}} dashboards, onboarding services into {{observability}}, and triaging {{elastic-sec}} alerts.

Elastic Docs MCP server
:   A connection to the public [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets the agent search and retrieve Elastic documentation during a conversation.

The plugins don't include credentials or a connection to your deployment or project.
Most skills that act on a cluster or on {{ecloud}} run their operations through the [Elastic CLI](cli://index.md), which you install and configure separately.

{applies_to}`stack: preview =9.2, ga 9.3+` {applies_to}`serverless: ga` To give the agent tools that work directly with your data, you can also connect it to the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md) of your deployment or project.

{applies_to}`serverless: ga` For an {{serverless-full}} project, Claude users can connect through the [Elastic Cloud Serverless connector for Claude](claude-connector.md), which connects Claude to the project's {{agent-builder}} MCP server without manual configuration.

## Plugins compared to installing skills directly

The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository is the authoritative source for Elastic agent skills.
You can [install skills directly](agent-skills.md#installation) from that repository into any compatible AI agent, and choose which skills to install.

Use a plugin when your agent supports one. A plugin installs all Elastic skills and the Elastic Docs MCP server together, in one step from the agent's plugin marketplace.

## Next steps

- [AI agent skills for Elastic](agent-skills.md): Install individual skills without a plugin, or learn about the skills format.
- [Elastic CLI](cli://index.md): Install and configure the CLI that most skills use to work with your deployment or project.
- {applies_to}`stack: preview =9.2, ga 9.3+` {applies_to}`serverless: ga` [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md): Connect an agent to the data in your deployment or project.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server): Connect other agents or tools to the same documentation server that the plugins register.
