---
navigation_title: Monitor entity risk
description: Review entity risk scores and anomalies, find the entities that need attention, and start AI-assisted investigations from the Entity analytics page in Elastic Security.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detection-entity-dashboard.html
  - https://www.elastic.co/guide/en/serverless/current/security-detection-entity-dashboard.html
applies_to:
  stack: ga
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
* To access this page, you need **Read** for the **Management** → **Saved Objects Management** feature.
* You also need the `read` index privilege for these index patterns:
  * {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` `entities-latest-<space-id>`, `.entities.v2.latest.<space-id>-*`, and `risk-score.risk-score-<space-id>`
  * {applies_to}`stack: ga 9.4-9.5` `entities-latest-<space-id>`, `.entities.v2.latest.security_<space-id>-*`, and `risk-score.risk-score-<space-id>` 
* {applies_to}`serverless: ga` If you're using a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md), make sure it grants `read` access to all the required index patterns.
* {applies_to}`stack: ga 9.1-9.2` To get access to this page, turn on the `securitySolution:enablePrivilegedUserMonitoring` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings). In later versions, this page is displayed by default, and its visibility is no longer controlled by an advanced setting. 
:::

The way you access this page and the elements it contains differ based on your version. Select your version to see the details:

:::::{applies-switch}

::::{applies-item} { stack: ga 9.6+, serverless: ga }

To access the page, find **Entity analytics** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The page contains the following elements:

* [Search bar and filters](#entity-search-filters)
* [Entities that need your attention](#entity-needs-attention)
* [Entity table](#entity-table)

$$$entity-search-filters$$$
**Search bar and filters**

Narrow the page to the part of your environment that you want to investigate. Use the search bar and filters in the following ways:

* Enter a Kibana Query Language (KQL) query to find entities by their field values. The search narrows both the **Entities that need your attention** tiles and the entity table. While a search is active, the tiles hide their change and trend indicators.
* Use the time filter next to the search bar to set the time range.
* Filter the tiles and the entity table by attributes such as entity type or risk level.

The page keeps your time range, filters, selected tile, and table layout in the URL, so you can bookmark or share a view.

$$$entity-needs-attention$$$
**Entities that need your attention**

:::{admonition} Requirements
* To display this section, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
* To display the number of matching entities on a tile, the tile needs access to the data it reads:
  * **Severely alerting** and **Watchlisted & alerting** need detection alerts and read access to them.
  * **Newly high-risk** and **Risk movers** need [risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md) turned on and enough risk score history to compare against.
  * **Anomalous** needs [prebuilt {{anomaly-jobs}}](/reference/machine-learning/ootb-ml-jobs-siem.md) that are [installed and running](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md), and read access to {{ml}} anomalies.
* The AI buttons next to the section heading require {{agent-builder}} to be your [AI chat experience](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md).
:::

The tiles at the top of the page show which entities to look at first. Each tile counts the entities that match one condition in the selected time range, and shows how the count changed from the previous period of the same length, along with a trend line.

| Tile | Counts entities that |
|---|---|
| **Severely alerting** | Have at least one high- or critical-severity alert |
| **Newly high-risk** | Have a risk level that climbed to high or critical |
| **Risk movers** | Have a risk score that went up by 10 or more points since the start of the time range |
| **New & alerting** | Were first seen in the time range and have at least one alert |
| **Anomalous** | Are flagged by at least one {{ml}} anomaly |
| **Watchlisted & alerting** | Are on a watchlist and have at least one alert |

Click a tile to filter the entity table to the entities it counts. The table shows up to 1,000 entities for a tile.

Use the buttons next to the section heading to start an {{agent-builder}} chat. A button doesn't appear if you don't meet its requirements.

  * Click **Generate AI brief** to ask the agent for a summary of the entity risk landscape in your current view, including the time range, filters, and tile counts, with recommended next steps. {{agent-builder}} opens and starts generating the brief right away.
  * Click **Hunt with AI** to open a new chat with a prefilled prompt that asks the agent for your latest active threat hunting leads, including why each was flagged and a first step to investigate it. Review the prompt, then send it.

$$$entity-table$$$
**Entity table**

:::{admonition} Requirements
To display the entity table, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
:::

The entity table provides a centralized view of all hosts, users, and services in your environment. It displays entities from the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md), which meet either of the following criteria:

* Have been observed by {{elastic-sec}}
* Have been added to {{elastic-sec}} through an integration, such as Active Directory or Okta

Interact with the table in the following ways:

* Use the field selector to add or remove fields as columns, and use the column selector to show or hide columns.
* Use **Rows** to select what each row represents:
  * **Resolved entities** (default): One row per resolved entity. Expand a row to see the individual records nested under it. Values such as the risk score and alerts cover the whole group, and the **Records** column shows how many records the group contains.
  * **Individual records**: One row per entity record, with that record's own values. The **Resolved to** column shows the primary entity that the record resolves to.
* Use **Group by** to group rows by **Entity type**, by **Resolution** (individual records only), or by a custom field, up to three levels deep.
* Use the icons in the **Actions** column to work with an entity:
  * **Investigate in timeline** {icon}`timeline`: Opens Timeline with a query for the entity.
  * **Open entity graph**: Opens the [graph view](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) of the entity and its relationships.
  * **More actions** {icon}`boxes_vertical`: Opens a menu with **Add to chat**, which starts an {{agent-builder}} chat with the entity attached, and **Add to case**, which attaches the entity to a case.
* Click an entity name to open the entity details flyout.

::::

::::{applies-item} stack: ga 9.4-9.5

To access the page, find **Entity analytics** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The page contains the following sections:

* [Threat hunting leads](#entity-threat-hunting-leads)
* [Entity risk levels](#entity-risk-levels)
* [Recent anomalies](#entity-recent-anomalies)
* [Entities](#entity-entities)

$$$entity-threat-hunting-leads$$$
**Threat hunting leads** {applies_to}`stack: preview 9.4-9.5`

:::{admonition} Requirements
* To display threat hunting leads, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
* To view or generate threat hunting leads, you need the following privileges:
  * **View leads**: `read` for `.entity_analytics.entity-leads*`
  * **Generate leads**:
    * `read`, `create_index`, and `write` for `.entity_analytics.entity-leads*`
    * **Read** for the **Management** → **Actions and Connectors** feature
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

$$$entity-risk-levels$$$
**Entity risk levels**

:::{admonition} Requirements
To display entity risk levels, you must [turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
:::

This panel shows the distribution of entity risk across your environment, grouped by risk level. For each level, it displays the associated risk score range and the number of entities at that level.

$$$entity-recent-anomalies$$$
**Recent anomalies**

:::{admonition} Requirements
* To display anomaly results, you must [install and run](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt {{anomaly-jobs}}](/reference/machine-learning/ootb-ml-jobs-siem.md).
* Loading this panel requires `read` privileges for the `.ml-anomalies-shared*` index and **Read** for the **Machine Learning** {{kib}} feature.
:::

This panel displays recent entity-related anomalies detected by prebuilt {{ml}} jobs. Interact with this section in the following ways:

* Use the **View by** dropdown to group anomalies by **Entity** or **Job ID**.
* Use the **Anomaly score** filters to focus on anomalies by severity range.
* Click **Open in Anomaly Explorer** to access and search all {{ml}} jobs in the **Anomaly Explorer**.

$$$entity-entities$$$
**Entities**

:::{admonition} Requirements
To display the **Entities** section, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
:::

This section provides a centralized view of all hosts, users, and services in your environment. It displays entities from the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md), which meet either of the following criteria:

* Have been observed by {{elastic-sec}}
* Have been added to {{elastic-sec}} through an integration, such as Active Directory or Okta

Interact with the table to filter and explore entity data:

* Use the **Group entities by** dropdown to group entities by **Resolution**, **Entity type**, or a custom field. By default, entities are grouped by **Resolution**: alias entities appear nested under their primary entity, while unresolved entities appear on their own.
* Filter the table by watchlist membership to focus on specific entity groups.
* Sort and filter by any entity store field.
* Click an entity row to expand it and view more details, or open the entity details flyout.
::::

::::{applies-item} stack: ga 9.0-9.3

To access the page:

* {applies_to}`stack: ga 9.1-9.3` Find **Entity analytics** → **Overview** in the navigation menu.
* {applies_to}`stack: ga =9.0` Find **Dashboards** → **Entity Analytics** in the navigation menu.

The page contains the following sections:

* [Entity KPIs (key performance indicators)](#entity-kpis)
* [User Risk Scores](#entity-user-risk-scores)
* [Host Risk Scores](#entity-host-risk-scores)
* [Service Risk Scores](#service-risk-scores)
* [Entities](#entity-entities-9-1)
* [Anomalies](#entity-anomalies)

$$$entity-kpis$$$
**Entity KPIs (key performance indicators)**

This section displays the total number of critical hosts, critical users, and anomalies. Select a link to jump to the **Hosts** page, **Users** page, or **Anomalies** table.

$$$entity-user-risk-scores$$$
**User Risk Scores**

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

$$$entity-host-risk-scores$$$
**Host Risk Scores**

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

$$$service-risk-scores$$$
**Service Risk Scores**

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

$$$entity-entities-9-1$$$
**Entities**

:::{admonition} Requirements
To display the **Entities** section, you must [enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md#enable-entity-store).
:::

This section provides a centralized view of all hosts, users, and services in your environment. It displays entities from the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md), which meet either of the following criteria:

* Have been observed by {{elastic-sec}}
* Have been added to {{elastic-sec}} through an integration, such as Active Directory or Okta
* Have an asset criticality assignment

Interact with the table to filter and explore entity data:

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

$$$entity-anomalies$$$
**Anomalies**

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
::::

:::::
