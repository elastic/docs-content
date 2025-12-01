---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/analyze-risk-score-data.html
  - https://www.elastic.co/guide/en/serverless/current/security-analyze-risk-score-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# View and analyze risk score data [analyze-risk-score-data]

The {{security-app}} provides several ways to monitor the change in the risk posture of entities in your environment.

::::{tip}
After reviewing an entity’s risk score, the recommended next step is to investigate the risky entity in [Timeline](/solutions/security/investigate/timeline.md).
::::

## Entity Analytics overview [entity-analytics-overview]

In the Entity Analytics overview, you can view entity key performance indicators (KPIs), risk scores, and levels. You can also click the number link in the **Alerts** column to investigate and analyze the alerts on the Alerts page.

If you have enabled the [entity store](entity-store.md), you'll also get access to the **Entities** section, where you can view all hosts, users, and services along with their risk and asset criticality data.

Access the Entity Analytics overview from the following pages:
* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` [Entity analytics](/solutions/security/advanced-entity-analytics/overview.md) 
* [Entity analytics dashboard](/solutions/security/dashboards/entity-analytics-dashboard.md)


## Alert triaging [alert-triaging]

You can prioritize alert triaging to analyze alerts associated with risky or business-critical entities using the following features in the {{security-app}}.


### Alerts page [alerts-page]

Use the Alerts table to investigate and analyze:

* Host, user, and service risk levels
* Host, user, and service risk scores
* Asset criticality

To display entity risk score and asset criticality data in the Alerts table, select **Fields**, and add the following:

* `user.risk.calculated_level`, `host.risk.calculated_level`, or `service.risk.calculated_level`
* `user.risk.calculated_score_norm`, `host.risk.calculated_score_norm`, or `service.risk.calculated_score_norm`
* `user.asset.criticality`, `host.asset.criticality`, or `service.asset.criticality`

Learn more about [customizing the Alerts table](../detect-and-alert/manage-detection-alerts.md#customize-the-alerts-table).

:::{image} /solutions/images/security-alerts-table-rs.png
:alt: Risk scores in the Alerts table
:screenshot:
:::


#### Triage alerts associated with high-risk or business-critical entities [triage-alerts-associated-with-high-risk-or-business-critical-entities]

To analyze alerts associated with high-risk or business-critical entities, you can filter or group them by entity risk level or asset criticality level.

::::{note}
If you change the entity’s criticality level after an alert is generated, that alert document will include the original criticality level and will not reflect the new criticality level.
::::


* Use the drop-down filter controls to filter alerts by entity risk level or asset criticality level. To do this, [edit the default controls](../detect-and-alert/manage-detection-alerts.md#drop-down-filter-controls) to filter by:

    * `user.risk.calculated_level`, `host.risk.calculated_level`, or `service.risk.calculated_level` for entity risk level:

        :::{image} /solutions/images/security-filter-by-host-risk-level.png
        :alt: Alerts filtered by high host risk level
        :screenshot:
        :::

    * `user.asset.criticality`, `host.asset.criticality`, or `service.asset.criticality` for asset criticality level:

        :::{image} /solutions/images/security-filter-by-asset-criticality.png
        :alt: Filter alerts by asset criticality level
        :screenshot:
        :::

* To group alerts by entity risk level or asset criticality level, select **Group alerts by**, then select **Custom field** and search for:

    * `host.risk.calculated_level`, `user.risk.calculated_level`, or `service.risk.calculated_level` for entity risk level:

        :::{image} /solutions/images/security-group-by-host-risk-level.png
        :alt: Alerts grouped by host risk levels
        :screenshot:
        :::

    * `host.asset.criticality`, `user.asset.criticality`, or `service.asset.criticality` for asset criticality level:

        :::{image} /solutions/images/security-group-by-asset-criticality.png
        :alt: Alerts grouped by entity asset criticality levels
        :screenshot:
        :::

    * You can further sort the grouped alerts by highest entity risk score:

        1. Expand a risk level group (for example, **High**) or an asset criticality group (for example, **high_impact**).
        2. Select **Sort fields** → **Pick fields to sort by**.
        3. Select fields in the following order:

            1. `host.risk.calculated_score_norm`, `user.risk.calculated_score_norm` or `service.risk.calculated_score_norm`: **High-Low**
            2. `Risk score`: **High-Low**
            3. `@timestamp`: **New-Old**


        :::{image} /solutions/images/security-hrl-sort-by-host-risk-score.png
        :alt: High-risk alerts sorted by host risk score
        :screenshot:
        :::



### Alert details flyout [alert-details-flyout]

To access risk score data in the alert details flyout, select **Insights** → **Entities** on the **Overview** tab:

:::{image} /solutions/images/security-alerts-flyout-rs.png
:alt: Risk scores in the Alerts flyout
:screenshot:
:::


### Hosts and Users pages [hosts-users-pages]

On the Hosts and Users pages, you can access the risk score data:

* In the **Host risk level** or **User risk level** column on the **All hosts** or **All users** tab:

    :::{image} /solutions/images/security-hosts-hr-level.png
    :alt: Host risk level data on the All hosts tab of the Hosts page
    :screenshot:
    :::

* On the **Host risk** or **User risk** tab:

    :::{image} /solutions/images/security-hosts-hr-data.png
    :alt: Host risk data on the Host risk tab of the Hosts page
    :screenshot:
    :::



### Host and user details pages [host-user-details-pages]

On the host details and user details pages, you can access the risk score data:

* In the Overview section:

    :::{image} /solutions/images/security-host-details-overview.png
    :alt: Host risk data in the Overview section of the host details page
    :screenshot:
    :::

* On the **Host risk** or **User risk** tab:

    :::{image} /solutions/images/security-host-details-hr-tab.png
    :alt: Host risk data on the Host risk tab of the host details page
    :screenshot:
    :::



### Entity details flyouts [entity-details-flyouts]

In the entity details flyouts, you can access the risk score data in the risk summary section:

:::{image} /solutions/images/security-risk-summary.png
:alt: Host risk data in the Host risk summary section
:screenshot:
:::

## Analyze entities over time [historical-entity-analysis]
```yaml {applies_to}
stack: ga 9.2
serverless: ga
```

The [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) allows you to analyze how entity attributes change over time, making it easier to investigate past activity, track trends, and identify unusual behavior or changes that may indicate risk. Use time-based queries in [Discover](/explore-analyze/discover.md) to answer questions such as:

* What did user A’s attributes look like on March 15?
* How has user B's risk score changed over the last 90 days?
* Which user had the biggest jump in their risk score since yesterday?

By analyzing current and past entity data, you can understand how your environment and its entities evolve over time.

::::{note}
If you enabled the entity store before upgrading to 9.2, you'll need to re-start it using the **On**/**Off** toggle to access the historical analysis feature.
::::