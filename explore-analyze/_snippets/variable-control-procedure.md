1. While you edit your {{esql}} query, the autocomplete menu suggests adding a control when relevant or when you type `?` in the query. Select **Create control**.

   ![{{esql}} query prompting to add a control](/explore-analyze/images/esql-visualization-control-suggestion.png " =40%")

2. A menu opens to let you configure the control. This is where you can specify:

    * The type of the control. 
      * For controls with **Static values**, enter available controls manually or select them from the dropdown list. 
      * For controls with **Values from a query**, write an {{esql}} query to populate the list of options.
    * The name of the control. You use this name to reference the control in {{esql}} queries. 
      * Start the name with `?` if you want the options to be simple static values.
      * Start the name with `??` if you want the options to be fields or functions. {applies_to}`stack: ga 9.1`
    * The values users can select for this control. You can add multiple values from suggested fields, or type in custom values. If you selected **Values from a query**, you must instead write an {{esql}} query at this step.
    * The label of the control. This is the label displayed in **Discover** or in the dashboard.
    * The width of the control.
    * Whether the control should allow selecting a single value or multiple values. This [requires using the `MV_CONTAINS` function in your query](#esql-multi-values-controls). {applies_to}`stack: preview 9.3` {applies_to}`serverless: preview`

    ![{{esql}} control settings](/explore-analyze/images/esql-visualization-control-settings.png "title =40%")

3. Save the control.

The variable is inserted into your query, and the control appears.