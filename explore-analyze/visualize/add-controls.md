---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-controls.html
navigation_title: Add controls
type: how-to
description: Add interactive filter controls to your Kibana dashboards to help users explore data with options lists, range sliders, and time sliders.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add controls to dashboards [add-controls]

Add interactive filter [controls](dashboard-controls.md) to your dashboards to help viewers explore data without writing queries. This page covers how to add, edit, and remove Options list, Range slider, and Time slider controls.

To add {{esql}}-powered variable controls instead, refer to [Add variable controls with ES|QL](add-variable-controls.md).

## Before you begin [add-controls-requirements]

To add Options list, Range slider, and Time slider controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

## Add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

{applies_to}`stack: ga 9.5` {applies_to}`serverless: ga` By default, a control is based on a data view field, as described in the following steps. You can also [populate its values with an {{esql}} query](#populate-control-values-with-esql) instead.

1. Open or create a new dashboard.
2. Add a control.

    ::::{applies-switch}
    :::{applies-item} {"serverless": "ga", "stack": "ga 9.2"}
    In **Edit** mode, select **Add** > **Controls** > **Control**.
    :::
    :::{applies-item} {"stack": "ga 9.0-9.1"}
    In **Edit** mode, select **Controls** > **Add control** in the dashboard toolbar.
    :::
    ::::

3. On the **Create control** flyout, from the **Data view** dropdown, select the data view that contains the field you want to use for the control.
4. In the **Field** list, select the field you want to filter on.
5. Under **Control type**, select **Options list** or **Range slider**. Range sliders are only compatible with number fields.
6. Configure the control's label, selections, search, and additional settings. For the full list of available settings, refer to [Dashboard control settings](dashboard-control-settings.md).
7. Select **Save**. The control can now be used.
8. Save the dashboard.

:::{note}
:applies_to: {"serverless": "ga", "stack": "ga 9.4"}
A new control is pinned to the dashboard header by default, where it applies to all panels. To place the control in the dashboard body instead, open its panel menu and select **Unpin**. When you place an unpinned control inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections), its filters apply only to the panels in that section. To move a control back to the header, select **Pin to Dashboard**. A dashboard supports up to 100 pinned controls.
:::

When you add several controls, their selections affect each other by default. How they interact depends on your version:

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
A selection in one control narrows the options available in all other controls on the dashboard, regardless of their position in the grid, including pinned controls. The exception is controls inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections), which only chain with other controls in the same section. To opt a control out of this default chaining, turn off its **Use global filters** setting when you create or edit it.
:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
Controls are applied from left to right. When the [Chain controls](dashboard-control-settings.md#configure-controls-settings) setting is enabled, the position of a control determines the options available in the next one.
:::
::::

### Populate control values with an {{esql}} query [populate-control-values-with-esql]
```{applies_to}
stack: ga 9.5
serverless: ga
```

Instead of basing an Options list or Range slider control on a data view field, you can populate its values with an {{esql}} query. This helps with high-cardinality fields, where fetching every distinct value can slow the dashboard, and it lets you filter or otherwise shape the values the control offers. The query can also reference [variable controls](add-variable-controls.md) with the `?variable_name` syntax to chain filtering.

1. In **Edit** mode, select **Add** > **Controls** > **Control**.
2. On the **Create control** flyout, select **Write a query**.
3. Write an {{esql}} query that returns a single column. The returned column determines the field the control is based on and the values it offers. Use a command such as `STATS BY` or `RENAME` to return a single column.
4. Select **Run query** to preview the values under **Values preview**. If the query returns more than one column, select a column from the list or narrow the query. If it returns no values, edit the query and run it again.
5. Under **Control type**, select **Options list** or **Range slider**. For a Range slider, the query results set the minimum and maximum values.
6. Configure the remaining settings, then select **Save**.
7. Save the dashboard.

## Add time slider controls [add-time-slider-controls]

You can add one interactive time slider control per dashboard. The time slider uses the dashboard's [global time filter](../query-filter/filtering.md) as its initial range.

:::{warning}
:applies_to: {"serverless": "ga", "stack": "ga 9.4"}
The time slider must be pinned to the dashboard header. It is not available as a free panel.
:::

1. Open or create a new dashboard.
2. Add a time slider control.

    ::::{applies-switch}
    :::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
    In **Edit** mode, select **Add** > **Controls** > **Time slider**.
    :::
    :::{applies-item} {"stack": "ga 9.2-9.3"}
    In **Edit** mode, select **Add** > **Controls** > **Time slider control**.
    :::
    :::{applies-item} {"stack": "ga 9.0-9.1"}
    In **Edit** mode, select **Controls** > **Add time slider control**.
    :::
    ::::

3. Save the dashboard. The control can now be used. To change its range, [change the global time filter](../query-filter/filtering.md).

## Edit controls [edit-controls]

Change the settings of an Options list or Range slider control.

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
1. Open the control's panel menu.
2. Select **Edit**.
3. In the **Edit control** flyout, change the options, then select **Save**.
:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
1. Hover over the control you want to edit, then select ![The Edit control icon that opens the Edit control flyout](/explore-analyze/images/kibana-dashboard_controlsEditControl_8.3.0.png "").
2. In the **Edit control** flyout, change the options, then select **Save**.
:::
::::

For the full list of available settings, refer to [Dashboard control settings](dashboard-control-settings.md).

## Clear, unpin, and delete controls [remove-controls]

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
Open the control's panel menu, then select an action:

- **Clear control** to reset the control's selections without changing its settings.
- **Unpin** to move a pinned control into the dashboard body, or **Pin to Dashboard** to move a control from the body into the header.
- **Remove** to delete the control from the dashboard.
:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
1. Hover over the control you want to delete, then select ![The Remove control icon that removes the control from the dashboard](/explore-analyze/images/kibana-dashboard_controlsRemoveControl_8.3.0.png "").
2. In the **Delete control?** window, select **Delete**.
:::
::::

:::{note}
If you delete a variable control that's used in an {{esql}} visualization, the visualization breaks. Edit the visualization query and remove or update the control reference.
:::
