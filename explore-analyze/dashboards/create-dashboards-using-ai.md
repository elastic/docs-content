---
navigation_title: Create using AI
description: Use Agent Builder or the Kibana dashboards agent skill to create dashboards from natural language, without writing API requests or learning the dashboard schema.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: kibana
type: overview
---

# Create dashboards using AI [create-dashboards-using-ai]

AI-powered tools let you create dashboards from natural language, without writing API requests or learning the dashboard schema. Use them to go from a question to a working dashboard through conversation, or to integrate dashboard generation into your own AI workflows.

| Tool | When to use this | What you get |
|---|---|---|
| [{{agent-builder}}](#agent-builder-dashboard-tools) | Creating dashboards through conversation in {{product.kibana}} or using the MCP server | Dashboard through chat that you save when ready |
| [{{product.kibana}} dashboards agent skill](#dashboards-agent-skill) | Building your own AI agent or LLM tool that generates dashboards | Saved dashboard (using the API) |

::::{tip}
If you need to create dashboards from code or CI/CD pipelines using REST APIs, refer to [Create dashboards programmatically](create-dashboards-programmatically.md) instead.
::::

## {{agent-builder}} [agent-builder-dashboard-tools]
```{applies_to}
stack: preview 9.4+
serverless: preview
```

{{agent-builder}} agents can create and update dashboards through natural language [chat](/explore-analyze/ai-features/agent-builder/chat.md), using the chat UI in {{product.kibana}}, the [Chat API](/explore-analyze/ai-features/agent-builder/kibana-api.md), or the [MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md). Describe what you want to visualize and the agent builds a dashboard with [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md)-powered visualizations. Dashboards are in-memory by default and exist as conversation attachments until you save them, so you can iterate freely before finalizing.

Use {{agent-builder}} when you want to:

- Go from a question to a working dashboard without writing API requests or learning the schema
- Explore an unfamiliar data source by asking the agent to surface and visualize key fields
- Prototype a dashboard through conversation, then save it when you are satisfied

{{agent-builder}} generates ES|QL-powered visualizations, Vega-Lite visualizations, markdown panels, collapsible sections, and interactive [filter controls](/explore-analyze/visualize/add-controls.md).

Refer to [Chat with {{agent-builder}} agents](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md).

## {{product.kibana}} dashboards agent skill [dashboards-agent-skill]
```{applies_to}
stack: preview 9.4+
serverless: preview
```

The [kibana-dashboards agent skill](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-dashboards) is an open-source skill for integrating dashboard generation into your own AI tools. It provides language models with the context and instructions to generate valid dashboard definitions and call the Dashboards API, so you can build custom interfaces, automation scripts, or agentic pipelines that create {{product.kibana}} dashboards without relying on the built-in {{agent-builder}} experience.

Use the agent skill when you are:

- Building a custom AI application that creates dashboards as part of a larger workflow
- Integrating dashboard generation into an agentic pipeline outside the {{product.kibana}} UI
- Extending how an LLM interacts with the Dashboards API beyond the built-in capabilities of {{agent-builder}}

The {{agent-builder}} built-in tools use a similar mechanism internally. The agent skill is for teams who need the same capability in their own tooling.

Pair it with the [elasticsearch-esql skill](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-esql) to give the agent the ability to discover available indices and fields before generating ES|QL queries for dashboard panels.
