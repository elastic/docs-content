---
navigation_title: "Connect an MCP host"
description: "Configure an MCP host to use an OAuth MCP client and complete the user consent flow to establish a connection to Agent Builder."
type: how-to
applies_to:
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
---

# Connect an MCP host to an MCP client [connect-mcp-host]

After [creating an MCP client](create-oauth-client.md), configure your MCP host with the client ID and MCP server URL, then complete the OAuth consent flow to establish the connection.

This page covers two common MCP hosts:
* Claude Code CLI, which has native OAuth support
* Claude Desktop, which uses the `mcp-remote` adapter

Other OAuth 2.1 hosts follow the same general pattern, so consult your host's documentation for the specific configuration format.

<!-- TODO: confirm Cursor is supported in tech preview — cp-iam-team#2974 still open as of 2026-07-03. -->

## Before you begin [connect-mcp-host-before-you-begin]

Confirm the following before you configure your MCP host:

- You have an MCP host that supports OAuth 2.1, such as the Claude Code CLI or Claude Desktop.
- You have a client ID and MCP server URL from [creating an MCP client](create-oauth-client.md).
- You have access to the {{serverless-short}} project that the MCP client is scoped to, not just organization-level access. The connection acts with your own permissions in that project, so you also need the privileges required for the tools you'll run through the MCP server, such as {{agent-builder}} access and read access to any data those tools query. To learn more, refer to [Permissions](/explore-analyze/ai-features/agent-builder/permissions.md).

## Step 1: Configure your MCP host

Choose the instructions for your host.

### Claude Code CLI

**Option 1: Native HTTP transport (recommended)**

The Claude Code CLI supports OAuth natively — no additional adapter is required. When you created the client, the redirect URI `http://localhost:3000/callback` should be in your redirect URI list.

Run the following command, replacing `{CLIENT_ID}` and `{MCP_SERVER_URL}` with the values from your client's details page in {{kib}}:

```bash
claude mcp add --transport http --client-id {CLIENT_ID} kibana-mcp {MCP_SERVER_URL}
```

:::{note}
For a confidential client, add the `--client-secret` flag. The flag takes no value: the CLI prompts for the secret with masked input. To skip the prompt, set the `MCP_CLIENT_SECRET` environment variable before you run the command.

```bash
claude mcp add --transport http --client-id {CLIENT_ID} --client-secret kibana-mcp {MCP_SERVER_URL}
```
:::

**Option 2: mcp-remote adapter**

Use this option if your version of Claude Code doesn't support native HTTP OAuth transport. When you created the client, the redirect URI `http://localhost:3000/oauth/callback` should be in your redirect URI list.

```bash
claude mcp add --transport stdio kibana-mcp -- \
  npx mcp-remote \
  "{MCP_SERVER_URL}" \
  --static-oauth-client-info \
  "{\"client_id\":\"{CLIENT_ID}\"}"
```

Replace `{MCP_SERVER_URL}` and `{CLIENT_ID}` with the values from your client's details page in {{kib}}.

:::{note}
Confidential clients must include the client secret in the `--static-oauth-client-info` JSON: `{"client_id":"{CLIENT_ID}","client_secret":"{CLIENT_SECRET}"}`.
:::

The server is now configured. Start a Claude Code session. The OAuth consent flow triggers automatically on the first use of the server.

### Claude Desktop

Claude Desktop uses the [mcp-remote](https://www.npmjs.com/package/mcp-remote) adapter to handle OAuth connections. When you created the client, the redirect URI `http://localhost:3000/oauth/callback` should be in your client's redirect URI list.

To configure Claude Desktop:

1. In Claude Desktop, open **Settings → Developer → Edit Config**. This opens `claude_desktop_config.json` in your text editor.
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

   Replace `{MCP_SERVER_URL}` and `{CLIENT_ID}` with the values from your client's details page in {{kib}}.

   :::{note}
   Confidential clients also require a `client_secret` in the `--static-oauth-client-info` JSON. Include it as `"client_secret":"{CLIENT_SECRET}"` alongside the `client_id`.
   :::

3. Save the file and restart Claude Desktop to load the new configuration.

### Other MCP hosts**

Most hosts that support OAuth 2.1 accept a similar configuration. Provide the `{MCP_SERVER_URL}` and `{CLIENT_ID}` in the format your host requires.

## Step 2: Authorize the connection

The first time your MCP host tries to use the configured server, it opens a browser window and starts the OAuth consent flow.

1. Your browser opens to an {{ecloud}} sign-in page. Sign in with your {{ecloud}} credentials, even if you already have an active session — authentication is always required before you can grant consent.
2. The **Connect and authorize** page opens, showing which project the MCP client is requesting access to. Click **Authorize** to grant access.
3. The browser confirms the authorization is complete. Close the tab and return to your MCP host.

A new app connection is created in {{kib}}, scoped to your account and the project the MCP client was registered for. The connection name is auto-generated in the format `<client-name>#<word-pair>`.

If you click **Deny**, no connection is created. The host retries the flow the next time you use a tool, or you can restart the host to trigger a fresh attempt.

## Optional: Verify the connection

To ensure that the connection is registered in {{kib}}, you can check the number of currently active connections for your client.

In {{kib}}, go to **Agent Builder** → **Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)** to confirm the connection count for your client has increased. If you don't see it within a minute of authorizing, refresh the page.

You can also check your connection in the {{ecloud}} Console at **Organization** → **Security settings** → **Application connections**.

## Troubleshoot

**The host shows an error and doesn't open a browser.**

Confirm the `{MCP_SERVER_URL}` in your config matches exactly what {{kib}} displays. The correct URL ends with `/api/agent_builder/mcp`. A typo, extra slash, or doubled path segment will prevent the OAuth discovery step from completing.

**Authorization completed but no connection appears in {{kib}}.**

Confirm you have access to the {{serverless-short}} project the client was registered for. If your account doesn't have project access, the consent step fails silently.

**The host shows a new sign-in prompt after a period of inactivity.**

Connections expire after 30 days without use. Complete the authorization flow again to re-establish the connection.

**The authorization flow fails after you wait on the consent page.**

The MCP host's local callback server times out if the **Connect and authorize** page is left open too long before you click **Authorize**. Start the flow again and click **Authorize** promptly without leaving the consent page open.

**You need to start fresh with a new connection.**

Consult your MCP host's documentation for how to clear cached OAuth credentials and force a new authorization. Most hosts maintain only one connection for each MCP server URL, so reconfiguring with the same URL will reuse the existing connection unless the cached credentials are cleared.

## Next steps

When access is no longer needed, [revoke the connection](revoke-oauth-client.md).

## Related pages

See also:

- [](oauth-clients.md)
- [](create-oauth-client.md)
- [](manage-app-connections.md)
