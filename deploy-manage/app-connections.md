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

Application connections let users authorize external applications to act on their behalf in {{serverless-short}} projects using OAuth 2.1.

During technical preview, only MCP clients for the [](/explore-analyze/ai-features/agent-builder/mcp-server.md) are supported. For that use case, OAuth 2.1 replaces static API keys when you need multi-user, delegated access. OAuth tokens are accepted only by the MCP server endpoint.

The sections below describe tasks for registering MCP clients, connecting hosts, revoking access, and managing connections at the project or organization level.

:::{note}
Application connections are not the same as [{{kib}} connectors](/deploy-manage/manage-connectors.md) or [search connectors](elasticsearch://reference/search-connectors/index.md). {{kib}} connectors store credentials so {{kib}} can send actions to external systems. Search connectors sync data from third-party sources into {{es}}.
:::

## Before you begin

To choose between an application connection or API keys to authorize external applications for the {{agent-builder}} MCP server, refer to [MCP server authentication](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication).

## Manage application connections [application-connections-tasks]

Use the following pages to set up and manage application connections for MCP clients:

- [](app-connections/oauth-clients.md): Set up and manage OAuth access for MCP clients, including registering clients, connecting hosts, and revoking access at the project level.
- [](app-connections/manage-app-connections.md): Audit and revoke authorized connections across your organization's {{serverless-short}} projects in the {{ecloud}} Console.
