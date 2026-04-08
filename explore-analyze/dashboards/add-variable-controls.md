---
type: how-to
description: Create ES|QL-powered variable controls for Kibana dashboards to enable dynamic filtering, multi-value selections, and chained controls.
applies_to:
  stack: preview 9.0
  serverless: preview
products:
  - id: kibana
---

# Add variable controls with ES|QL [add-variable-control]

Variable controls let you bind interactive controls to variables in your {{esql}} visualization queries. Unlike standard [dashboard controls](add-controls.md) that filter using data view fields, variable controls work directly with {{esql}} queries to enable dynamic filtering, grouping, and function selection.

:::{note}
:applies_to: stack: ga 9.0-9.1
In versions `9.0` and `9.1`, variable controls are called {{esql}} controls.
:::

## Before you begin

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* An {{esql}} visualization on your dashboard, or the intent to create one

## Create a variable control [create-variable-control]

You can bind controls to your {{esql}} visualizations in dashboards. When creating an {{esql}} visualization, the autocomplete suggestions prompt control insertion for field values, field names, function configuration, and function names. {{esql}} controls act as variables in your {{esql}} visualization queries.

{applies_to}`{ serverless: ga, stack: ga 9.4 }` When you add a variable control from an {{esql}} panel, for example, by choosing **Create control** from the autocomplete menu, you can place it **beside** the panel so the control appears directly next to the visualization that uses it. This enables controls that only apply to specific panels in your dashboards, and exposes visualization configuration such as date histogram interval controls to dashboard users.

Only **Options lists** are supported for {{esql}}-based controls. Options can be:
- values or fields that can be static or defined by a query
- {applies_to}`stack: ga 9.1` functions 

:::{include} ../_snippets/variable-control-procedure.md
:::

If you added it by starting from a query, the control is directly inserted in that query and you can continue editing it.
You can then insert it in any other {{esql}} visualization queries by typing the control's name.

:::{tip}
You can also create variable controls to add later to any query by selecting **Add** > **Controls** > **Variable control** in the dashboard's toolbar. 
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
serverless: ga
stack: ga 9.3+
```

You can set up variable controls in such a way that the selection of one control determines the options available for another control.

This allows you to narrow down control selections dynamically without affecting the entire dashboard, which is especially useful when working with data from multiple indices or when you need hierarchical filtering.

To chain variable controls, you reference one control's variable in another control's {{esql}} query using the `?variable_name` syntax.

**Example**: You create a dashboard that analyzes web traffic by region and IP address. Next, you want to see only the IP addresses that are active in a selected region, and then analyze traffic patterns for a specific IP, all without filtering the entire dashboard by region.

![Chaining controls filtering an {{esql}} visualization in a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltf697c4ba34f1baf8/6967d6ca03b22700081fadb3/dashboard-chaining-variable-controls.gif "=75%")

1. Create the first control that will be referenced in other controls.

   :::{tip}
   Create the controls that will be referenced in other controls first. This allows the {{esql}} editor to provide proper autocomplete suggestions.
   :::
   
   In **Edit** mode, select **Add** > **Controls** > **Variable control** in the toolbar, then define the control:
   
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

## Import a Discover query along with its controls [import-discover-query-controls]
```{applies_to}
stack: preview 9.2
serverless: preview
```

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::
