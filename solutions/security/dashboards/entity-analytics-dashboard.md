---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/detection-entity-dashboard.html
  - https://www.elastic.co/guide/en/serverless/current/security-detection-entity-dashboard.html
---

# Entity Analytics dashboard


The Entity Analytics dashboard provides a centralized view of emerging insider threats - including host risk, user risk, and anomalies from within your network. Use it to triage, investigate, and respond to these emerging threats.

::::{admonition} Requirements
In {{stack}}, a [Platinum subscription](https://www.elastic.co/pricing/) or higher is required.
::::


The dashboard includes the following sections:

* [Entity KPIs (key performance indicators)](/solutions/security/dashboards/entity-analytics-dashboard.md#entity-kpis)
* [User Risk Scores](/solutions/security/dashboards/entity-analytics-dashboard.md#entity-user-risk-scores)
* [Host Risk Scores](/solutions/security/dashboards/entity-analytics-dashboard.md#entity-host-risk-scores)
* [Entities](/solutions/security/dashboards/entity-analytics-dashboard.md#entity-entities)
* [Anomalies](/solutions/security/dashboards/entity-analytics-dashboard.md#entity-anomalies)

:::{image} ../../../images/security-entity-dashboard.png
:alt: Entity dashboard
:class: screenshot
:::


## Entity KPIs (key performance indicators) [entity-kpis]

Displays the total number of critical hosts, critical users, and anomalies. Select a link to jump to the **Hosts** page, **Users** page, or **Anomalies** table.


## User Risk Scores [entity-user-risk-scores]

::::{admonition} Requirements
To display user risk scores, you must [turn on the risk scoring engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).

::::


Displays user risk score data for your environment, including the total number of users, and the five most recently recorded user risk scores, with their associated user names, risk data, and number of detection alerts. Like host risk scores, user risk scores are calculated using a weighted sum on a scale of 0 (lowest) to 100 (highest).

:::{image} ../../../images/security-user-score-data.png
:alt: User risk table
:class: screenshot
:::

Interact with the table to filter data, view more details, and take action:

* Select the **User risk level** menu to filter the chart by the selected level.
* Click a user name link to open the user details flyout.
* Hover over a user name link to display inline actions: **Add to timeline**, which adds the selected value to Timeline, and **Copy to Clipboard**, which copies the user name value for you to paste later.
* Click **View all** in the upper-right to display all user risk information on the Users page.
* Click the number link in the **Alerts** column to view the alerts on the Alerts page. Hover over the number and select **Investigate in timeline** (![Investigate in timeline icon](../../../images/security-timeline-button-osquery.png "")) to launch Timeline with a query that includes the associated user name value.

For more information about user risk scores, refer to [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Host Risk Scores [entity-host-risk-scores]

::::{admonition} Requirements
To display host risk scores, you must [turn on the risk scoring engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
::::


Displays host risk score data for your environment, including the total number of hosts, and the five most recently recorded host risk scores, with their associated host names, risk data, and number of detection alerts. Host risk scores are calculated using a weighted sum on a scale of 0 (lowest) to 100 (highest).

:::{image} ../../../images/security-host-score-data.png
:alt: Host risk scores table
:class: screenshot
:::

Interact with the table to filter data, view more details, and take action:

* Select the **Host risk level** menu to filter the chart by the selected level.
* Click a host name link to open the host details flyout.
* Hover over a host name link to display inline actions: **Add to timeline**, which adds the selected value to Timeline, and **Copy to Clipboard**, which copies the host name value for you to paste later.
* Click **View all** in the upper-right to display all host risk information on the Hosts page.
* Click the number link in the **Alerts** column to view the alerts on the Alerts page. Hover over the number and select **Investigate in timeline** (![Investigate in timeline icon](../../../images/security-timeline-button-osquery.png "")) to launch Timeline with a query that includes the associated host name value.

For more information about host risk scores, refer to [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Entities [entity-entities]


::::{admonition} Requirements
To display the **Entities** section, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
::::


The **Entities** section provides a centralized view of all hosts and users in your environment. It displays entities from the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md), which meet any of the following criteria:

* Have been observed by {{elastic-sec}}
* Have an asset criticality assignment
* Have been added to {{elastic-sec}} through an integration, such Active Directory or Okta

::::{note}
The **Entities** table only shows a subset of the data available for each entity. You can query the `.entities.v1.latest.security_user_<space-id>` and `.entities.v1.latest.security_host_<space-id>` indices to see all the fields for each entity in the entity store.
::::


:::{image} ../../../images/security-entities-section.png
:alt: Entities section
:class: screenshot
:::

Entity data from different sources appears in the **Entities** section based on the following timelines:

* When you first enable the entity store, only data stored in the last 24 hours is processed. After that, data is processed continuously.
* Observed events from the {{elastic-sec}} default data view are processed in near real-time.
* Entity Analytics data, such as entity risk scores and asset criticality (including bulk asset criticality upload), is also processed in near real-time.
* The availability of entities extracted from Entity Analytics integrations depends on the specific integration. Refer to [Active Directory Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_ad), [Microsoft Entra ID Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_entra_id), and [Okta Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_okta) for more details.

Interact with the table to filter data and view more details:

* Select the **Risk level** dropdown to filter the table by the selected user or host risk level.
* Select the **Criticality** dropdown to filter the table by the selected asset criticality level.
* Select the **Source** dropdown to filter the table by the data source.
* Click the **View details** icon (![View details icon](../../../images/security-view-details-icon.png "")) to open the entity details flyout.


## Anomalies [entity-anomalies]

Anomaly detection jobs identify suspicious or irregular behavior patterns. The Anomalies table displays the total number of anomalies identified by these prebuilt {{ml}} jobs (named in the **Anomaly name** column).

::::{admonition} Requirements
To display anomaly results, you must [install and run](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt anomaly detection jobs](asciidocalypse://docs/docs-content/docs/reference/security/prebuilt-jobs.md). You cannot add custom anomaly detection jobs to the Entity Analytics dashboard.
::::


:::{image} ../../../images/security-anomalies-table.png
:alt: Anomalies table
:class: screenshot
:::

Interact with the table to view more details:

* Click **View all host anomalies** to go to the Anomalies table on the Hosts page.
* Click **View all user anomalies** to go to the Anomalies table on the Users page.
* Click **View all** to display and manage all machine learning jobs on the Anomaly Detection Jobs page.

::::{tip}
To learn more about {{ml}}, refer to [What is Elastic machine learning?](/explore-analyze/machine-learning.md)
::::
