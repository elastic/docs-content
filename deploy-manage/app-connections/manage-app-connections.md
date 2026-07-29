---
description: "Audit and revoke OAuth client connections across an Elastic Cloud organization's serverless projects from a single organization-level view."
type: how-to
applies_to:
  serverless: preview
products:
  - id: cloud-serverless
---

# Manage application connections

The **Application connections** page in the {{ecloud}} Console gives organization administrators a single place to audit and revoke [OAuth client](oauth-clients.md) connections that members of your organization have authorized across their {{serverless-short}} projects.

To create an OAuth client or connect an MCP host such as Claude Desktop, refer to [](oauth-clients.md). This page covers organization-level management only.

## Before you begin [manage-application-connections-before-you-begin]

Before you manage application connections:

* You have access to the {{ecloud}} Console for your organization. To open the page, go to **Organization** → **Security settings** → **Application connections**.
* Your role determines what you can see and revoke:
  * **Organization owners** see every application connection in the organization.
  * Other users see connections for the projects they administer, plus any connections they authorized themselves.

## View application connections

The **Application connections** page shows each OAuth client and its connections. 

The page offers two views, toggled by the **Group by client** and **List view** buttons:

* **Group by client**: Lists each OAuth client with a count of its connections.
* **List view**: Shows all connections in a flat, sortable table.

In grouped view, expand a client to see its individual connections. Each connection row shows the following details:

| Column | Description |
| --- | --- |
| Connection name | The name of the connection, derived from the OAuth client name. |
| Authorization date | When the user authorized the connection. |
| Connected by | The email address of the user who authorized the connection. |
| Status | The current state of the connection. See [Connection statuses](#connection-statuses). |

:::{note}
This page shows all OAuth clients for your organization, including clients created through the {{kib}} API using an {{ecloud}} API key. Those clients are not visible in the Agent Builder client list in {{kib}} — the organization-level view here is the only place to manage them.
:::

To narrow the list, use the search box to filter by name, or use the **Status** filter.

If no project in your organization has any OAuth client connections yet, the page shows an empty state. Open a {{serverless-short}} project to begin. Connections appear here once users start authorizing OAuth clients.

### Connection statuses

A connection has one of the following statuses:

* **Active**: The connection is authorized. The session may have expired if unused for 30 or more days.
* **Expired**: The connection's refresh window lapsed after 30 days of inactivity. The user must re-authorize to use it again.
* **Revoked**: The connection was revoked and can no longer be used.

<!-- TODO: confirm retention windows for tech preview. -->
Revoked connections remain visible for 3 months and revoked clients for 1 year. Expired connections remain visible until re-authorized or removed.

## View OAuth client details

Select a client to open its details panel. The panel shows the connection details a user needs to configure an MCP host, for reference:

* **Client ID**: The unique identifier for the OAuth client.
* **MCP server URL**: The redirect URIs configured for this client. These are the callback URLs used during the OAuth authorization flow.
* If a client secret is configured, an indicator that a client secret is required for this client.

<!-- Do NOT hardcode the MCP server URL / AS URL in examples — format is changing per cp-iam-team #2957. -->

To create or edit a client, click **Manage MCP client** to open the project's [MCP clients page](oauth-clients.md) in {{kib}}.

## Revoke connections

Revoking removes the selected connections only. The OAuth client stays registered and can accept new connections, and an application can be reconnected at any time.

To revoke a single connection, click **Revoke** in its row.

To revoke several connections at once:

1. Select the checkbox for each connection you want to revoke. In grouped view, use **Select all connections for this client** to select every connection under a client, or **Clear selection** to start over.
2. Click **Revoke *N* connections**.
3. Review the connections in the confirmation dialog, then click **Revoke access**.

You can revoke up to 100 connections at a time.

:::{tip}
Removing a user from your identity provider does **not** automatically revoke that user's connections. When a user leaves, revoke their connections here to cut off access.
:::

To revoke an entire OAuth client and all its connections, the client's creator removes it from the project's Agent Builder client management in Kibana. Refer to [](revoke-oauth-client.md).

## Next steps

To restore access after revoking a client, [create a new OAuth client](create-oauth-client.md) and distribute the credentials to users.

## Related pages

* [](create-oauth-client.md)
* [](connect-mcp-host.md)
* [](revoke-oauth-client.md)
* [](oauth-clients.md)
