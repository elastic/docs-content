---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/drilldowns.html
navigation_title: Drilldowns
description: Drilldowns open another dashboard, a URL, or Discover from a dashboard panel and keep the selected value, filters, and time range.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
---

# Drilldowns [drilldowns]

A drilldown is a navigation action on a dashboard panel. When you select a value, it opens a destination you define: another dashboard, a URL, or **Discover**.

The destination keeps the context of that selection. That includes the value you selected, the filters on the dashboard, and the time range.

Selecting a value can also filter the dashboard you have open, for example when you select a slice or drag a time range. Add a drilldown when you want that same selection to open another view.

## Drilldown types [drilldown-types]

You can add three types of drilldown:

* **[Dashboard](create-dashboard-drilldown.md)**: Open another dashboard from a panel. For example, open a host dashboard from a summary dashboard, with a filter for the host name you selected.
* **[URL](create-url-drilldown.md)**: Open a website from a panel. For example, open a search page that includes the host name you selected.
* **[Discover](create-discover-drilldown.md)**: Open **Discover** from a visualization panel. For example, open the documents for one slice of a pie chart.

:::{image} /explore-analyze/images/kibana-dashboard_createDrilldown.png
:alt: Create drilldown flyout for a URL, with Single click selected
:screenshot:
:::

## How a drilldown uses the selected value [drilldowns-requirements]

A drilldown uses a value from a field in the data source. You cannot filter on a value created at query time, because that value has no field in the index. This includes a Lens formula, an aggregation result, and an {{esql}} `EVAL` or `STATS` result.

[Add drilldowns to an {{esql}} visualization](../visualize/esorql.md#esql-viz-drilldowns) includes examples of a renamed index field and a value created in the query.

For a value created at query time with an {{esql}} query:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` The visualization explains that you cannot filter or drill down from that value. A date value does not show that explanation.
* {applies_to}`stack: ga =9.4` The filter and drilldown actions are not shown. You can still add a drilldown on the panel for an index field.

For more information about filter pills, refer to [Add pills by interacting with visualizations](using.md#_add_pills_by_interacting_with_visualizations).

## Next steps [drilldowns-next-steps]

* [Create a dashboard drilldown](create-dashboard-drilldown.md)
* [Create a URL drilldown](create-url-drilldown.md)
* [Create a Discover drilldown](create-discover-drilldown.md)
* [Manage drilldowns](manage-drilldowns.md)

## Related pages [drilldowns-related-pages]

* [Add drilldowns to an {{esql}} visualization](../visualize/esorql.md#esql-viz-drilldowns)
* [Add pills by interacting with visualizations](using.md#_add_pills_by_interacting_with_visualizations)
