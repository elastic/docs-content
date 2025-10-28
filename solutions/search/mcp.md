---
navigation_title: MCP servers
applies_to:
  stack:
  serverless:
---

# Model Context Protocol (MCP) servers

Elastic offers two MCP server options for connecting agents to your {{es}} data. The Agent Builder MCP server is the recommended approach for {{es}} 9.2+ and Serverless deployments, offering full access to built-in and custom tools. For older {{es}} versions without Agent Builder, the `mcp-elasticsearch` server provides basic connectivity with simpler tooling.

## {{agent-builder}} MCP server
```{applies_to}
stack: preview 9.2
serverless: preview
```
Elastic 9.2.0+ and Serverless deployments provide an [Agent Builder MCP server endpoint](https://www.elastic.co/docs/solutions/search/agent-builder/mcp-server) that exposes all built-in and custom [tools](https://www.elastic.co/docs/solutions/search/agent-builder/tools) you can use to power agentic workflows.

## {{es}} MCP server

For users running older versions of Elasticsearch without Agent Builder, [elastic/mcp-server-elasticsearch](https://github.com/elastic/mcp-server-elasticsearch?tab=readme-ov-file#elasticsearch-mcp-server) provides basic MCP connectivity. This server enables connecting agents to your {{es}} data and allows you to interact with your {{es}} indices through natural language conversations, though with a more limited feature set compared to the Agent Builder MCP server.
