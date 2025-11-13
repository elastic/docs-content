---
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
navigation_title: "Permissions & access control"
---


# Permissions and access control in {{agent-builder}}

Use this page to learn how to configure security roles and API keys for Agent Builder. Understanding these privileges helps you control who can use agents, which tools they can access, and what data they can query.

Agent Builder requires privileges at three levels:

- [{{kib}} feature access](#kib-privileges)
- [{{es}} cluster access](#es-cluster-privileges)      
- [{{es}} index access](#es-index-privileges)

### {{kib}} privileges

Agent Builder access control is managed by the `agentBuilder` {{kib}} feature:

- "Read" access to the `agentBuilder` feature: Required to use agents, send chat messages, view tools, and access conversations.
- "All" access to the `agentBuilder` feature: Required to create, update, or delete custom agents and tools.
- "Read" access to the "Actions and Connectors" feature: Required to use AI connectors with agents. 

Learn more about [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

### {{es}} cluster privileges

Agent Builder requires cluster-level privileges for AI-powered query generation:

- `monitor_inference`: Required for agents to use AI-powered tools. The built-in tools `search` and `generate_esql`, as well as [index search tools](tools/index-search-tools.md), call the {{es}} Inference API to generate queries from natural language.

Learn more about [cluster privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-cluster).

### {{es}} index privileges

Tools execute queries against {{es}} indices as the current user. Required privileges depend on which indices the tools access:

- `read`: Required for tools that query data
- `view_index_metadata`: Required for tools that inspect index structure. Also required for the built-in `search` tool and [index search tools](tools/index-search-tools.md), which may use index exploration capabilities internally

Learn more about [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).

### Granting access with roles

[Roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) are {{es}} security constructs that bundle together {{kib}} feature privileges and {{es}} privileges. To grant users access to Agent Builder, create a role that includes the required privileges.

Example role for users who need full Agent Builder access:

```json
POST /_security/role/agent-builder-full
{
  "cluster": ["monitor_inference"],
  "indices": [
    {
      "names": ["logs-*", "metrics-*"],
      "privileges": ["read", "view_index_metadata"]
    }
  ],
  "applications": [
    {
      "application": "kibana-.kibana",
      "privileges": [
        "feature_agentBuilder.all",
        "feature_actions.read"
      ],
      "resources": ["space:default"]
    }
  ]
}
```

:::{tip}
For read-only access, use `feature_agentBuilder.read` instead of `feature_agentBuilder.all`.
:::

### API keys for programmatic access

When using the Agent Builder APIs programmatically, authenticate with an API key that includes the required privileges.

Unlike roles, which use UI-friendly feature privilege names like `feature_agentBuilder.all`, API keys use the underlying API privilege names (`read_onechat`, `manage_onechat`). This is because API keys interact directly with the {{kib}} API layer rather than through the UI.

Refer to these pages for API key configuration examples:
- [MCP server](mcp-server.md#api-key-application-privileges)
- [{{kib}} API](kibana-api.md)

Learn more about [API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).

### Spaces

Agent Builder respects {{kib}} Spaces when enabled. All conversations, custom agents, and custom tools are scoped to the current Space.

When configuring roles or API keys, specify the Space in the application privileges resources (e.g., `"resources": ["space:production"]`). Users and API keys cannot access resources in other Spaces.

Learn how to [Copy your MCP server URL](tools.md#copy-your-mcp-server-url).

:::{important}
When accessing Agent Builder APIs or the MCP server from a custom Space, include the space name in the URL path: `https://<deployment>/s/<space-name>/api/agent_builder/...`

The default space uses the standard URL format without `/s/<space-name>`.
:::

Learn more about [{{kib}} Spaces](/deploy-manage/manage-spaces.md).