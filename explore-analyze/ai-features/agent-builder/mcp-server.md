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

### Development and testing

For development, grant access to all indices:

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "1d",
  "role_descriptors": {
    "mcp-access": {
      "indices": [
        {
          "names": ["*"], <1>
          "privileges": ["all"] <2>
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana", <3>
          "privileges": ["feature_agentBuilder.read"],
          "resources": ["*"] <4>
        }
      ]
    }
  }
}
```

1. `["*"]` allows tools to query any index.
2. `["all"]` grants full index permissions for development convenience.
3. Must be exactly `kibana-.kibana` - this is how {{kib}} registers its application privileges with Elasticsearch.
4. `["*"]` grants access to all {{kib}} Spaces. Use `["space:default"]` to restrict to a specific Space.

### Production

For production, restrict to specific index patterns:

```json
POST /_security/api_key
{
  "name": "my-mcp-api-key",
  "expiration": "30d",
  "role_descriptors": {
    "mcp-access": {
      "indices": [
        {
          "names": ["logs-*", "metrics-*"], <1>
          "privileges": ["read", "view_index_metadata"]
        }
      ],
      "applications": [
        {
          "application": "kibana-.kibana",
          "privileges": ["feature_agentBuilder.read"],
          "resources": ["*"]
        }
      ]
    }
  }
}
```

1. Only these index patterns are accessible. Queries to other indices will fail with security exceptions. Adjust patterns based on what data your tools should access.

:::{important}
**Always set an expiration date** on API keys. Use shorter durations (1-7 days) for development and longer durations (30-90 days) for production.

**Required configuration:**

- `application: "kibana-.kibana"`
- `privileges: ["feature_agentBuilder.read"]`
- `indices` with appropriate privileges

The key differences between development and production:

- **Index patterns**: `["*"]` (all indices) vs specific patterns like `["logs-*", "metrics-*"]`
- **Index privileges**: `["all"]` (permissive) vs `["read", "view_index_metadata"]` (read-only)
  :::
