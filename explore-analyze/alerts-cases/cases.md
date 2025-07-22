---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/cases.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Cases [cases]

Cases are used to open and track issues directly in {{kib}}. You can add assignees and tags to your cases, set their severity and status, and add alerts, comments, and visualizations. You can create cases automatically when alerts occur or send cases to external incident management systems by configuring connectors.

You can also optionally add custom fields and case templates. [preview]

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


::::{note} 
{applies_to}`stack: ga 9.1` With the appropriate index access, you can [build visualizations and metrics](../../explore-analyze/alerts-cases/cases/visualize-case-data.md) of data in {{observability}}, {{stack-manage-app}}, and {{elastic-sec}} cases. This can provide improved visibility into patterns and trends of cases within your space.
::::

## Limitations [kibana-case-limitations]

* If you create cases in {{stack-manage-app}}, they are not visible from {{observability}} or the {{security-app}}. Likewise, the cases you create in {{observability}}, they are not visible in {{stack-manage-app}} or {{elastic-sec}}. 
* You cannot attach alerts from {{observability}} or {{elastic-sec}} to cases in {{stack-manage-app}}.
