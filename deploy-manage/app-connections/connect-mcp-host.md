---
navigation_title: "Connect an MCP host"
description: "Configure an MCP host to use an OAuth client and complete the authorization flow to establish a connection to Agent Builder."
type: how-to
applies_to:
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
---

# Connect an MCP host to {{agent-builder}}

After an OAuth client is [created](create-oauth-client.md), configure your MCP host, usually your AI agent, with the client ID and MCP server URL, then complete the OAuth authorization flow to establish the connection. After completing the setup, your MCP host has an authorized OAuth connection to {{agent-builder}} and can run its tools with your permissions.

This page covers several common MCP hosts:
* Claude Code CLI
* Claude desktop app
* claude.ai
* ChatGPT
* Cursor


Other OAuth 2.1 hosts follow the same general pattern, so consult your host's documentation for the specific configuration format.

## Before you begin [connect-mcp-host-before-you-begin]

Confirm the following before you configure your MCP host:

- You have an MCP host that supports OAuth 2.1 with a pre-registered client ID. Hosts that rely solely on dynamic client registration are not supported.
- You have the client ID and MCP server URL for the OAuth client. You either [created the client](create-oauth-client.md) yourself or received these values from the person who did.
- You have access to the {{serverless-short}} project that the OAuth client is scoped to, not just organization-level access. The connection acts with your own permissions in that project, so you also need the privileges required for the tools you'll run through the MCP server, such as {{agent-builder}} access and **Read** access to any data those tools query. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md).

## Connect your MCP host to an OAuth client [connect-mcp-host]

Complete the following steps to start using your OAuth client in your MCP host.

::::::::{stepper}

:::::::{step} Configure your MCP host

Choose the instructions for your host.

:::::{dropdown} Claude Code CLI

The Claude Code CLI supports OAuth natively, so no additional adapter is required.

Run the following command, replacing `{CLIENT_ID}` and `{MCP_SERVER_URL}` with the values for your OAuth client:

```bash
claude mcp add --transport http --client-id {CLIENT_ID} kibana-mcp {MCP_SERVER_URL}
```

:::{note}
For a confidential client, add the `--client-secret` flag. The flag takes no value: the CLI prompts for the secret with masked input. To skip the prompt, set the `MCP_CLIENT_SECRET` environment variable before you run the command.

```bash
claude mcp add --transport http --client-id {CLIENT_ID} --client-secret kibana-mcp {MCP_SERVER_URL}
```
:::

When Claude Code starts the OAuth flow, it listens for the authorization response at `http://localhost/callback`. This is one of the default redirect URIs populated in the [OAuth client registration form](/deploy-manage/app-connections/create-oauth-client.md#create-the-client), so it should be included in your client's redirect URIs unless you explicitly removed it.

::::{dropdown} Alternative: mcp-remote adapter
Use this option if your version of Claude Code doesn't support native HTTP OAuth transport.

```bash
claude mcp add --transport stdio kibana-mcp -- \
  npx mcp-remote \
  "{MCP_SERVER_URL}" \
  --static-oauth-client-info \
  "{\"client_id\":\"{CLIENT_ID}\"}"
```

Replace `{MCP_SERVER_URL}` and `{CLIENT_ID}` with the values for your OAuth client.

:::{note}
Confidential clients must include the client secret in the `--static-oauth-client-info` JSON: `{"client_id":"{CLIENT_ID}","client_secret":"{CLIENT_SECRET}"}`.
:::

When the `mcp-remote` adapter starts the OAuth flow, it listens for the authorization response at `http://localhost/oauth/callback`. This is one of the default redirect URIs populated in the [OAuth client registration form](/deploy-manage/app-connections/create-oauth-client.md#create-the-client), so it should be included in your client's redirect URIs unless you explicitly removed it.

:::{note}
The `mcp-remote` adapter stores OAuth credentials locally on your machine, keyed by MCP server URL. If more than one MCP host uses `mcp-remote` with the same server URL and client ID, those hosts share one app connection. After you complete the authorization flow in the first host, additional hosts that use the same configuration don't prompt you to authorize again.
:::

The server is now configured. Start a Claude Code session. The OAuth authorization flow triggers automatically on the first use of the server.
::::

:::::

:::::{dropdown} Claude desktop app
The Claude desktop app supports OAuth natively, so no additional adapter is required.

To configure the Claude desktop app:

1. Start the Claude desktop app and log in.
2. Open **Settings → Connectors → Add → Add custom connector**.
3. Enter a name, the URL, and Client ID.


:::{note}
Confidential clients also require a Client Secret.
:::

4. Click **Add**.
5. Click **Connect**.

When Claude desktop starts the OAuth flow, it expects an authorization callback at `https://claude.ai/api/mcp/auth_callback`.
If you get an authorization error, check [the OAuth client](/deploy-manage/app-connections/create-oauth-client.md#create-the-client) you created includes this redirect URI.

:::{note}
Some enterprises may restrict adding custom connectors in this way. See the mcp-remote adapter alternative below.
:::

::::{dropdown} Alternative: mcp-remote adapter
The Claude desktop app supports local MCP servers, and can use the [mcp-remote](https://www.npmjs.com/package/mcp-remote) adapter to handle OAuth connections.

To configure the Claude desktop app:

1. In the Claude desktop app, open **Settings → Developer → Edit Config**. This opens `claude_desktop_config.json` in your text editor.
2. Add your MCP client to the `mcpServers` object:

   ```json
   {
     "mcpServers": {
       "kibana-mcp": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "{MCP_SERVER_URL}",
           "--static-oauth-client-info",
           "{\"client_id\":\"{CLIENT_ID}\"}"
         ]
       }
     }
   }
   ```

   Replace `{MCP_SERVER_URL}` and `{CLIENT_ID}` with the values for your OAuth client.

   :::{note}
   Confidential clients also require a `client_secret` in the `--static-oauth-client-info` JSON: `{"client_id":"{CLIENT_ID}","client_secret":"{CLIENT_SECRET}"}`.
   :::

3. Save the file and restart the Claude desktop app to load the new configuration.

When the `mcp-remote` adapter starts the OAuth flow, it listens for the authorization response at `http://localhost/oauth/callback`. This is one of the default redirect URIs populated in the [OAuth client registration form](/deploy-manage/app-connections/create-oauth-client.md#create-the-client), so it should be included in your client's redirect URIs unless you explicitly removed it.

:::{note}
The `mcp-remote` adapter stores OAuth credentials locally on your machine, keyed by MCP server URL. If more than one MCP host uses `mcp-remote` with the same server URL and client ID, those hosts share one app connection. After you complete the authorization flow in the first host, additional hosts that use the same configuration don't prompt you to authorize again.
:::
::::

:::::

:::::{dropdown} claude.ai

The Claude web interface (https://claude.ai) supports OAuth natively, so no additional adapter is required.

To connect from claude.ai:

1. Log in to claude.ai.
2. Click your account menu, and then go to **Settings → Connectors → Add → Add custom connector**.
3. Enter a name, the URL, and Client ID. Confidential clients also require a Client Secret.
4. Click **Add**.
5. Click **Connect**

When the Claude web interface starts the OAuth flow, it listens for the authorization response at `https://claude.ai/api/mcp/auth_callback`.
If you get an authorization error, check [the OAuth client](/deploy-manage/app-connections/create-oauth-client.md#create-the-client) you created includes this redirect URI.

:::::

:::::{dropdown} ChatGPT

ChatGPT supports OAuth natively for custom MCP apps.

:::{important}
ChatGPT assigns a unique callback URL to each app. You won't know this URL until you start the following app creation flow. You need to add the URL to your [OAuth client](/deploy-manage/app-connections/create-oauth-client.md#create-the-client) as a remote redirect URI before you can finish the ChatGPT setup.
:::

To connect from ChatGPT:

1. Go to **Settings → Security and login** and enable **Developer mode**.
2. Go to **Settings → Plugins**, then click the plus button to create a new plugin.
3. Enter a name and the MCP server URL, and select **OAuth** as the authentication type.
4. Under **Registration method**, select **User-Defined OAuth Client**.
5. Copy the **Callback URL** that ChatGPT displays. This URL is unique to the app and looks like `https://chatgpt.com/connector/oauth/{callback_id}`. Open your [OAuth client](/deploy-manage/app-connections/create-oauth-client.md#create-the-client) in a separate tab and add this URL as a **Remote** redirect URI.
6. Return to ChatGPT. Enter the **Client ID** and **Client Secret** from your Elastic OAuth client.
7. Click **Scan Tools** to start the OAuth flow, then complete the authorization prompt.
:::::

:::::{dropdown} Cursor

Cursor supports OAuth natively for remote MCP servers through `mcp.json`.

To connect from Cursor:

1. Open your Cursor MCP configuration file. Use `.cursor/mcp.json` for project-specific config, or `~/.cursor/mcp.json` for global config.
2. Add the server with static OAuth credentials:

   ```json
   {
     "mcpServers": {
       "kibana-mcp": {
         "url": "{MCP_SERVER_URL}",
         "auth": {
           "CLIENT_ID": "{CLIENT_ID}",
           "CLIENT_SECRET": "{CLIENT_SECRET}"
         }
       }
     }
   }
   ```

   Replace `{MCP_SERVER_URL}`, `{CLIENT_ID}`, and `{CLIENT_SECRET}` with the values for your OAuth client. For public clients, omit the `CLIENT_SECRET` field.

3. Open **Cursor Settings → Tools & MCP**. The server appears with a **Connect** button.
4. Click **Connect** to start the OAuth flow.

When Cursor starts the OAuth flow, it redirects to one of two callback URLs depending on the surface:

- **Cursor desktop**: `http://localhost:8787/callback`. The authorization server accepts any localhost port, and `/callback` is one of the default redirect URIs populated in the [OAuth client registration form](/deploy-manage/app-connections/create-oauth-client.md#create-the-client), so it should be included in your client's redirect URIs unless you explicitly removed it.
- **Cursor web and Cursor Agents**: `https://www.cursor.com/agents/mcp/oauth/callback`. If you get an authorization error, check that your [OAuth client](/deploy-manage/app-connections/create-oauth-client.md#create-the-client) includes this as a Remote redirect URI.
:::::

:::::{dropdown} Other

Most hosts that support OAuth 2.1 accept a similar configuration to Claude. Provide the `{MCP_SERVER_URL}` and `{CLIENT_ID}` in the format your host requires.

:::::

::::::

:::::::

:::::::{step} Authorize the connection
:anchor: authorize-connection

The first time your MCP host tries to use the configured server, it opens a browser window and starts the OAuth authorization flow.

:::{note} 
Some tools might require additional manual steps. For example, Claude Code CLI requires that you enter `/mcp` or run `claude mcp login <mcp-server-name>` before the browser window opens.
:::

1. Your browser opens to an {{ecloud}} sign-in page. Sign in with your {{ecloud}} credentials. If you have an active session, you are not prompted to log in again.
2. The **Connect and authorize** page opens, showing which project the OAuth client is requesting access to. Click **Authorize** to grant access.
3. The browser confirms the authorization is complete. Close the tab and return to your MCP host.

A new app connection is created scoped to your account and the project associated with the OAuth client. The connection name is auto-generated in the format `<client-name>#<word-pair>`. This connection is visible in both {{kib}} and the {{ecloud}} Console.

If you click **Deny** on the **Connect and authorize** page, then no connection is created. The host retries the flow the next time you use a tool, or you can restart the host to trigger a fresh attempt.

:::: {admonition} Application permissions
:::{include} /deploy-manage/_snippets/app-connection-permissions.md
:::
::::

:::::::

:::::::{step} Verify the connection

This step is optional. To ensure that the connection is registered in {{kib}}, you can check the number of currently active connections for your client.

In {{kib}}, go to **Agent Builder** → **Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)** to confirm the connection count for your client has increased. If you don't see it within a minute of authorizing, refresh the page.

You can also check your connection in the {{ecloud}} Console at **Organization** → **Security settings** → **Application connections**.

:::::::

::::::::

## Troubleshoot

**The host shows an error and doesn't open a browser.**

Confirm the `{MCP_SERVER_URL}` in your config matches exactly what {{kib}} displays. The correct URL ends with `/api/agent_builder/mcp`. A typo, extra slash, or doubled path segment will prevent the OAuth discovery step from completing.

**Authorization completed but no connection appears in {{kib}}.**

Confirm you have access to the {{serverless-short}} project associated with the OAuth client. If your account doesn't have project access, the authorization step fails silently.

**The host shows a new sign-in prompt after a period of inactivity.**

Connections expire after 30 days without use. Complete the authorization flow again to re-establish the connection.

**The authorization flow fails after you wait on the authorization page.**

The MCP host's local callback server times out if the **Connect and authorize** page is left open too long before you click **Authorize**. Start the flow again and click **Authorize** promptly without leaving the page open.

**You need to start fresh with a new connection.**

Consult your MCP host's documentation for how to clear cached OAuth credentials and force a new authorization. Most hosts maintain only one connection for each MCP server URL, so reconfiguring with the same URL reuses the existing connection unless the cached credentials are cleared.

## Next steps

When access is no longer needed, [revoke the connection](revoke-oauth-client.md).

## Related pages

- [](oauth-clients.md)
- [](create-oauth-client.md)
- [](manage-app-connections.md)
