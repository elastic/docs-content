---
description: Use the Dashboards API, the Lens Visualizations API, or AI-powered tools to create and manage Kibana dashboards and visualizations programmatically.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
navigation_title: "Create programmatically"
---

# Create dashboards and visualizations programmatically [create-programmatically]

You can create and manage {{product.kibana}} dashboards and visualizations outside the UI using APIs or AI-powered tools. This is useful for automation workflows, GitOps pipelines, version-controlled dashboard definitions, and LLM-assisted generation.

## Dashboards API [programmatic-dashboards-api]

{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview`

The Dashboards API lets you create, retrieve, update, and delete dashboards programmatically using standard HTTP requests. Use it to build dashboards from code, integrate dashboard management into CI/CD pipelines, or generate dashboards from templates.

Refer to the [Dashboards API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-dashboards) for the full schema and available endpoints.

## Lens Visualizations API [programmatic-lens-api]

{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview`

The Lens Visualizations API lets you create and manage reusable Lens visualizations independently of any dashboard. Use it to build a library of visualizations that can be shared across dashboards or updated centrally.

Refer to the [Lens Visualizations API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-lens) for the full schema and available endpoints.

## Agent skill for dashboards [programmatic-agent-skill]

The kibana-dashboards agent skill enables LLM-driven workflows that create and manage dashboards through natural language. It exposes the Dashboards API as a callable skill for AI agents, making it straightforward to integrate dashboard automation into larger AI-powered pipelines.

Refer to the [kibana-dashboards agent skill](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-dashboards) on GitHub for setup instructions and usage examples.

## Agent Builder dashboard tools [programmatic-agent-builder-tools]

{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview`

The Agent Builder includes built-in dashboard tools (`dashboard.create_dashboard` and `dashboard.update_dashboard`) that let you create and update dashboards through Elastic's AI assistant without leaving the chat interface. These tools are in tech preview and are tracked at [elastic/kibana#237795](https://github.com/elastic/kibana/issues/237795).
