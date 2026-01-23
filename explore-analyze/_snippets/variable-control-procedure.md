1. While you edit your {{esql}} query, the autocomplete menu suggests adding a control when relevant or when you type `?` in the query. Select **Create control**.

   ![{{esql}} query prompting to add a control](/explore-analyze/images/esql-visualization-control-suggestion.png " =40%")

2. A menu opens to let you configure the control. This is where you can specify:

    * The type of the control. 
      * For controls with **Static values**, enter available controls manually or select them from the dropdown list. 
      * For controls with **Values from a query**, write an {{esql}} query to populate the list of options. This option is useful for dynamically retrieving control values or perform advanced actions such as [defining chaining controls](/explore-analyze/dashboards/add-controls.md#chain-variable-controls).
        :::{tip} - Only display values available for the selected time range
        By linking the control to the global time range, the control only shows values that exist within the time range selected in the dashboard or Discover session. You can do that by specifying `WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart` in the control's query, or [custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters) if your indices don't have a `@timestamp` field.
        :::
    * The name of the control. You use this name to reference the control in {{esql}} queries. 
      * Start the name with `?` if you want the options to be simple static values.
      * {applies_to}`stack: ga 9.1` Start the name with `??` if you want the options to be fields or functions.
    * The values users can select for this control. You can add multiple values from suggested fields, or type in custom values. If you selected **Values from a query**, you must instead write an {{esql}} query at this step.
    * The label of the control. This is the label displayed in **Discover** or in the dashboard.
    * The width of the control.
    * Whether the control should allow selecting a single value or multiple values. This [requires using the `MV_CONTAINS` function in your query](#esql-multi-values-controls). {applies_to}`stack: preview 9.3` {applies_to}`serverless: preview`

    ![{{esql}} control settings](/explore-analyze/images/esql-visualization-control-settings.png "title =40%")

3. Save the control.

The variable is inserted into your query, and the control appears.