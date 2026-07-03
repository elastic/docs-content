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

<!-- this url is referenced in the UI - do not move without a redirect -->

# Application connections [app-connections]

Application connections let users authorize external applications to act on their behalf in {{serverless-short}} projects using OAuth. Each user grants their own connection, project administrators can revoke individual connections, and organization owners can audit connections across projects.

During technical preview, the only supported application type is MCP clients connecting to the [](/explore-analyze/ai-features/agent-builder/mcp-server.md). For that use case, OAuth replaces static API keys when you need multi-user, delegated access. OAuth tokens are accepted only by the MCP server endpoint.

The sections below describe tasks for registering MCP clients, connecting hosts, revoking access, and managing connections at the project or organization level.

:::{note}
Application connections are not the same as [Kibana connectors](/deploy-manage/manage-connectors.md) or [search connectors](elasticsearch://reference/search-connectors/index.md). Kibana connectors store credentials so {{kib}} can send actions to external systems. Search connectors sync data from third-party sources into {{es}}.
:::

## Before you begin

To choose between an application connection or API keys for the {{agent-builder}} MCP server, refer to [MCP server authentication](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication).

## Manage application connections [application-connections-tasks]

Use the following pages to learn how to create and manage application connections for MCP clients.

Tasks for all users with appropriate permissions:

- [](app-connections/oauth-clients.md): Learn how OAuth client registration, app connections, and tokens work.
- [](app-connections/create-oauth-client.md): Register a client in {{agent-builder}} and get the credentials your MCP host needs.
- [](app-connections/connect-mcp-host.md): Configure your MCP host and complete browser consent.
- [](app-connections/revoke-oauth-client.md): Remove access for one user or an entire client at the project level.

Tasks for organization owners:
- [](app-connections/manage-application-connections.md): Audit and revoke authorized connections across your organization's {{serverless-short}} projects in the {{ecloud}} Console.
