# Service-level objectives (SLOs) [slo]

::::{important}
To create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html#node-roles) present, and [SLO access](../../../solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.

::::


SLOs allow you to set clear, measurable targets for your service performance, based on factors like availability, response times, error rates, and other key metrics. You can define SLOs based on different types of data sources, such as custom KQL queries and APM latency or availability data.

Once you’ve defined your SLOs, you can monitor them in real time, with detailed dashboards and alerts that help you quickly identify and troubleshoot any issues that may arise. You can also track your progress against your SLO targets over time, with a clear view of your error budgets and burn rates.


## Important concepts [slo-important-concepts]

The following table lists some important concepts related to SLOs:

Service-level indicator (SLI)
:   The measurement of your service’s performance, such as service latency or availability.

SLO
:   The target you set for your SLI. It specifies the level of performance you expect from your service over a period of time.

Error budget
:   The amount of time that your SLI can not meet the SLO target before it violates your SLO.

Burn rate
:   The rate at which your service consumes your error budget.

In addition to these key concepts related to SLO functionality, see [Understanding SLO internals](../../../troubleshoot/observability/troubleshoot-service-level-objectives-slos.md#slo-understanding-slos) for more information on how SLOs work and their relationship with other system components, such as [{{es}} Transforms](../../../explore-analyze/transforms.md).


## SLO overview [slo-in-elastic]

From the SLO overview, you can see all of your SLOs and a quick summary of what’s happening in each one:

:::{image} ../../../images/observability-slo-dashboard.png
:alt: slo dashboard
:class: screenshot
:::

Select an SLO from the overview to see additional details including:

* **Burn rate:** the percentage of bad events over different time periods (1h, 6h, 24h, 72h) and the risk of exhausting your error budget within those time periods.
* **Historical SLI:** the SLI value and how it’s trending over the SLO time window.
* **Error budget burn down:** the remaining error budget and how it’s trending over the SLO time window.
* **Alerts:** active alerts if you’ve set any [SLO burn rate alert rules](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md) for the SLO.

:::{image} ../../../images/observability-slo-detailed-view.png
:alt: slo detailed view
:class: screenshot
:::


### Search and filter SLOs [filter-SLOs]

You can apply searches and filters to quickly find the SLOs you’re interested in.

:::{image} ../../../images/observability-slo-filtering-options.png
:alt: Options for filtering SLOs in the overview
:class: screenshot
:::

* **Apply structured filters:** Next to the search field, click the **Add filter** ![Add filter icon](../../../images/observability-addFilter.svg "") icon to add a custom filter. Notice that you can use `OR` and `AND` to combine filters. The structured filter can be disabled, inverted, or pinned across all apps.
* **Enter a semi-structured search:** In the search field, start typing a field name to get suggestions for field names and operators that you can use to build a structured query. The semi-structured search will filter SLOs for matches, and only return matching SLOs.
* Use the **Status** and **Tags** menus to include or exclude SLOs from the view based on the status or defined tags.

There are also options to sort and group the SLOs displayed in the overview:

:::{image} ../../../images/observability-slo-group-by.png
:alt: SLOs sorted by SLO status and grouped by tags
:class: screenshot
:::

* **Sort by**: SLI value, SLO status, Error budget consumed, or Error budget remaining.
* **Group by**: None, Tags, Status, or SLI type.
* Click icons to switch between a card view (![Card view icon](../../../images/observability-apps.svg "")), list view (![List view icon](../../../images/observability-list.svg "")), or compact view (![Compact view icon](../../../images/observability-tableDensityCompact.svg "")).


## SLO dashboard panels [slo-dashboard-panels]

SLO data is also available as Dashboard *panels*. Panels allow you to curate custom data views and visualizations to bring clarity to your data.

Available SLO panels include:

* **SLO Overview**: Visualize a selected SLO’s health, including name, current SLI value, target, and status.
* **SLO Alerts**: Visualize one or more SLO alerts, including status, rule name, duration, and reason. In addition, configure and update alerts, or create cases directly from the panel.

:::{image} ../../../images/observability-slo-dashboard-panel.png
:alt: slo dashboard panel
:class: screenshot
:::

See [Dashboard and visualizations](../../../explore-analyze/dashboards.md) to learn how to add panels to a Dashboard.


## Upgrade from beta to GA [slo-upgrade-to-ga]

Starting in version 8.12.0, SLOs are generally available (GA). If you’re upgrading from a beta version of SLOs (available in 8.11.0 and earlier), you must migrate your SLO definitions to a new format.

Refer to [Upgrade from beta to GA](../../../troubleshoot/observability/troubleshoot-service-level-objectives-slos.md#slo-troubleshoot-beta) for more details on how to proceed.


## Next steps [slo-overview-next-steps]

Get started using SLOs to measure your service performance:

* [Configure SLO access](../../../solutions/observability/incident-management/configure-service-level-objective-slo-access.md)
* [Create an SLO](../../../solutions/observability/incident-management/create-an-slo.md)
* [Create an SLO burn rate alert rule](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md)
* [View alerts](../../../solutions/observability/incident-management/view-alerts.md)
* [Triage SLO burn rate breaches](../../../solutions/observability/incident-management/triage-slo-burn-rate-breaches.md)
