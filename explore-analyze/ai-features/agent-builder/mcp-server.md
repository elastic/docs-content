---
navigation_title: "MCP server"
description: "Learn how to connect Claude Desktop, Cursor, and VS Code to Elastic Agent Builder tools using the Model Context Protocol (MCP) server."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} MCP server

The [**Model Context Protocol (MCP) server**](https://modelcontextprotocol.io/docs/getting-started/intro) provides a standardized interface for external clients to access {{agent-builder}} tools.

## MCP server endpoint

The MCP server is available at:

```
{KIBANA_URL}/api/agent_builder/mcp
```

When using a custom {{kib}} Space, include the space name in the URL:

```
{KIBANA_URL}/s/{SPACE_NAME}/api/agent_builder/mcp
```

:::{tip}
You can copy your MCP server URL directly in the Tools GUI. Refer to [](tools.md#mcp-server-access).
:::

## Configuring MCP clients

Most MCP clients (such as Claude Desktop, Cursor, VS Code, etc.) have similar configuration patterns. To connect to your Elastic instance, you need to provide your {{kib}} URL and API key in the client's configuration file, typically in the following format:

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
        "AUTH_HEADER": "ApiKey ${API_KEY}" <1>
      }
    }
  }
}
```

1. Refer to [Create a read-only client key](api-keys.md#create-a-read-only-client-key).

:::{note}
Set the following environment variables:

```bash
export KIBANA_URL="your-kibana-url"
export API_KEY="your-api-key"
```

For a complete API key example, refer to [Create a read-only client key](api-keys.md#create-a-read-only-client-key).

Tools execute with the scope assigned to the API key. Restrict the key to only the spaces, indices, and data that you want to expose through the MCP server.
:::

The key must include `feature_agentBuilder.read` for the space in the MCP endpoint URL. Without this application privilege, the MCP endpoint returns `403 Forbidden`.
