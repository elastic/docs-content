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

## OAuth clients

- [OAuth clients](app-connections/oauth-clients.md): overview of OAuth client registration, app connections, and tokens
- [Create an OAuth client](app-connections/create-oauth-client.md)
- [Connect an MCP host](app-connections/connect-mcp-host.md)
- [Revoke an OAuth client or connection](app-connections/revoke-oauth-client.md)

## Manage connections

- [Manage application connections](app-connections/manage-application-connections.md): organization-level view in the {{ecloud}} Console

## Related pages

- [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md): API key authentication path
