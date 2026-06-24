---
navigation_title: "MCP client OAuth"
description: "OAuth 2.1 lets MCP clients authenticate to the Agent Builder MCP server on behalf of a user, using short-lived tokens instead of static API keys."
type: overview
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Authenticate MCP clients with OAuth [mcp-client-oauth]

The [{{agent-builder}} MCP server](mcp-server.md) supports OAuth 2.1 as a way for MCP clients to authenticate on behalf of a user, alongside [API keys](mcp-server.md#api-key-application-privileges).

OAuth suits interactive, agentic use cases: instead of configuring a static, long-lived API key, a user connects an MCP host such as Claude Desktop and consents in the browser. The MCP client then acts with that user's permissions, using short-lived tokens that the user, a project administrator, or an organization owner can revoke at any time.

:::{note}
During technical preview, OAuth for the MCP server is available on {{serverless-short}} projects only. <!-- TODO: confirm tool scope for tech preview — PRD said "read-only, ES|QL-based tools only", but QA testing (June 23 2026) shows 22 tools including write operations (delete_stream, create_partition, update_stream, cases, etc.). Remove or correct this sentence once confirmed with Jake Landis / Elena Shostak. --> To register a client, you provide a single {{serverless-short}} project, so each client is scoped to one project.
:::

## OAuth or API keys?

Both methods let an MCP client reach the {{agent-builder}} MCP server. Choose based on how the client runs and who acts through it.

| | OAuth | API key |
|---|---|---|
| Best for | Interactive agents acting on behalf of a person (Claude Desktop, Cursor) | Automation and static, machine-to-machine access |
<!-- TODO: confirm Cursor is supported in tech preview before publishing — cp-iam-team#2974 (custom redirect URI support for Cursor) is still open as of 2026-06-23. Remove this comment once resolved. -->
| Identity | The consenting user; permissions are the user's live permissions | The key's snapshotted permissions |
| Credential lifetime | Short-lived tokens, refreshed automatically | Long-lived until it expires or is revoked |
| Setup | Register an MCP client, then consent in the browser | Generate a key and add it to the client configuration |

For API key configuration, refer to [](mcp-server.md). The rest of this page covers the OAuth path.

## Key concepts

Understanding these terms makes the setup and management pages easier to follow.

- **MCP host**: The application a user runs that contains MCP clients, such as Claude Desktop or Cursor. Users connect hosts; hosts use clients.
<!-- TODO: confirm Cursor is supported in tech preview — cp-iam-team#2974 still open as of 2026-06-23. -->
- **MCP client**: The registered application that holds the credentials (a client ID, and a client secret for confidential clients). You create one in {{kib}} before connecting a host.
- **MCP server**: The interface that exposes {{agent-builder}} tools to MCP hosts. The MCP server is the only resource the OAuth tokens grant access to. This is separate from [MCP tools](tools/mcp-tools.md), which let your agents call external MCP servers — the reverse direction.
- **App connection**: The record created when a user consents, linking that user, the MCP client, and the {{serverless-short}} project. A connection is the unit of access and revocation. If two people use the same client ID, each consent creates a separate connection.

## How it works

1. A user [creates an MCP client](mcp-client-create.md) in {{kib}}, scoped to one {{serverless-short}} project, and copies the generated configuration into their MCP host.
2. The first time the host needs access, it opens a browser for the user to authenticate and consent. Authentication is always required for consent, even if the user already has an active {{ecloud}} session.
3. On consent, an app connection is created and the client receives tokens. The MCP client presents these to the MCP server, which exchanges them internally to access {{es}} with the user's current permissions.
4. The user, a project administrator, or an organization owner can [revoke](mcp-client-revoke.md) the connection or the whole client at any time.

OAuth tokens are accepted only by the {{agent-builder}} MCP server. They don't grant direct access to {{kib}} or {{es}} APIs.

### About tokens

Access tokens are short-lived and refreshed automatically in the background, so an active connection keeps working without user action. Refresh is inactivity-based: after 30 days without use, a connection expires and the user must consent again. Because expiry is detected only when a connection is next used, a connection that shows as connected might be idle and not yet revalidated.

### Permissions

A connected client inherits the consenting user's permissions in the project. <!-- TODO: confirm tool scope — same as above. If write tools are available in tech preview, remove "read-only, {{esql}}-based" qualifier and update the "can't modify data" statement. --> When a user's permissions change, the change applies on the next token refresh; changes to a custom role apply immediately.

## Next steps

- [Create an MCP client](mcp-client-create.md)
- [Connect an MCP host to an MCP client](mcp-client-connect.md)

## Related pages

- [Revoke an MCP client or connection](mcp-client-revoke.md)
- [Manage application connections](/deploy-manage/users-roles/cloud-organization/manage-mcp-client-connections.md) at the organization level
- [{{agent-builder}} MCP server](mcp-server.md)
