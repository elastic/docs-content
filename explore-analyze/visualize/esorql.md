---
navigation_title: ES|QL
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/esql-visualizations.html
description: Create visualizations with ES|QL queries from Discover or dashboards. Generate charts dynamically from query results with automatic visualization type suggestions.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# ES|QL visualizations [esql-visualizations]

You can add {{esql}} visualizations to a dashboard directly from queries in Discover, or you can start from a dashboard.

## Edit and add from Discover [_edit_and_add_from_discover]

In Discover, [typing ES|QL queries](../query-filter/languages/esql-kibana.md) automatically shows a visualization. The visualization type depends on the content of the query: histogram, bar charts, etc. You can manually make changes to that visualization and edit its type and display options using the pencil button ![pencil button](/explore-analyze/images/kibana-esql-icon-edit-visualization.svg "").

You can then **Save** and add it to an existing or a new dashboard using the save button of the visualization ![save button](/explore-analyze/images/kibana-esql-icon-save-visualization.svg "").

## Create from dashboard [_create_from_dashboard]

1. Add a new panel from your dashboard.

    * {applies_to}`stack: ga 9.2` Select **Add** > **New panel** in the toolbar.
    * {applies_to}`stack: ga 9.0` Click **Add panel** in the dashboard toolbar.

   ::::{tip}
   If you haven't created a [data view](/explore-analyze/find-and-organize/data-views.md) and you don't have a dashboard yet, the **Dashboards** page offers you the possibility to **Try ES|QL** right away. By selecting this option, a dashboard is created with an ES|QL visualization that you can interact with and configure using ES|QL.
   ::::

2. Choose **ES|QL** under **Visualizations**. An ES|QL editor appears and lets you configure your query and its associated visualization. The **Suggestions** panel can help you find alternative ways to configure the visualization.

   ::::{tip}
   Check the [ES|QL reference](elasticsearch://reference/query-languages/esql.md) to get familiar with the syntax and optimize your query.
   ::::

3. When editing your query or its configuration, run the query to update the preview of the visualization.

    ![Previewing an ESQL visualization](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt69dcceb4f1e12bc1/66c752d6aff77d384dc44209/edit-esql-visualization.gif "")

    :::{note}
    {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga`

    When you edit the query and run it again, the visualization configuration persists as long as it is compatible with the query changes. Refer to [](#chart-config-persist) for more details.
    :::

4. You can bind controls to your ES|QL visualizations in dashboards by creating [ES|QL controls](../dashboards/add-controls.md#add-variable-control).
5. Select **Apply and close** to save the visualization to the dashboard.

### Customize the appearance of your {{esql}} visualization

When editing an {{esql}} visualization, you can customize the appearance of the chart. To do that:

1. Click one of the fields representing an axis of the chart to open its details.

   ![Click on the axis field to open its details](/explore-analyze/images/esql-visualization-customize-axis.png)

2. Define the appearance of your choice from the available options.

   ![Appearance customization options for ESQL charts](/explore-analyze/images/esql-visualization-customization-options.png)

3. Return to the previous menu, then **Apply and close** the configuration to save your changes.

### Chart configuration persistence over {{esql}} query update [chart-config-persist]
```{applies_to}
stack: ga 9.1
serverless: ga
```

When you edit the {{esql}} query and run it again, the visualization configuration persists as you defined it as long as it is compatible with the query changes.

The chart configuration resets or follows automatic suggestions when:
- {applies_to}`stack: ga 9.2` You manually select a different chart type incompatible with the one previously selected.
- {applies_to}`stack: ga 9.2` You create a new chart and haven't edited the visualization's options yet.
- The query changes significantly and no longer returns compatible columns.

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


