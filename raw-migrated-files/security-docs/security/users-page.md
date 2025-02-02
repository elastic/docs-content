# Users page [users-page]

The Users page provides a comprehensive overview of user data to help you understand authentication and user behavior within your environment. Key performance indicator (KPI) charts, data tables, and interactive widgets let you view specific data and drill down for deeper insights.

:::{image} ../../../images/security-users-page.png
:alt: User's page
:class: screenshot
:::

The Users page has the following sections:


## User KPI (key performance indicator) charts [_user_kpi_key_performance_indicator_charts]

KPI charts show the total number of users and successful and failed user authentications within the time range specified in the date picker. Data in the KPI charts is visualized through linear and bar graphs.

::::{tip}
Hover inside a KPI chart to display the actions menu (**…​**), where you can perform these actions: inspect, open in Lens, and add to a new or existing case.
::::



## Data tables [_data_tables]

Beneath the KPI charts are data tables, which are useful for viewing and investigating specific types of data. Select the relevant tab to view the following details:

* **Events**: Ingested events that contain the `user.name` field. You can stack by the `event.action`, `event.dataset`, or `event.module` field. To display alerts received from external monitoring tools, scroll down to the Events table and select **Show only external alerts** on the right.
* **All users**: A chronological list of unique user names, when they were last active, and the associated domains.
* **Authentications**: A chronological list of user authentication events and associated details, such as the number of successes and failures, and the host name of the last successful destination.
* **Anomalies**: Unusual activity discovered by machine learning jobs that contain user data.
* **User risk**: The latest recorded user risk score for each user, and its user risk classification. This feature requires a [Platinum subscription](https://www.elastic.co/pricing) or higher and must be enabled to display the data. Click **Enable** on the **User risk** tab to get started. To learn more, refer to our [entity risk scoring documentation](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring.md).

The Events table includes inline actions and several customization options. To learn more about what you can do with the data in these tables, refer to [*Manage detection alerts*](../../../solutions/security/detect-and-alert/manage-detection-alerts.md).


## User details page [user-details-page]

A user’s details page displays all relevant information for the selected user. To view a user’s details page, click its **User name** link from the **All users** table.

The user details page includes the following sections:

* **Asset Criticality**: This section displays the user’s current [asset criticality level](../../../solutions/security/advanced-entity-analytics/asset-criticality.md).
* **Summary**: Details such as the user ID, when the user was first and last seen, the associated IP address(es), and operating system. If the user risk score feature is enabled, this section also displays user risk score data.
* **Alert metrics**: The total number of alerts by severity, rule, and status (`Open`, `Acknowledged`, or `Closed`).
* **Data tables**: The same data tables as on the main Users page, except with values for the selected user instead of for all users.

:::{image} ../../../images/security-user-details-pg.png
:alt: User details page
:class: screenshot
:::


## User details flyout [user-details-flyout]

In addition to the user details page, relevant user information is also available in the user details flyout throughout the {{elastic-sec}} app. You can access this flyout from the following places:

* The Alerts page, by clicking on a user name in the Alerts table
* The Entity Analytics dashboard, by clicking on a user name in the User Risk Scores table
* The **Events** tab on the Users and user details pages, by clicking on a user name in the Events table
* The **User risk** tab on the user details page, by clicking on a user name in the Top risk score contributors table
* The **Events** tab on the Hosts and host details pages, by clicking on a user name in the Events table
* The **Host risk** tab on the host details page, by clicking on a user name in the Top risk score contributors table

The user details flyout includes the following sections:

* [User risk summary](../../../solutions/security/explore/users-page.md#user-risk-summary), which displays user risk data and inputs.
* [Asset Criticality](../../../solutions/security/explore/users-page.md#user-asset-criticality-section), which allows you to view and assign asset criticality.
* [Insights](../../../solutions/security/explore/users-page.md#user-insights), which displays misconfiguration findings for the user.
* [Observed data](../../../solutions/security/explore/users-page.md#user-observed-data), which displays user details.

:::{image} ../../../images/security-user-details-flyout.png
:alt: User details flyout
:class: screenshot
:::


### User risk summary [user-risk-summary]

::::{admonition} Requirements
The **User risk summary** section is only available if the [risk scoring engine is turned on](../../../solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).

::::


The **User risk summary** section contains a risk summary visualization and table.

The risk summary visualization shows the user risk score and user risk level. Hover over the visualization to display the **Options** menu. Use this menu to inspect the visualization’s queries, add it to a new or existing case, save it to your Visualize Library, or open it in Lens for customization.

The risk summary table shows the category, score, and number of risk inputs that determine the user risk score. Hover over the table to display the **Inspect** button, which allows you to inspect the table’s queries.

To expand the **User risk summary** section, click **View risk contributions**. The left panel displays additional details about the user’s risk inputs:

* The asset criticality level and contribution score from the latest risk scoring calculation.
* The top 10 alerts that contributed to the latest risk scoring calculation, and each alert’s contribution score.

If more than 10 alerts contributed to the risk scoring calculation, the remaining alerts' aggregate contribution score is displayed below the **Alerts** table.

:::{image} ../../../images/security-user-risk-inputs.png
:alt: User risk inputs
:class: screenshot
:::


### Asset Criticality [user-asset-criticality-section]

The **Asset Criticality** section displays the selected user’s [asset criticality level](../../../solutions/security/advanced-entity-analytics/asset-criticality.md). Asset criticality contributes to the overall [user risk score](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring.md). The criticality level defines how impactful the user is when calculating the risk score.

:::{image} ../../../images/security-user-asset-criticality.png
:alt: Asset criticality
:class: screenshot
:::

Click **Assign** to assign a criticality level to the selected user, or **Change** to change the currently assigned criticality level.


### Insights [user-insights]

The **Insights** section displays [Misconfiguration Findings](../../../solutions/security/cloud/findings-page.md) for the user. Click **Misconfigurations** to expand the flyout and view this data.


### Observed data [user-observed-data]

This section displays details such as the user ID, when the user was first and last seen, and the associated IP addresses and operating system.

:::{image} ../../../images/security-user-observed-data.png
:alt: User observed data
:class: screenshot
:::
