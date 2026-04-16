---
navigation_title: Create programmatically
description: Compare the Dashboards API, Visualizations API, and AI-powered tools to create and manage Kibana dashboards and visualizations programmatically.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: kibana
type: overview
---

# Create dashboards and visualizations programmatically [create-dashboards-programmatically]

REST APIs and AI-powered tools give you several ways to create and manage dashboards and visualizations outside the {{product.kibana}} UI. Use them to automate deployments, manage dashboards as code, or generate them through natural language.

## Choose your approach [choose-your-approach]

| Approach | When to choose this | What you get |
|---|---|---|
| [Dashboards API](#dashboards-api) | Managing dashboards as code: scripted deployments, CI/CD, version control | Saved dashboard |
| [Visualizations API](#lens-visualizations-api) | Building a reusable chart library you can embed by reference in multiple dashboards | Saved visualization |
| [{{agent-builder}}](#agent-builder-dashboard-tools) | Creating dashboards from natural language, in {{product.kibana}} or using the Agent Builder MCP server | Dashboard through chat that you can save when ready |
| [{{product.kibana}} dashboards agent skill](#dashboards-agent-skill) | Building your own AI agent or LLM tool that generates dashboards | Saved dashboard (using the API) |

## Dashboards API [dashboards-api]
```{applies_to}
stack: preview 9.4+
serverless: preview
```

The Dashboards API gives you full read and write access to dashboards, including their panels, controls, sections, and display options. You define panels inline as JSON, so you can store dashboard definitions in version control and deploy them through automated pipelines.

Use the Dashboards API when you need to:

- Deploy dashboards across environments from a CI/CD pipeline
- Track dashboard definitions in version control alongside your other infrastructure code
- Automate dashboard creation or updates as part of your own tooling
- Create dashboards with [ES|QL](/explore-analyze/query-filter/languages/esql-kibana.md)-powered visualizations. This is the only programmatic path for ES|QL charts.

The API supports all panel types that have a defined schema, including visualizations, Discover sessions, markdown panels, and filter controls. Panel types without a schema, such as Maps and Links, are not supported yet and return an error on write.

Refer to the [Dashboards API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-dashboards) for the full request schema, panel types, and authentication requirements.

## Visualizations API [lens-visualizations-api]
```{applies_to}
stack: preview 9.4+
serverless: preview
```

The Visualizations API lets you create and manage visualizations as standalone saved objects in the {{product.kibana}} Visualizations library. Embed them in dashboards by referencing their ID, so a single update propagates to every dashboard that uses them.

Use the Visualizations API when you need to:

- Maintain a library of reusable charts and metrics across multiple dashboards
- Update a visualization once and have the change reflected everywhere it appears
- Manage visualization definitions independently from dashboard definitions in your automation or tooling

To embed a saved visualization in a dashboard, add a `vis` panel to your Dashboards API request with `config.ref_id` set to the visualization's ID.

Refer to the [Visualizations API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-lens).

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

{{agent-builder}} generates ES|QL-powered visualizations, markdown panels, and collapsible sections. For  panel types that the agent does not support yet such as controls, use the Dashboards API directly.


Refer to [Chat with {{agent-builder}} agents](/explore-analyze/ai-features/agent-builder/chat.md).

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
