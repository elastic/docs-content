---
navigation_title: Elastic plugin for Claude
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

## Use cases

### Work with {{es}} and {{kib}} from a Claude environment

The plugin contains **Agent skills** — skill packages synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository.
See [AI agent skills for Elastic](agent-skills.md) for the full list and how skills work.

Once installed, these skills give Claude the procedural knowledge to perform common Elastic tasks without leaving your editor or terminal:

- Write and run ES|QL queries against a live cluster.
- Build and manage {{kib}} dashboards, alerting rules, and workflows.
- Onboard a service into {{observability}} using {{edot}}.
- Triage {{elastic-sec}} alerts and manage cases.
- Provision Elastic Cloud resources and manage user access.

::::{note}
The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository is the authoritative source for Elastic agent skills.
You can install skills directly from that repository into _any_ compatible AI coding agent, including Claude.
The plugin provides a smoother in-app installation experience.
::::

### Access Elastic documentation in conversations

The plugin registers the [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server), which lets Claude search and retrieve Elastic documentation as part of any conversation.
Claude can look up configuration options, API references, and feature guides without leaving the chat session.

## Install the plugin

In Claude on the web or in the desktop app, open **Settings** → **Plugins** → **Discover**, search for **Elastic**, and click **Add**.

:::{image} images/claude-code-discover-elastic-plugin.png
:screenshot:
:alt: The Claude settings panel with Plugins selected in the sidebar, showing the Discover tab with a search for Elastic. The Elastic plugin appears as the top result with an Add button.
:width: 700px
:::

::::{note}
Plugins installed via the Claude web app are synced to Claude Code, but with some nuances.
See the official [Claude documentation on synced plugins](https://code.claude.com/docs/en/plugins/loading#synced-plugins) for more details.
::::

## Next steps

- [AI agent skills for Elastic](agent-skills.md) — install individual skills without a plugin, or learn about the skills format.
- [Elastic Docs MCP server](/get-started/machine-readable-docs.md#docs-mcp-server) — connect other agents or tools to the same documentation server the plugin registers.
- [elastic/claude-plugin on GitHub](https://github.com/elastic/claude-plugin) — source code, changelog, and contribution guide.
