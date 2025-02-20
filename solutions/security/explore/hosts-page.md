---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/hosts-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-hosts-overview.html
---

# Hosts page

The Hosts page provides a comprehensive overview of all hosts and host-related security events. Key performance indicator (KPI) charts, data tables, and interactive widgets let you view specific data, drill down for deeper insights, and interact with Timeline for further investigation.

:::{image} ../../../images/security-hosts-ov-pg.png
:alt: Hosts page
:class: screenshot
:::

The Hosts page has the following sections:


## Host KPI (key performance indicator) charts [host-KPI-charts]

KPI charts show metrics for hosts and unique IPs within the time range specified in the date picker. This data is visualized using linear or bar graphs.

::::{tip}
Hover inside a KPI chart to display the actions menu (**…​**), where you can perform these actions: inspect, open in Lens, and add to a new or existing case.
::::



## Data tables [host-data-tables]

Beneath the KPI charts are data tables, categorized by individual tabs, which are useful for viewing and investigating specific types of data. Select the relevant tab to view the following data:

* **Events**: All host events. To display alerts received from external monitoring tools, scroll down to the Events table and select **Show only external alerts** on the right.
* **All hosts**: High-level host details.
* **Uncommon processes**: Uncommon processes running on hosts.
* **Anomalies**: Anomalies discovered by machine learning jobs.
* **Host risk**: The latest recorded host risk score for each host, and its host risk classification. In {{stack}}, this feature requires a [Platinum subscription](https://www.elastic.co/pricing) or higher. In serverless, this feature requires the Security Analytics Complete [project feature](/deploy-manage/deploy/elastic-cloud/project-settings.md). Click **Enable** on the **Host risk** tab to get started. To learn more, refer to our [entity risk scoring documentation](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).
* **Sessions**: Linux process events that you can open in [Session View](/solutions/security/investigate/session-view.md), an investigation tool that allows you to examine Linux process data at a hierarchal level.

The tables within the **Events** and **Sessions** tabs include inline actions and several customization options. To learn more about what you can do with the data in these tables, refer to [*Manage detection alerts*](/solutions/security/detect-and-alert/manage-detection-alerts.md).

:::{image} ../../../images/security-events-table.png
:alt: Events table
:class: screenshot
:::


## Host details page [host-details-page]

A host’s details page displays all relevant information for the selected host. To view a host’s details page, click its **Host name** link in the **All hosts** table.

The host details page includes the following sections:

* **Asset Criticality**: This section displays the host’s current [asset criticality level](/solutions/security/advanced-entity-analytics/asset-criticality.md).
* **Summary**: Details such as the host ID, when the host was first and last seen, the associated IP addresses, and associated operating system. If the host risk score feature is enabled, this section also displays host risk score data.
* **Alert metrics**: The total number of alerts by severity, rule, and status (`Open`, `Acknowledged`, or `Closed`).
* **Data tables**: The same data tables as on the main Hosts page, except with values for the selected host instead of all hosts.

:::{image} ../../../images/security-hosts-detail-pg.png
:alt: Host's details page
:class: screenshot
:::


## Host details flyout [host-details-flyout]

In addition to the host details page, relevant host information is also available in the host details flyout throughout the {{elastic-sec}} app. You can access this flyout from the following places:

* The Alerts page, by clicking on a host name in the Alerts table
* The Entity Analytics dashboard, by clicking on a host name in the Host Risk Scores table
* The **Events** tab on the Users and user details pages, by clicking on a host name in the Events table
* The **User risk** tab on the user details page, by clicking on a host name in the Top risk score contributors table
* The **Events** tab on the Hosts and host details pages, by clicking on a host name in the Events table
* The **Host risk** tab on the host details page, by clicking on a host name in the Top risk score contributors table

The host details flyout includes the following sections:

* [Host risk summary](/solutions/security/explore/hosts-page.md#host-risk-summary), which displays host risk data and inputs.
* [Asset Criticality](/solutions/security/explore/hosts-page.md#host-asset-criticality-section), which allows you to view and assign asset criticality.
* [Insights](/solutions/security/explore/hosts-page.md#host-details-insights), which displays vulnerabilities findings for the host.
* [Observed data](/solutions/security/explore/hosts-page.md#host-observed-data), which displays host details.

:::{image} ../../../images/security-host-details-flyout.png
:alt: Host details flyout
:class: screenshot
:::


### Host risk summary [host-risk-summary]

::::{admonition} Requirements
The **Host risk summary** section is only available if the [risk scoring engine is turned on](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).

::::


The **Host risk summary** section contains a risk summary visualization and table.

The risk summary visualization shows the host risk score and host risk level. Hover over the visualization to display the **Options** menu. Use this menu to inspect the visualization’s queries, add it to a new or existing case, save it to your Visualize Library, or open it in Lens for customization.

The risk summary table shows the category, score, and number of risk inputs that determine the host risk score. Hover over the table to display the **Inspect** button, which allows you to inspect the table’s queries.

To expand the **Host risk summary** section, click **View risk contributions**. The left panel displays additional details about the host’s risk inputs:

* The asset criticality level and contribution score from the latest risk scoring calculation.
* The top 10 alerts that contributed to the latest risk scoring calculation, and each alert’s contribution score.

If more than 10 alerts contributed to the risk scoring calculation, the remaining alerts' aggregate contribution score is displayed below the **Alerts** table.

:::{image} ../../../images/security-host-risk-inputs.png
:alt: Host risk inputs
:class: screenshot
:::


### Asset Criticality [host-asset-criticality-section]

The **Asset Criticality** section displays the selected host’s [asset criticality level](/solutions/security/advanced-entity-analytics/asset-criticality.md). Asset criticality contributes to the overall [host risk score](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md). The criticality level defines how impactful the host is when calculating the risk score.

:::{image} ../../../images/security-host-asset-criticality.png
:alt: Asset criticality
:class: screenshot
:::

Click **Assign** to assign a criticality level to the selected host, or **Change** to change the currently assigned criticality level.


### Insights [host-details-insights]

The **Insights** section displays [Vulnerabilities Findings](https://www.elastic.co/guide/en/security/current/vuln-management-findings.html) for the host. Click **Vulnerabilities** to expand the flyout and view this data.

:::{image} ../../../images/security--host-details-insights-expanded.png
:alt: Host details flyout with the Vulnerabilities section expanded
:::


### Observed data [host-observed-data]

This section displays details such as the host ID, when the host was first and last seen, the associated IP addresses and operating system, and the relevant Endpoint integration policy information.

:::{image} ../../../images/security-host-observed-data.png
:alt: Host observed data
:class: screenshot
:::
