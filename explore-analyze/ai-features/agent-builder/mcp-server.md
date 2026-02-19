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
You can copy your MCP server URL directly in the Tools GUI. Refer to [](tools.md#copy-your-mcp-server-url).
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

1. Refer to [](#api-key-application-privileges)

:::{note}
Set the following environment variables:

```bash
export KIBANA_URL="your-kibana-url"
export API_KEY="your-api-key"
```

For information on generating API keys, refer to [](/deploy-manage/api-keys.md).

Tools execute with the scope assigned to the API key. Make sure your API key has the appropriate permissions to only access the indices and data that you want to expose through the MCP server. To learn more, refer to [](#api-key-application-privileges).
:::

## API key application privileges

To access the MCP server endpoint, your API key must include {{kib}} application privileges for {{agent-builder}}.

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "30d",
  "role_descriptors": {
    "mcp-access": {
      "cluster": ["monitor_inference"], <1>
      "indices": [
        {
          "names": ["*"],
          "privileges": ["read", "view_index_metadata"]
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana", <2>
          "privileges": ["feature_agentBuilder.read"],
          "resources": ["space:default"]
        }
      ]
    }
  }
}
```

1. Required to use {{es}} inference endpoints. You can also use `"cluster": ["all"]` for broader access during development.
2. Must be exactly `kibana-.kibana` — this is how {{kib}} registers its application privileges with {{es}}. Without the `feature_agentBuilder.read` privilege, you'll receive a `403 Forbidden` error.

:::{note}
Without the `feature_agentBuilder.read` application privilege, you'll receive a `403 Forbidden` error when attempting to connect to the MCP endpoint.
:::

## Best practices

### Set API key expiration dates

Always set an expiration date on API keys for security. Use shorter durations (1-7 days) for development and longer durations (30-90 days) for production, rotating keys regularly.

### Limit Agent Builder to specific indices

For production environments, restrict API keys to only the indices your tools need to access. This follows the principle of least privilege and prevents agents from querying sensitive data.

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "30d",
  "role_descriptors": {
    "mcp-access": {
      "cluster": ["monitor_inference"], <1>
      "indices": [
        {
          "names": ["logs-*", "metrics-*"], <2>
          "privileges": ["read", "view_index_metadata"] <3>
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana", <4>
          "privileges": ["feature_agentBuilder.read"],
          "resources": ["space:default"]
        }
      ]
    }
  }
}
```

1. Required to use {{es}} inference endpoints. You can also use `"cluster": ["all"]` for broader access during development.
2. Restrict index access to only the indices your tools need to query. Adjust the index patterns based on your security requirements.
3. Read-only privileges prevent the agent from modifying data.
4. Must be exactly `kibana-.kibana` - this is how {{kib}} registers its application privileges with {{es}}.
