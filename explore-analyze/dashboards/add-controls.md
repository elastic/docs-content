---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-controls.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add filter controls [add-controls]

**Controls** are interactive panels that you add to your dashboards to help viewers filter and display only the data they want to explore quicker. Controls apply to all relevant panels in a dashboard.

There are three types of controls:

* [**Options list**](#create-and-add-options-list-and-range-slider-controls) — Adds a dropdown that allows to filter data by selecting one or more values.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add an options list for the `machine.os.keyword` field that allows you to display only the logs generated from `osx` and `ios` operating systems.
  ![Options list control for the `machine.os.keyword` field with the `osx` and `ios` options selected](/explore-analyze/images/kibana-dashboard_controlsOptionsList_8.7.0.png "title =50%")

* [**Range slider**](#create-and-add-options-list-and-range-slider-controls) — Adds a slider that allows to filter the data within a specified range of values. This type of control only works with numeric fields.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add a range slider for the `hour_of_day` field that allows you to display only the log data from 9:00AM to 5:00PM.
  ![Range slider control for the `hour_of_day` field with a range of `9` to `17` selected](/explore-analyze/images/kibana-dashboard_controlsRangeSlider_8.3.0.png "title =50%")

* [**Time slider**](#add-time-slider-controls) — Adds a time range slider that allows to filter the data within a specified range of time, advance the time range backward and forward by a unit that you can define, and animate your change in data over the specified time range.
  For example, you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, and the global time filter is **Last 7 days**. When you add the time slider, you can select the previous and next buttons to advance the time range backward or forward, and select the play button to watch how the data changes over the last 7 days.
  ![Time slider control for the the Last 7 days](/explore-analyze/images/dashboard_timeslidercontrol_8.17.0.gif)



## Create and add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

1. Open or create a new dashboard.
2. In **Edit** mode, select **Controls** > **Add control** in the dashboard toolbar.
3. On the **Create control** flyout, from the **Data view** dropdown, select the data view that contains the field you want to use for the **Control**.
4. In the **Field** list, select the field you want to filter on.
5. Under **Control type**, select whether the control should be an **Options list** or a **Range slider**.
   ::::{tip}
   Range sliders are for Number type fields only.
   ::::

6. Define how you want the control to appear:

    * **Label**: Overwrite the default field name with a clearer and self-explanatory label.
    * **Minimum width**: How much horizontal space does the control occupies. The final width can vary depending on the other controls and their own width setting.
    * **Expand width to fit available space**: Expand the width of the control to fit the available horizontal space on the dashboard.

7. Specify the additional settings:

    * For Options lists:

        * Define whether users can select multiple values to filter with the control, or only one.
        * For Options list controls on *string* and *IP address* type fields, you can define how the control’s embedded search should behave:

            * **Prefix**: Show options that *start with* the entered value.
            * **Contains**: Show options that *contain* the entered value. This setting option is only available for *string* type fields. Results can take longer to show with this option.
            * **Exact**: Show options that are a 100% match with the entered value.

              ::::{tip}
              The search is not case sensitive. For example, searching for `ios` would still retrieve `iOS` if that value exists.
              ::::

        * **Ignore timeout for results** delays the display of the list of values to when it is fully loaded. This option is useful for large data sets, to avoid missing some available options in case they take longer to load and appear when using the control.

    * For Range sliders, set the step size. The step size determines the number of steps of the slider. The smaller the step size is, the more steps there is in the slider.

8. Select **Save and close**. The control can now be used.
9. Consider the position of the control if you have several controls active on the dashboard. Controls are applied from left to right, which can change the options available depending on their position when the [Chain controls](#configure-controls-settings) setting is enabled.
10. Save the dashboard.


## Add time slider controls [add-time-slider-controls]

You can add one interactive time slider control to a dashboard.

1. Open or create a new dashboard.
2. In **Edit** mode, select **Controls** > **Add time slider control**.
3. The time slider control uses the time range from the global time filter. To change the time range in the time slider control, [change the global time filter](../query-filter/filtering.md).
4. Save the dashboard. The control can now be used.


## Add {{esql}} controls [add-esql-control]
```{applies_to}
stack: preview 9.0
serverless: preview
```

You can bind controls to your {{esql}} visualizations in dashboards. When creating an {{esql}} visualization, the autocomplete suggestions prompt control insertion for field values, field names, function configuration, and function names. {{esql}} controls act as variables in your {{esql}} visualization queries.

This enables controls that only apply to specific panels in your dashboards, and exposes visualization configuration such as date histogram interval controls to dashboard users.

:::{note}
Only **Options lists** are supported for {{esql}}-based controls. Options can be:
- values or fields that can be static or defined by a query
- functions {applies_to}`stack: ga 9.1`
:::

1. Use one of the following options to start creating an {{esql}} control:
   - **From the dashboard Controls menu**: In **Edit** mode, select **Controls** > **Add {{esql}} control** in the dashboard toolbar. {applies_to}`stack: ga 9.1`
   - **From your {{esql}} visualization's query**: While editing your {{esql}} visualization's query, the autocomplete menu suggests adding a control when relevant or when typing `?` in the query.

   ![ESQL query prompting to add a control](/explore-analyze/images/esql-visualization-control-suggestion.png)

2. A menu opens to let you configure the control. This is where you can specify:

    * The type of the control. 
      * For controls with **Static values**, you select the options available in the controls by entering them manually or by using a dropdown listing available values. 
      * For controls with **Values from a query**, you write an {{esql}} query to populate the list of options.
    * The name of the control. This name is used to reference the control in {{esql}} queries. 
      * Start the name with `?` if you want the options to be simple static values.
      * Start the name with `??` if you want the options of the control to be fields or functions. {applies_to}`stack: ga 9.1`
    * Values available to select for users with this control. You can add multiple values from suggested fields, or type in custom values. If you selected **Values from a query**, you must instead write an {{esql}} query at this step.
    * The label of the control. This is the label displayed for users viewing the dashboard for that control.
    * The width of the control.

    ![ESQL control settings](/explore-analyze/images/esql-visualization-control-settings.png "title =50%")

3. Save the control. 

The panel closes and the control is added to the dashboard.
If you added it by starting from a query, the control is directly inserted in that query and you can continue editing it.

You can then insert it in any other {{esql}} visualization queries by typing the control's name.


**Examples**

* Integrate filtering into your {{esql}} experience

  ```esql
  | WHERE field == ?value
  ```

* Fields in controls for dynamic group by

  ```esql
  | STATS count=COUNT(*) BY ?field
  ```

* Variable time ranges? Bind function configuration settings to a control

  ```esql
  | BUCKET(@timestamp, ?interval),
  ```

* Make the function itself dynamic

  ```esql
  | STATS metric = ?function
  ```

![Editing {{esql}} controls from a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blte42dfaa404bfc2d6/67d2e31e2e4dc59da190d78f/dashboard-esql-controls.gif)


## Configure the controls settings [configure-controls-settings]

Several settings that apply to all controls of the same dashboard are available.

1. In **Edit** mode, select **Controls** > **Settings**.
2. On the **Control settings** flyout, configure the following settings:

    * **Label position** — Specify where the control label appears.
    * **Filtering** settings:

        * **Apply global filters to controls** — Define whether controls should ignore or apply any filter specified in the main filter bar of the dashboard.
        * **Apply global time range to controls** — Define whether controls should ignore or apply the main time range specified for the dashboard. Note that [time slider controls](#add-time-slider-controls) rely on the global time range and don’t work properly when this option is disabled.

    * **Selections** settings:

        * **Validate user selections** — When selected, any selected option that results in no data is ignored.
        * **Chain controls** — When selected, controls are applied sequentially from left to right, and line by line. Any selected options in one control narrows the available options in the next control.
        * **Apply selections automatically** — The dashboard is updated dynamically when options are selected in controls. When this option is disabled, users first need to **Apply** their control selection before they are applied to the dashboard.

    * To remove all controls from the dashboard, select **Delete all**.

3. Select **Save and close** to apply the changes.


## Edit Options list and Range slider control settings [edit-controls]

Change the settings for Options list and Range slider controls.

1. Hover over the control you want to edit, then select ![The Edit control icon that opens the Edit control flyout](/explore-analyze/images/kibana-dashboard_controlsEditControl_8.3.0.png "").
2. In the **Edit control** flyout, change the options, then select **Save and close**.


## Delete controls [remove-controls]

Delete controls from your dashboard.

1. Hover over the control you want to delete, then select ![The Remove control icon that removes the control from the dashboard](/explore-analyze/images/kibana-dashboard_controlsRemoveControl_8.3.0.png "").
2. In the **Delete control?** window, select **Delete**.

:::{note}
If you delete an {{esql}} control that's used in an {{esql}} visualization, the visualization will break. You must edit the visualization query and remove or update the control reference.
:::
