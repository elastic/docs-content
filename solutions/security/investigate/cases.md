---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-overview.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
navigation_title: Cases
---

# Cases for {{elastic-sec}} [security-cases-overview]

Collect and share information about security issues by opening a case in {{elastic-sec}}. Cases allow you to track key investigation details, collect alerts in a central location, and more. The {{elastic-sec}} UI provides several ways to create and manage cases. Alternatively, you can use the [cases API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-cases) to perform the same tasks.

{applies_to}`stack: ga 9.2` Cases are automatically assigned human-readable numeric IDs, which you can use for easier referencing. Each time you create a new case in your [space](docs-content://deploy-manage/manage-spaces.md), the case ID increments by one. IDs are assigned to cases by a background task that runs every 10 minutes, which can cause a delay in ID assignment, especially in spaces with many cases. You can find the case ID after the case's name and can use it while searching the Cases table.

You can also send cases to these external systems by [configuring external connectors](/solutions/security/investigate/configure-case-settings.md#cases-ui-integrations):

* {{sn-itsm}}
* {{sn-sir}}
* {{jira}} (including Jira Service Desk)
* {{ibm-r}}
* {{swimlane}}
* {{webhook-cm}}

:::{image} /solutions/images/security-cases-home-page.png
:alt: Case UI Home
:screenshot:
:::

::::{tip}
:applies_to: {stack: preview 9.2, serverless: unavailable}
After creating cases, use case data to build dashboards and visualizations that provide insights into case trends and operational metrics. Refer to [Cases as data](/explore-analyze/alerts-cases/cases/cases-as-data.md) to learn more.
::::


## Limitations [security-case-limitations]

* If you create cases in the {{security-app}}, they are not visible from {{observability}} or {{stack-manage-app}}. Likewise, the cases you create in {{stack-manage-app}} are not visible in {{elastic-sec}} or {{observability}}.
* You cannot attach alerts from the {{observability}} or {{stack-manage-app}} to cases in {{elastic-sec}}.






