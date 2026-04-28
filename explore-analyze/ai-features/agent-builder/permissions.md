---
navigation_title: "Permissions"
description: "Learn how to configure security roles, API keys, and privileges for Agent Builder."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Permissions and access control in {{agent-builder}}

Use this page to learn how to configure security roles and API keys for {{agent-builder}}. Understanding these privileges helps you control who can use agents, which tools they can access, and what data they can query.

::::{admonition}
This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

## Required privileges

{{agent-builder}} requires privileges at three levels:

- [{{kib}} feature access](#kib-privileges)
- [{{es}} cluster access](#es-cluster-privileges)
- [{{es}} index access](#es-index-privileges)

### {{kib}} privileges

{{agent-builder}} access control is managed by the `agentBuilder` {{kib}} feature. Assign either `Read` or `All` based on what users need to do.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
#### `Read`

Required to use agents, send chat messages, view tools, and access conversations.

Instead of `All`, you can pair `Read` with individual sub-features for more granular control over what users can manage:

- `Manage agents`: Create, update, or delete custom agents.
- `Manage tools`: Create, update, or delete custom tools.

#### `All`

The broadest access level. Grants everything in `Read`, plus the ability to create, update, or delete custom agents and tools. Includes both management sub-features by default.
:::

:::{applies-item} { stack: ga 9.2-9.3 }
#### `Read`

Required to use agents, send chat messages, view tools, and access conversations.

#### `All`

The broadest access level. Grants everything in `Read`, plus the ability to create, update, or delete custom agents and tools.
:::

::::

:::{note}
If the agent uses AI connectors, also grant `Read` access to the {{connectors-feature}} feature.
:::

Learn more about [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

### {{es}} cluster privileges

{{agent-builder}} requires cluster-level privileges for AI-powered query generation:

- `monitor_inference`: Required when the agent uses an AI connector that calls the {{es}} Inference API (such as the Elastic default LLM or other AI connectors configured to use the Inference API). The built-in tools `search` and `generate_esql`, as well as [index search tools](tools/index-search-tools.md), use this API to generate queries from natural language. This privilege is not required when the agent uses other {{kib}} GenAI connectors.

Learn more about [cluster privileges](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-privileges.html#privileges-list-cluster).

### {{es}} index privileges

Tools execute queries against {{es}} indices as the current user. Required privileges depend on which indices the tools access:

- `read`: Required for tools that query data.
- `view_index_metadata`: Required for tools that inspect index structure. Also required for the built-in `search` tool and [index search tools](tools/index-search-tools.md), which might use index exploration capabilities internally.

Learn more about [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices).

## Grant access

You can grant users access to {{agent-builder}} using these methods:

- [Roles](#grant-access-with-roles) to bundle privileges for users.
- [API keys](#grant-access-with-api-keys) for programmatic access.
- [Spaces](#working-with-spaces) to scope access to specific environments.

### Grant access with roles

[Roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) are {{es}} security constructs that bundle together {{kib}} feature privileges and {{es}} privileges. To grant users access to {{agent-builder}}, create a role that includes the required privileges.

:::{note}
When configuring roles in the {{kib}} UI, {{agent-builder}} privileges are currently located under the **Analytics** section, not the {{es}} section.
:::

Example role for users who need full {{agent-builder}} access:

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
        "feature_agentBuilder.all", <1>
        "feature_actions.read"
      ],
      "resources": ["space:default"]
    }
  ]
}
```

1. For read-only access, use `feature_agentBuilder.read` instead of `feature_agentBuilder.all`. [Learn more](#kib-privileges).

:::{note}
:applies_to: {"stack": "ga 9.4+", "serverless": "ga"}

For granular access, pair `feature_agentBuilder.read` with only the sub-feature privileges needed. To learn more, refer to [Kibana privileges](#kib-privileges).
:::

### Grant access with API keys

When using the {{agent-builder}} APIs programmatically, authenticate with an API key that includes the required privileges.

Unlike roles, which use UI-friendly feature privilege names like `feature_agentBuilder.all`, API keys use the underlying API privilege names (`read_onechat`, `manage_onechat`). This is because API keys interact directly with the {{kib}} API layer rather than through the UI.

Refer to these pages for API key configuration examples:
- [MCP server](mcp-server.md#api-key-application-privileges)
- [{{kib}} API](kibana-api.md)

Learn more about [API keys](/deploy-manage/api-keys/elasticsearch-api-keys.md).

### Working with spaces

{{agent-builder}} respects {{kib}} spaces when enabled. Conversations, custom agents, and custom tools are scoped to the current space. Built-in agents are space-agnostic and are available in all spaces. The default Elastic AI Agent is an exception {applies_to}`stack: ga 9.4+`: it is a standard persisted agent that is space-aware and automatically created per space.

When configuring roles or API keys, specify the space in the application privileges resources (for example, `"resources": ["space:production"]`). Users and API keys cannot access resources in other spaces.

Learn how to [Copy your MCP server URL](tools.md#mcp-server-access).

:::{important}
When accessing {{agent-builder}} APIs or the MCP server from a custom space, include the space name in the URL path: `https://<deployment>/s/<space-name>/api/agent_builder/...`

The default space uses the standard URL format without `/s/<space-name>`.
:::

Learn more about [{{kib}} Spaces](/deploy-manage/manage-spaces.md).