---
navigation_title: "Programmatic access"
applies_to:
  stack: preview 9.2
  deployment: 
    self: unavailable
  serverless:
    elasticsearch: preview
---

# Work programmatically with {{agent-builder}}

{{agent-builder}} provides comprehensive APIs and additional integration options for programmatic access and automation.

- **APIs**: RESTful APIs for creating, managing, and executing tools programmatically
- **MCP server**: A standardized interface at `/api/chat/mcp` that allows external MCP clients (such as Claude Desktop) to access {{agent-builder}} tools
- **A2A server**: Agent-to-agent communication endpoints that follow the A2A protocol specification, enabling external A2A clients to interact with {{agent-builder}} agents

These interfaces enable you to build integrations with other applications and extend {{agent-builder}}'s capabilities to fit your specific requirements.

## Working with the API

The Chat API allows you to programmatically create and manage tools. You can use this API to:
- Create new tools
- Update existing tool configurations
- Delete tools when they're no longer needed
- List available tools

Here's an example API call to create a new custom {{esql}} tool:

```console
POST kbn://api/chat/tools
{
  "id": "recent_orders",
  "description": "Find recent orders for a customer",
  "configuration": {
    "query": "FROM orders | WHERE customer_id == ?customer_id | SORT @timestamp DESC | LIMIT 5",
    "params": {
      "customer_id": {
        "type": "keyword",
        "description": "Customer identifier"
      }
    }
  },
  "type": "esql",
  "tags": ["orders", "customers"]
}
```

## MCP server

The [**Model Context Protocol (MCP) server**](https://modelcontextprotocol.io/docs/getting-started/intro) server provides a standardized interface for external clients to access {{agent-builder}} tools.

### MCP server endpoint

The MCP server is available at:

```
/api/chat/mcp
```

### Configuring Claude Desktop for MCP integration

To use Claude Desktop with your Elastic instance:

```json
{
  "mcpServers": {
    "elastic": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://your-kibana-url/api/chat/mcp",
        "--header",
        "Authorization:${AUTH_HEADER}"
      ],
      "env": {
        "AUTH_HEADER": "ApiKey your-api-key-here"
      }
    }
  }
}
```

## Agent-to-Agent (A2A) server 

The [**Agent-to-Agent (A2A)server**](https://github.com/a2aproject/A2A) enables external A2A clients to communicate with {{agent-builder}} agents.

### Agentcards endpoint

Get metadata about available agents:

```
GET /api/chat/a2a/{agentId}.json
```

### A2A protocol endpoint

Interact with agents following the A2A protocol specification:

```
POST /api/chat/a2a/{agentId}
```