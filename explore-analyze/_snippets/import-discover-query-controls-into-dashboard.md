To add the results of your Discover explorations to a dashboard in a way that preserves the [controls created from Discover](/explore-analyze/discover/esql-variable-controls.md#add-variable-control) and also adds them to the dashboard, you have two methods:

**Method 1: Adding the Discover session's results**

This method allows you to add the result table of your Discover {{esql}} query to any dashboard.

1. Save the {{esql}} query containing the variable control into a Discover session. If your Discover session contains several tabs:
   - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` You can select which tab the panel displays after adding the session to a dashboard.
   - {applies_to}`stack: ga 9.2-9.3` Only the first tab is imported to the dashboard.

1. Go to **Dashboards** and open or create one.

1. Select **Add**, then **From library**.

1. Find and select the Discover session you saved earlier.

A new panel appears on the dashboard with the results of the query along with any attached controls. If the dashboard already has a control with the same variable name, {{kib}} doesn't add a second one and keeps the existing control as it is. The new panel then responds to that control's current selection.

:::{image} /explore-analyze/images/import-discover-control-dashboard.png
:alt: Importing Discover session with controls into a dashboard
:width: 40%
:screenshot:
:::

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.3+` **Method 2: Adding the Discover visualization**

This method allows you to add the visualization of your Discover {{esql}} query to any dashboard.

1. Next to the Discover visualization, select {icon}`add_to_dashboard` **Save visualization to dashboard**. In 9.3, the button is {icon}`save` **Save visualization**.

   :::{image} /explore-analyze/images/save-discover-viz-to-dashboard.png
   :alt: The Save visualization to dashboard button next to the Discover chart, with its tooltip.
   :width: 70%
   :screenshot:
   :::

1. Select the dashboard to add the visualization to. You can select an existing dashboard or create one.

The selected dashboard opens. It now includes a new panel that shows the visualization imported from Discover. Existing controls from the initial query in Discover are also added. You can find them at the top of the dashboard.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the dashboard already has a control for the same variable, saving the visualization updates that control instead of adding a second one. The control takes the selection and settings from Discover and keeps its position, whether it's pinned or unpinned. Controls match when they have the same variable name and both use **Static values**, or both use **Values from a query**. If the existing control is inside a section, {{kib}} doesn't update it and adds the control from Discover as a second control.

