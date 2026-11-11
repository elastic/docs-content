---
navigation_title: "{{mcp-service}}"
description: Connect Model Context Protocol (MCP) hosts to Elastic Serverless projects with the Elastic Global MCP Service. One authorized connection covers every accessible project.
type: overview
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

# {{mcp-service}} [elastic-mcp-service]

The {{mcp-service}} provides an interface for Model Context Protocol hosts (such as Claude, Cursor, Visual Studio Code, ChatGPT, Codex, or Gemini) to access your {{serverless-full}} projects.
After you authorize it, the host and any agent in it can find your projects, answer questions, and run built-in tools with your permissions.

## Use cases [use-cases]

- **Start in the host you already use.** Use your existing IDE, CLI, or chat app to sign in to the service, then ask it to create a {{serverless-short}} project and work with the data you add to it.
- **Use every project you can access from one connection.** Unlike the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md), which is a separate endpoint for each project, this service is one URL, `https://mcp.elastic.co`.
- **Let an agent do the work as you.** After you authorize the connection, an agent in the host can take the same actions you can take in those projects.

Choose a different option when:

- You want {{agent-builder}} tools, including tools you created. Use the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md), which also works on {{stack}} deployments.
- The project uses [private connectivity](/deploy-manage/security/private-connectivity.md). The {{mcp-service}} doesn't support those projects.
- You use {{ech}} or a self-managed cluster. This service is for {{serverless-short}} projects only. Use the [Elastic CLI](cli://index.md) or the {{agent-builder}} MCP server when those apply.

## How it works [how-it-works]

You connect the MCP host to `https://mcp.elastic.co` and authorize it with OAuth 2.1. The service finds the {{serverless-short}} projects you can access and routes each call to the project. Your data stays in the project. The connection acts as you.

The {{mcp-service}} maps {{es}}, {{kib}}, and Cloud control-plane REST APIs onto the [tools](#available-tools) below.
One tool searches the API catalog so the host can find the operation it needs, read its schema, and run the call.
That keeps the conversation from filling with the full API surface, and Elastic can change an API without breaking the host.

Read, write, and destructive calls are separate so a destructive call can be confirmed. Hosts that support confirmation ask you before that call runs.

You can create and update projects through this service. You can't delete a project through it.

:::{important}
The connection can do what you can do. You can't limit it to selected projects or to read-only actions.
:::

## Available tools [available-tools]

When you talk to an agent in natural language, it picks appropriate tools based on your request.
The agent uses them to find your projects, find the Elastic API that matches your request, and run it.

`list_projects`
:   Lists the {{serverless-short}} projects you can access.

`discover_tool`
:   Searches for the Elastic API that matches a request. Each result names the API and which of `execute_read`, `execute_write`, or `execute_destructive` can run it.

`describe_tool`
:   Returns arguments and response details when the agent needs more than that result.

`describe_type`
:   Returns a type that `describe_tool` left out. The agent can skip both describe tools when it already knows the API.

`execute_read`
:   Runs a read-only API. Refuses an API that can write or delete data.

`execute_write`
:   Runs an API that reads or writes data. Refuses an API that can delete or overwrite data.

`execute_destructive`
:   Runs any API, including one that deletes or overwrites data.

## How it relates to other Elastic features [how-it-relates]

- [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md): Use this when you want {{agent-builder}} tools, including custom tools, for one project or deployment. The {{agent-builder}} MCP server is one endpoint per project. The [{{serverless-full}} connector for Claude](/explore-analyze/ai-features/claude-connector.md) uses this server.
- [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md): Use this when you want to chat in {{kib}} and build agents, tools, and skills in the product.
- [Docs MCP server](/get-started/machine-readable-docs.md): Use this when you want Elastic documentation only. It doesn't need an Elastic account and it doesn't connect to your data.
- [AI agent skills](/explore-analyze/ai-features/agent-skills.md): Use these when you want Elastic procedures in the host. Skills don't connect the host to a project. You can install them with this service, but they aren't required.
- [Elastic CLI](cli://index.md): Use this when you want a terminal instead of an MCP host, including for self-managed clusters this service doesn't cover.

## Next steps [next-steps]

- Connect a host at [`https://mcp.elastic.co`](https://mcp.elastic.co).
- If you don't have a project yet, [create an {{serverless-full}} project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md). You can also ask the connected host to create one.

## Related pages [related-pages]

- [Create an {{serverless-full}} project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md)
- [Ingest for search use cases](/solutions/search/ingest-for-search.md)
- [Elastic fundamentals](/get-started/index.md)
