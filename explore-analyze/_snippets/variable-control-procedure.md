1. While you edit your {{esql}} query, the autocomplete menu suggests adding a control when relevant or when you type `?` in the query. Select **Create control**.

   :::{image} /explore-analyze/images/esql-visualization-control-suggestion.png
   :alt: ES|QL query prompting to add a control
   :width: 40%
   :screenshot:
   :::

2. A flyout opens to let you configure the control. Specify:

    * The type of the control:
      * For controls with **Static values**, enter available values manually or select them from the dropdown list.
      * For controls with **Values from a query**, write an {{esql}} query to populate the list of options. Use this option to dynamically retrieve control values or to set up [chained controls](/explore-analyze/visualize/add-variable-controls.md#chain-variable-controls).

        :::{tip}
        To restrict the options to values that exist within the selected time range, add `WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart` to the control's query. If your indices don't have a `@timestamp` field, use [custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters) instead.
        :::

    * The name of the control. You use this name to reference the control in {{esql}} queries.
      * Start the name with `?` for options that are static values.
      * {applies_to}`stack: ga 9.1` Start the name with `??` for options that are fields or functions.
    * The values users can select. You can add multiple values from suggested fields or type in custom values. If you selected **Values from a query**, write an {{esql}} query instead.
    * The label of the control. This is the label displayed in **Discover** or in the dashboard.
    * {applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` Whether the control allows a single selection or multiple selections. Multiple selections require using the [`MV_CONTAINS` or `MV_INTERSECTS`](#esql-multi-values-controls) functions in your query.

3. Save the control.

The variable is inserted into your query, and the control appears.