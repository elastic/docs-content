---
navigation_title: Elastic connector for Claude
description: "Add the Elastic Cloud Serverless connector from the Claude directory so Claude can search and analyze your project data through the Agent Builder MCP server."
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

## How the connector relates to the Elastic plugin for Claude

The connector and the [Elastic plugin for Claude](claude-plugin.md) complement each other:

- The **connector** gives Claude access to your data in one {{serverless-short}} project.
- The **plugin** gives Claude knowledge about Elastic, through agent skills and the Elastic Docs MCP server.
  The plugin doesn't connect Claude to your data.

Install both to have Claude follow Elastic best practices while working with your data.

## Requirements [elastic-claude-connector-requirements]

- You need an {{serverless-full}} project.
  The connector doesn't support {{ech}} deployments or self-managed clusters.
  For those, connect Claude to the MCP server with an [API key](/explore-analyze/ai-features/agent-builder/mcp-server-api-keys.md) instead.
- Each person who uses the connector needs access to the project, plus the privileges required by the tools they run.
  To learn more, refer to [](/explore-analyze/ai-features/agent-builder/permissions.md).
- On Claude Team and Enterprise plans, an organization Owner must add the connector for the organization before members can connect to it.
  Your organization might also restrict which directory connectors members can find.

## Set up the connector [elastic-claude-connector-setup]

::::::{stepper}

:::::{step} Create an OAuth client in your project
In your {{serverless-short}} project, [create an OAuth client](/deploy-manage/app-connections/create-oauth-client.md), and select **Generate confidential MCP client**.
Add the redirect URIs for the Claude apps you connect from.
For the redirect URI that each Claude app uses, refer to [](/deploy-manage/app-connections/connect-mcp-host.md).

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

On Claude Team and Enterprise plans, the connect button reads **Connect for your team** for organization Owners, and adds the connector for everyone in the organization.
To learn more, refer to [Get started with connectors](https://claude.com/docs/connectors/getting-started) in the Claude documentation.
:::::

:::::{step} Authorize the connection
Claude opens an {{ecloud}} sign-in page.
Sign in, review the project that Claude is requesting access to, and then select **Authorize**.

To confirm that the connection works, return to Claude and ask it to list the indices in your project.

To learn more about this step and how to verify the resulting connection, refer to [Authorize the connection](/deploy-manage/app-connections/connect-mcp-host.md#authorize-connection).
:::::

::::::

After you authorize the connection, you can manage or revoke it like any other application connection.
To learn more, refer to [](/deploy-manage/app-connections/revoke-oauth-client.md) and [](/deploy-manage/app-connections/manage-app-connections.md).

## Connect Claude to more than one project [elastic-claude-connector-multiple-projects]

Each OAuth client, and therefore each connection, is scoped to a single {{serverless-short}} project.
Claude supports only one configuration of a directory connector for each Claude account or organization, which means:

- On Claude Free, Pro, and Max plans, the connector connects your account to one project at a time.
- On Claude Team and Enterprise plans, the Owner who adds the connector chooses the project for the whole organization.
  Every member connects to that project, with their own {{ecloud}} account and permissions.

To connect Claude to additional projects, create an OAuth client in each project, and then add each project as a uniquely named [custom connector](/deploy-manage/app-connections/connect-mcp-host.md) with that project's MCP server URL, client ID, and client secret.
On Team and Enterprise plans, an Owner adds custom connectors for the organization.
To learn more, refer to [Add a connector that isn't in the directory](https://claude.com/docs/connectors/custom/add-unlisted) in the Claude documentation.

:::{note}
This limitation comes from how Claude manages directory connectors, and might change in future Claude releases.
:::

## Related pages

- [](/explore-analyze/ai-features/agent-builder/mcp-server.md)
- [](/deploy-manage/app-connections/oauth-clients.md)
- [](/deploy-manage/app-connections/connect-mcp-host.md)
- [](claude-plugin.md)
