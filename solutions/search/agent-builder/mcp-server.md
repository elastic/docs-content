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
      "args": [
        "mcp-remote",
        "<YOUR_KIBANA_URL>/api/agent_builder/mcp",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "ApiKey <YOUR_API_KEY>"
      }
    }
}
```

:::{note}
Replace `<YOUR_KIBANA_URL>` with your actual Kibana URL and `<YOUR_API_KEY>` with your API key. For information on generating API keys, see [API keys](https://www.elastic.co/docs/solutions/search/search-connection-details).

Tools will be executed with the scope assigned to the API key. Make sure your API key has the appropriate permissions to only access the indices and data that you want to expose via the MCP server.
:::
