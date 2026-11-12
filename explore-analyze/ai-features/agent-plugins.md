---
navigation_title: Agent plugins
description: "Install official Elastic plugins for Claude and Cursor to give AI agents Elastic agent skills and access to Elastic documentation through the Elastic Docs MCP server."
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

Elastic publishes official, open-source plugins for AI agent tools such as Claude and Cursor.
Each plugin packages [Elastic agent skills](agent-skills.md) and a connection to the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server) so you can add them to your agent in one step, from the tool's own plugin marketplace.
You install a plugin in the AI tool, not in {{es}}, {{kib}}, or your {{serverless-short}} project.

## Available plugins

| Plugin | Install from | Source |
| --- | --- | --- |
| [Elastic plugin for Claude](agent-plugins/claude-plugin.md) | Claude **Plugins** settings | [elastic/claude-plugin](https://github.com/elastic/claude-plugin) |
| [Elastic plugin for Cursor](agent-plugins/cursor-plugin.md) | [Cursor Marketplace](https://cursor.com/marketplace/elastic) | [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) |

## What the plugins include

Both plugins contain the same two components:

Agent skills
:   Skill packages synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository on each release. Skills give the agent procedural knowledge for common Elastic tasks, such as writing {{esql}} queries, building {{kib}} dashboards, onboarding services into {{observability}}, and triaging {{elastic-sec}} alerts.

Elastic Docs MCP server
:   A connection to the public [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets the agent search and retrieve Elastic documentation during a conversation.

The plugins give the agent knowledge about Elastic. They don't give it access to the data in your deployment or project.
To work with your data, connect the agent to the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md) of your deployment or project. Claude users can add the [Elastic Cloud Serverless connector for Claude](claude-connector.md) instead.

## Plugins compared to installing skills directly

The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository is the authoritative source for Elastic agent skills.
You can [install skills directly](agent-skills.md#installation) from that repository into any compatible AI agent, and choose which skills to install.

Use a plugin when your agent supports one. A plugin installs all Elastic skills and the Elastic Docs MCP server together, in one step from the agent's plugin marketplace.
