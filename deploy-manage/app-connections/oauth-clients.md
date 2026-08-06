---
navigation_title: "OAuth for MCP clients"
description: "OAuth 2.1 lets MCP clients authenticate to the Agent Builder MCP server on behalf of a user, using short-lived tokens instead of static API keys."
type: overview
applies_to:
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
---

# OAuth for MCP clients

The [](/explore-analyze/ai-features/agent-builder/mcp-server.md) supports OAuth 2.1 as a way for MCP clients to authenticate on behalf of a user, alongside [API keys](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md).

OAuth is best for interactive, agentic use cases: instead of configuring a static, long-lived API key, a user connects an MCP host such as Claude Desktop and authorizes the connection in the browser. The connection then acts with that user's own permissions, using short-lived tokens that the user, a project administrator, or an organization owner can revoke at any time.

:::{note}
OAuth for the MCP server is available on {{serverless-short}} projects only. OAuth clients are registered within a specific {{serverless-short}} project, so each client is scoped to one project.
:::

## OAuth or API keys?

The way that you configure your MCP server depends on your authentication method. Both methods let an MCP client reach the {{agent-builder}} MCP server. To compare them, refer to [MCP server authentication and configuration](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication).

To learn how to configure your MCP server with API keys, refer to [](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md). The rest of this page describes configuring your MCP server with OAuth.

## Key concepts

Understanding these terms makes the setup and management pages easier to follow.

| Term | Definition |
| --- | --- |
| MCP host | The application a user runs that contains MCP clients, such as Claude Desktop or Cursor. Users connect hosts; hosts use clients. |
| OAuth client | The OAuth client registration that holds the credentials (a client ID, and a client secret for confidential clients) your MCP host uses to authenticate to the MCP server. You create one in {{kib}} before connecting a host; the {{kib}} UI labels this an **MCP client**. |
| MCP server | The interface that exposes {{agent-builder}} tools to MCP hosts. The MCP server is the only resource the OAuth tokens grant access to. This is separate from the [](/explore-analyze/ai-features/agent-builder/tools/mcp-tools.md), which let your agents call external MCP servers. |
| App connection | The record created when a user authorizes a connection, linking that user, the OAuth client, and the {{serverless-short}} project. A connection is established on top of an OAuth client, and is the unit of access and revocation. If two people use the same client ID, each authorization creates a separate connection. |

In practice, the pieces connect in order. An OAuth client is registered in {{kib}}, and its credentials are added to an MCP host such as Claude Desktop. The host's MCP client uses those credentials to reach the {{agent-builder}} MCP server. When a user authorizes access, an app connection is created, and the host's tools then run with that user's permissions.

## How it works

An OAuth flow follows these steps over its lifecycle:

1. A user with {{agent-builder}} access creates an OAuth client in {{kib}}, scoped to one {{serverless-short}} project, and receive a client ID and an MCP server URL used to [configure an MCP host](connect-mcp-host.md).
2. An end user adds the client ID and MCP server URL to their MCP host (AI agent). The first time the host needs access, it opens a browser for the user to authenticate and authorize access. Authentication is always required, but might not prompt for login if the user already has an active {{ecloud}} session.
3. On authorization, an app connection is created and the host receives tokens. The OAuth client presents these to the MCP server, which exchanges them internally to access {{es}} with that user's current permissions.
4. The user, a project administrator, or an organization owner can revoke a single connection or the entire client at any time, at the [project](revoke-oauth-client.md) or [organization](manage-app-connections.md#revoke-connections) level.

OAuth tokens are accepted only by the {{agent-builder}} MCP server. They don't grant direct access to {{kib}} or {{es}} APIs.

### Sharing a client

A single OAuth client registration can be reused by any number of people. After you create a client, you can share its connection details so that others configure the same client in their own MCP hosts (AI agents). Each person authenticates and authorizes access separately, which creates a distinct app connection scoped to that person's own permissions. Revoking one person's connection leaves the others active, while revoking the client ends access for everyone.

### Access tokens

Access tokens are short-lived and refreshed automatically in the background, so an active connection keeps working without user action. Refresh is inactivity-based: after 30 days without use, a connection expires and the user must re-authorize. Because expiry is detected only when a connection is next used, a connection that shows as connected might be idle and not yet revalidated.

### Permissions

:::{include} /deploy-manage/_snippets/app-connection-permissions.md
:::

## Set up and manage OAuth for MCP clients [oauth-clients-tasks]

Use the following pages to create and manage OAuth access for MCP clients:

- [](create-oauth-client.md): Register a client in {{agent-builder}} and get the client ID and MCP server URL your MCP host needs.
- [](connect-mcp-host.md): Configure your MCP host with those values and complete browser authorization.
- [](revoke-oauth-client.md): Remove access for a single connection or an entire client at the project level.

## Related pages

- [](manage-app-connections.md): Audit and revoke connections across your organization's {{serverless-short}} projects in the {{ecloud}} Console.
- [](/explore-analyze/ai-features/agent-builder/mcp-server.md): Configure the {{agent-builder}} MCP server and compare authentication methods.
- [](/deploy-manage/api-keys.md): Authenticate to the MCP server with API keys instead of OAuth.
