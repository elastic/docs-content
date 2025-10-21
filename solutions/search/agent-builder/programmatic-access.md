---
navigation_title: "Programmatic access"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Work programmatically with {{agent-builder}}

{{agent-builder}} provides comprehensive integration options for programmatic access and automation.

These interfaces enable you to build integrations with other applications and extend Agent Builder's capabilities to fit your specific requirements.

:::{tip}
Most users will probably want to integrate with Agent Builder using MCP or A2A, but you can also work programmatically with tools, agents, and conversations using the Kibana APIs.
:::

- **[MCP server](mcp-server.md)**: A standardized interface that allows external MCP clients (such as Claude Desktop or Cursor) to access {{agent-builder}} tools.
- **[A2A server](a2a-server.md)**: Agent-to-agent communication endpoints that follow the A2A protocol specification, enabling external A2A clients to interact with {{agent-builder}} agents.
- **[Kibana API](kibana-api.md)**: RESTful APIs for working with {{agent-builder}} programmatically.

