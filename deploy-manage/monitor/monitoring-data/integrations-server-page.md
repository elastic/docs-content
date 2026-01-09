---
applies_to:
  deployment:
    ess: all
    ece: all
    eck: unavailable
    self: all
products:
  - id: kibana
---


# {{integrations-server}} metrics [integrations-server-page]


To view the key metrics that indicate the overall health of {{integrations-server}} itself, click **Overview** in the {{integrations-server}} section of the **Stack Monitoring** page. 

The **APM server overview** page opens, showing both resource usage for {{integrations-server}} and various metrics for {{apm-server}}.

:::{image} /deploy-manage/images/kibana-monitoring-integrations-server-overview.png
:alt: {{integrations-server}} Overview
:screenshot:
:::

1. To view {{integrations-server}} instance metrics, click **Integrations Servers**.

    The Instances section shows the status of each {{integrations-server}} instance, which includes both resource usage for {{integrations-server}} and metrics data for {{apm-server}}.

2. Click the name of an instance to view its instance statistics over time.
