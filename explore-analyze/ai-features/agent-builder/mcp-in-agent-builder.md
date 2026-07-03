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
| **{{agent-builder}} as an MCP server** | Exposes your agents and their tools to external MCP hosts (Claude Desktop, Cursor, Claude Code) | External host connects to Kibana | [](mcp-server.md) |
| **{{agent-builder}} as an MCP client** | Lets your agents call tools on external MCP servers | Kibana connects out to an external server | [](tools/mcp-tools.md) |

These are independent features. You can use one, both, or neither.

## Agent Builder as an MCP server

The {{agent-builder}} [](mcp-server.md) lets external MCP hosts connect to Kibana and invoke your agent's tools directly — for example, running an {{esql}} query from Claude Desktop without opening the Kibana UI.

The MCP server supports the following authentication methods:

- **API keys**: Static credentials for stack deployments and {{serverless-short}} projects. See the [](mcp-server-api-keys.md).
- **OAuth 2.1**: Browser consent for interactive MCP access on {{serverless-short}} projects. See the [](/deploy-manage/app-connections/oauth-clients.md). {applies_to}`serverless: preview`

To compare the two paths, refer to [Authentication](mcp-server.md#mcp-server-authentication) on the MCP server page.

## Agent Builder as an MCP client

The [](tools/mcp-tools.md) let you extend your agents by pointing them at external MCP servers. You configure an MCP connector (the connection details for the remote server), then import individual tools from that server into your agent's tool catalog. The agent can then call those tools during a conversation.

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

See also:

- [](mcp-server.md)
- [](/deploy-manage/app-connections/oauth-clients.md)
- [](tools/mcp-tools.md)
