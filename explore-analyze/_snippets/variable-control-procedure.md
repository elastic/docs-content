1. While you edit your {{esql}} query, the autocomplete menu suggests adding a control when relevant or when you type `?` in the query. Select **Create control**.

2. A flyout opens to let you configure the control. Specify:

    * The type of the control:
      * For controls with **Static values**, enter available values manually or select them from the dropdown list.
      * For controls with **Values from a query**, write an {{esql}} query that returns a single column to populate the list of options. Use this option to dynamically retrieve control values or to set up [chained controls](/explore-analyze/visualize/add-variable-controls.md#chain-variable-controls). This type is available only for controls that replace values, such as a host name or a number. Controls that replace field names, function names, or time intervals use **Static values**.

        :::{tip} - Only display values available for the selected time range
        To restrict the options to values that exist within the selected time range, add `WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart` to the control's query. If your indices don't have a `@timestamp` field, replace `@timestamp` with your time field, as described in [custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters).
        :::

    * The name of the control. You use this name to reference the control in {{esql}} queries. You can't change the name after you save the control, so the prefix is also fixed. The prefix tells {{esql}} what the control inserts into the query:
      * Start the name with `?` when the options are values, such as a host name, a number, or a time interval. The control inserts the value you select.
      * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1+` Start the name with `??` when the options are field names or function names. The control inserts the name you select.
    * The values users can select. You can add multiple values from suggested fields or type in custom values. If you selected **Values from a query**, write an {{esql}} query instead.
    * The label of the control. This is the label displayed in **Discover** or in the dashboard.
    * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.3+` Whether the control allows a single selection or multiple selections. Multiple selections require using the [`MV_CONTAINS`](#esql-multi-values-controls) function in your query.
      * {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` To match any selected value instead of all of them, use `MV_INTERSECTS` instead of `MV_CONTAINS`.

3. Save the control.

The control is created. If you created it while editing a query, its variable is inserted into that query, which you can keep editing.