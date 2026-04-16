---
navigation_title: Create programmatically
description: Compare the Dashboards API, Visualizations API, and AI-powered tools to create and manage Kibana dashboards and visualizations programmatically.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
---

# Create dashboards and visualizations programmatically [create-programmatically]

In addition to the {{product.kibana}} UI, you can create and manage dashboards and visualizations using REST APIs or AI-powered tools. This is useful when you need to automate dashboard deployments, manage them in version control, build tooling around the dashboard lifecycle, or produce dashboards from natural language instructions.

## Choose your approach [choose-your-approach]

The right option depends on what you are building and how you prefer to work:

| Approach | Best for | Output |
|---|---|---|
| [Dashboards API](#dashboards-api) | Scripted deployments, GitOps, CI/CD automation | Saved dashboard object |
| [Visualizations API](#lens-visualizations-api) | Reusable visualization libraries shared across dashboards | Saved visualization object |
| [{{agent-builder}} chat](#agent-builder-dashboard-tools) | Conversational dashboard creation without writing API requests | In-memory dashboard (save when ready) |
| [Kibana dashboards agent skill](#dashboards-agent-skill) | Building AI applications that create dashboards programmatically | Depends on implementation |

## Dashboards API [dashboards-api]

```{applies_to}
stack: preview 9.4
serverless: preview
```

The Dashboards API provides full CRUD access to dashboards, including their panels, controls, sections, and display options. Panels are defined inline in the request body as JSON, so you can store dashboard definitions in version control and deploy them through automated pipelines.

Use the Dashboards API when you need to:

- Deploy dashboards across environments (staging, production) from a CI/CD pipeline
- Manage dashboard definitions as code and track changes in version control
- Automate dashboard creation or updates as part of your own tooling or integrations
- Create dashboards that include [ES|QL](/explore-analyze/query-your-data-with-esql.md)-powered visualizations inline. This is the only programmatic path for ES|QL charts.

The API supports all panel types that have a defined schema, including visualizations, Discover sessions, markdown panels, and filter controls. Panels that lack a schema, such as Maps and Links, return an error on write.

Refer to the [Dashboards API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-dashboards) for the full request schema, panel types, and authentication requirements.

## Visualizations API [lens-visualizations-api]

```{applies_to}
stack: preview 9.4
serverless: preview
```

The Visualizations API lets you create and manage visualizations as standalone saved objects in the Kibana Visualizations library. A saved visualization can then be embedded in one or more dashboards by referencing its ID, rather than repeating the visualization definition in each dashboard.

Use the Visualizations API when you need to:

- Build a library of reusable charts and metrics that appear in multiple dashboards
- Update a visualization once and have the change propagate to every dashboard that references it
- Separate visualization management from dashboard management in your automation or tooling

To embed a saved visualization in a dashboard, create a `vis` panel in the Dashboards API with the saved object ID in `config.ref_id`.

Refer to the [Visualizations API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-lens).

## {{agent-builder}} chat [agent-builder-dashboard-tools]

```{applies_to}
stack: preview 9.4
serverless: preview
```

{{agent-builder}} agents can create and update dashboards through natural language chat in the {{product.kibana}} UI. Describe what you want to visualize and the agent generates a dashboard with [{{esql}}](/explore-analyze/query-your-data-with-esql.md)-powered visualizations. Dashboards are in-memory by default. They exist only as conversation attachments and are not saved until you save them, so you can iterate freely before committing.

Use {{agent-builder}} when you want to:

- Create a working dashboard quickly without writing API requests or learning the schema
- Explore an unfamiliar data source by asking the agent to surface and visualize key fields
- Prototype a dashboard layout through conversation and refine it before building a more permanent version
- Get started with dashboards without prior experience with the {{product.kibana}} editor

{{agent-builder}} creates ES|QL-powered visualizations, markdown panels, and collapsible sections. If you need DSL-based visualizations or panel types not supported by the agent, use the Dashboards API directly.

:::{tip}
Full-screen standalone chat mode provides the best experience for working with dashboards. The larger canvas area makes it easier to preview and interact with the generated content.
:::

Refer to [Chat with {{agent-builder}} agents](/explore-analyze/ai-features/agent-builder/chat.md).

## Kibana dashboards agent skill [dashboards-agent-skill]

The [kibana-dashboards agent skill](https://github.com/elastic/agent-skills/tree/main/skills/kibana/kibana-dashboards) is an open-source skill for developers building AI agents and LLM-powered applications. It provides language models with the context and instructions required to generate valid dashboard definitions and interact with the Dashboards API on behalf of a user.

Use the agent skill when you are:

- Building a custom AI application or chatbot that creates {{product.kibana}} dashboards as part of a larger workflow
- Integrating dashboard generation into an agentic pipeline outside of the {{product.kibana}} UI
- Extending or customizing how an LLM interacts with the Dashboards API beyond the built-in capabilities of {{agent-builder}}

The {{agent-builder}} built-in tools use a similar mechanism internally. The agent skill is for developers who need the same capability in their own tooling.
