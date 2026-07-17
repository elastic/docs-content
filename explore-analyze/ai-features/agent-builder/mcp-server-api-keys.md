---
navigation_title: "API key authentication"
description: "Configure external MCP hosts to connect to the Agent Builder MCP server using API keys."
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

# Authenticate MCP clients with API keys

The [{{agent-builder}} MCP server](mcp-server.md) supports API key authentication for MCP clients. For example, you can let a scheduled script or automated service query your data through {{agent-builder}} tools without a person signing in.

:::{tip}
:applies_to: serverless: preview
In {{serverless-short}} projects, MCP clients can also authenticate using OAuth 2.1 through an [application connection](/deploy-manage/app-connections/oauth-clients.md). To compare authentication options, refer to [MCP server authentication](mcp-server.md#mcp-server-authentication).
:::

## Step 1: Create an API key [api-key-application-privileges]

Before configuring your MCP client, create an API key with {{kib}} application privileges for {{agent-builder}}. You can use the following key types:

* {{stack}}: [](/deploy-manage/api-keys/elasticsearch-api-keys.md)
* {{serverless-short}}: [](/deploy-manage/api-keys/serverless-project-api-keys.md), or [](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with {{es}} and {{kib}} API access.

Tools execute with the scope assigned to the API key. Restrict your key to only the indices and data you want to expose through the MCP server. Refer to [Best practices](#best-practices) for additional recommendations.

The following example creates an {{es}} API key or {{serverless-short}} project API key with {{kib}} application privileges for {{agent-builder}}.

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
          "privileges": ["feature_agentBuilder.read", "feature_actions.read"],
          "resources": ["space:default"]
        }
      ]
    }
  }
}
```

1. Required to use {{es}} inference endpoints. You can also use `"cluster": ["all"]` for broader access during development.
2. Must be exactly `kibana-.kibana`. This is how {{kib}} registers its application privileges with {{es}}. Without the `feature_agentBuilder.read` privilege, you'll receive a `403 Forbidden` error.

:::{note}
Without the `feature_agentBuilder.read` application privilege, you'll receive a `403 Forbidden` error when attempting to connect to the MCP endpoint.
:::

## Step 2: Configure your MCP client

Configure a client connection in MCP hosts such as Claude Desktop, Cursor, or VS Code by adding your {{kib}} URL and API key, typically in the following format:

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
          "privileges": ["feature_agentBuilder.read", "feature_actions.read"],
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
