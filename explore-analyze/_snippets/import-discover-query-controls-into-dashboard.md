To add the results of your Discover explorations to a dashboard in a way that preserves the [controls created from Discover](/explore-analyze/discover/try-esql.md#add-variable-control) and also adds them to the dashboard, you have two methods:

**Method 1: Adding the Discover session's results**

This method allows you to add the result table of your Discover {{esql}} query to any dashboard.

1. Save the {{esql}} query containing the variable control into a Discover session. If your Discover session contains several tabs, only the first tab will be imported to the dashboard.

1. Go to **Dashboards** and open or create one.

1. Select **Add**, then **From library**.

1. Find and select the Discover session you saved earlier.

A new panel appears on the dashboard with the results of the query along with any attached controls.

![Importing Discover session with controls into a dashboard](/explore-analyze/images/import-discover-control-dashboard.png " =40%")

**Method 2: Adding the Discover visualization** {applies_to}`serverless:` {applies_to}`stack: ga 9.3`

This method allows you to add the visualization of your Discover {{esql}} query to any dashboard.

1. Next to the Discover visualization, select {icon}`save` **Save visualization**.

   ![Importing Discover visualization with controls into a dashboard](/explore-analyze/images/save-discover-viz-to-dashboard.png " =70%")

1. Select the dashboard to add the visualization to. You can choose an existing dashboard or create one.

The selected dashboard opens. It now includes a new panel that shows the visualization imported from Discover. Existing controls from the initial query in Discover are also added. You can find them at the top of the dashboard.

