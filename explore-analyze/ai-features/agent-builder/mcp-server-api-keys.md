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
:applies_to: serverless: ga
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

Add your {{kib}} MCP server URL and API key to your MCP client, such as Claude Desktop, Cursor, or VS Code. Configuration formats differ between clients.

1. **Get your MCP server URL.** The URL is `https://<your-kibana-url>/api/agent_builder/mcp`. To copy it from the UI instead, use the MCP server dropdown on the Tools page and select **Copy MCP Server URL**. Refer to [MCP server access](/explore-analyze/ai-features/agent-builder/tools.md#mcp-server-access).

   If you use a custom {{kib}} space, use the endpoint for that space instead. Refer to [](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-endpoint).

2. **Test the connection outside your client.** In [MCP Inspector](https://github.com/modelcontextprotocol/inspector), connect to your MCP server URL over HTTP (the `streamable-http` transport option in the UI, or `--transport http` in the CLI), and add an `Authorization` header with the value `ApiKey <your-api-key>`.

3. **Add the server to your client's configuration.** Use your client's documentation for the exact format. The following example is for reference only:

   ```json
   {
     "mcpServers": {
       "elastic-agent-builder": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "https://<your-kibana-url>/api/agent_builder/mcp",
           "--header",
           "Authorization:${AUTH_HEADER}"
         ],
         "env": {
           "AUTH_HEADER": "ApiKey <your-api-key>" <1>
         }
       }
     }
   }
   ```

   1. Refer to [](#api-key-application-privileges)

   In this example, `mcp-remote` replaces `${AUTH_HEADER}` in the `--header` value with the `AUTH_HEADER` environment variable that your client sets from `env`. It doesn't expand variables in the server URL, so enter the URL literally. Other clients might not expand `${VAR}` placeholders or inherit your shell variables, so use literal values unless your client's documentation says otherwise.

:::{note}
Elastic doesn't provide support for third-party MCP clients. For help configuring a client, refer to its documentation or contact its vendor.
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
