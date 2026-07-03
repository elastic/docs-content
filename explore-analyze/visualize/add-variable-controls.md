---
navigation_title: Add variable controls
type: how-to
description: Create ES|QL-powered variable controls for Kibana dashboards to enable dynamic filtering, multi-value selections, and chained controls.
applies_to:
  stack: preview 9.0
  serverless: preview
products:
  - id: kibana
---

# Add variable controls to dashboards [add-variable-control]

Variable controls bind interactive controls to variables in your {{esql}} visualization queries. Unlike the standard [dashboard controls](dashboard-controls.md) that filter using data view fields, variable controls work directly with {{esql}} queries to enable dynamic filtering, grouping, and function selection.

:::{note}
:applies_to: {"stack": "ga 9.0-9.1"}
In versions 9.0 and 9.1, variable controls are called {{esql}} controls.
:::

## Before you begin [add-variable-controls-requirements]

To add variable controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* An {{esql}} visualization on your dashboard, or the intent to create one

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` A dashboard supports up to 100 pinned controls.

## Add variable controls [create-variable-control]

Variable controls act as variables in your {{esql}} visualization queries. Only **Options lists** are supported. A control's options can be:

- Values or fields, either static or defined by a query.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1` Functions.

You create a variable control while writing an {{esql}} query: the autocomplete suggests adding a control for field values, field names, function configuration, or function names.

:::{include} ../_snippets/variable-control-procedure.md
:::

The variable is inserted into your query directly, and you can keep editing the query. To reuse the control in another {{esql}} visualization, type the control's name in its query.

Where you place a variable control affects which panels it filters. For details, refer to [How controls affect the dashboard](dashboard-controls.md#controls-scope).

:::{tip}
:applies_to: {"stack": "ga 9.5", "serverless": "ga"}
In **Edit** mode, you can select a variable control's label to highlight the panels related to it: the panels within the control's scope whose {{esql}} query uses the control's variable. Only one control's related panels are highlighted at a time, and you can select the label again to stop highlighting them. A variable control that no visualization uses displays a warning.
:::

:::{include} ../_snippets/variable-control-examples.md
:::

## Allow multi-value selections [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

## Chain variable controls [chain-variable-controls]
```{applies_to}
stack: ga 9.3
serverless: ga
```

Chain variable controls so that the selection in one control determines the options available in another. This is useful when you work with data from multiple indices or need hierarchical filtering, because it narrows control selections dynamically without filtering the entire dashboard.

To chain variable controls, reference one control's variable in another control's {{esql}} query using the `?variable_name` syntax.

**Example**: You create a dashboard that analyzes web traffic by region and IP address. Next, you want to see only the IP addresses that are active in a selected region, and then analyze traffic patterns for a specific IP, all without filtering the entire dashboard by region.

![Chaining controls filtering an ES|QL visualization in a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltf697c4ba34f1baf8/6967d6ca03b22700081fadb3/dashboard-chaining-variable-controls.gif "=75%")

1. Create the first control that will be referenced in other controls.

   :::{tip}
   Create the controls that will be referenced in other controls first. This allows the {{esql}} editor to provide proper autocomplete suggestions.
   :::
   
   In **Edit** mode, select **Add** > **Controls** > **Variable control** in the application menu, then define the control:
   
   * **Type**: Values from a query
   * **Query**: 
     ```esql
     FROM kibana_sample_data_logs | WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart | STATS BY geo.dest
     ```
   * **Variable name**: `?region`
   * **Label**: Region
   
   This control extracts all unique destination regions from your logs.

2. Create the second control that depends on the first control.
   
   Add another variable control:
   
   * **Type**: Values from a query
   * **Query**: 
     ```esql
     FROM kibana_sample_data_logs 
     | WHERE @timestamp <= ?_tend AND @timestamp > ?_tstart AND geo.dest == ?region 
     | STATS BY ip
     ```
   * **Variable name**: `?ip`
   * **Label**: IP address
   
   This control references the `?region` variable and the built-in time range variables (`?_tstart` and `?_tend`). The available IP addresses will be only those associated with the selected region.

3. Test the chained controls. Both controls are now visible on your dashboard. Select different values in the **Region** control and observe how the available IP addresses in the **IP address** control change to show only IPs from that region.

4. Create an {{esql}} visualization that uses the `?ip` control to filter data. For example:
   
   ```esql
   FROM kibana_sample_data_logs
   | WHERE ip == ?ip
   | STATS count = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp)
   | SORT day
   ```
   
   This visualization filters data based on the selected IP address, while the IP address options themselves are filtered by the selected region.

:::{note}
When you select a value in a parent control, the child control's query reruns automatically. If the currently selected value in the child control is no longer available in the new result set, it is marked as invalid or incompatible.
:::

## Import a Discover query along with its controls into a dashboard [import-discover-query-controls]
```{applies_to}
stack: preview 9.2
serverless: preview
```

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

## Manage variable controls [manage-variable-controls]

You can edit or remove a variable control from the dashboard:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Open the control's panel menu, then select **Edit** or **Remove**.
- {applies_to}`stack: ga 9.0-9.3` Hover over the control, then select the edit or delete icon.

Editing opens the control's flyout, where you can change settings such as its query, variable name, and label. You can also update a control by editing the {{esql}} query that references it.

:::{note}
If you delete a variable control that's used in an {{esql}} visualization, the visualization breaks. Edit the visualization query and remove or update the control reference.
:::
