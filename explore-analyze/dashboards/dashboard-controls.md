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

**Controls** are interactive panels that you add to your dashboards to help viewers filter and display only the data they want to explore. Controls apply filters to relevant panels to focus on specific data segments without writing filtering queries.

Controls can be **pinned** to the dashboard header, where they apply to all panels, or **unpinned** and placed anywhere in the dashboard body. When an unpinned control is inside a [collapsible section](arrange-panels.md#collapsible-sections), its filters apply only to panels within that section. Refer to [Organize dashboard panels](arrange-panels.md#collapsible-sections) for how section placement affects filter scope.

:::{note}
:applies_to: stack: ga 9.0-9.3
Up until version 9.3, controls are always pinned to the dashboard header and some settings such as chaining and validation apply to all controls at once. Refer to [Dashboard control settings](dashboard-control-settings.md) to manage these shared settings.
:::

## Requirements [dashboard-controls-requirements]

To add controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

## Control types [control-types]

There are four types of controls:

* **Options list** — A dropdown that allows to filter data by selecting one or more values.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add an options list for the `machine.os.keyword` field that allows you to display only the logs generated from `osx` and `ios` operating systems.

  ![Options list control for the `machine.os.keyword` field with the `osx` and `ios` options selected](/explore-analyze/images/kibana-dashboard_controlsOptionsList.png "title =50%")

* **Range slider** — A slider that allows to filter the data within a specified range of values. This type of control only works with numeric fields.
  For example, if you are using the **[Logs] Web Traffic** dashboard from the sample web logs data, you can add a range slider for the `hour_of_day` field that allows you to display only the log data from 9:00AM to 5:00PM.

  ![Range slider control for the `hour_of_day` field with a range of `9` to `17` selected](/explore-analyze/images/kibana-dashboard_controlsRangeSlider_8.3.0.png "title =50%")

* **Time slider** — A time range slider that allows to filter the data within a specified range of time, advance the time range backward and forward, and animate your change in data over the specified time range.

  ![Time slider control for the Last 7 days](/explore-analyze/images/dashboard_timeslidercontrol_8.17.0.gif)

* **Variable control** — An {{esql}}-powered control that binds to variables in {{esql}} visualization queries, enabling dynamic filtering, grouping, and function selection.

## Next steps

* [Add controls to dashboards](add-controls.md): Add options list, range slider, and time slider controls to your dashboards.
* [Add variable controls with ES|QL](add-variable-controls.md): Create {{esql}}-powered controls for dynamic filtering and chaining.
* [Dashboard control settings](dashboard-control-settings.md): Reference for all available control settings per type and version.
