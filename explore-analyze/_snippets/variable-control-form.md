* The type of the control. 
  * For controls with **Static values**, select the options available in the controls by entering them manually or by using a dropdown listing available values. 
  * For controls with **Values from a query**, write an {{esql}} query to populate the list of options.
* The name of the control. This name is used to reference the control in {{esql}} queries. 
  * Start the name with `?` if you want the options to be simple static values.
  * {applies_to}`stack: ga 9.1` Start the name with `??` if you want the options of the control to be fields or functions.
* The values users can select for this control. You can add multiple values from suggested fields, or type in custom values. If you selected **Values from a query**, you must instead write an {{esql}} query at this step.
* The label of the control. This is the label displayed in **Discover** or in the dashboard.
* The width of the control.

  ![ESQL control settings](/explore-analyze/images/esql-visualization-control-settings.png "title =50%")