---
navigation_title: Act on data
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-act-on-data.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-act-on-data.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Act on application data

In addition to exploring visualizations in the Applications UI in {{kib}}, you can make your application data more actionable with:

|     |     |
| --- | --- |
| [Rules and alerts](/solutions/observability/apm/create-apm-rules-alerts.md) | The Applications UI allows you to define rules to detect complex  conditions within your APM data and trigger built-in actions when those conditions are met. |
| [Custom links](/solutions/observability/apm/create-custom-links.md) | Build URLs that contain relevant metadata from a specific trace.  For example, you can create a link that will take you to a page where you can open a new GitHub issue  with context already auto-populated in the issue body.  These links will be shown in the *Actions* context menu in selected areas of the Applications UI (for example, by transaction details). |