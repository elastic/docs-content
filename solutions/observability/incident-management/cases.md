---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/create-cases.html
  - https://www.elastic.co/guide/en/serverless/current/observability-cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
navigation_title: Cases
---

# Cases for Elastic {{observability}} [observability-cases]

Collect and share information about observability issues by creating a case. Cases allow you to track key investigation details, add assignees and tags to your cases, set their severity and status, and add alerts, comments, and visualizations. You can also send cases to third-party systems by [configuring external connectors](/solutions/observability/incident-management/configure-case-settings.md).

{applies_to}`stack: ga 9.2` Cases are automatically assigned human-readable numeric IDs, which you can use for easier referencing. Each time you create a new case in your [space](docs-content://deploy-manage/manage-spaces.md), the case ID increments by one. IDs are assigned to cases by a background task that runs every 10 minutes, which can cause a delay in ID assignment, especially in spaces with many cases. You can find the case ID after the case's name and can use it while searching the Cases table.

:::{image} /solutions/images/observability-cases.png
:alt: Cases page
:screenshot:
:::

::::{tip}
:applies_to: {stack: preview 9.2, serverless: unavailable}
After creating cases, use case data to build dashboards and visualizations that provide insights into case trends and operational metrics. Refer to [Use cases as data](/explore-analyze/alerts-cases/cases/cases-as-data.md) to learn more.
::::

## Limitations [observability-case-limitations]

* If you create cases in {{observability}}, they are not visible from the {{security-app}} or {{stack-manage-app}}. Likewise, the cases you create in {{stack-manage-app}} are not visible in the {{observability}} or {{elastic-sec}}.
* You cannot attach alerts from {{elastic-sec}} or {{stack-manage-app}} to cases in {{observability}}.