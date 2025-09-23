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

::::{note}
From {{elastic-sec}} in the {{stack}}, you cannot access cases created in {{observability}} or Stack Management.
::::





