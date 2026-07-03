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

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` A dashboard supports up to 100 pinned controls.

## Add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

1. Open or create a dashboard.
2. Open the **Create control** flyout:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** > **Controls** > **Control**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Add control** in the dashboard toolbar.

3. Choose how to populate the values available in the control:

    - **Select a field**: base the control on a [data view](../find-and-organize/data-views.md) field. The control offers the values found in that field.
    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5` **Write a query**: populate the control with the results of an {{esql}} query. Use this for high-cardinality fields, or when you want to filter or otherwise shape the values the control offers.

    Then select the matching option at the top of the flyout and configure it:

    ::::{tab-set}
    :::{tab-item} Select a field
    :sync: field
    1. From the **Data view** dropdown, select the data view that contains the field you want to use.
    2. In the **Field** list, select the field you want to filter on.
    :::

    :::{tab-item} Write a query
    :sync: query
    ```{applies_to}
    stack: ga 9.5
    serverless: ga
    ```
    1. Write an {{esql}} query that returns a single column. The column determines the field the control filters on and the values it offers. Use a command such as `STATS BY` to return a single column.
    2. Run the query to preview the values it returns under **Values preview**. If the query returns more than one column, select a column or narrow the query. If it returns no values, edit the query and run it again.

    To chain filtering, reference a [variable control](add-variable-controls.md) in the query with the `?variable_name` syntax.
    :::
    ::::

4. Under **Control type**, select **Options list** or **Range slider**. Range sliders are only compatible with number fields.

    :::{tip}
    :applies_to: {"serverless": "ga", "stack": "ga 9.5"}
    When you populate a Range slider with a query, the query results set the slider's minimum and maximum values.
    :::

5. Configure how the control looks and behaves. You can give it a clearer label, allow single or multiple selections, adjust how its search matches values, and set whether it chains with other controls. The available settings depend on the control type; for the complete list, refer to [Dashboard control settings](dashboard-control-settings.md).
6. Select **Save** to add the control to the dashboard. Viewers can now use it to filter the relevant panels.
7. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Choose where the control appears. A new control is pinned to the dashboard header by default, where it applies to all panels. To place it in the dashboard body instead, open its panel menu and select **Unpin**. An unpinned control inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections) filters only the panels in that section. To move a control back to the header, select **Pin to Dashboard**.
8. Save the dashboard to keep the control.

## Add time slider controls [add-time-slider-controls]

You can add one interactive time slider control per dashboard. The time slider uses the dashboard's [global time filter](../query-filter/filtering.md) as its initial range.

:::{warning}
:applies_to: {"serverless": "ga", "stack": "ga 9.4"}
The time slider must be pinned to the dashboard header. It is not available as a free panel.
:::

1. Open or create a new dashboard.
2. Add a time slider control:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** > **Controls** > **Time slider**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Add time slider control**.

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
