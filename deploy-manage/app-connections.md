---
navigation_title: Application connections
description: Register OAuth clients and manage application connections for authorized access to Elastic Serverless projects.
type: overview
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
  - id: kibana
---

# Application connections [app-connections]

Application connections let users authorize OAuth-based applications to act on their behalf in {{serverless-short}} projects. During technical preview, only MCP clients are supported.

Use these pages to register OAuth clients, connect an MCP host, revoke access, and manage connections at the project or organization level.

## When to use application connections [when-to-use-application-connections]

Elastic offers several ways to authorize external access or connect Elastic to external systems. They differ by direction and purpose.

:::{include} /deploy-manage/_snippets/external-access-comparison-table-full.md
:::

### Application connections compared to API keys

:::{include} /deploy-manage/_snippets/external-access-auth-comparison-details.md
:::

:::{include} /deploy-manage/_snippets/external-access-app-connections-api-key-scope.md
:::

For unattended MCP access to your project's data without per-user consent, use a [serverless project API key](/deploy-manage/api-keys/serverless-project-api-keys.md) with [{{agent-builder}} application privileges](/explore-analyze/ai-features/agent-builder/mcp-server.md#api-key-application-privileges) instead. Refer to [Elastic API keys](/deploy-manage/api-keys.md) for other API key types.

:::{include} /deploy-manage/_snippets/external-access-connector-clients-note.md
:::

## OAuth clients

- [OAuth clients](app-connections/oauth-clients.md): overview of OAuth client registration, app connections, and tokens
- [Create an OAuth client](app-connections/create-oauth-client.md)
- [Connect an MCP host](app-connections/connect-mcp-host.md)
- [Revoke an OAuth client or connection](app-connections/revoke-oauth-client.md)

## Manage connections

- [Manage application connections](app-connections/manage-application-connections.md): organization-level view in the {{ecloud}} Console

## Related pages

- [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md): API key authentication path
- [Elastic API keys](/deploy-manage/api-keys.md): programmatic access with static credentials
