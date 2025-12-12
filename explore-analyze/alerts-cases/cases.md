---
navigation_title: Cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Overview of case management for tracking and collaborating on incidents and issues.
---

# Cases in {{kib}} [cases]

**Cases** provide a centralized workspace for tracking and collaborating on incidents and issues directly in {{kib}}. You can create cases manually or automatically from alerts, add assignees and tags, set severity and status, and attach alerts, comments, and visualizations. Cases integrate with external incident management systems through connectors, enabling seamless workflows for investigation and resolution.

{applies_to}`stack: preview` {applies_to}`serverless: preview` You can also optionally add custom fields and case templates.

{applies_to}`stack: ga 9.2` Cases are automatically assigned human-readable numeric IDs, which you can use for easier referencing. Each time you create a new case in your [space](docs-content://deploy-manage/manage-spaces.md), the case ID increments by one. IDs are assigned to cases by a background task that runs every 10 minutes, which can cause a delay in ID assignment, especially in spaces with many cases. You can find the case ID after the case's name and can use it while searching the Cases table.

:::{image} /explore-analyze/images/kibana-cases-list.png
:alt: Cases page
:screenshot:
:::

::::{note}
If you create cases in the {{observability}} or {{security-app}}, they are not visible in **{{stack-manage-app}}**. Likewise, the cases you create in **{{stack-manage-app}}** are not visible in the {{observability}} or {{security-app}}. You also cannot attach alerts from the {{observability}} or {{security-app}} to cases in **{{stack-manage-app}}**.
::::

* [Configure access to cases](cases/setup-cases.md)
* [Open and manage cases](cases/manage-cases.md)
* [Configure case settings](cases/manage-cases-settings.md)
* {applies_to}`stack: preview 9.2` {applies_to}`serverless: unavailable`[Use cases as data](cases/cases-as-data.md)

## Limitations [kibana-case-limitations]

* If you create cases in {{stack-manage-app}}, they are not visible from {{observability}} or the {{security-app}}. Likewise, the cases you create in {{observability}} are not visible in {{stack-manage-app}} or {{elastic-sec}}. 
* You cannot attach alerts from {{observability}} or {{elastic-sec}} to cases in {{stack-manage-app}}.
