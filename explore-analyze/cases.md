---
navigation_title: Cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/cases.html
  - https://www.elastic.co/guide/en/security/current/cases-overview.html
  - https://www.elastic.co/guide/en/observability/current/create-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-overview.html
  - https://www.elastic.co/guide/en/serverless/current/observability-cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Track incidents, document findings, and coordinate response efforts with cases in Elastic Security, Observability, or Stack Management.
---

# Cases [cases]

Cases provide a central place to track incidents, document findings, and coordinate response efforts. Whether you're a security analyst triaging threats, a site reliability engineer responding to outages, or a platform engineer monitoring your Elastic Stack, cases bring together alerts, evidence, and team communication in one place.

You can create cases in {{elastic-sec}}, {{observability}}, or {{stack-manage-app}} depending on your workflow. Attach alerts and files, add comments and context, assign team members, and push updates to external systems like Jira or ServiceNow.

## Get started [cases-get-started]

Start by [creating your first case](cases/create-cases.md), then [configure case settings](cases/configure-case-settings.md) to add external connectors, custom fields, and templates. Once you have cases, you can [add alerts, files, and visualizations](cases/manage-cases.md) to document your investigation, and [share cases](cases/search-share-cases.md) with external systems. 

:::{note}
If you're using {{elastic-sec}}, explore [Security case features](/solutions/security/investigate/security-cases.md#security-cases-features) for additional capabilities like adding events and Timelines to cases.
:::