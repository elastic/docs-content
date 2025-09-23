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
{applies_to}`stack: ga 9.1` With the appropriate index access, you can [build visualizations and metrics](../../../explore-analyze/alerts-cases/cases/visualize-case-data.md) of data in {{observability}}, {{stack-manage-app}}, and {{elastic-sec}} cases. This can provide improved visibility into patterns and trends of cases within your space.
::::

## Limitations [security-case-limitations]

* If you create cases in the {{security-app}}, they are not visible from {{observability}} or {{stack-manage-app}}. Likewise, the cases you create in {{stack-manage-app}} are not visible in {{elastic-sec}} or {{observability}}.
* You cannot attach alerts from the {{observability}} or {{stack-manage-app}} to cases in {{elastic-sec}}.






