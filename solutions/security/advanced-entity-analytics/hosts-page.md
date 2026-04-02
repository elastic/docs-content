---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/hosts-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-hosts-overview.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Hosts page

The Hosts page provides a comprehensive overview of all hosts and host-related security events. Key performance indicator (KPI) charts, data tables, and interactive widgets let you view specific data, drill down for deeper insights, and interact with Timeline for further investigation.

:::{image} /solutions/images/security-hosts-ov-pg.png
:alt: Hosts page
:screenshot:
:::

The Hosts page has the following sections:


## Host KPI (key performance indicator) charts [host-KPI-charts]

KPI charts show metrics for hosts and unique IPs within the time range specified in the date picker. This data is visualized using linear or bar graphs.

::::{tip}
Hover inside a KPI chart to display the actions menu (**…**), where you can perform these actions: inspect, open in Lens, and add to a new or existing case.
::::



## Data tables [host-data-tables]

Beneath the KPI charts are data tables, categorized by individual tabs, which are useful for viewing and investigating specific types of data. Select the relevant tab to view the following data:

* **Events**: All host events. To display alerts received from external monitoring tools, scroll down to the Events table and select **Show only external alerts** on the right.
* **All hosts**: High-level host details.
* **Uncommon processes**: Uncommon processes running on hosts.
* **Anomalies**: Anomalies discovered by [{{ml}} jobs](/solutions/security/advanced-entity-analytics/anomaly-detection.md).
* **Host risk**: The latest recorded host risk score for each host, and its host risk classification. In {{stack}}, this feature requires a [Platinum subscription](https://www.elastic.co/pricing) or higher. In serverless, this feature requires the Security Analytics Complete [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md). Click **Enable** on the **Host risk** tab to get started. To learn more, refer to our [entity risk scoring documentation](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).
* **Sessions**: Linux process events that you can open in [Session View](/solutions/security/investigate/session-view.md), an investigation tool that allows you to examine Linux process data at a hierarchal level.

The tables within the **Events** and **Sessions** tabs include inline actions and several customization options. To learn more about what you can do with the data in these tables, refer to [*Manage detection alerts*](/solutions/security/detect-and-alert/manage-detection-alerts.md).

:::{image} /solutions/images/security-events-table.png
:alt: Events table
:screenshot:
:::


## Host details page [host-details-page]

A host’s details page displays all relevant information for the selected host. To view a host’s details page, click its **Host name** link in the **All hosts** table.

The host details page includes the following sections:

* **Asset Criticality**: This section displays the host’s current [asset criticality level](/solutions/security/advanced-entity-analytics/asset-criticality.md).
* **Summary**: Details such as the host ID, when the host was first and last seen, the associated IP addresses, and associated operating system. If the host risk score feature is enabled, this section also displays host risk score data.
* **Alert metrics**: The total number of alerts by severity, rule, and status (`Open`, `Acknowledged`, or `Closed`).
* **Data tables**: The same data tables as on the main Hosts page, except with values for the selected host instead of all hosts.

:::{image} /solutions/images/security-hosts-detail-pg.png
:alt: Host's details page
:screenshot:
:::

