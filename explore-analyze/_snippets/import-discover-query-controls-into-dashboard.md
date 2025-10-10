To add a Discover query to a dashboard in a way that preserves the [controls created from Discover](/explore-analyze/discover/try-esql.md#add-variable-control-discover) and also adds them to the dashboard, do as follows:

1. Save the {{esql}} query containing the variable control into a Discover session. If your Discover session contains several tabs, only the first tab will be imported to the dashboard.

1. Go to **Dashboards** and open or create one.

1. Select **Add**, then **From library**.

1. Find and select the Discover session you saved earlier.

A new panel with the results of the query is added to the dashboard, and any existing controls attached to that query are added to the dashboard.

![Importing Discover controls into a dashboard](/explore-analyze/images/import-discover-control-dashboard.png " =40%")

:::{note}
When directly adding the visualization to a dashboard using the {icon}`save` **Save visualization** option, controls are not added to the dashboard.
:::