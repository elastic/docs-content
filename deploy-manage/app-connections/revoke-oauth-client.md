---
navigation_title: "Revoke an MCP client or connection"
description: "Remove an individual connection or an entire MCP client from Agent Builder to cut off OAuth access for a user or application."
type: how-to
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Revoke an MCP client or connection

Revoking OAuth access in {{agent-builder}} immediately cuts off an MCP host's ability to use the Agent Builder tools. You can revoke access at two levels:

- **Revoke a connection**: Removes one user's authorized session for an MCP client, while leaving the client registered. The user can reconnect by going through the consent flow again.
- **Revoke an MCP client**: Revokes the entire client and all its connections. Users whose connections are removed can no longer connect until a new client is created.

Organization owners and project administrators can revoke connections for projects they administer from the {{ecloud}} Console. Users can also revoke connections they created themselves from the {{ecloud}} Console. Refer to [](manage-app-connections.md).
  
:::{warning}
Removing a user from your identity provider does **not** automatically revoke that user's connections. Revoke their connections manually when offboarding.
:::

## Before you begin [revoke-oauth-client-before-you-begin]

Revoking connections or clients from the **Application connections** page in {{kib}} requires the `manage_security` cluster privilege. A user with only `read_security` can view connections but can't revoke them.

## Revoke a connection

To revoke a single connection:

1. In {{kib}}, go to **Admin and settings** → **Application connections**.

   You can also reach this page from **Agent Builder** → **Tools library** → **Manage MCP** → **Manage MCP clients (OAuth)** by clicking **Manage application connections**.
2. Find the connection. In **Group by client** view, expand a client row to see its connections. Switch to **List view** to see all connections in a flat list.
3. Click **Revoke** in the connection's row. Alternatively, select the checkbox next to each connection you want to revoke and click **Revoke *N* connections**.
4. Review the details in the confirmation dialog, then click **Revoke**.

The connection is revoked immediately. The MCP client stays registered and can accept new connections. Applications can be reconnected at any time by going through the consent flow again.

## Revoke an MCP client

Revoking a client immediately terminates all its connections. The client is no longer listed in Agent Builder, and existing OAuth tokens for those connections stop working at the next validation.

To revoke an MCP client:

1. In {{kib}}, go to **Agent Builder** → **Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)**.
2. Find the client and click **Revoke** in its row.
3. In the **Revoke [client name]?** dialog, review the number of active connections that will be affected.
4. In the **MCP client name** field, type the client name exactly as shown to confirm, then click **Revoke**.

After revocation, users can no longer connect with that client until a new MCP client is created.

To restore access after revoking a client, you can [create a new MCP client](create-oauth-client.md) and distribute the new credentials to users.

## Related pages

- [](oauth-clients.md)
- [](create-oauth-client.md)
- [](connect-mcp-host.md)
- [](manage-app-connections.md): Revoke connections at the organization level in the {{ecloud}} Console.
