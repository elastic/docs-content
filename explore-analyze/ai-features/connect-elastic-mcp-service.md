---
navigation_title: Connect an MCP host
description: Add an MCP host to the Elastic Global MCP Service, complete OAuth sign-in, and confirm the connection by listing Serverless projects or creating one.
type: how-to
# Lifecycle is unconfirmed. preview is a placeholder until product names preview, beta, or ga.
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: cloud-serverless
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Connect an MCP host to the {{mcp-service}} [connect-elastic-mcp-service]

Connect your MCP host to the [{{mcp-service}}](/explore-analyze/ai-features/elastic-mcp-service.md) so an agent in that host can work with every {{serverless-full}} project you can access.
You add the service URL, sign in with Elastic in the browser, then ask a sample question to confirm the connection.
After you authorize it, the host acts with your permissions.

## Before you begin [connect-elastic-mcp-service-before-you-begin]

You need the following before you connect:

- An {{ecloud}} account. If you don't have one yet, [sign up](/deploy-manage/deploy/elastic-cloud/create-an-organization.md).
- An MCP host that supports OAuth 2.1, such as Claude Code, Cursor, Visual Studio Code, Codex, or Gemini CLI.

An existing {{serverless-short}} project is optional.
You can create one from the host after you connect if you have the `admin` [predefined role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) or an equivalent custom role.

:::{note}
This service can't reach a project that uses [private connectivity](/deploy-manage/security/private-connectivity.md).
:::

## Connect the host [connect-elastic-mcp-service-steps]

::::::{stepper}

:::::{step} Add the server

Add {{mcp-service-mcp-url}} to your host.

Choose the instructions for your host.

::::{tab-set}

:::{tab-item} Claude Code

Run the following command:

```bash subs=true
claude mcp add --transport http --scope user elastic {{mcp-service-mcp-url}}
```

:::

:::{tab-item} Cursor

Add the following to `.cursor/mcp.json` in your project or home directory:

```json subs=true
{
  "mcpServers": {
    "elastic": {
      "url": "{{mcp-service-mcp-url}}"
    }
  }
}
```

:::

:::{tab-item} Visual Studio Code

Add the following to `.vscode/mcp.json` in your project:

```json subs=true
{
  "servers": {
    "elastic": {
      "type": "http",
      "url": "{{mcp-service-mcp-url}}"
    }
  }
}
```

:::

:::{tab-item} Codex

Run the following command:

```bash subs=true
codex mcp add elastic --url {{mcp-service-mcp-url}}
```

:::

:::{tab-item} Gemini CLI

Add the following to `~/.gemini/settings.json`:

```json subs=true
{
  "mcpServers": {
    "elastic": {
      "httpUrl": "{{mcp-service-mcp-url}}",
      "oauth": {
        "enabled": true
      }
    }
  }
}
```

:::

::::

For ChatGPT, Gemini Enterprise, or Amazon Bedrock AgentCore, refer to [Hosts that register their own OAuth application](#hosts-that-register-oauth).
:::::

:::::{step} Authenticate in the browser

Complete sign-in in the host. The host opens a browser so you can sign in to Elastic and approve the connection.

After you sign in, the **Connect and authorize** page names your {{ecloud}} organization and the access the host will have, based on your current roles. Review it, then select **Authorize**.

If you're unsure what those roles allow, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md). For how organizations work, refer to [Cloud organization users](/deploy-manage/users-roles/cloud-organization.md).

Until you finish that sign-in, the host might show that the server needs authentication. That's expected.

If sign-in doesn't start on its own, open the host's MCP settings and authenticate there.
:::::

:::::{step} Ask a sample question

Start a session in the host and ask something that needs the service. The question you use depends on whether you already have a {{serverless-short}} project.

If you already have projects, ask:

```text
Which Elastic projects can I access?
```

The agent should list the projects you can access. An empty list means the connection works and you don't have a project yet.

If you don't have a project, ask:

```text
Create an Elastic project.
```

The agent typically asks for details such as the project type, name, and region.
If you're choosing a type, refer to [{{serverless-short}} project types](/deploy-manage/deploy/elastic-cloud/serverless.md#choose-a-project-type). For available regions, refer to [{{serverless-short}} regions](/deploy-manage/deploy/elastic-cloud/regions.md).
You can create and update projects through this service. You can't delete a project through it.
:::::

::::::

## Hosts that register their own OAuth application [hosts-that-register-oauth]

ChatGPT, Gemini Enterprise, and Amazon Bedrock AgentCore need you to register an OAuth application in that host, not only add a URL.

Unlike when you [connect a host to {{agent-builder}}](/deploy-manage/app-connections/connect-mcp-host.md), this service does not use a {{kib}} OAuth client. Use {{mcp-service-mcp-url}} as the server URL and follow the host's documentation for a remote MCP server that requires sign-in.

## Next steps [connect-elastic-mcp-service-next-steps]

- Learn what the [{{mcp-service}}](/explore-analyze/ai-features/elastic-mcp-service.md) can do after you connect.
- If you prefer the console, [create an {{serverless-full}} project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md).

## Related pages [connect-elastic-mcp-service-related]

- [{{mcp-service}}](/explore-analyze/ai-features/elastic-mcp-service.md)
- [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md)
- [{{serverless-short}} regions](/deploy-manage/deploy/elastic-cloud/regions.md)