---
navigation_title: Elastic Serverless Claude connector
description: "The official Elastic Cloud Serverless connector enables Claude to search and analyze your Elastic Cloud Serverless project data using the Agent Builder MCP server."
type: overview
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
  - id: kibana
  - id: elasticsearch
  - id: observability
  - id: security
---

# Elastic Cloud Serverless connector for Claude [elastic-claude-connector]

The [Elastic Cloud Serverless connector](https://claude.com/marketplace/connectors/elastic-cloud-serverless) is an official, Anthropic-verified [Claude connector](https://claude.com/docs/connectors/getting-started) that connects Claude to the [{{agent-builder}} Model Context Protocol (MCP) server](/explore-analyze/ai-features/agent-builder/mcp-server.md) of an {{serverless-full}} project.
After you connect it, Claude can use {{agent-builder}} tools to search and analyze the data in your project with your own permissions.

The connector is listed in the Claude connectors directory, so you can add it without configuring a custom connector.
It authenticates with [OAuth 2.1](/deploy-manage/app-connections/oauth-clients.md): each person authorizes access in the browser, and Claude acts with that person's permissions in the project.

## Use cases

After you set up the connector, you can ask Claude to work with the data in your project, for example to:

- Explore your indices and their mappings.
- Write and run {{esql}} queries.
- Investigate logs and other {{observability}} data.
- Run and monitor [workflows](/explore-analyze/workflows.md).

The tools available to Claude are the [{{agent-builder}} tools](/explore-analyze/ai-features/agent-builder/tools.md) that your project exposes through the MCP server.
The exact set depends on your project type and on any custom tools you've created.

## How Claude connector and plugin work together

The connector and the [Elastic plugin for Claude](claude-plugin.md) complement each other:

- The **connector** gives Claude access to your data in one {{serverless-short}} project.
- The **plugin** gives Claude knowledge about Elastic, through agent skills and the Elastic Docs MCP server.
  The plugin doesn't connect Claude to your data.

The plugin is an add-on that you install in Claude.
It doesn't need your project's URL or credentials, and it isn't installed in or connected to your {{serverless-short}} project.
Use it with the connector to have Claude follow Elastic best practices while working with your data.

## Requirements [elastic-claude-connector-requirements]

- You need an {{serverless-full}} project.
  The connector doesn't support {{ech}} deployments or self-managed clusters.
  For those, connect Claude to the MCP server with an [API key](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md) instead.
- Each person who uses the connector needs access to the project, plus the privileges required by the tools they run.
  To learn more, refer to [](/explore-analyze/ai-features/agent-builder/permissions.md).
- On Claude Team and Enterprise plans, an organization Owner must set up the connector for the organization before members can connect to it.
  Your organization might also restrict which directory connectors members can find.

## Set up the connector [elastic-claude-connector-setup]

Setting up the connector means creating an OAuth client in your project and entering its credentials in Claude:

- On Claude Free, Pro, and Max plans, you set up the connector for your own account.
- On Claude Team and Enterprise plans, an organization Owner sets up the connector once for the whole organization.
  Members don't create OAuth clients or enter credentials.
  Instead, they [connect to the configured connector](#elastic-claude-connector-member).

::::::{stepper}

:::::{step} Create an OAuth client in your project
In your {{serverless-short}} project, [create an OAuth client](/deploy-manage/app-connections/create-oauth-client.md), and select **Generate confidential MCP client**.
Add the redirect URI for the Claude app you use to set up the connector, as described in the [claude.ai](/deploy-manage/app-connections/connect-mcp-host.md#connect-claude-ai) or [Claude desktop app](/deploy-manage/app-connections/connect-mcp-host.md#connect-claude-desktop) instructions.

Copy the **Client ID**, **Client secret**, and **MCP server URL** from the **Copy server details** dialog.
{{kib}} shows the client secret only once.
:::::

:::::{step} Add the connector in Claude
1. Open the [Elastic Cloud Serverless connector listing](https://claude.com/marketplace/connectors/elastic-cloud-serverless), and then select **Connect to Claude**.

   You can also find the connector in Claude on the web or in the desktop app: go to **Settings** → **Connectors**, browse the connectors directory, and search for **Elastic Cloud Serverless**.
2. In the **Connect Elastic Cloud Serverless** dialog, enter the values from your OAuth client:
   - **Server URL**: the MCP server URL
   - **OAuth Client ID**: the client ID
   - **OAuth Client Secret**: the client secret
3. Select **Connect**.

:::{image} images/claude-connect-elastic-cloud-serverless.png
:screenshot:
:alt: The Connect Elastic Cloud Serverless dialog in Claude, with fields for the Server URL, OAuth Client ID, and OAuth Client Secret, and a Connect button.
:width: 500px
:::

:::{note}
On Claude Team and Enterprise plans, Owners see **Connect for your team** instead of **Connect to Claude**.
Connecting for your team adds the connector for everyone in the organization, but doesn't connect your own account.
To use the connector yourself, connect your own account afterward, as members do.
To learn more, refer to [Get started with connectors](https://claude.com/docs/connectors/getting-started) in the Claude documentation.
:::
:::::

:::::{step} Authorize the connection
Claude opens an {{ecloud}} sign-in page.
Sign in, review the project that Claude is requesting access to, and then select **Authorize**.

To learn more about this step, refer to [Authorize the connection](/deploy-manage/app-connections/connect-mcp-host.md#authorize-connection).
:::::

::::::

After setup, [check that the connector works](#elastic-claude-connector-verify).

## Connect as an organization member [elastic-claude-connector-member]

On Claude Team and Enterprise plans, after an Owner sets up the connector for the organization, each member connects their own account.
You don't need an OAuth client or credentials of your own.

1. In Claude, go to **Settings** → **Connectors**, and find **Elastic Cloud Serverless**.
2. Select **Connect**.
3. Sign in to {{ecloud}}, review the project that Claude is requesting access to, and then select **Authorize**.

You connect to the project that the Owner chose, with your own {{ecloud}} account and permissions.

## Check that the connector works [elastic-claude-connector-verify]

1. In Claude, start a new conversation, and make sure that the **Elastic Cloud Serverless** connector is turned on for that conversation.
2. Ask Claude to list the indices in your project.
3. If Claude asks for your approval before it uses a tool, approve the request.

Claude lists your indices by using the {{agent-builder}} tools in your project.
To learn more about turning connectors on and approving tool use, refer to [Use the connector in a conversation](https://claude.com/docs/connectors/getting-started#use-the-connector-in-a-conversation) in the Claude documentation.

After you authorize the connection, you can manage or revoke it like any other application connection.
To learn more, refer to [](/deploy-manage/app-connections/revoke-oauth-client.md) and [](/deploy-manage/app-connections/manage-app-connections.md).

## Connect Claude to more than one project [elastic-claude-connector-multiple-projects]

Each OAuth client, and therefore each connection, is scoped to a single {{serverless-short}} project.
Claude supports only one configuration of a directory connector for each Claude account or organization, which means:

- On Claude Free, Pro, and Max plans, the connector connects your account to one project at a time.
- On Claude Team and Enterprise plans, the Owner who sets up the connector chooses the project for the whole organization.

:::{note}
This one-configuration limit comes from how Claude manages directory connectors, and might change in future Claude releases.
:::

You don't always need another connection to work with data from several projects.
If your projects are linked through [{{cps}}](/explore-analyze/cross-project-search.md), tool calls through one connection can search the linked projects.
To learn more, refer to [Use tools with data from multiple projects](/explore-analyze/ai-features/agent-builder/mcp-server.md#agent-builder-mcp-cps).

To connect Claude to the MCP servers of additional projects:

1. In each additional project, [create an OAuth client](/deploy-manage/app-connections/create-oauth-client.md).
2. In Claude, add each project as a uniquely named [custom connector](/deploy-manage/app-connections/connect-mcp-host.md#connect-claude-ai), using that project's MCP server URL, client ID, and client secret.

On Team and Enterprise plans, an Owner adds custom connectors for the organization.
To learn more, refer to [Add a connector that isn't in the directory](https://claude.com/docs/connectors/custom/add-unlisted) in the Claude documentation.

## Related pages

- [](/explore-analyze/ai-features/agent-builder/mcp-server.md)
- [](/deploy-manage/app-connections/oauth-clients.md)
- [](/deploy-manage/app-connections/create-oauth-client.md)
- [](/deploy-manage/app-connections/connect-mcp-host.md)
- [](claude-plugin.md)
