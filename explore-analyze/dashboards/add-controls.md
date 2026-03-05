---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-controls.html
description: Add interactive filter controls to your Kibana dashboards to help users explore data with options lists, range sliders, and time sliders.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add filter controls [add-controls]

**Controls** are interactive panels that you add to your dashboards to help future viewers filter and display only the data they want to explore more efficiently. Controls apply filters to relevant panels to focus on specific data segments without writing filtering queries.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` 

**Pinned** control
:   Appear in the dashboard's sticky header and apply to the whole dashboard. 

**Unpinned** control 
:   Live in the dashboard body; when a control is inside a [collapsible section](arrange-panels.md#collapsible-sections), its filters apply only to panels within that section. Controls outside sections (or pinned) have global scope. Refer to [Organize dashboard panels](arrange-panels.md#collapsible-sections) for how section placement affects filter scope.

**Universally chained** control
:   A change in one control will impact all other controls on the dashboard, regardless of their positioning in the grid, including pinned controls. The only exception to this is controls within a collapsible section. These controls will only chain with other controls in their section. This is the default behaviour of controls. If you want to change this behaviour, turn off the **Use global filters** setting.

## Requirements [add-controls-requirements]

To add controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

## Control types [control-types]

There are three types of controls:

* [**Options list**](#create-and-add-options-list-and-range-slider-controls) — Adds a dropdown that allows to filter data by selecting one or more values.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add an options list for the `machine.os.keyword` field that allows you to display only the logs generated from `osx` and `ios` operating systems.

  ![Options list control for the `machine.os.keyword` field with the `osx` and `ios` options selected](/explore-analyze/images/kibana-dashboard_controlsOptionsList.png "title =50%")

* [**Range slider**](#create-and-add-options-list-and-range-slider-controls) — Adds a slider that allows to filter the data within a specified range of values. This type of control only works with numeric fields.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add a range slider for the `hour_of_day` field that allows you to display only the log data from 9:00AM to 5:00PM.

  ![Range slider control for the `hour_of_day` field with a range of `9` to `17` selected](/explore-analyze/images/kibana-dashboard_controlsRangeSlider_8.3.0.png "title =50%")

* [**Time slider**](#add-time-slider-controls) — Adds a time range slider that allows to filter the data within a specified range of time, advance the time range backward and forward by a unit that you can define, and animate your change in data over the specified time range.
  For example, you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, and the global time filter is **Last 7 days**. When you add the time slider, you can select the previous and next buttons to advance the time range backward or forward, and select the play button to watch how the data changes over the last 7 days.

  ![Time slider control for the Last 7 days](/explore-analyze/images/dashboard_timeslidercontrol_8.17.0.gif)

## Create and add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

1. Open or create a new dashboard.
2. Add a control.
       
    {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` 
    - Add as pinned control: In **Edit** mode, select **Add** > **Controls** > **Control**. The control is pinned and applies to the whole dashboard.
    - Add as free panel: Select **Add new panel** > **Controls**, then place the control on the dashboard. If you place a control inside a [collapsible section](arrange-panels.md#collapsible-sections), its filters apply only to panels in that section. To move a control between the header and the dashboard body, open the control's panel menu and select **Pin to top** or **Unpin**.
    
    {applies_to}`serverless:` {applies_to}`stack: ga 9.2-9.3` 
    
    In **Edit** mode, select **Add** > **Controls** > **Control** in the toolbar.
    
    {applies_to}`stack: ga 9.0-9.1` 
    
    In **Edit** mode, select **Controls** > **Add control** in the dashboard toolbar.

3. On the **Create control** flyout, from the **Data view** dropdown, select the data view that contains the field you want to use for the **Control**.
4. In the **Field** list, select the field you want to filter on.
5. Under **Control type**, select whether the control should be an **Options list** or a **Range slider**.
   ::::{tip}
   Range sliders are for Number type fields only.
   ::::

6. Define how you want the control to appear:

    * **Label**: Overwrite the default field name with a clearer and self-explanatory label.
    * **Minimum width**: Specify how much horizontal space does the control should occupy. The final width can vary depending on the other controls and their own width setting.
    * **Expand width to fit available space**: Expand the width of the control to fit the available horizontal space on the dashboard.

    {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` 
    For pinned controls, the settings **Minimum width** and **Expand width to fit available space** are available by clicking the     Settings {icon}`gear` on the control.


7. Specify the additional settings:

    * For Options lists:

        * Define whether users can select multiple values to filter with the control, or only one.
        * For Options list controls on *string* and *IP address* type fields, you can define how the control’s embedded search should behave:

            * **Prefix**: Show options that *start with* the entered value.
            * **Contains**: Show options that *contain* the entered value. This setting option is only available for *string* type fields. Results can take longer to show with this option.
            * **Exact**: Show options that are an *exact* match with the entered value.

              ::::{tip}
              The search is not case sensitive. For example, searching for `ios` would still retrieve `iOS` if that value exists.
              ::::

        * **Ignore timeout for results**: Delays the display of the list of values until it is fully loaded. This option is useful for large data sets, to avoid missing some available options in case they take longer to load and appear when using the control.

    * For Range sliders, set the step size. The step size determines the slider's number of steps. The smaller a slider's step size, the more steps it has.

8. Select **Save**. The control can now be used.
9. Consider control order when you have several controls.

   {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Controls are chained by default: each control narrows the options available in subsequent controls based on position. 
   {applies_to}`stack: ga 9.0-9.3` Controls are applied from left to right; when the [Chain controls](#configure-controls-settings) setting is enabled, their position changes the options available in the next control.

10. Save the dashboard.

## Add variable controls [add-variable-control]
```{applies_to}
stack: preview 9.0
serverless: preview
```

In versions `9.0` and `9.1`, variable controls are called {{esql}} controls.

You can bind controls to your {{esql}} visualizations in dashboards. When creating an {{esql}} visualization, the autocomplete suggestions prompt control insertion for field values, field names, function configuration, and function names. {{esql}} controls act as variables in your {{esql}} visualization queries.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` 
When you add a variable control from an {{esql}} panel, for example, by choosing **Create control** from the autocomplete menu, you can place it **beside** the panel so the control appears directly next to the visualization that uses it.

This enables controls that only apply to specific panels in your dashboards, and exposes visualization configuration such as date histogram interval controls to dashboard users.

Only **Options lists** are supported for {{esql}}-based controls. Options can be:
- values or fields that can be static or defined by a query
- {applies_to}`stack: ga 9.1` functions 

:::{include} ../_snippets/variable-control-procedure.md
:::

If you added it by starting from a query, the control is directly inserted in that query and you can continue editing it.
You can then insert it in any other {{esql}} visualization queries by typing the control's name.

:::{tip}
You can also create variable controls to add later to any query by selecting **Add** > **Controls** > **Variable control** in the dashboard's toolbar. 
:::

![Editing {{esql}} controls from a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte42dfaa404bfc2d6/67d2e31e2e4dc59da190d78f/dashboard-esql-controls.gif)

:::{include} ../_snippets/variable-control-examples.md
:::

### Allow multi-value selections for {{esql}}-based variable controls [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

### Make variable control values depend on another variable control [chain-variable-controls]
```{applies_to}
serverless: ga
stack: ga 9.3+
```

You can set up variable controls in such a way that the selection of one control determines the options available for another control.

This allows you to narrow down control selections dynamically without affecting the entire dashboard, which is especially useful when working with data from multiple indices or when you need hierarchical filtering.

To chain variable controls, you reference one control's variable in another control's {{esql}} query using the `?variable_name` syntax.

**Example**: You create a dashboard that analyzes web traffic by region and IP address. Next, you want to see only the IP addresses that are active in a selected region, and then analyze traffic patterns for a specific IP, all without filtering the entire dashboard by region.

![Chaining controls filtering an {{esql}} visualization in a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltf697c4ba34f1baf8/6967d6ca03b22700081fadb3/dashboard-chaining-variable-controls.gif "=75%")

1. Create the first control that will be referenced in other controls.

   :::{tip}
   Create the controls that will be referenced in other controls first. This allows the {{esql}} editor to provide proper autocomplete suggestions.
   :::
   
   In **Edit** mode, select **Add** > **Controls** > **Variable control** in the toolbar, then define the control:
   
   * **Type**: Values from a query
   * **Query**: 
     ```esql
     FROM kibana_sample_data_logs | WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart | STATS BY geo.dest
     ```
   * **Variable name**: `?region`
   * **Label**: Region
   
   This control extracts all unique destination regions from your logs.

2. Create the second control that depends on the first control.
   
   Add another variable control:
   
   * **Type**: Values from a query
   * **Query**: 
     ```esql
     FROM kibana_sample_data_logs 
     | WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart AND geo.dest == ?region 
     | STATS BY ip
     ```
   * **Variable name**: `?ip`
   * **Label**: IP address
   
   This control references the `?region` variable and the built-in time range variables (`?_tstart` and `?_tend`). The available IP addresses will be only those associated with the selected region.

3. Test the chained controls. Both controls are now visible on your dashboard. Select different values in the **Region** control and observe how the available IP addresses in the **IP address** control change to show only IPs from that region.

4. Create an {{esql}} visualization that uses the `?ip` control to filter data. For example:
   
   ```esql
   FROM kibana_sample_data_logs
   | WHERE ip == ?ip
   | STATS count = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp)
   | SORT day
   ```
   
   This visualization filters data based on the selected IP address, while the IP address options themselves are filtered by the selected region.

:::{note}
When you select a value in a parent control, the child control's query reruns automatically. If the currently selected value in the child control is no longer available in the new result set, it is marked as invalid or incompatible.
:::

### Import a Discover query along with its controls into a dashboard
```{applies_to}
stack: preview 9.2
serverless: preview
```

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

## Add time slider controls [add-time-slider-controls]

You can add one interactive time slider control to a dashboard.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
The time slider can only be added as a pinned control (to the sticky header). It is not available as a free panel.

1. Open or create a new dashboard.
2. Add a time slider control.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In **Edit** mode, select **Add** > **Controls** > **Time slider control** in the toolbar.
    * {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Add time slider control**.

3. The time slider control uses the time range from the global time filter. To change the time range in the time slider control, [change the global time filter](../query-filter/filtering.md).
4. Save the dashboard. The control can now be used.

## Configure the controls settings [configure-controls-settings]

Several settings apply to all controls that are part of a dashboard.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
Controls are always chained: each control narrows the options available in subsequent controls. The **Control settings** flyout no longer has a **Chain controls** toggle. **Auto apply filters** is a dashboard-level setting: when it is disabled, users apply pending control selections using the unified search **Apply** button.

1. Configure the control settings.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In **Edit** mode, select **Add** > **Controls** > **Settings** in the toolbar.
    * {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Settings**.

2. On the **Control settings** flyout, configure the following settings:

    * **Label position** — Specify where the control label appears.
    * **Filtering** settings:

        * **Apply global filters to controls** — Define whether controls should ignore or apply any filter specified in the main filter bar of the dashboard.
        * **Apply global time range to controls** — Define whether controls should ignore or apply the main time range specified for the dashboard. Note that [time slider controls](#add-time-slider-controls) rely on the global time range and don’t work properly when this option is disabled.

    * **Selections** settings:

        * **Validate user selections** — When selected, any selected option that results in no data is ignored.
        * {applies_to}`stack: ga 9.0-9.3` **Chain controls** — When selected, controls are applied sequentially from left to right, and line by line. Any selected options in one control narrows the available options in the next control.
        * {applies_to}`stack: ga 9.0-9.3` **Apply selections automatically** — The dashboard is updated dynamically when options are selected in controls. When this option is disabled, users first need to **Apply** their control selection before they are applied to the dashboard.
        * {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` **Auto apply filters** — When enabled (default), the dashboard updates as soon as options are selected in controls. When disabled, users must click the unified search **Apply** button to apply pending control selections.

    * To remove all controls from the dashboard, select **Delete all**.

3. Select **Save** to apply the changes.


## Edit Options list and Range slider control settings [edit-controls]

Change the settings for Options list and Range slider controls.

1. Hover over the control you want to edit, then select ![The Edit control icon that opens the Edit control flyout](/explore-analyze/images/kibana-dashboard_controlsEditControl_8.3.0.png "").
2. In the **Edit control** flyout, change the options, then select **Save and close**.


## Delete controls [remove-controls]

Delete controls from your dashboard.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga`
To remove a control from view without deleting it, use **Unpin** from the control's panel menu; the control moves into the dashboard body. To remove it from the dashboard entirely, use **Delete** from the panel menu.

1. Hover over the control you want to delete, then select ![The Remove control icon that removes the control from the dashboard](/explore-analyze/images/kibana-dashboard_controlsRemoveControl_8.3.0.png "").
2. In the **Delete control?** window, select **Delete**.

:::{note}
If you delete an variable control that's used in an {{esql}} visualization, the visualization will break. You must edit the visualization query and remove or update the control reference.
:::
