---
navigation_title: Create programmatically
description: Use the Dashboards API and Visualizations API to create and manage Kibana dashboards and visualizations from code, CI/CD pipelines, or custom tooling.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: kibana
type: overview
---

# Create dashboards programmatically [create-dashboards-programmatically]

The Dashboards API and Visualizations API let you create and manage dashboards and visualizations outside the {{product.kibana}} UI. Use them to automate deployments, manage dashboards and visualizations as code, or integrate dashboard creation into your own tooling.

| API | When to use this | What you get |
|---|---|---|
| [Dashboards API](#dashboards-api) | Managing dashboards as code: scripted deployments, CI/CD, version control | Saved dashboard |
| [Visualizations API](#lens-visualizations-api) | Building a reusable chart library to embed by reference across multiple dashboards | Saved visualization |

::::{tip}
If you want to create dashboards from natural language without writing API requests, refer to [Create dashboards using AI](create-dashboards-using-ai.md) instead.
::::

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

Refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/#tag/Dashboards) for the full request schema, panel types, and authentication requirements.

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

Refer to the [Visualizations API reference](https://elastic.github.io/dashboards-api-spec/#tag/Visualizations).
