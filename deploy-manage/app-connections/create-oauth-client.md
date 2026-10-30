---
navigation_title: "Create or edit an OAuth client"
description: "Register an OAuth client in Agent Builder to get the credentials and server URL needed to connect an MCP host over OAuth, or edit an existing client's name, logo, and redirect URIs."
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

# Create or edit an OAuth client in {{agent-builder}}

Register a new OAuth client in {{agent-builder}} to generate the credentials that an MCP host, such as Claude Desktop, needs to connect over OAuth 2.1. This is a one-time step you complete before connecting any host to {{agent-builder}}.

Each OAuth client is scoped to a single {{serverless-short}} project. Creating a client gives you a client ID and the MCP server URL for that project. For confidential clients, you also get a client secret that is shown only once and can't be retrieved later.

:::{note}
In the {{kib}} UI, OAuth clients are labeled **MCP clients**. The button and menu labels in these steps, such as **Add MCP client**, refer to the OAuth client you're creating.
:::

You can also [edit an existing client](#edit-oauth-client) to change its name, logo, or redirect URIs without replacing its credentials.

## Before you begin [create-oauth-client-before-you-begin]

Before you create an OAuth client:

- Familiarize yourself with the following concepts:
  - [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md), which provides the tools and agents you'll access.
  - The [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md), which exposes those tools to external MCP hosts, and its [authentication methods](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication). OAuth is one of two ways to authenticate to the MCP server, so confirm it fits your use case.
  - [MCP clients and the OAuth flow](oauth-clients.md).
- Make sure you have **Read** access to the {{agent-builder}} {{kib}} feature, which grants access to the MCP client management UI. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md#kib-privileges).

## Create the client

:::::{stepper}

::::{step} Open the MCP client management page
1. Find **Agents** in the navigation menu. You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the secondary navigation, select **Tools**.
3. In the **Tools** workspace, click **Manage all tools**.
4. In the **Tools library** workspace, click **Manage MCP**, and then select **Manage MCP clients (OAuth)**. 
5. Click **Add MCP client**.

You can also get to this page by searching for **Application connections** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md), then selecting **Manage MCP clients**.
::::

::::{step} Name the client
Enter a **Client name**. The name is visible to users during the authorization flow, so use something that clearly identifies the application (for example, `Claude Desktop — Engineering`).
::::

::::{step} Select a client logo
Optionally set a **Client logo** to identify the application in the list. Use **Select logo** to choose from provided options, or select **Upload logo** to use a custom image.

Selecting a logo is cosmetic, and does not pre-configure any settings.
::::

::::{step} Set the redirect URI
The redirect URI tells the authorization server where to return the user after they authorize the connection. Select the redirect URI type:

- **Local** — For applications running on your local machine. The redirect URIs are pre-populated with `http://localhost/callback` and `http://localhost/oauth/callback`. Replace or supplement these values to match your Agent's expected callback URL. The authorization server accepts any localhost port, but the path must match exactly. 

  Common values:
  - Claude desktop app: `http://localhost/oauth/callback`
  - Claude Code CLI (native HTTP): `http://localhost/callback`
  - Cursor (desktop): `http://localhost/callback` (Cursor uses port 8787, which is accepted automatically)
- **Remote** — For hosted or cloud-based applications. Enter a single `https://` URL. Plain HTTP is not accepted.

  Common values:
  - claude.ai: `https://claude.ai/api/mcp/auth_callback`
  - Cursor (web/agents): `https://www.cursor.com/agents/mcp/oauth/callback`
  - ChatGPT: `https://chatgpt.com/connector/oauth/{callback_id}`
  
    :::{warning}
    The ChatGPT callback URL is unique to each app. You must [start the app creation flow first](/deploy-manage/app-connections/connect-mcp-host.md) to get this URL, then return here to add it to your OAuth client.
    :::

For local clients that need more than one redirect URI, click **Add local URL** to add additional URLs.
::::

::::{step} Optional: Generate a client secret
You can optionally select **Generate confidential MCP client** to add a client secret for extra security. This is most useful when your MCP host can store a secret securely, such as a server-side service. 

The client secret is displayed after you create the client. The secret is only displayed once and can't be retrieved later.
::::

::::{step} Save the client
Click **Create client**. The **Copy server details for [client name]** dialog displays the values your MCP host (AI agent) needs to authenticate:

- **Client ID**: The identifier for this client.
- **MCP server URL**: The endpoint your MCP host uses to reach this project's {{agent-builder}} tools.
- **Client secret**: Appears for confidential clients only. This value is displayed only once and can't be retrieved later, so copy or download it before you close the dialog.

You'll use these values to [connect an MCP host](connect-mcp-host.md).

The client ID and MCP server URL can be retrieved at any time from the **MCP clients** page.
::::

:::::

## Edit a client [edit-oauth-client]

You can edit an active client's name, logo, and redirect URIs. You can't edit its client type, client ID, MCP server URL, or client secret. Revoked clients can't be edited.

To edit a client:

1. Find **Agents** in the navigation menu. You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the secondary navigation, select **Tools**.
3. In the **Tools** workspace, click **Manage all tools**.
4. In the **Tools library** workspace, click **Manage MCP**, and then select **Manage MCP clients (OAuth)**.
5. Find the client. Click **Actions**, and then click **Edit**.
6. Edit any of the following fields:
   - **Name**
   - **Client logo (optional)**: Select a provided logo, upload a custom logo, or remove the existing logo.
   - **Redirect URI type**: Select **Local** or **Remote**, then add, remove, or edit a redirect URI.

   The edited fields must meet the same requirements described in [Create the client](#create-the-client).
7. Click **Update**.

{{kib}} returns you to the **MCP clients** page and confirms that the client was updated.

## Next steps

After creating a client, [configure your MCP host](connect-mcp-host.md) with its client ID and MCP server URL.

You can also share these values so that other people connect the same client in their own MCP hosts. Each person authorizes access separately and gets their own connection.

## Related pages

- [](oauth-clients.md)
- [](revoke-oauth-client.md)
- [](manage-app-connections.md)
