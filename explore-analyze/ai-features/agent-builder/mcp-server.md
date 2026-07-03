---
navigation_title: "MCP server"
description: "Learn how to connect Claude Desktop, Cursor, and VS Code to Elastic Agent Builder tools using the Model Context Protocol (MCP) server."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} MCP server

The [**Model Context Protocol (MCP) server**](https://modelcontextprotocol.io/docs/getting-started/intro) provides a standardized interface for external MCP hosts to access {{agent-builder}} tools.

## MCP server endpoint [mcp-server-endpoint]

The MCP server is available at the following endpoint:

```
{KIBANA_URL}/api/agent_builder/mcp
```

When using a custom {{kib}} Space, include the space name in the endpoint path:

```
{KIBANA_URL}/s/{SPACE_NAME}/api/agent_builder/mcp
```

:::{tip}
You can copy your MCP server URL directly in the Tools GUI. Refer to [MCP server access in the Tools GUI](tools.md#mcp-server-access).
:::

## Authentication [mcp-server-authentication]

External MCP hosts need credentials to reach the MCP server endpoint. Choose API keys or OAuth based on your deployment type and use case.

Use one of the following authentication paths:

- [API key authentication](mcp-server-api-keys.md)
- [OAuth authentication](/deploy-manage/app-connections/oauth-clients.md) using an [application connection](/deploy-manage/app-connections.md) {applies_to}`serverless: preview`

The following table compares the two paths.

<!-- TODO: confirm tool scope for tech preview. PRD said "read-only, ES|QL-based tools only", but QA testing (June 23 2026) shows 22 tools including write operations (delete_stream, create_partition, update_stream, cases, etc.). Remove or correct this row once confirmed with Jake Landis / Elena Shostak. -->

| Consideration | API key | OAuth |
| --- | --- | --- |
| Supported platforms | {{stack}} deployments and {{serverless-short}} projects | {{serverless-short}} projects only (technical preview) |
| Best for | Automation, unattended access, and shared machine-to-machine use | Interactive MCP hosts acting on behalf of a person (Claude Desktop, Cursor) |
| Identity | The key's snapshotted permissions | The consenting user; permissions are the user's live permissions in the project |
| Credential lifetime | Long-lived until the key expires or is revoked | Short-lived tokens, refreshed automatically |
| Setup | Generate a key and add it to the host configuration | Register an MCP client, then consent in the browser |
| {{agent-builder}} tools through MCP | Full tool catalog, including [Elastic Workflows](/explore-analyze/workflows.md) | Read-only, {{esql}}-based tools |

## Related pages

See also:

- [](mcp-in-agent-builder.md)
- [](programmatic-access.md)
- [](/deploy-manage/app-connections.md)
