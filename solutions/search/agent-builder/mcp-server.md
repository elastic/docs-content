---
navigation_title: "MCP server"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

# MCP server

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

The [**Model Context Protocol (MCP) server**](https://modelcontextprotocol.io/docs/getting-started/intro) provides a standardized interface for external clients to access {{agent-builder}} tools.

## MCP server endpoint

The MCP server is available at:

```
{KIBANA_URL}/api/agent_builder/mcp
```
:::{tip}
You can copy your MCP server URL directly in the Tools GUI. Refer to [](tools.md#mcp-server-access).
:::

## Configuring MCP clients

Most MCP clients (such as Claude Desktop, Cursor, VS Code, etc.) have similar configuration patterns. To connect to your Elastic instance, you'll need to provide your Kibana URL and API key in the client's configuration file, typically in the following format:

```json

{
  "mcpServers": {
    "elastic-agent-builder": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "${KIBANA_URL}/api/agent_builder/mcp",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "KIBANA_URL": "${KIBANA_URL}",
        "AUTH_HEADER": "ApiKey ${API_KEY}"
      }
    }
}
```

:::{note}
Set the following environment variables:

```bash
export KIBANA_URL="your-kibana-url"
export API_KEY="your-api-key"
```

For information on generating API keys, see [API keys](https://www.elastic.co/docs/solutions/search/search-connection-details).

Tools will be executed with the scope assigned to the API key. Make sure your API key has the appropriate permissions to only access the indices and data that you want to expose via the MCP server.
:::
