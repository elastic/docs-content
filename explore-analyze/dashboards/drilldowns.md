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

## Values that cannot open a drilldown [drilldowns-requirements]

A drilldown uses a value from a field in the data source. You cannot filter or open a drilldown from a value created at query time, because that value has no field in the index. This includes a Lens formula, an aggregation result, and an {{esql}} `EVAL` or `STATS` result.

::::{dropdown} ES|QL example

In the following query, `status` does not exist in the index. The query creates `status` from `response.keyword`. For that reason, you cannot filter or open a drilldown from `status` in the resulting visualization.

```esql
FROM kibana_sample_data_logs
| STATS COUNT(*) BY response.keyword
| EVAL status = CASE(
    response.keyword == "200", "ok",
    response.keyword == "503", "critical error",
    response.keyword == "404", "warning"
  )
| KEEP status, `COUNT(*)`
```

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` When you hover over a value in an {{esql}} visualization, the chart explains that you cannot filter or open a drilldown from that value because it relies on a field created at query time.

:::{image} /explore-analyze/images/kibana-esql-query-time-value.png
:alt: Tooltip on the critical error bar of an ES|QL chart. The tooltip says you cannot filter or drill down from a value created at query time.
:screenshot:
:::

:::{tip}
:applies_to: {"serverless": "ga", "stack": "ga 9.5+"}

From this version, you can filter and open a drilldown when the query gives an index field a new name.

- Assign the new name in the `BY` clause of `STATS`.

  ```esql
  STATS count(*) BY host = hostname
  ```

- Rename the field with the `RENAME` command.

  ```esql
  RENAME hostname AS host
  ```
:::

::::

For more information about filter pills, refer to [Add pills by interacting with visualizations](using.md#_add_pills_by_interacting_with_visualizations).

## Next steps [drilldowns-next-steps]

* [Create a dashboard drilldown](create-dashboard-drilldown.md)
* [Create a URL drilldown](create-url-drilldown.md)
* [Create a Discover drilldown](create-discover-drilldown.md)
* [Manage drilldowns](manage-drilldowns.md)

## Related pages [drilldowns-related-pages]

* [Add drilldowns to an {{esql}} visualization](../visualize/esorql.md#esql-viz-drilldowns)
* [Add pills by interacting with visualizations](using.md#_add_pills_by_interacting_with_visualizations)
