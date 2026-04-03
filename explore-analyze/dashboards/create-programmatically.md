---
navigation_title: Create programmatically
description: Use the Dashboards API, the Lens Visualizations API, or AI-powered tools to create and manage Kibana dashboards and visualizations programmatically.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
---

# Create dashboards and visualizations programmatically [create-programmatically]

You can create and manage Kibana dashboards and visualizations outside of the UI, using REST APIs or AI-powered tools. This is useful for automating dashboard deployments, managing them in version control, building tooling around dashboard lifecycle management, or using AI agents to generate dashboards on demand.

## Dashboards API [dashboards-api]

```{applies_to}
stack: preview 9.4
serverless: preview
```

The Dashboards API provides full CRUD access to dashboards, including their panels, controls, sections, and display options. Use it to create dashboards from code, update them programmatically, or integrate dashboard management into your own tooling.

Refer to the [Dashboards API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-dashboards).

## Lens Visualizations API [lens-visualizations-api]

```{applies_to}
stack: preview 9.4
serverless: preview
```

The Lens Visualizations API lets you create and manage reusable Lens visualizations as saved objects. Once created, a visualization can be embedded in a dashboard by reference. Use it to build a library of reusable charts and metrics that can be shared across multiple dashboards.

Refer to the [Lens Visualizations API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-lens).

## Kibana dashboards agent skill [dashboards-agent-skill]

The Kibana dashboards agent skill enables AI agents and LLM-powered tools to create and manage dashboards through natural language instructions. It is designed for agentic workflows where a language model generates dashboard definitions and applies them automatically.

Refer to the [kibana-dashboards agent skill](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-dashboards) on GitHub.

## Agent Builder dashboard tools [agent-builder-dashboard-tools]

```{applies_to}
stack: preview 9.4
serverless: preview
```

Elastic's built-in AI assistant includes dashboard tools that let you create and update dashboards through a chat interface, without leaving the Kibana UI. Describe what you want to build, and the assistant generates the dashboard for you.

Refer to [Agent Builder](../ai-features/elastic-agent-builder.md) for an overview of the available built-in tools.
