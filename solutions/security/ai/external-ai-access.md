---
navigation_title: External AI access
description: Work with Elastic Security data from AI tools outside Kibana, such as Claude, Cursor, and Visual Studio Code, using the Model Context Protocol.
applies_to:
  stack: preview 9.4
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# External AI access to {{elastic-sec}} [external-ai-access]

You can work with {{elastic-sec}} from AI tools that run outside {{kib}}, such as Claude, Cursor, and Visual Studio Code. These tools connect to {{elastic-sec}} through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), so you can triage alerts, hunt threats, and manage cases without leaving your AI conversation.

| Tool | What it does |
|---|---|
| [Elastic Security MCP App](/solutions/security/mcp-app/elastic-security-mcp-app.md) | Brings interactive {{elastic-sec}} dashboards into Claude, Cursor, Visual Studio Code, and other MCP hosts. Each action writes back to {{es}} and {{kib}} through the same APIs the product uses. |

For AI features that run inside {{elastic-sec}}, refer to [Built-in AI](/solutions/security/ai/built-in-ai.md).
