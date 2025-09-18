---
navigation_title: "MCP server"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

# MCP server

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

The [**Model Context Protocol (MCP) server**](https://modelcontextprotocol.io/docs/getting-started/intro) provides a standardized interface for external clients to access {{agent-builder}} tools.

## MCP server endpoint

The MCP server is available at:

```
{KIBANA_URL}/api/agent_builder/mcp
```

## Configuring MCP clients

Most MCP clients (such as Claude Desktop, Cursor, VS Code, etc.) have similar configuration patterns. To connect to your Elastic instance, you'll need to provide your Kibana URL and API key in the client's configuration file, typically in the following format:

```json
{
  "mcpServers": {
    "elastic-agent-builder": {
      "command": "npx",
      "args": ["@elastic/agent-builder-mcp"],
      "env": {
        "KIBANA_URL": "<YOUR_KIBANA_URL>",
        "API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

:::{note}
Replace `<YOUR_KIBANA_URL>` with your actual Kibana URL and `<YOUR_API_KEY>` with your API key. For information on generating API keys, see [API keys](https://www.elastic.co/docs/solutions/search/search-connection-details).
:::
