---
navigation_title: Cases
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Cases in {{kib}} [cases]

Cases are used to open and track issues directly in {{kib}}. You can add assignees and tags to your cases, set their severity and status, and add alerts, comments, and visualizations. You can create cases automatically when alerts occur or send cases to external incident management systems by configuring connectors.

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
