---
navigation_title: "MCP server"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Model Context Protocol (MCP) server

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
You can copy your MCP server URL directly in the Tools GUI. Refer to [](tools.md#copy-your-mcp-server-url).
:::

## Configuring MCP clients

Most MCP clients (such as Claude Desktop, Cursor, VS Code, etc.) have similar configuration patterns. To connect to your Elastic instance, you need to provide your Kibana URL and API key in the client's configuration file, typically in the following format:

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
1. Refer to [](#api-key-application-privileges)

:::{note}
Set the following environment variables:

```bash
export KIBANA_URL="your-kibana-url"
export API_KEY="your-api-key"
```

For information on generating API keys, refer to [](/deploy-manage/api-keys/serverless-project-api-keys.md).

Tools execute with the scope assigned to the API key. Make sure your API key has the appropriate permissions to only access the indices and data that you want to expose through the MCP server. To learn more, refer to [](#api-key-application-privileges).
:::

## API key application privileges

To access the MCP server endpoint, your API key must include {{kib}} application privileges. 

### Development and testing

For development and testing purposes, you can create an unrestricted API key with full access:

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "1d",
  "role_descriptors": {
    "unrestricted": {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["all"]
        }
      ]
    }
  }
}
```

### Production

For production environments, use a restricted API key with specific application privileges:

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "1d",   
  "role_descriptors": { 
    "mcp-access": {
      "cluster": ["all"],
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read", "view_index_metadata"]
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana",
          "privileges": ["read_onechat", "space_read"], <1>
          "resources": ["space:default"]
        }
      ]
    }
  }
}
```
1. The `read_onechat` and `space_read` application privileges are required to authorize access to the MCP endpoint. Without these privileges, you'll receive a 403 Forbidden error.
