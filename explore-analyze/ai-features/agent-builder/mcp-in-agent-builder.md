---
navigation_title: "MCP in Agent Builder"
description: "Agent Builder uses MCP in two distinct ways: as a server that external tools can connect to, and as a client that can call external MCP servers."
type: overview
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---


# MCP in Agent Builder [mcp-in-agent-builder]

{{agent-builder}} has two distinct, complementary uses of the Model Context Protocol (MCP). Understanding the difference helps you navigate the relevant documentation.

## Two directions

| | What it does | Who initiates | Where to configure |
|---|---|---|---|
| **{{agent-builder}} as an MCP server** | Exposes your agents and their tools to external MCP hosts (Claude Desktop, Cursor, Claude Code) | External host connects to Kibana | [{{agent-builder}} MCP server](mcp-server.md) |
| **{{agent-builder}} as an MCP client** | Lets your agents call tools on external MCP servers | Kibana connects out to an external server | [MCP tools](tools/mcp-tools.md) |

These are independent features. You can use one, both, or neither.

## Agent Builder as an MCP server

The {{agent-builder}} [MCP server](mcp-server.md) lets external MCP hosts connect to Kibana and invoke your agent's tools directly — for example, running an {{esql}} query from Claude Desktop without opening the Kibana UI.

External clients authenticate using either:

- **OAuth 2.1** — for interactive, user-consented access. An MCP host such as Claude Desktop opens a browser for the user to authenticate, then acts with that user's permissions. See [OAuth clients](/deploy-manage/app-connections/oauth-clients.md).
- **API keys** — for static, machine-to-machine access. See [{{agent-builder}} MCP server](mcp-server.md).

## Agent Builder as an MCP client

[MCP tools](tools/mcp-tools.md) let you extend your agents by pointing them at external MCP servers. You configure an MCP connector (the connection details for the remote server), then import individual tools from that server into your agent's tool catalog. The agent can then call those tools during a conversation.

This direction is unrelated to authentication on the Kibana side — it's about what your agents can reach outward.

## Terminology quick reference

<!-- TODO: confirm this table is consistent with the glossary.md and with the mcp-server.md / mcp-tools.md pages before publishing -->

| Term | Meaning in Agent Builder |
|---|---|
| MCP server | The Kibana interface that external hosts connect to |
| MCP client | An OAuth-registered application allowed to connect to the Kibana MCP server |
| MCP host | The application a user runs (Claude Desktop, Cursor); contains one or more MCP clients |
| MCP connector | Configuration in Agent Builder for reaching an external MCP server |
| MCP tool | A specific callable function imported from an external MCP server into an agent |

## Related pages

- [{{agent-builder}} MCP server](mcp-server.md)
- [OAuth clients](/deploy-manage/app-connections/oauth-clients.md)
- [MCP tools](tools/mcp-tools.md)
