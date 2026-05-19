---
navigation_title: Security MCP App
description: Bring interactive Elastic Security dashboards into Claude, Cursor, Visual Studio Code, and other AI tools using the Elastic Security MCP App reference implementation.
applies_to:
  stack: preview 9.4
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Elastic Security MCP App [elastic-security-mcp-app]

The Elastic Security MCP App brings interactive {{elastic-sec}} dashboards into Claude, Cursor, Visual Studio Code, and other [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) hosts. Use it to triage alerts, hunt threats, correlate attack chains, and open cases inside the AI conversation, with each action writing back to {{es}} and {{kib}} through the same APIs the product uses.

The app is a reference implementation that you install on your own machine. The [`elastic/example-mcp-app-security`](https://github.com/elastic/example-mcp-app-security) repository hosts the open-source project, including the source code, releases, and host-specific setup guides. The app is not a built-in {{kib}} feature.

:::{warning}
This feature is in technical preview and might change in future releases. Test it in non-production environments before relying on it for production workflows.
:::

For a demo, refer to the following video (click to view).

[![Elastic Security MCP App demo](https://play.vidyard.com/Axjk85zS4bxE7kdU48Xqwe.jpg)](https://videos.elastic.co/watch/Axjk85zS4bxE7kdU48Xqwe?)

## What you can do [what-you-can-do]

The Elastic Security MCP App ships with six tools, each backed by an interactive React UI that renders inline in the AI host conversation:

| Tool | What it does |
|---|---|
| **Alert Triage** | Retrieve, filter, and triage {{elastic-sec}} alerts with AI verdict cards, a process tree, and network event details. |
| **Attack Discovery** | Run AI-correlated attack chain analysis on demand, with confidence scoring, entity risk, and MITRE ATT&CK mapping. |
| **Case Management** | Create, search, and manage SOC investigation cases, with AI-assisted summary, next-step, IOC extraction, and timeline actions. |
| **Detection Rules** | Browse, tune, and manage detection rules, with Kibana Query Language (KQL) search, query validation, and noisy-rule analysis. |
| **Threat Hunt** | Run an {{esql}} workbench with clickable entities and an interactive investigation graph for pivot analysis. |
| **Sample Data** | Generate Elastic Common Schema (ECS)-compliant security events for four pre-built attack scenarios so you can demo or test without production data. |

For per-tool capabilities and screenshots, refer to the [features overview](https://github.com/elastic/example-mcp-app-security/blob/main/docs/features.md) in the repository.

## Requirements [requirements]

::::{admonition} Requirements
* {{stack}} 9.4 or later, or an {{sec-serverless}} project.
* A supported MCP host, such as: [Claude Desktop](https://claude.ai/download), [Claude.ai](https://claude.ai/), [Cursor](https://cursor.com/), [Visual Studio Code](https://code.visualstudio.com/) with [GitHub Copilot Chat](https://code.visualstudio.com/docs/copilot/overview), or [Claude Code](https://docs.claude.com/en/docs/claude-code).
* The {{es}} URL, {{kib}} URL, and an {{es}} API key for an account with the [required permissions](#permissions).
* A configured [large language model (LLM) connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md) in {{kib}} for any tool that calls Attack Discovery.
* Node.js is not required if you install with the prebuilt `.mcpb` bundle. Build-from-source workflows require Node.js 20 or later.
::::

## How it works [how-it-works]

The Elastic Security MCP App builds on the [MCP Apps extension](https://modelcontextprotocol.io/docs/extensions/apps.md) to the Model Context Protocol, which lets a tool server return an interactive HTML interface alongside its text response. The host renders that interface inside a sandboxed iframe in the conversation, and the app communicates with the host through a JSON-RPC channel that uses the [`postMessage` API](https://developer.mozilla.org/docs/Web/API/Window/postMessage).

When you ask Claude (or another supported host) to triage alerts or run a threat hunt, the host calls a model-facing tool on the app's MCP server. The server returns a compact text summary that the model reasons over, plus a React UI that renders inline. From that point on, the UI calls app-only tools directly for all subsequent interactions, which keeps the LLM context small while the UI has full data access.

The MCP server runs locally on your machine and connects directly to {{es}} using your API key. The LLM only ever receives the compact summaries; the UI loads full investigation data through the same server. The same role-based access controls you enforce through your {{es}} API key apply to every action the app takes.

## Permissions [permissions]

The Elastic Security MCP App authenticates to {{es}} with an API key. The fastest way to set up a working API key is to combine a built-in {{kib}} role with a small companion role that grants the index privileges the app needs.

For most users, the built-in `editor` role (full-featured) or `viewer` role (read-only) covers all the {{kib}} feature privileges the app needs (Security, Cases, Timeline, Notes, Rules, Alerts, AI Assistant, Attack Discovery, Actions and Connectors). You only need to add a companion role that grants {{es}} index privileges on the alert backing indices, `logs-*`, and `risk-score.risk-score-latest-*`, plus the cluster `monitor` privilege.

For step-by-step instructions, including the full Quickstart procedure, a fully scripted custom-role JSON, version-specific feature names for {{stack}} 9.0 through 9.4, and troubleshooting for common 401 and 403 errors, refer to the repository's [permissions guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/permissions.md).

:::{note}
The repository's permissions guide currently targets stateful deployments ({{stack}} self-managed and {{ech}}). {{serverless-short}} permissions guidance, including the role mapping for {{sec-serverless}} tiers such as `t1_analyst` and `soc_manager`, is pending. If you run the app against an {{sec-serverless}} project, contact the repository maintainers for guidance.
:::

## Get started [get-started]

Pick the tab for your MCP host. Each tab covers the fastest path to a working install. For full configuration options and troubleshooting, follow the linked setup guide in the repository.

:::::{tab-set}

::::{tab-item} Claude Desktop
:sync: claude-desktop

The fastest path is the one-click `.mcpb` bundle, which includes everything the app needs and prompts you for your {{es}} URL, {{kib}} URL, and API key during install.

1. Download [`example-mcp-app-security.mcpb`](https://github.com/elastic/example-mcp-app-security/releases/latest) from the latest release.
2. Double-click the file. Claude Desktop opens the installer.
3. When prompted, paste your {{es}} URL, {{kib}} URL, and API key.
4. Restart Claude Desktop and ask the agent to generate sample data to confirm the install.

For manual configuration, updating to a newer release, and troubleshooting, refer to the [Claude Desktop setup guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-claude-desktop.md).
::::

::::{tab-item} Cursor
:sync: cursor

Connect the MCP app to Cursor through `npx` or by pointing Cursor at a locally running server. Follow the [Cursor setup guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-cursor.md) for the exact configuration block to add to your Cursor settings, including the environment variables for your {{es}} URL, {{kib}} URL, and API key.
::::

::::{tab-item} Visual Studio Code
:sync: vscode

Connect the MCP app to Visual Studio Code GitHub Copilot through `npx` or by pointing the editor at a locally running server. Follow the [Visual Studio Code setup guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-vscode.md) for the exact configuration block to add to your MCP settings.
::::

::::{tab-item} Claude Code
:sync: claude-code

Register the MCP app with the [`claude mcp add`](https://docs.claude.com/en/docs/claude-code/mcp) CLI. Follow the [Claude Code setup guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-claude-code.md) for the exact command, including the environment variables for your {{es}} URL, {{kib}} URL, and API key.
::::

::::{tab-item} Claude.ai
:sync: claude-ai

Expose the MCP app to Claude.ai through a [`cloudflared`](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) tunnel that fronts your local server. Follow the [Claude.ai setup guide](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-claude-ai.md) for the tunnel configuration and the Claude.ai connector setup steps.
::::

:::::

Next, install the [skills](https://github.com/elastic/example-mcp-app-security/blob/main/docs/setup-skills.md) that help your agent determine when to use each tool.

## Example workflow [example-workflow]

The six tools compose into an end-to-end SOC loop you can drive entirely from the AI conversation. A typical walkthrough looks like this:

1. **Generate sample data.** Ask the agent to populate your cluster with one of the four pre-built attack scenarios (ransomware, lateral movement, credential theft, or data exfiltration). The Sample Data tool writes ECS-compliant events you can safely clean up later.
2. **Triage alerts.** Ask the agent to triage by host, rule, user, or time window. The Alert Triage tool returns AI verdict cards above the raw alert list. Click any alert for the process tree, network events, related alerts, and MITRE ATT&CK tags.
3. **Hunt for threats.** Ask the agent to hunt across your indices. The Threat Hunt tool returns an {{esql}} workbench with the query pre-populated and auto-executed, plus an investigation graph for entity pivots.
4. **Run Attack Discovery.** Ask the agent to correlate the alerts and findings into attack chains. The Attack Discovery tool calls the [Attack Discovery API](/solutions/security/ai/attack-discovery.md) and returns ranked findings with MITRE tactics, risk scores, and impacted hosts and users.
5. **Open cases.** Approve findings in bulk or ask the agent to open cases for specific alerts. The Case Management tool creates one case per finding, attaches the source alerts, and renders the live case list inline.

For the narrative version of this walkthrough, refer to the [Elastic Security Labs blog post](https://www.elastic.co/security-labs/elastic-security-mcp-app).

## Known limitations [known-limitations]

* The app currently targets the `default` {{kib}} space only. Cross-space workflows aren't supported in this release.
* The app is a reference implementation, not a built-in {{kib}} feature. It's licensed under [Elastic-2.0](https://github.com/elastic/example-mcp-app-security/blob/main/LICENSE.txt) and supported through the [project repository](https://github.com/elastic/example-mcp-app-security/issues), not Elastic support channels.
* {{serverless-short}} permissions guidance is pending. The repository's permissions guide currently covers {{stack}} self-managed and {{ech}} only.
* Host support depends on the MCP host. Refer to the [MCP Apps client matrix](https://modelcontextprotocol.io/extensions/client-matrix) for the current list of compatible hosts.

## Related pages [related-pages]

* [Attack Discovery](/solutions/security/ai/attack-discovery.md): The native, in-{{kib}} version of the attack-correlation engine the MCP app calls.
* [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md): The native, in-{{kib}} agent platform that complements the MCP app's external-host workflow.
* [LLM connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md): Set up a generative AI provider for Attack Discovery and other AI-powered features.
* [MCP Apps overview](https://modelcontextprotocol.io/docs/extensions/apps.md): The Model Context Protocol extension that powers the interactive UI surface.
* [Elastic Security Labs blog post](https://www.elastic.co/security-labs/elastic-security-mcp-app): The release announcement, with screenshots, a narrative walkthrough, and a perspective from Elastic's Chief Information Security Officer.
