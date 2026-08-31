---
navigation_title: "Revoke or delete a client or connection"
description: "Remove an individual connection or an entire OAuth client from Agent Builder to cut off OAuth access for a user or application, or permanently delete the retained record after revocation."
type: how-to
applies_to:
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Revoke or delete an OAuth client or connection

Revoking OAuth access in {{agent-builder}} immediately cuts off an MCP host's ability to use the Agent Builder tools. You can revoke access at two levels:

- **Revoke a connection**: Removes one user's authorized session for an OAuth client, while leaving the client registered. The user can reconnect by going through the authorization flow again.
- **Revoke an OAuth client**: Revokes the entire client and all its connections. Users whose connections are removed can no longer connect until a new client is created.

After revocation, you can permanently delete the retained [connection](#delete-a-connection) or [client](#delete-an-oauth-client) record. Deletion can't be undone.

Organization owners and project administrators can revoke connections for projects they administer from the {{ecloud}} Console. Users can also revoke connections they created themselves from the {{ecloud}} Console. Refer to [](manage-app-connections.md).
  
:::{warning}
Removing a user from your identity provider does **not** automatically revoke that user's connections. Revoke their connections manually when offboarding.
:::

## Before you begin [revoke-oauth-client-before-you-begin]

- Revoking or deleting connections from the **Application connections** page in {{kib}} requires the `manage_security` cluster privilege. A user with only `read_security` can view connections but can't revoke or delete them.
- Revoking or deleting clients requires **Read** access to the {{agent-builder}} {{kib}} feature. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md#kib-privileges).

## Revoke a connection

To revoke a single connection:

1. In {{kib}}, go to **Admin and settings** → **Application connections**.

   You can also reach this page from **Agent Builder** → **Tools library** → **Manage MCP** → **Manage MCP clients (OAuth)** by clicking **Manage application connections**.
2. Find the connection. In **Group by client** view, expand a client row to see its connections. Switch to **List view** to see all connections in a flat list.
3. Click **Revoke** in the connection's row. Alternatively, select the checkbox next to each connection you want to revoke, then click the bulk revoke button, which displays the number of selected connections, for example: **Revoke 9 connections**.
4. Review the details in the confirmation dialog, then click **Revoke**.

The connection is revoked immediately. The OAuth client stays registered and can accept new connections. Applications can be reconnected at any time by going through the authorization flow again.

## Delete a connection

Only revoked connections can be deleted. Revoked connections otherwise remain visible for 90 days. Deleting a connection permanently removes it immediately and can't be undone.

To delete one or more connections:

1. In {{kib}}, go to **Admin and settings** → **Application connections**.
2. Find a revoked connection. In **Group by client** view, expand a client row to see its connections. Switch to **List view** to see all connections in a flat list.
3. Click **Delete** in the connection's row. Alternatively, select the checkbox next to each revoked connection you want to delete, then click the bulk delete button, which displays the number of selected connections, for example: **Delete 9 connections**.
4. Review the connections in the confirmation dialog, then click **Delete permanently**.

The deleted connections are removed from the list. This action can't be undone. The OAuth client stays registered and can accept new connections.

## Revoke an OAuth client

Revoking a client immediately terminates all its connections. The client remains listed with a revoked status, and existing OAuth tokens for its connections stop working at the next validation.

To revoke an OAuth client:

1. In {{kib}}, go to **Agent Builder** → **Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)**.
2. Find the client. Click **Actions**, and then click **Revoke**.
3. In the **Revoke [client name]?** dialog, review the number of active connections that will be affected.
4. In the **MCP client name** field, type the client name exactly as shown to confirm, then click **Revoke**.

After revocation, users can no longer connect with that client until a new OAuth client is created.

To restore access after revoking a client, you can [create a new OAuth client](create-oauth-client.md) and distribute the new credentials to users.

## Delete an OAuth client

Only revoked clients can be deleted. Deleting a client permanently removes it and can't be undone.

To delete an OAuth client:

1. In {{kib}}, go to **Agent Builder** → **Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)**.
2. Find the revoked client. Click **Actions**, and then click **Delete**.
3. In the **Delete [client name]?** dialog, type the client name to confirm, then click **Delete**.

The client is permanently removed from the **MCP clients** page.

## Related pages

- [](oauth-clients.md)
- [](create-oauth-client.md)
- [](connect-mcp-host.md)
- [](manage-app-connections.md): Revoke or delete connections at the organization level in the {{ecloud}} Console.
