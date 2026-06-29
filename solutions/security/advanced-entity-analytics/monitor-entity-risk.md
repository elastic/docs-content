---
navigation_title: Monitor entity risk
description: Monitor entity risk scores, behavioral anomalies, and AI-generated threat hunting leads from the Entity analytics page in Elastic Security.
applies_to:
  stack: ga 9.1+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Monitor entity risk and anomalies

The **Entity analytics** page provides a centralized workspace for investigating entity risk across your environment. Use it to explore entity risk scores, surface behavioral anomalies, and prioritize threat investigations.

:::{image} /solutions/images/security-entity-analytics-overview.png
:alt: Entity analytics overview page
:screenshot:
:::

:::{admonition} Requirements
* This feature requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.

* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` To access this page, you need the following privileges:
  * `read` for `entities-latest-<space-id>`, `.entities.v2.latest.security_<space-id>-*`, and `risk-score.risk-score-<space-id>`
  * **Read** for the **Management → Saved Objects Management** feature 
* {applies_to}`serverless: ga` If you're using a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md), make sure it grants `read` access to all the required index patterns.
* {applies_to}`serverless: removed` {applies_to}`stack: removed 9.3` To get access to this page, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#access-privileged-user-monitoring).
:::

To access the page:
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Find **Entity analytics** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
- {applies_to}`stack: ga 9.1-9.3` Find **Entity analytics** → **Overview** in the navigation menu. 

## Threat hunting leads [entity-threat-hunting-leads]
```yaml {applies_to}
stack: preview 9.4+
serverless: preview
```

:::{admonition} Requirements
* To display threat hunting leads, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
* To view or generate threat hunting leads, you need the following privileges:
  * **View leads**: `read` for `.entity_analytics.entity-leads-*`
  * **Generate leads**:
    * `read`, `create_index`, and `write` for `.entity_analytics.entity-leads-*`
    * **Read** for the **Management > Actions and Connectors** feature
:::

AI-generated leads appear at the top of the page, giving threat hunters a curated starting point for their investigations. Leads are refreshed every 24 hours and are derived from observations about entities in the entity store, including:

* Recent increases in entity risk score
* Newly added privileged users
* High numbers of alerts on a given entity

Interact with this section in the following ways:

* Click **Generate** or **Regenerate** to manually trigger a new set of leads without waiting for the next automatic refresh.
* Click **See recent leads** to access and search the most recent leads.
* Click **Hunt with AI** to open an AI-assisted investigation session in Agent Builder without any pre-loaded lead context.
* Click the options menu {icon}`boxes_vertical` to select a connector and toggle **Auto-generate every 24 hours** on or off.
* Click a lead to open an AI-assisted investigation session in Agent Builder with that lead's context pre-loaded.


## Entity risk levels [entity-risk-levels]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

:::{admonition} Requirements
To display entity risk levels, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
:::

This panel shows the distribution of entity risk across your environment, grouped by risk level. For each level, it displays the associated risk score range and the number of entities at that level.


## Recent anomalies [entity-recent-anomalies]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

:::{admonition} Requirements
To display anomaly results, you must [install and run](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt anomaly detection jobs](/reference/machine-learning/ootb-ml-jobs-siem.md).
:::

This panel displays recent entity-related anomalies detected by prebuilt {{ml}} jobs. Interact with this section in the following ways:

* Use the **View by** dropdown to group anomalies by **Entity** or **Job ID**.
* Use the **Anomaly score** filters to focus on anomalies by severity range.
* Click **Open in Anomaly Explorer** to access and search all {{ml}} jobs in the **Anomaly Explorer**.


## Entities [entity-entities]

:::{admonition} Requirements
To display the **Entities** section, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
:::

This section provides a centralized view of all hosts, users, and services in your environment. It displays entities from the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md), which meet any of the following criteria:

* Have been observed by {{elastic-sec}}
* Have been added to {{elastic-sec}} through an integration, such as Active Directory or Okta
* {applies_to}`stack: ga 9.1-9.3` Have an asset criticality assignment


Interact with the table to filter and explore entity data:
:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

* Use the **Group entities by** dropdown to group entities by **Resolution**, **Entity type**, or a custom field. By default, entities are grouped by **Resolution**: alias entities appear nested under their primary entity, while unresolved entities appear on their own.
* Filter the table by watchlist membership to focus on specific entity groups.
* Sort and filter by any entity store field.
* Click an entity row to expand it and view more details, or open the entity details flyout.
::::

::::{applies-item} stack: ga 9.1-9.3

* Select the **Risk level** dropdown to filter the table by the selected user, host, or service risk level.
* Select the **Criticality** dropdown to filter the table by the selected asset criticality level.
* Select the **Source** dropdown to filter the table by the data source.
* Click the **View details** icon ({icon}`expand` ) to open the entity details flyout.

:::{note}
The **Entities** table only shows a subset of the data available for each entity. You can query the `.entities.v1.latest.security_user_<space-id>`, `.entities.v1.latest.security_host_<space-id>`, and `.entities.v1.latest.security_service_<space-id>` indices to see all the fields for each entity in the entity store.
:::


Entity data from different sources appears in the **Entities** section based on the following timelines:

* When you first enable the entity store, only data stored in the last 24 hours is processed. After that, data is processed continuously.
* Observed events from the {{elastic-sec}} default data view are processed in near real-time.
* Entity Analytics data, such as entity risk scores and asset criticality (including bulk asset criticality upload), is also processed in near real-time.
* The availability of entities extracted from Entity Analytics integrations depends on the specific integration. Refer to [Active Directory Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_ad), [Microsoft Entra ID Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_entra_id), and [Okta Entity Analytics](https://docs.elastic.co/en/integrations/entityanalytics_okta) for more details.

::::

:::::


## Entity KPIs (key performance indicators) [entity-kpis]
```yaml {applies_to}
stack: removed 9.4+, ga 9.1-9.3
serverless: removed
```

This section displays the total number of critical hosts, critical users, and anomalies. Select a link to jump to the **Hosts** page, **Users** page, or **Anomalies** table.


## User Risk Scores [entity-user-risk-scores]
```yaml {applies_to}
stack: removed 9.4+, ga 9.1-9.3
serverless: removed
```

:::{admonition} Requirements
To display user risk scores, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
:::

This section displays user risk score data for your environment, including the total number of users, and the five most recently recorded user risk scores, with their associated user names, risk data, and number of detection alerts. User risk scores are [calculated](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#how-is-risk-score-calculated) using a weighted sum on a scale of 0 (lowest) to 100 (highest).


Interact with the table to filter data, view more details, and take action:

* Select the **User risk level** menu to filter the chart by the selected level.
* Click **View all** to display all user risk information on the **Users** page.
* Click a user name link to open the entity details flyout.
* Hover over a user name link to display inline actions: **Add to timeline** ({icon}`timeline`) and **Copy to Clipboard** ({icon}`copy_clipboard`).
* Click the number link in the **Alerts** column to view the alerts on the **Alerts** page. Hover over the number and select **Investigate in timeline** ({icon}`timeline`) to launch Timeline with a query that includes the associated user name value.

For more information about user risk scores, refer to [](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Host Risk Scores [entity-host-risk-scores]
```yaml {applies_to}
stack: removed 9.4+, ga 9.1-9.3
serverless: removed
```

:::{admonition} Requirements
To display host risk scores, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
:::

This section displays host risk score data for your environment, including the total number of hosts, and the five most recently recorded host risk scores, with their associated host names, risk data, and number of detection alerts. Host risk scores are [calculated](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#how-is-risk-score-calculated) using a weighted sum on a scale of 0 (lowest) to 100 (highest).


Interact with the table to filter data, view more details, and take action:

* Select the **Host risk level** menu to filter the chart by the selected level.
* Click **View all** to display all host risk information on the **Hosts** page.
* Click a host name link to open the entity details flyout.
* Hover over a host name link to display inline actions: **Add to timeline** ({icon}`timeline`) and **Copy to Clipboard** ({icon}`copy_clipboard`).
* Click the number link in the **Alerts** column to view the alerts on the **Alerts** page. Hover over the number and select **Investigate in timeline** ({icon}`timeline`) to launch Timeline with a query that includes the associated host name value.

For more information about host risk scores, refer to [](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Service Risk Scores [service-risk-scores]
```yaml {applies_to}
stack: removed 9.4+, ga 9.1-9.3
serverless: removed
```

:::{admonition} Requirements
To display service risk scores, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
:::

This section displays service risk score data for your environment, including the total number of services, and the five most recently recorded service risk scores, with their associated service names, risk data, and number of detection alerts. Service risk scores are [calculated](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#how-is-risk-score-calculated) using a weighted sum on a scale of 0 (lowest) to 100 (highest).


Interact with the table to filter data, view more details, and take action:

* Select the **Service risk level** menu to filter the chart by the selected level.
* Click a service name link to open the service details flyout.
* Hover over a service name link to display inline actions: **Add to timeline** ({icon}`timeline`) and **Copy to Clipboard** ({icon}`copy_clipboard`).
* Click the number link in the **Alerts** column to view the alerts on the **Alerts** page. Hover over the number and select **Investigate in timeline** ({icon}`timeline`) to launch Timeline with a query that includes the associated service name value.

For more information about service risk scores, refer to [](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).


## Anomalies [entity-anomalies]
```yaml {applies_to}
stack: removed 9.4+, ga 9.1-9.3
serverless: removed
```

Anomaly detection jobs identify suspicious or irregular behavior patterns. The **Anomalies** table displays the total number of anomalies identified by these prebuilt {{ml}} jobs (named in the **Anomaly name** column).

:::{admonition} Requirements
To display anomaly results, you must [install and run](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt anomaly detection jobs](/reference/machine-learning/ootb-ml-jobs-siem.md). You cannot add custom anomaly detection jobs to the **Entity analytics** page.
:::

Interact with the table to view more details:

* Click **View all host anomalies** to go to the **Anomalies** table on the **Hosts** page.
* Click **View all user anomalies** to go to the **Anomalies** table on the **Users** page.
* Click **View all** to display and manage all machine learning jobs on the **Anomaly Detection Jobs** page.

:::{tip}
To learn more about {{ml}}, refer to [](/explore-analyze/machine-learning.md)
:::
