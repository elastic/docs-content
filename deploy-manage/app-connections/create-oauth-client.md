---
navigation_title: "Create an OAuth client"
description: "Register an OAuth client in Agent Builder to get the credentials and server URL needed to connect an MCP host over OAuth."
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Create an OAuth client in {{agent-builder}}

Register a new OAuth client in {{agent-builder}} to generate the credentials that an MCP host, such as Claude Desktop, needs to connect over OAuth 2.1. This is a one-time step you complete before connecting any host to {{agent-builder}}.

Each OAuth client is scoped to a single {{serverless-short}} project. Creating a client gives you a client ID and the MCP server URL for that project. For confidential clients, you also get a client secret that is shown only once and can't be retrieved later.

:::{note}
In the {{kib}} UI, OAuth clients are labeled **MCP clients**. The button and menu labels in these steps, such as **Add MCP client**, refer to the OAuth client you're creating.
:::

## Before you begin [create-oauth-client-before-you-begin]

Before you create an OAuth client:

- Familiarize yourself with the following concepts:
  - [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md), which provides the tools and agents you'll access.
  - The [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md), which exposes those tools to external MCP hosts, and its [authentication methods](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication). OAuth is one of two ways to authenticate to the MCP server, so confirm it fits your use case.
  - [MCP clients and the OAuth flow](oauth-clients.md).
- Make sure you have **Read** access to the {{agent-builder}} {{kib}} feature, which grants access to the MCP client management UI. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md#kib-privileges).
- Enable the **Manage OAuth clients for MCP** [{{kib}} advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings). 
  
  You can access the **Advanced Settings** management page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Create the client

:::::{stepper}

::::{step} Open the MCP client management page
1. Find **Agents** in the navigation menu. You can also search for **Agent Builder** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Manage components** at the bottom of the left sidebar, then select **Tools**.
3. On the tools library page, click **Manage MCP**, and then select **Manage MCP clients (OAuth)**. 
4. Click **Add MCP client**.

You can also get to this page from **Admin and settings** → **Application connections** → **Manage MCP clients**.
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

- **Local** — For applications running on your local machine. The redirect URIs are pre-populated with `http://localhost/callback` and `http://localhost/oauth/callback`. Replace or supplement these values to match your Agent's expected callback URL. The authorization server accepts any localhost port, but the path must match exactly. Common values:
  - Claude Desktop (mcp-remote): `http://localhost/oauth/callback`
  - Claude Code CLI (native HTTP): `http://localhost/callback`
- **Remote** — For hosted or cloud-based applications. Enter a single `https://` URL. Plain HTTP is not accepted.

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

## Next steps

Now that you have the client ID and MCP server URL for your OAuth client, [configure your MCP host to use them](connect-mcp-host.md).

You can also share these values so that other people connect the same client in their own MCP hosts. Each person authorizes access separately and gets their own connection.

## Related pages

- [](oauth-clients.md)
- [](revoke-oauth-client.md)
- [](manage-app-connections.md)
