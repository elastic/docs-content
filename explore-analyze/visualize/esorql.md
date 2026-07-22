---
navigation_title: Visualizations (ES|QL query)
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/esql-visualizations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Lens visualizations using ES|QL queries [esql-visualizations]

Creating visualizations using an {{esql}} query is particularly useful when you need to:

- Query data across multiple indices without a pre-configured data view
- Apply complex filtering, transforms, or custom calculations in a single query
- Prototype a visualization directly from an {{esql}} query in Discover

For less advanced aggregations on a known index, [the point-and-click mode](lens.md) is a good alternative.

You can add {{esql}} visualizations to a dashboard directly from queries in Discover, or you can start from a dashboard.

:::{note}
:applies_to: {"stack": "preview 9.5", "serverless": "preview"}
If your visualization's query uses exactly one `STATS` command, dashboard users can turn on {icon}`bolt` **Fast mode** to get faster, estimated results for it. Refer to [](/explore-analyze/query-filter/languages/esql-kibana.md#approximation-fast-mode).
:::

## Edit and add from Discover [_edit_and_add_from_discover]

In Discover, [typing ES|QL queries](../query-filter/languages/esql-kibana.md) automatically shows a visualization. The visualization type depends on the content of the query: histogram, bar charts, etc. You can manually make changes to that visualization and edit its type and display options using the pencil button ![pencil button](/explore-analyze/images/kibana-esql-icon-edit-visualization.svg "").

You can then **Save** and add it to an existing or a new dashboard using the save button of the visualization ![save button](/explore-analyze/images/kibana-esql-icon-save-visualization.svg "").

## Create from dashboard [_create_from_dashboard]

1. Add a new panel from your dashboard.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` Select **Add** in the application menu and, if required, **New panel**.
    * {applies_to}`stack: ga 9.0-9.1` Select **Add panel** in the application menu.

   ::::{tip}
   If you haven't created a [data view](/explore-analyze/find-and-organize/data-views.md) and you don't have a dashboard yet, the **Dashboards** page offers you the possibility to **Try ES|QL** right away. By selecting this option, a dashboard is created with an ES|QL visualization that you can interact with and configure using ES|QL.
   ::::

2. Select **Visualization (query)** or **ES|QL** under **Visualizations**, depending on your {{kib}} version.

   An ES|QL editor appears and lets you configure your query and its associated visualization. The **Suggestions** panel can help you find alternative ways to configure the visualization.

   ::::{tip}
   Check the [ES|QL reference](elasticsearch://reference/query-languages/esql.md) to get familiar with the syntax and [optimize your query](elasticsearch://reference/query-languages/esql/esql-query-performance.md).
   ::::

3. When editing your query or its configuration, run the query to update the preview of the visualization.

    ![Previewing an ESQL visualization](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt69dcceb4f1e12bc1/66c752d6aff77d384dc44209/edit-esql-visualization.gif "")

    :::{note}
    :applies_to: { "stack": "ga 9.1+", "serverless": "ga" }

    When you edit the query and run it again, the visualization configuration persists as long as it is compatible with the query changes. Refer to [](#chart-config-persist) for more details.
    :::

4. You can bind controls to your ES|QL visualizations in dashboards by creating [ES|QL controls](add-variable-controls.md).
5. Select **Apply and close** to save the visualization to the dashboard.

### Customize the appearance of your {{esql}} visualization

When editing an {{esql}} visualization, you can customize the appearance of the chart. To do that:

1. Click one of the fields representing an axis of the chart to open its details.

   ![Click on the axis field to open its details](/explore-analyze/images/esql-visualization-customize-axis.png)

2. Define the appearance of your choice from the available options.

   ![Appearance customization options for ESQL charts](/explore-analyze/images/esql-visualization-customization-options.png)

3. Return to the previous menu, then **Apply and close** the configuration to save your changes.

### Break down a chart by multiple fields [esql-viz-multi-field-breakdown]
```{applies_to}
stack: ga 9.4
serverless: ga
```

On bar, line, and area charts built from an {{esql}} query, the **Breakdown** dimension can hold more than one field at the same time. Each unique combination of values is rendered as its own series, with the values joined by a `›` separator in the legend.

When the query groups a metric by more than one field, {{kib}} places the first field on the **Horizontal axis** and the remaining fields in the **Breakdown** dimension. For example, the following query counts web log events over time, broken down by host and file extension:

```esql
FROM kibana_sample_data_logs
| WHERE extension.keyword != ""
| STATS count(*) BY BUCKET(@timestamp, 100, ?_tstart, ?_tend), host.keyword, extension.keyword
```

In the resulting chart, the time buckets are placed on the **Horizontal axis**, while `host.keyword` and `extension.keyword` are combined in the **Breakdown** dimension. Each legend entry represents a unique combination, such as `artifacts.elastic.co › deb` or `artifacts.elastic.co › gz`.

![Stacked bar chart of web log events over time, broken down by host and file extension](/explore-analyze/images/esql-visualization-multi-field-breakdown.png)

To add another field to the breakdown, select **Add a field** under **Breakdown** and choose a column from your query. You can also drag the fields inside the **Breakdown** dimension to change the order in which their values appear in the combined label.

### Chart configuration persistence over {{esql}} query update [chart-config-persist]
```{applies_to}
stack: ga 9.1
serverless: ga
```

When you edit the {{esql}} query and run it again, the visualization configuration persists as you defined it as long as it is compatible with the query changes.

The chart configuration resets or follows automatic suggestions when:
- {applies_to}`stack: ga 9.2+` You manually select a different chart type incompatible with the one previously selected.
- {applies_to}`stack: ga 9.2+` You create a new chart and haven't edited the visualization's options yet.
- The query changes significantly and no longer returns compatible columns.

### Query data from multiple projects [esql-viz-cps]
```{applies_to}
serverless: preview
stack: unavailable
```

When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), your {{esql}} visualization queries data based on the current [{{cps}} scope](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana).

To target specific projects from within the query, add [`SET project_routing`](elasticsearch://reference/query-languages/esql/directives/set.md) at the beginning of your {{esql}} query. When you do this, the visualization panel displays a **Custom CPS scope** badge on the dashboard, indicating that it uses a different scope than the {{cps-init}} scope selector. Refer to [View data from multiple projects](/explore-analyze/dashboards/using.md#dashboard-cps-scope) for details.

## Add drilldowns to an {{esql}} visualization [esql-viz-drilldowns]
```{applies_to}
stack: ga 9.4
serverless: ga
```

{{esql}} visualizations support the following [drilldown types](../dashboards/drilldowns.md):

- **Dashboard** drilldowns: open another dashboard from a data point.
- **URL** drilldowns: open an external URL from a data point.
- {applies_to}`stack: ga 9.5` {applies_to}`serverless:` **Discover** drilldowns: open **Discover** from a data point. Dashboard filters and the dashboard KQL or Lucene query are translated into the panel's ES|QL query, so the same context applies.

Drilldowns can only be triggered from values backed by a field that exists in the underlying index. Values produced by {{esql}} commands like `EVAL` or `STATS` are not backed by an index field, so the drilldown option is not available when you click on those columns or series. For more information, refer to [Add pills by interacting with visualizations](../dashboards/using.md#_add_pills_by_interacting_with_visualizations).

## Ignore dashboard filters [esql-viz-ignore-dashboard-filters]
```{applies_to}
stack: ga 9.5
serverless: ga
```

By default, an {{esql}} visualization applies the filters and the KQL or Lucene query set at the dashboard level. To force a layer to run its query without these filters:
1. Select the {icon}`gear` **Settings** icon on the layer header.
2. Turn off **Use global filters**.

This option covers the dashboard's filter pills and the query from the search bar. The dashboard time range is a separate control that always applies, whether or not the option is turned on.

## Create an alert from your {{esql}} visualization
```{applies_to}
stack: ga 9.1
serverless:
   elasticsearch: ga
   observability: ga
   security: unavailable
```

Once you've created an {{esql}} panel, you can create an {{es}} threshold rule directly from the visualization panel, based on the data it displays. When you do this, the rule query is automatically generated and either describes the data and sets a specific threshold, or describes the data without setting a specific threshold.

::::{note}
{{elastic-sec}} rule types are not supported.
::::
To create a rule with the threshold pre-specified:

- Right-click a data point in the visualization and click **Add alert rule**. This opens the **Create rule** flyout. The generated query will define a threshold that corresponds to the data point you selected.
- [Configure](/solutions/observability/incident-management/create-an-elasticsearch-query-rule.md) your {{es}} rule.

To create a rule without the threshold pre-specified:

- Open the **More actions** (three dots) menu in the upper right of the panel and select **Add alert rule**. This opens the **Create rule** flyout. The generated query will define a threshold that corresponds to the data point you selected.
- [Configure](/solutions/observability/incident-management/create-an-elasticsearch-query-rule.md) your {{es}} rule.

## Use emojis in visualizations [esql-table-emojis]

:::{include} _snippets/emoji-table-esql.md
:::
