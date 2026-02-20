---
navigation_title: "Programmatic access"
description: "Learn how to integrate with Agent Builder using the MCP server, A2A protocol, or Kibana REST APIs. Extend AI capabilities to external clients like Claude and Cursor."
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

# Programmatic access to {{agent-builder}}

{{agent-builder}} provides comprehensive integration options for programmatic access and automation.

These interfaces enable you to build integrations with other applications and extend Agent Builder's capabilities to fit your specific requirements.

:::{tip}
Most users will probably want to integrate with Agent Builder using MCP or A2A, but you can also work programmatically with tools, agents, and conversations using the Kibana APIs.
:::

- **[MCP server](mcp-server.md)**: A standardized interface that allows external MCP clients (such as Claude Desktop or Cursor) to access {{agent-builder}} tools.
- **[A2A server](a2a-server.md)**: Agent-to-agent communication endpoints that follow the A2A protocol specification, enabling external A2A clients to interact with {{agent-builder}} agents.
- **[Kibana API](kibana-api.md)**: RESTful APIs for working with {{agent-builder}} programmatically.

