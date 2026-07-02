---
type: overview
description: Learn about interactive filter controls for Kibana dashboards, including options lists, range sliders, time sliders, and ES|QL variable controls.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Dashboard controls [dashboard-controls]

**Controls** are interactive panels that you add to your dashboards to help viewers filter and display only the data they want to explore. Controls apply filters to relevant panels so viewers can focus on specific data segments without writing filtering queries.

Controls can be **pinned** to the dashboard header, where they apply to all panels, or **unpinned** and placed anywhere in the dashboard body. When an unpinned control sits inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections), its filters apply only to the panels within that section.

{applies_to}`stack: ga 9.4` A dashboard supports up to 100 pinned controls.

:::{note}
:applies_to: {"stack": "ga 9.0-9.3"}
In versions earlier than 9.4, controls are always pinned to the dashboard header, and settings such as chaining and validation apply to all controls on the dashboard at once. Refer to [Dashboard control settings](dashboard-control-settings.md) to manage these shared settings.
:::

## Requirements [dashboard-controls-requirements]

To add controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

## Control types [control-types]

There are four types of controls:

* **Options list**: A dropdown that filters data by one or more selected values.
  For example, in the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add an options list for the `machine.os.keyword` field to display only the logs generated from `osx` and `ios` operating systems.

  ![Options list control for the `machine.os.keyword` field with the `osx` and `ios` options selected](/explore-analyze/images/kibana-dashboard-controls-options-list.png "title =50%")

* **Range slider**: A slider that filters data within a specified range of values. Only compatible with numeric fields.
  For example, in the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add a range slider for the `hour_of_day` field to display only the log data from 9:00 AM to 5:00 PM.

  ![Range slider control for the `hour_of_day` field with a range of `9` to `17` selected](/explore-analyze/images/kibana-dashboard-controls-range-slider.png "title =50%")

* **Time slider**: A time range slider that filters data within a specified time range. Advance the range backward and forward, or animate the data change across the range.

  ![Time slider control for the Last 7 days](/explore-analyze/images/dashboard_timeslidercontrol_8.17.0.gif)

* **Variable control**: An {{esql}}-powered control that binds to variables in {{esql}} visualization queries, enabling dynamic filtering, grouping, and function selection.

## Next steps

* [Add controls to dashboards](add-controls.md): Add options list, range slider, and time slider controls to your dashboards.
* [Add variable controls with ES|QL](add-variable-controls.md): Create {{esql}}-powered controls for dynamic filtering and chaining.
* [Dashboard control settings](dashboard-control-settings.md): Reference for all available control settings per type and version.
