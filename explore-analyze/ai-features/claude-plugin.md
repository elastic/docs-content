---
navigation_title: Elastic plugin for Claude
description: "Install the official Elastic plugin for Claude to give the Claude AI assistant specialized skills, MCP server access, and Elastic-stack knowledge in any Claude environment."
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

The [Elastic plugin for Claude](https://github.com/elastic/claude-plugin) is an official, open-source [Claude plugin](https://docs.claude.com/en/docs/claude-code/plugins) that bundles Elastic agent skills and an Elastic Docs MCP server connection into a single installable unit. It gives Claude specialized knowledge of the {{stack}} so it can perform Elastic tasks more accurately and efficiently. The plugin is compatible with Claude Code and Claude Cowork, and has been tested on the desktop and web apps.

## Use cases

### Work with {{es}} and {{kib}} from a Claude environment

Once installed, the plugin gives Claude the procedural knowledge to perform common Elastic tasks without leaving your editor or terminal:

- Write and run ES|QL queries against a live cluster.
- Build and manage {{kib}} dashboards, alerting rules, and workflows.
- Onboard a service into {{observability}} using EDOT.
- Triage {{elastic-sec}} alerts and manage cases.
- Provision Elastic Cloud resources and manage user access.

### Access Elastic documentation in conversations

The plugin registers the Elastic Docs MCP server, which lets Claude search and retrieve Elastic documentation as part of any conversation. Claude can look up configuration options, API references, and feature guides without leaving the chat session.

## What's in the plugin

The plugin bundles two components:

- **Agent skills** — skill packages synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository. Each skill is a `SKILL.md` file with metadata and instructions that Claude loads on demand when it detects a matching task. Skills cover {{es}}, {{kib}}, {{observability}}, {{elastic-sec}}, and Elastic Cloud. See [AI agent skills for Elastic](agent-skills.md) for the full list and how skills work.
- **Elastic Docs MCP server** — an `.mcp.json` entry that registers the public [Elastic Docs MCP server](https://www.elastic.co/docs/_mcp/) so Claude can query documentation directly.

Skills are maintained in the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository and synced into the plugin on each release. The MCP server configuration is authored directly in the plugin repository and is not overwritten by the sync.

## Relationship to agent skills

The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository is the authoritative source for Elastic agent skills. You can install skills from that repository into any compatible AI coding agent, including those outside Claude environments. See [AI agent skills for Elastic](agent-skills.md) for installation instructions.

The Elastic plugin for Claude packages those same skills into the Claude plugin format and adds the MCP server registration on top. The plugin is the recommended approach for Claude users because it installs everything in one step, but the underlying skills are identical.

## Installation

### Claude UI

1. Open **Settings** → **Plugins** → **Discover**.
2. Search for **Elastic**.
3. Select **Add** to install the plugin.

:::{image} images/claude-code-discover-elastic-plugin.png
:screenshot:
:alt: The Claude Code plugins panel showing the Discover tab with a search for Elastic. The Elastic plugin appears as the top result with an Add button.
:width: 700px
:::

### Claude CLI

```bash
claude plugin install elastic
```

## Next steps

- [AI agent skills for Elastic](agent-skills.md) — install individual skills without a plugin, or learn about the skills format.
- [Elastic Docs MCP server](/get-started/machine-readable-docs#docs-mcp-server) — connect other agents or tools to the same documentation server the plugin registers.
- [elastic/claude-plugin on GitHub](https://github.com/elastic/claude-plugin) — source code, changelog, and contribution guide.

## Related pages

- [AI agent skills for Elastic](agent-skills.md)
- [Access Elastic docs in machine-readable formats](/get-started/machine-readable-docs)
- [Plugins in {{agent-builder}}](agent-builder/plugins.md)
