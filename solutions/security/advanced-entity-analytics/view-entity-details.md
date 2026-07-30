---
description: Inspect an entity's risk summary, resolution group, insights, and connection graph from the entity details flyout in Elastic Security.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# View entity details

You can learn more about an entity (host, user, or service) from the entity details flyout, which is available throughout the {{elastic-sec}} app. To access this flyout, click on an entity name in places such as:

* The Alerts table
* The **Entity analytics** page
* The **Users** and user details pages
* The **Hosts** and host details pages

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` You can also use the entity details flyout to attach an entity to a [case](/solutions/security/investigate/security-cases.md). To do this, click **Take action** at the bottom of the flyout, then select **Add to new case** or **Add to existing case**.

## Entity details flyout

The entity details flyout includes the following sections:

* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Flyout header, which displays key entity information and allows you to assign asset criticality.
* [Entity summary](#entity-summary), which allows you to generate an AI summary of the entity.
* [Entity risk summary](#entity-risk-summary), which displays entity risk data and inputs.
* [Behavioral anomalies](#behavioral-anomalies), which shows {{ml}} anomalies detected for the entity, mapped to the MITRE ATT&CK framework.
* [Visualizations](#visualizations), which shows a graph preview of the entity's connections and relationships.
* [Resolution](#resolution), which allows you to view and manage the entity's resolution group.
* [Insights](#insights), which displays vulnerabilities or misconfiguration findings for the entity.
* [Observed data](#observed-data), which displays entity details.
* [Asset Criticality](#asset-criticality), which allows you to view and assign asset criticality.


### Entity summary
```yaml {applies_to}
stack: ga 9.3
serverless: ga
```

::::{note}
* To generate an AI summary, you need to configure a [generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
* This feature is only available for users and hosts.
::::

The **Entity summary** section allows you to generate an AI-powered summary of the entity's security context. Click **Generate** to create a comprehensive overview that aggregates information from:

* Risk scores and risk inputs
* Asset criticality levels
* Vulnerabilities
* {{ml-cap}} anomalies associated with the entity

The summary provides a consolidated view of the entity's security posture, helping you quickly assess its significance and prioritize investigations. It includes information such as:

* The entity's current risk score with details about which alerts or rules contribute most significantly to the score
* The entity's asset criticality level and how it contributes to the overall risk score
* Details about detected vulnerabilities, including CVE identifiers, CVSS scores, affected packages or systems, and remediation guidance
* Recommended next steps based on the entity's security posture, such as updating vulnerable packages, investigating specific alerts, or implementing additional security controls

::::{tip}
If you have [AI Assistant](/solutions/security/ai/ai-assistant.md) or [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md) set up, you can select **More actions** ({icon}`boxes_vertical`) → **Ask AI Assistant** or **Add to chat** to continue the conversation about the entity in AI Assistant or Agent Builder.
::::

### Entity risk summary

::::{admonition} Requirements
The entity risk summary section is only available if the [risk scoring engine is turned on](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
::::

The entity risk summary section contains a risk summary visualization and table.

The risk summary visualization shows the entity risk score and risk level. Hover over the visualization to display the **Options** menu. Use this menu to inspect the visualization's queries, add it to a new or existing case, save it to your Visualize Library, or open it in Lens for customization.

The risk summary table shows the category, score, and number of risk inputs that determine the entity risk score. Hover over the table to display the **Inspect** button, which allows you to inspect the table's queries.

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` For entities that belong to a [resolution group](/solutions/security/advanced-entity-analytics/entity-resolution.md), the section shows both the individual **Entity risk score** and the **Resolution group risk score** — the aggregated score across all linked entities in the group — each with their own score and inputs breakdown.

To expand the entity risk summary section, click **View risk contributions**. The **Risk contributions** tab displays additional details about the entity's risk inputs.

#### Risk score history [risk-score-history]
```yaml {applies_to}
stack: ga 9.5+
serverless: ga
```

Risk scoring recalculates every hour, and every calculation is retained. The expanded entity risk summary opens with a risk score history chart, which shows the entity's score over time so you can identify when its risk posture changed. Dashed reference lines mark the **Low**, **Moderate**, **High**, and **Critical** [risk levels](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#how-is-risk-score-calculated), which helps you spot when the entity crossed a threshold.

To change the time range, use the time filter. Each point on the chart shows the highest risk score recorded for that period.

To investigate an earlier score, click its point on the chart. The **Contexts** and **Alerts** tables switch from the latest calculation to the calculation you selected, and a callout confirms which scoring run you're viewing. This allows you to answer questions such as which alerts drove a spike last week, or what an entity's asset criticality level was at the time it was scored.

To return to the latest calculation, click **Back to latest** in the callout, or click the selected point again.

#### Contexts [risk-contexts]

The **Contexts** table shows non-alert risk inputs and their contribution scores, including:

* Asset criticality level
* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Watchlist membership 
* {applies_to}`stack: removed 9.4+, ga =9.3, preview 9.1-9.2` Privileged user status

#### Alerts [risk-alerts]

The **Alerts** table shows the top 10 alerts that contributed to the risk scoring calculation, and each alert's contribution score. If more than 10 alerts contributed to the calculation, the remaining alerts' aggregate contribution score is displayed below the table.

### Behavioral anomalies [behavioral-anomalies]
```yaml {applies_to}
stack: ga 9.5+
serverless: ga
```

::::{admonition} Requirements
* To display anomaly results, you must [install and run](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) one or more [prebuilt {{anomaly-jobs}}](/reference/machine-learning/ootb-ml-jobs-siem.md).
* Viewing behavioral anomalies requires `read` privileges for the `.ml-anomalies-shared*` index and **Read** for the **Machine Learning** {{kib}} feature.
* This feature is only available for users and hosts.
::::

The **Behavioral anomalies** section surfaces {{ml}} anomalies detected for the entity over the selected time range, mapped to the [MITRE ATT&CK](https://attack.mitre.org) framework. It helps you spot suspicious activity — such as an unusual login from an atypical location — in the context of an attack chain.

The section overview displays:

* The total number of anomalies and an attack chain showing the MITRE ATT&CK tactics associated with them, with a badge indicating the number of anomalies per tactic.
* A table listing the three most recent anomalies, with the {{ml}} job that detected each one, its timestamp, and the anomalous value observed for the entity. Click a {{ml}} job name to open the record in the [Single Metric Viewer](/explore-analyze/machine-learning/anomaly-detection/ml-ad-view-results.md).

Click **All anomalies** to expand the flyout and open the **Behavioral anomalies** tab. The tab provides:

* **Filters**: filter anomalies by time range and anomaly score severity range.
* **Attack chain**: a visualization of the MITRE ATT&CK tactics represented in the detected anomalies. Select a tactic to filter the timeline and table to that tactic's anomalies.
* **Anomaly timeline**: a swimlane chart showing the anomalies over time, grouped by tactic and colored by severity.
* **Anomalies** table: a detailed, sortable list of anomaly records. Expand a row to see a plain-language explanation of the anomaly, the number of anomalous events, and the key fields that triggered it.

From the **Row actions** menu {icon}`boxes_vertical` of the **Anomalies** table, you can add an anomaly to Timeline, view its underlying events in Discover, or open the record in the Single Metric Viewer.

### Visualizations [visualizations]
```yaml {applies_to}
stack: preview 9.4+
serverless: preview
```

::::{admonition} Requirements
[Entity store](/solutions/security/advanced-entity-analytics/entity-store.md) must be enabled and populated in the active space.
::::

The **Visualizations** section shows a collapsible graph preview centered on the entity, covering the last 30 days of connections and [relationships](/solutions/security/advanced-entity-analytics/entity-relationships.md). To open the full interactive graph, click **Graph preview** to expand the flyout. In the graph view, you can:

* Hover over an entity node and click the plus {icon}`plus_in_circle` to open the actions menu, where you can show or hide entity relationships, the entity's actions, actions done to the entity, or related events, or show the entity's details.

* Filter the graph using KQL syntax in the search bar. Supported fields include EUID values (for example, `entity.id : "user:alice@example.com"`) and raw ECS identity fields such as `user.id`, `user.email`, or `user.name`.

* Select **Investigate in Timeline** ({icon}`timeline`) to open the current graph view in Timeline.

### Resolution [resolution]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

The **Resolution** section shows whether the entity belongs to a [resolution group](/solutions/security/advanced-entity-analytics/entity-resolution.md). Click **Resolution group** to open the tab, which displays all entity records linked to this entity — including the primary entity and any aliases — with their entity name, ID, source, and risk score.

To add an entity to the group, search by entity name or ID in the **Add entities to resolution group** table and click the add icon {icon}`plus_in_circle` next to the entity you want to link. To remove an entity from the group, click **X** {icon}`cross` in the **Actions** column of the **Resolution group** table. Entities must be removed individually.

### Insights

The **Insights** section displays [Vulnerabilities Findings](/solutions/security/cloud/findings-page-3.md) for the host or [Misconfiguration Findings](/solutions/security/cloud/findings-page.md) for the user. Click **Vulnerabilities** or **Misconfigurations** to expand the flyout and view this data.

### Observed data

This section displays details such as the entity ID, when the entity was first and last seen, and the associated IP addresses and operating system.

### Asset Criticality
```yaml {applies_to}
stack: removed 9.4+, ga 9.0-9.3
serverless: removed
```

The **Asset Criticality** section displays the selected entity's [asset criticality level](/solutions/security/advanced-entity-analytics/asset-criticality.md). Asset criticality contributes to the overall [entity risk score](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md). The criticality level defines how impactful the entity is when calculating the risk score.

Click **Assign** to assign a criticality level to the selected entity, or **Change** to change the currently assigned criticality level.