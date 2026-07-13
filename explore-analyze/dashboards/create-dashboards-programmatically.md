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

The Dashboards API and Visualizations API let you create and manage dashboards and visualizations outside the {{product.kibana}} UI. Use them to automate deployments, manage dashboards and visualizations as code, or integrate dashboard creation into your own tooling. To use these APIs in a Git-based workflow that version-controls dashboards and deploys them across environments, refer to [Manage dashboards as code](manage-dashboards-as-code.md).

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

The API supports any panel type that has a defined schema:

- Visualizations
- Discover sessions
- Markdown
- Image
- Controls: options list, range slider, time slider, and {{esql}}
- SLO panels: overview, alerts, error budget, and burn rate
- Synthetics panels: stats overview and monitors
- {applies_to}`stack: ga 9.5` Links
- {applies_to}`stack: ga 9.5` APM service map
- {applies_to}`stack: ga 9.5` Machine learning panels: single metric viewer, anomaly swim lane, and anomaly charts
- {applies_to}`stack: ga 9.5` Log rate analysis, change point detection, and pattern analysis panels

Panel types without a defined schema, such as Maps, aren't supported yet and return an error on write.

Dashboard requests are subject to [panel limits](arrange-panels.md#dashboard-panel-limits): up to 1,000 top-level items (panels and sections combined), 1,000 panels per section, and 100 pinned controls. The total number of panels, sections, and pinned controls across the dashboard also can't exceed 1,000. Requests that exceed these limits are rejected with a validation error.

Refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards) for the full request schema, panel types, and authentication requirements. For panel sizing and layout guidance when specifying grid coordinates by hand, refer to [Organize dashboard panels](arrange-panels.md#dashboard-grid-layout).

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

Refer to the [Visualizations API reference](https://elastic.github.io/dashboards-api-spec/visualizations#tag/Visualizations).
