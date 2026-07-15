---
navigation_title: "Create an MCP client"
description: "Register an MCP client in Agent Builder to get the credentials and server URL needed to connect an MCP host over OAuth."
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Create an MCP client in Agent Builder [create-oauth-client]

Register a new MCP client in {{agent-builder}} to generate the credentials that an MCP host, such as Claude Desktop, needs to connect over OAuth 2.1. This is a one-time pre-registration step: OAuth requires each client to be registered with the MCP server before any host can connect or any user can authenticate and consent.

Each MCP client is scoped to a single {{serverless-short}} project. Creating a client gives you a client ID and the MCP server URL for that project. For confidential clients, you also get a client secret that is shown only once and can't be retrieved later.

## Before you begin [create-oauth-client-before-you-begin]

Before you create an MCP client:

- Familiarize yourself with the following concepts:
  - [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md), which provides the tools and agents you'll access.
  - The [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md), which exposes those tools to external MCP hosts, and its [authentication methods](/explore-analyze/ai-features/agent-builder/mcp-server.md#mcp-server-authentication). OAuth is one of two ways to authenticate to the MCP server, so confirm it fits your use case.
  - [MCP clients and the OAuth flow](oauth-clients.md).
- Make sure you have **Read** access to the {{agent-builder}} {{kib}} feature, which grants access to the MCP client management UI. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md#kib-privileges).

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
Enter a **Client name**. The name is visible to users during the authorization consent flow, so use something that clearly identifies the application (for example, `Claude Desktop — Engineering`).
::::

::::{step} Select a client logo
Optionally set a **Client logo** to identify the application in the list. Use **Select logo** to choose from provided options, or select **Upload logo** to use a custom image.

Selecting a logo is cosmetic, and does not pre-configure any settings.
::::

::::{step} Set the redirect URI
The redirect URI tells the authorization server where to return the user after they grant consent. Select the redirect URI type:

- **Local** — For applications running on your local machine. The redirect URIs are pre-populated with `http://localhost:3000/callback` and `http://localhost/oauth/callback`. Replace or supplement these values to match your Agent's expected callback URL. The authorization server accepts any localhost port, but the path must match exactly. Common values:
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
- **MCP server URL**: The endpoint your MCP host (AI agent) uses to reach this project's {{agent-builder}} tools.
- **Client secret**: Appears for confidential clients only. This value is displayed only once and can't be retrieved later, so copy or download it before you close the dialog.

You'll use these values to [connect an MCP host](connect-mcp-host.md).

The client ID and MCP server URL can be retrieved at any time from the **MCP clients** page.
::::

:::::

% todo: endpoint link
:::{note}

MCP clients can also be created through the {{kib}} API. To create a client through the API, you must use an {{ecloud}} API key with [Cloud, {{es}}, and {{kib}} API access](/deploy-manage/api-keys/elastic-cloud-api-keys.md#project-access). Creating a client with an API key created directly in {{es}} is not supported. 

Clients created through the API are not visible in the Agent Builder client list in {{kib}}, because they are not owned by a specific user. They appear only in the organization-level [Application connections](manage-app-connections.md) view in the {{ecloud}} Console.

% source: https://elastic.slack.com/archives/C0AH1CA7S3Y/p1780340150585789
:::

## Next steps

Now that you have the connection information for your MCP client, [configure your MCP host to use it](connect-mcp-host.md).

## Related pages

- [](oauth-clients.md)
- [](revoke-oauth-client.md)
- [](manage-app-connections.md)
