---
navigation_title: "Connect an MCP host"
description: "Configure an MCP host to use an OAuth MCP client and complete the user consent flow to establish a connection to Agent Builder."
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

# Connect an MCP host to an MCP client [mcp-client-connect]

After [creating an MCP client](mcp-client-create.md), configure your MCP host with the client ID and MCP server URL, then complete the OAuth consent flow to establish the connection.

This page covers two common MCP hosts: the **Claude Code CLI** (which has native OAuth support) and **Claude Desktop** (which uses the `mcp-remote` adapter). Other hosts that support OAuth 2.1 with PKCE follow the same general pattern — consult your host's documentation for the specific configuration format.

## Before you begin [mcp-client-connect-before-you-begin]

- You have a client ID and MCP server URL from [creating an MCP client](mcp-client-create.md).
- You have access to the {{serverless-short}} project that the MCP client is scoped to.

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
Confidential clients also require `--client-secret {CLIENT_SECRET}` in the preceding command.

<!-- TODO: confirm `--client-secret` flag name for confidential clients in Claude Code CLI.
     Source: Jake Landis (back from PTO 2026-07-06). -->
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

<!-- TODO (Jake Landis, back 2026-07-06): confirm whether Option 2 (mcp-remote + stdio) should
     be kept in public docs for tech preview users, or whether all preview-era Claude Code CLI
     builds support native HTTP OAuth and Option 2 can be removed. Both options appear in
     cp-iam-team#2963 testing notes (June 18) as equally valid QA paths; Elena Shostak confirmed
     --transport http working in #cp-iam-oauth-project June 5 + June 18. Jake to advise on
     public-facing guidance. -->

The server is now configured. Start a Claude Code session — the OAuth consent flow triggers automatically on the first use of the server.

### Claude Desktop

Claude Desktop uses the [mcp-remote](https://www.npmjs.com/package/mcp-remote) adapter to handle OAuth connections. When you created the client, the redirect URI `http://localhost:3000/oauth/callback` should be in your client's redirect URI list.

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

**Other MCP hosts** — most hosts that support OAuth 2.1 with PKCE accept a similar configuration. Provide the `{MCP_SERVER_URL}` and `{CLIENT_ID}` in the format your host requires.

## Step 2: Authorize the connection

The first time your MCP host tries to use the configured server, it opens a browser window and starts the OAuth consent flow.

1. Your browser opens to an {{ecloud}} sign-in page. Sign in with your {{ecloud}} credentials, even if you already have an active session — authentication is always required before you can grant consent.
2. The **Connect and authorize** page opens, showing which project the MCP client is requesting access to. Click **Authorize** to grant access.
3. The browser confirms the authorization is complete. Close the tab and return to your MCP host.

A new **app connection** is created in {{kib}}, scoped to your account and the project the MCP client was registered for. The connection name is auto-generated in the format `<client-name>#<word-pair>`.

:::{note}
If you click **Deny**, no connection is created. The host retries the flow the next time you use a tool, or you can restart the host to trigger a fresh attempt.
:::

## Verify the connection

In {{kib}}, go to **Agent Builder → Tools library**, click **Manage MCP**, and select **Manage MCP clients (OAuth)** to confirm the connection count for your client has increased. If you don't see it within a minute of authorizing, refresh the page.

You can also check your connection in the Cloud Console at **Organization → Security settings → Application connections**.

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

Consult your MCP host's documentation for how to clear cached OAuth credentials and force a new authorization. Most hosts maintain only one connection per MCP server URL, so reconfiguring with the same URL will reuse the existing connection unless the cached credentials are cleared.

<!-- Guardrail: do NOT include ~/.mcp-auth rm, NODE_TLS_REJECT_UNAUTHORIZED=0,
     or any QA-environment-specific credential-clearing commands. -->

## Next steps

- [Revoke an MCP client or connection](mcp-client-revoke.md) when access is no longer needed.

## Related pages

- [Authenticate MCP clients with OAuth](mcp-client-oauth.md)
- [Create an MCP client](mcp-client-create.md)
- [Manage application connections](/deploy-manage/users-roles/cloud-organization/manage-mcp-client-connections.md)
