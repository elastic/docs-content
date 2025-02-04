---
navigation_title: "Entity Analytics"
---

# Entity Analytics dashboard [security-detection-entity-dashboard]


The Entity Analytics dashboard provides a centralized view of emerging insider threats - including host risk, user risk, and anomalies from within your network. Use it to triage, investigate, and respond to these emerging threats.

::::{admonition} Requirements
:class: note

To display host and user risk scores, you must [turn on the risk scoring engine](../../../solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).

::::


The dashboard includes the following sections:

* [Entity KPIs (key performance indicators)](../../../solutions/security/dashboards/entity-analytics-dashboard.md#entity-kpis)
* [Host Risk Scores](../../../solutions/security/dashboards/entity-analytics-dashboard.md#entity-host-risk-scores)
* [User Risk Scores](../../../solutions/security/dashboards/entity-analytics-dashboard.md#entity-user-risk-scores)
* [Anomalies](../../../solutions/security/dashboards/entity-analytics-dashboard.md#entity-anomalies)

:::{image} ../../../images/serverless--dashboards-entity-dashboard.png
:alt: Entity dashboard
:class: screenshot
:::


## Entity KPIs (key performance indicators) [entity-kpis]

Displays the total number of critical hosts, critical users, and anomalies. Select a link to jump to the Host risk table, User risk table, or Anomalies table.


## Host Risk Scores [entity-host-risk-scores]

Displays host risk score data for your environment, including the total number of hosts, and the five most recently recorded host risk scores, with their associated host names, risk data, and number of detection alerts. Host risk scores are calculated using a weighted sum on a scale of 0 (lowest) to 100 (highest).

:::{image} ../../../images/serverless--dashboards-host-score-data.png
:alt: Host risk scores table
:class: screenshot
:::

Interact with the table to filter data, view more details, and take action:

* Select the **Host risk level** menu to filter the chart by the selected level.
* Click a host name link to open the host details flyout.
* Hover over a host name link to display inline actions: **Add to timeline**, which adds the selected value to Timeline, and **Copy to Clipboard**, which copies the host name value for you to paste later.
* Click **View all** in the upper-right to display all host risk information on the Hosts page.
* Click the number link in the **Alerts** column to view the alerts on the Alerts page. Hover over the number and select **Investigate in timeline** (![Timeline](../../../images/serverless-timeline.svg "")) to launch Timeline with a query that includes the associated host name value.

For more information about host risk scores, refer to [Entity risk scoring](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## User Risk Scores [entity-user-risk-scores]

Displays user risk score data for your environment, including the total number of users, and the five most recently recorded user risk scores, with their associated user names, risk data, and number of detection alerts. Like host risk scores, user risk scores are calculated using a weighted sum on a scale of 0 (lowest) to 100 (highest).

:::{image} ../../../images/serverless--dashboards-user-score-data.png
:alt: User risk table
:class: screenshot
:::

Interact with the table to filter data, view more details, and take action:

* Select the **User risk level** menu to filter the chart by the selected level.
* Click a user name link to open the user details flyout.
* Hover over a user name link to display inline actions: **Add to timeline**, which adds the selected value to Timeline, and **Copy to Clipboard**, which copies the user name value for you to paste later.
* Click **View all** in the upper-right to display all user risk information on the Users page.
* Click the number link in the **Alerts** column to view the alerts on the Alerts page. Hover over the number and select **Investigate in timeline** (![Timeline](../../../images/serverless-timeline.svg "")) to launch Timeline with a query that includes the associated user name value.

For more information about user risk scores, refer to [Entity risk scoring](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Anomalies [entity-anomalies]

Anomaly detection jobs identify suspicious or irregular behavior patterns. The Anomalies table displays the total number of anomalies identified by these prebuilt {{ml}} jobs (named in the **Anomaly name** column).

::::{admonition} Requirements
:class: note

To display anomaly results, you must [install and run](../../../explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt anomaly detection jobs](https://www.elastic.co/guide/en/security/current/prebuilt-ml-jobs.html). You cannot add custom anomaly detection jobs to the Entity Analytics dashboard.

::::


:::{image} ../../../images/serverless--dashboards-anomalies-table.png
:alt: Anomalies table
:class: screenshot
:::

Interact with the table to view more details:

* Click **View all host anomalies** to go to the Anomalies table on the Hosts page.
* Click **View all user anomalies** to go to the Anomalies table on the Users page.
* Click **View all** to display and manage all machine learning jobs on the Anomaly Detection Jobs page.

::::{tip}
To learn more about {{ml}}, refer to [What is Elastic machine learning?](../../../explore-analyze/machine-learning.md)

::::
