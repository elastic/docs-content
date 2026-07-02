---
navigation_title: "Create an MCP client"
description: "Register an MCP client in Agent Builder to get the credentials and server URL needed to connect an MCP host over OAuth."
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

# Create an MCP client in Agent Builder [create-oauth-client]

Register a new MCP client in {{agent-builder}} to generate the credentials that an MCP host (such as **Claude Desktop**) needs to connect over OAuth 2.1.

Each MCP client is scoped to a single {{serverless-short}} project. Creating a client gives you a client ID, the MCP server URL for that project, and — for confidential clients — a client secret that is shown only once.

## Before you begin [create-oauth-client-before-you-begin]

- You need access to a {{serverless-short}} project with {{agent-builder}} enabled.
- [Understand OAuth for MCP clients](oauth-clients.md) before choosing client type and redirect URIs.

## Create the client

:::::{stepper}

::::{step}
Open the MCP client management page.

In {{kib}}, go to **Agent Builder → Tools library**, then click **Manage MCP** and select **Manage MCP clients (OAuth)**. Click **Add MCP client**.
::::

::::{step}
Name the client.

Enter a **Client name**. The name is visible to users during the authorization consent flow, so use something that clearly identifies the application (for example, `Claude Desktop — Engineering`).
::::

::::{step}
Select a client logo.

Optionally set a **Client logo** to identify the application in the list. Toggle between **Select logo** (choose from provided options) or **Upload logo** (use a custom image). Available logos: MCP client logo (default), Claude desktop, Open AI, Azure Open AI, Google AI Studio, Azure AI studio.

Selecting a logo is cosmetic — it does not pre-configure redirect URIs.
::::

::::{step}
Set the redirect URI.

The redirect URI tells the authorization server where to return the user after they grant consent. Select the redirect URI type:

- **Local** — for applications running on your local machine. The field is pre-populated with `http://localhost:3000/callback`. Replace or supplement this value to match your host's expected path. The authorization server accepts any localhost port, but the path must match exactly. Common values:
  - Claude Desktop (mcp-remote): `http://localhost:3000/oauth/callback`
  - Claude Code CLI (native HTTP): `http://localhost:3000/callback`
- **Remote** — for hosted or cloud-based applications. Enter a single `https://` URI. Plain HTTP is not accepted.

For local clients that need more than one redirect URI, click **Add local URL**.
::::

::::{step}
Save the client.

Click **Create client**. The **Copy server details for [client name]** dialog displays:

- **Client ID** — copy this; you'll need it when configuring the MCP host.
- **MCP server URL** — the endpoint your MCP host uses to reach this project's Agent Builder tools. Copy this alongside the client ID. Verify that the URL ends with `/api/agent_builder/mcp` and does not contain a doubled path segment. <!-- TODO: remove this note once kibana/274061 is resolved -->
- **Client secret** (confidential clients only) — the secret is shown **once** and cannot be retrieved later. Copy or download it immediately and store it securely.

Copy the new Client ID and the Server URL into the application config file, and save your changes. To apply the new configuration, restart the application.
::::

:::::

:::{note}
MCP clients can also be created through the {{kib}} API, authenticated with an {{ecloud}} API key. ES API keys are not accepted and are rejected early with a 400 error. Clients created this way are not visible in the Agent Builder client list — they appear only in the organization-level [Application connections](manage-application-connections.md) view in the {{ecloud}} Console.
:::

<!-- review: Liam — confirm whether this note belongs in Before you begin vs. here. Source: Jake Landis / Dennis Tismenko thread, 2026-06-01. -->

## What's next

Now that you have a client ID and MCP server URL, configure your MCP host to use them:

- [Connect an MCP host to an MCP client](connect-mcp-host.md)

## Related pages

- [Authenticate MCP clients with OAuth](oauth-clients.md)
- [Revoke an MCP client or connection](revoke-oauth-client.md)
- [Manage application connections](manage-application-connections.md)
