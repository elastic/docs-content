---
applies_to:
  deployment:
    ess: all
    ece: all
products:
  - id: kibana
---


# {{integrations-server}} metrics [integrations-server-page]

{{integrations-server}} is available in {{ech}} and {{ece}} deployments as a combined offering of [Application Performance Monitoring (APM) Server](/solutions/observability/apm/index.md) and [Fleet Server](/reference/fleet/index.md):

 - Use {{apm-server}} to monitor your software services and applications in real time.
 - Use {{fleet-server}} to manage your {{agents}} running on one or more hosts, and the policies that the agents run under.


**To view an overview of {{integrations-server}} health:**

1. In the {{integrations-server}} section of the **Stack Monitoring** page, click **Integrations server overview**.

    The **APM server overview** page opens, showing both resource usage for {{integrations-server}} and various metrics for {{apm-server}}.

    :::{image} /deploy-manage/images/kibana-monitoring-integrations-server-overview.png
    :alt: {{integrations-server}} Overview
    :screenshot:
    :::

2. Adjust the time period for the visualizations as needed.

3. From this page you can also [create alerts](/explore-analyze/alerts-cases/alerts/create-manage-rules.md) to be triggered when the {{integrations-server}} metrics meet a defined set of conditions. 

**To view metrics for a specific {{integrations-server}} instance:**

1. In the {{integrations-server}} section of the **Stack Monitoring** page, click **Integrations Servers**.

    The **APM server instances** page opens, showing the status of each instance, including both resource usage for {{integrations-server}} and metrics data for [{{apm-server}}](/solutions/observability/apm/index.md).
  
1. Click the name of an instance to view its statistics over time.

1. Adjust the time period for the visualizations as needed.

1. As with the **APM server overview** page, you can also [create alerts](/explore-analyze/alerts/create-manage-rules.md) to be triggered when the instance metrics meet a defined set of conditions. 
