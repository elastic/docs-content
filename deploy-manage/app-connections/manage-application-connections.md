---
navigation_title: "Application connections"
description: "Audit and revoke MCP client connections across an Elastic Cloud organization's serverless projects from a single organization-level view."
type: how-to
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Manage application connections [manage-application-connections]

The **Application connections** page in the Elastic Cloud Console gives organization administrators a single place to audit and revoke [OAuth client](oauth-clients.md) connections that members of your organization have authorized across their {{serverless-short}} projects.

:::{note}
During technical preview, application connections cover **MCP clients only**, and connected applications get **read-only** access through Elasticsearch Query Language (ES|QL)-based tools. Support is limited to {{serverless-short}} projects.
:::

To create an OAuth client or connect an MCP host such as **Claude Desktop**, see [Connect an MCP host](connect-mcp-host.md). This page covers organization-level management only.

## Before you begin [manage-application-connections-before-you-begin]

To access this page, open **Organization → Security settings → Application connections** in the Elastic Cloud Console. What you can see and revoke depends on your role:

* **Organization owners** see every application connection in the organization.
* **Other users** see connections for the projects they administer, plus any connections they authorized themselves.

<!-- TODO: confirm exact Cloud role names (e.g. "Organization owner") against the final RBAC copy. Source: Lloyd Chan / Simona. -->
<!-- Authoritative per AS TDD (Jake, v1.0): org owner sees all org connections; a normal user sees
     connections for projects they administer + connections directly their own; grouped by client_id. -->

The page offers two views, toggled by the **Group by client** and **List view** buttons:

* **Group by client** (default for organization owners) — lists each MCP client with a count of its connections. Expand a client row to see individual connections.
* **List view** — shows all connections in a flat, sortable table.

## View application connections

The **Application connections** page shows each MCP client and its connections. In grouped view, expand a client to see its individual connections. Each connection row shows the following details:

| Column | Description |
| --- | --- |
| Connection name | The name of the connection, derived from the MCP client name. |
| Authorization date | When the user authorized the connection. |
| Connected by | The email address of the user who authorized the connection. |
| Status | The current state of the connection. See [Connection statuses](#connection-statuses). |

<!-- TODO: confirm behavior when the user is no longer an org member — code review (lib.ts) shows email is
     tried first (memberEmail), with a fallback to raw user_id. Email display confirmed from QA screenshot
     (June 23 2026). Source: Dennis Tismenko. -->

:::{note}
This page shows all MCP clients for your organization, including clients created through the {{kib}} API using an {{ecloud}} API key. Those clients are not visible in the Agent Builder client list in {{kib}} — the organization-level view here is the only place to manage them.
:::

To narrow the list, use the search box to filter by name, or use the **Status** filter.

If no project in your organization has any MCP client connections yet, the page shows an empty state. Open a {{serverless-short}} project to begin. Connections appear here once users start authorizing MCP clients.

### Connection statuses

A connection has one of the following statuses:

* **Active** — the connection is authorized. The session may have expired if unused for 30 or more days.
* **Expired** — the connection's refresh window lapsed after 30 days of inactivity. The user must re-authorize to use it again.
* **Revoked** — the connection was revoked and can no longer be used.

<!-- Statuses per Jake (Apr 9) + PRD. Expiry is lazy/inactivity-based (30-day refresh window per AS TDD). -->

<!-- TODO: confirm retention windows for tech preview. -->
Revoked connections remain visible for 3 months and revoked clients for 1 year (use the status filter to show them). Expired connections remain visible until re-authorized or removed.

## View MCP client details

Select a client to open its details panel. The panel shows the connection details a user needs to configure an MCP host, for reference:

* **Client ID** — the unique identifier for the MCP client.
* **MCP server URLs** — the redirect URIs configured for this client (the callback URLs used during the OAuth consent flow).
* A reminder that the **client secret** is required for confidential clients and is shown only once, when the client is created.

<!-- TODO: the "MCP server URLs" field in the Cloud Console flyout renders client.redirect_uris, not the
     MCP server endpoint. The tooltip says "Elastic MCP server endpoint" but the actual data is redirect URIs.
     Confirm with Simona/Dennis whether this is intentional before publish — it may be a labeling issue. -->
<!-- Do NOT hardcode the MCP server URL / AS URL in examples — format is changing per cp-iam #2957. -->

To create or edit a client, click **Manage MCP client** to open the project's Agent Builder client management in Kibana.

<!-- TODO: confirm "Manage MCP client" button target (Kibana Agent Builder → Manage MCP Clients) and whether to
     cross-link or describe. Source: Dennis Tismenko. -->

## Revoke connections

Revoking removes the selected connections only. The MCP client stays registered and can accept new connections, and an application can be reconnected at any time.

To revoke a single connection, click **Revoke** in its row.

To revoke several connections at once:

1. Select the checkbox for each connection you want to revoke. In grouped view, use **Select all connections for this client** to select every connection under a client, or **Clear selection** to start over.
2. Click **Revoke *N* connections**.
3. Review the connections in the confirmation dialog, then click **Revoke access**.

You can revoke up to 100 connections at a time.

:::{tip}
Removing a user from your identity provider does **not** automatically revoke that user's connections. When a user leaves, revoke their connections here to cut off access.
:::

To revoke an entire MCP client and all its connections, the client's creator removes it from the project's Agent Builder client management in Kibana. See [Revoke an MCP client or connection](revoke-oauth-client.md).

## Next steps

- To restore access after revoking a client, [create a new MCP client](create-oauth-client.md) and distribute the credentials to users.

## Related pages

* [Create an OAuth client](create-oauth-client.md)
* [Connect an MCP host](connect-mcp-host.md)
* [Revoke an OAuth client or connection](revoke-oauth-client.md)
* [OAuth clients](oauth-clients.md)
