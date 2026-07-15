---
navigation_title: "MCP client OAuth"
description: "OAuth 2.1 lets MCP clients authenticate to the Agent Builder MCP server on behalf of a user, using short-lived tokens instead of static API keys."
type: overview
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
---

# OAuth for MCP clients [oauth-clients]

The [](/explore-analyze/ai-features/agent-builder/mcp-server.md) supports OAuth 2.1 as a way for MCP clients to authenticate on behalf of a user, alongside [API keys](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md).

OAuth is best for interactive, agentic use cases: instead of configuring a static, long-lived API key, a user connects an MCP host such as Claude Desktop and consents in the browser. The MCP client then acts with that user's permissions, using short-lived tokens that the user, a project administrator, or an organization owner can revoke at any time.

:::{note}
OAuth for the MCP server is available on {{serverless-short}} projects only. Clients are registered within a specific {{serverless-short}} project, so each client is scoped to one project.
:::

## OAuth or API keys?

The way that you configure your MCP server depends on your authentication method. Both methods let an MCP client reach the {{agent-builder}} MCP server. To compare them, refer to [MCP server authentication and configuration](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication).

To learn how to configure your MCP server with API keys, refer to [](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md). The rest of this page describes configuring your MCP server with OAuth.

## Key concepts

Understanding these terms makes the setup and management pages easier to follow.

| Term | Definition |
| --- | --- |
| MCP host | The application a user runs that contains MCP clients, such as Claude Desktop or Cursor. Users connect hosts; hosts use clients. |
| OAuth client | The OAuth client registration that holds the credentials (a client ID, and a client secret for confidential clients) your MCP host uses to authenticate to the MCP server. You create one in {{kib}} before connecting a host. |
| MCP server | The interface that exposes {{agent-builder}} tools to MCP hosts. The MCP server is the only resource the OAuth tokens grant access to. This is separate from the [](/explore-analyze/ai-features/agent-builder/tools/mcp-tools.md), which let your agents call external MCP servers. |
| App connection | The record created when a user consents, linking that user, the MCP client, and the {{serverless-short}} project. A connection is the unit of access and revocation. If two people use the same client ID, each consent creates a separate connection. |

## How it works

The OAuth flow follows these steps:

1. A user [creates an OAuth client](create-oauth-client.md) in {{kib}}, scoped to one {{serverless-short}} project, and receives a client ID and an MCP server URL. These values can be used to [configure MCP hosts](connect-mcp-host.md).
2. The first time the MCP host (AI agent) needs access, it opens a browser for the user to authenticate and consent. Authentication is always required for consent, but might not require an explicit login if the user already has an active {{ecloud}} session.
3. On consent, an app connection is created and the client receives tokens. The OAuth client presents these to the MCP server, which exchanges them internally to access {{es}} with the user's current permissions.
4. The user, a project administrator, or an organization owner can revoke the connection or the whole client at any time, at the [project](revoke-oauth-client.md) or [organization](manage-app-connections.md) level.

OAuth tokens are accepted only by the {{agent-builder}} MCP server. They don't grant direct access to {{kib}} or {{es}} APIs.

### Sharing a client

A single OAuth client registration can be reused by any number of people. After you create a client, you can share its connection details so that others configure the same client in their own MCP hosts (AI agents). Each person authenticates and consents separately, which creates a distinct app connection scoped to that person's own permissions. Revoking one person's connection leaves the others active, while revoking the client ends access for everyone.

### About tokens

Access tokens are short-lived and refreshed automatically in the background, so an active connection keeps working without user action. Refresh is inactivity-based: after 30 days without use, a connection expires and the user must consent again. Because expiry is detected only when a connection is next used, a connection that shows as connected might be idle and not yet revalidated.

### Permissions

:::{include} _snippets/app-connection-permissions.md
:::

## Set up and manage OAuth for MCP clients [oauth-clients-tasks]

Use the following pages to create and manage OAuth access for MCP clients:

- [](create-oauth-client.md): Register a client in {{agent-builder}} and get the client ID and MCP server URL your MCP host needs.
- [](connect-mcp-host.md): Configure your MCP host with those values and complete browser consent.
- [](revoke-oauth-client.md): Remove access for a single connection or an entire client at the project level.

## Related pages

- [](manage-app-connections.md): Audit and revoke connections across your organization's {{serverless-short}} projects in the {{ecloud}} Console.
- [](/explore-analyze/ai-features/agent-builder/mcp-server.md): Configure the {{agent-builder}} MCP server and compare authentication methods.
- [](/deploy-manage/api-keys.md): Authenticate to the MCP server with API keys instead of OAuth.
