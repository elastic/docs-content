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
---

# Cases [cases]

Cases are a collaboration and tracking tool, which is particularly useful for incidents or issues that arise from alerts. You can group related alerts into a case for easier management, add notes and comments to provide context, track investigation progress, and assign cases to team members or link them to external systems. Cases ensure that teams have a central place to track and resolve alerts efficiently.

## External incident management systems [cases-external-systems]

You can send cases to these external incident management systems by configuring connectors:

* {{ibm-r}}
* {{jira}} (including Jira Service Desk)
* {{sn-itsm}}
* {{sn-sir}}
* {{swimlane}}
* {{hive}}
* {{webhook-cm}}
:::

For details on configuring connectors, refer to [Configure case settings](cases/manage-cases-settings.md).

## Get started with cases [cases-get-started]

* [Configure access to cases](cases/configure-case-access.md)
* [Open and manage cases](cases/manage-cases.md)
* [Configure case settings](cases/manage-cases-settings.md)
* {applies_to}`stack: preview 9.2` {applies_to}`serverless: unavailable` [Use cases as data](cases/cases-as-data.md)

For information on Security-specific case features like Timeline integration, events, indicators, and export/import, refer to [Security case features](/solutions/security/investigate/security-cases-features.md).

## Limitations [cases-limitations]

Cases created in one solution are not visible in other solutions:

* Cases created in **{{stack-manage-app}}** are not visible in {{observability}} or {{elastic-sec}}
* Cases created in **{{observability}}** are not visible in {{stack-manage-app}} or {{elastic-sec}}
* Cases created in **{{elastic-sec}}** are not visible in {{stack-manage-app}} or {{observability}}

You cannot attach alerts from one solution to cases in another solution.