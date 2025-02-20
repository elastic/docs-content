---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/analyze-risk-score-data.html
  - https://www.elastic.co/guide/en/serverless/current/security-analyze-risk-score-data.html
---

# View and analyze risk score data [analyze-risk-score-data]

The {{security-app}} provides several options to monitor the change in the risk posture of hosts and users from your environment. Use the following places in the {{security-app}} to view and analyze risk score data:

* [Entity Analytics dashboard](#entity-analytics-dashboard)
* [Alerts page](#alerts-page)
* [Alert details flyout](#alert-details-flyout)
* [Hosts and Users pages](#hosts-users-pages)
* [Host and user details pages](#host-user-details-pages)
* [Host and user details flyouts](#host-and-user-details-flyouts)

::::{tip}
We recommend that you prioritize [alert triaging](#alert-triaging) to identify anomalies or abnormal behavior patterns.
::::



## Entity Analytics dashboard [entity-analytics-dashboard]

From the Entity Analytics dashboard, you can access entity key performance indicators (KPIs), risk scores, and levels. You can also click the number link in the **Alerts** column to investigate and analyze the alerts on the Alerts page.

If you have enabled the [entity store](entity-store.md), the dashboard also displays the [**Entities** section](../dashboards/entity-analytics-dashboard.md#entity-entities), where you can view all hosts and users along with their risk and asset criticality data.

:::{image} ../../../images/security-entity-dashboard.png
:alt: Entity Analytics dashboard
:class: screenshot
:::


## Alert triaging [alert-triaging]

You can prioritize alert triaging to analyze alerts associated with risky or business-critical entities using the following features in the {{security-app}}.


### Alerts page [alerts-page]

Use the Alerts table to investigate and analyze:

* Host and user risk levels
* Host and user risk scores
* Asset criticality

To display entity risk score and asset criticality data in the Alerts table, select **Fields**, and add the following:

* `user.risk.calculated_level` or `host.risk.calculated_level`
* `user.risk.calculated_score_norm` or `host.risk.calculated_score_norm`
* `user.asset.criticality` or `host.asset.criticality`

Learn more about [customizing the Alerts table](../detect-and-alert/manage-detection-alerts.md#customize-the-alerts-table).

:::{image} ../../../images/security-alerts-table-rs.png
:alt: Risk scores in the Alerts table
:class: screenshot
:::


#### Triage alerts associated with high-risk or business-critical entities [triage-alerts-associated-with-high-risk-or-business-critical-entities]

To analyze alerts associated with high-risk or business-critical entities, you can filter or group them by entity risk level or asset criticality level.

::::{note}
If you change the entity’s criticality level after an alert is generated, that alert document will include the original criticality level and will not reflect the new criticality level.
::::


* Use the drop-down filter controls to filter alerts by entity risk level or asset criticality level. To do this, [edit the default controls](../detect-and-alert/manage-detection-alerts.md#drop-down-filter-controls) to filter by:

    * `user.risk.calculated_level` or `host.risk.calculated_level` for entity risk level:

        :::{image} ../../../images/security-filter-by-host-risk-level.png
        :alt: Alerts filtered by high host risk level
        :class: screenshot
        :::

    * `user.asset.criticality` or `host.asset.criticality` for asset criticality level:

        :::{image} ../../../images/security-filter-by-asset-criticality.png
        :alt: Filter alerts by asset criticality level
        :class: screenshot
        :::

* To group alerts by entity risk level or asset criticality level, select **Group alerts by**, then select **Custom field** and search for:

    * `host.risk.calculated_level` or `user.risk.calculated_level` for entity risk level:

        :::{image} ../../../images/security-group-by-host-risk-level.png
        :alt: Alerts grouped by host risk levels
        :class: screenshot
        :::

    * `host.asset.criticality` or `user.asset.criticality` for asset criticality level:

        :::{image} ../../../images/security-group-by-asset-criticality.png
        :alt: Alerts grouped by entity asset criticality levels
        :class: screenshot
        :::

    * You can further sort the grouped alerts by highest entity risk score:

        1. Expand a risk level group (for example, **High**) or an asset criticality group (for example, **high_impact**).
        2. Select **Sort fields** → **Pick fields to sort by**.
        3. Select fields in the following order:

            1. `host.risk.calculated_score_norm` or `user.risk.calculated_score_norm`: **High-Low**
            2. `Risk score`: **High-Low**
            3. `@timestamp`: **New-Old**


        :::{image} ../../../images/security-hrl-sort-by-host-risk-score.png
        :alt: High-risk alerts sorted by host risk score
        :class: screenshot
        :::



### Alert details flyout [alert-details-flyout]

To access risk score data in the alert details flyout, select **Insights** → **Entities** on the **Overview** tab:

:::{image} ../../../images/security-alerts-flyout-rs.png
:alt: Risk scores in the Alerts flyout
:class: screenshot
:::


### Hosts and Users pages [hosts-users-pages]

On the Hosts and Users pages, you can access the risk score data:

* In the **Host risk level** or **User risk level** column on the **All hosts** or **All users** tab:

    :::{image} ../../../images/security-hosts-hr-level.png
    :alt: Host risk level data on the All hosts tab of the Hosts page
    :class: screenshot
    :::

* On the **Host risk** or **User risk** tab:

    :::{image} ../../../images/security-hosts-hr-data.png
    :alt: Host risk data on the Host risk tab of the Hosts page
    :class: screenshot
    :::



### Host and user details pages [host-user-details-pages]

On the host details and user details pages, you can access the risk score data:

* In the Overview section:

    :::{image} ../../../images/security-host-details-overview.png
    :alt: Host risk data in the Overview section of the host details page
    :class: screenshot
    :::

* On the **Host risk** or **User risk** tab:

    :::{image} ../../../images/security-host-details-hr-tab.png
    :alt: Host risk data on the Host risk tab of the host details page
    :class: screenshot
    :::



### Host and user details flyouts [host-and-user-details-flyouts]

In the host details and user details flyouts, you can access the risk score data in the risk summary section:

:::{image} ../../../images/security-risk-summary.png
:alt: Host risk data in the Host risk summary section
:class: screenshot
:::
