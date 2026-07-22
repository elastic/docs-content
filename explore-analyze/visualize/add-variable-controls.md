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

:::{include} ../_snippets/control-limits.md
:::

## Add variable controls [create-variable-control]

Variable controls act as variables in your {{esql}} visualization queries. On the dashboard, they appear as options lists. A control's options can be:

- Values or fields, either static or defined by a query.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.1` Functions.

You create a variable control while writing an {{esql}} query: the autocomplete suggests adding a control for field values, field names, function configuration, or function names.

On a dashboard, you can also add a variable control directly by selecting **Add** → **Controls** → **Variable control**.

:::{include} ../_snippets/variable-control-procedure.md
:::

For controls that use **Values from a query**, you can shape the options the control offers:

:::{include} ../_snippets/esql-query-control-value-examples.md
:::

You can reference the control in your {{esql}} visualization queries by typing its name.

Where you place a variable control affects which panels it filters. For details, refer to [How controls affect the dashboard](dashboard-controls.md#controls-scope).

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
stack: preview 9.3
serverless: preview
```

Chain variable controls so that the selection in one control determines the options available in another. This is useful when you work with data from multiple indices or need hierarchical filtering, because it narrows control selections dynamically without filtering the entire dashboard.

To chain variable controls, reference one control's variable in another control's {{esql}} query using the `?variable_name` syntax.

**Example**: You create a dashboard that analyzes web traffic by region and IP address. Next, you want to see only the IP addresses that are active in a selected region, and then analyze traffic patterns for a specific IP, all without filtering the entire dashboard by region.

![Chaining controls filtering an ES|QL visualization in a dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltf697c4ba34f1baf8/6967d6ca03b22700081fadb3/dashboard-chaining-variable-controls.gif "=75%")

1. Create the first control that will be referenced in other controls.

   :::{tip}
   Create the controls that will be referenced in other controls first. This allows the {{esql}} editor to provide proper autocomplete suggestions.
   :::
   
   In **Edit** mode, select **Add** → **Controls** → **Variable control** in the application menu, then define the control:
   
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

After a variable control is on your dashboard, you can edit it, adjust its display, move it, or delete it. How you access these actions depends on whether the control is pinned:

- **When pinned**, hover over the control to reveal its action icons.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` **When unpinned**, hover over the control to reveal its action icons, or open its panel menu, which adds standard panel actions such as **Duplicate** and **Copy to dashboard**.

| Action | Description |
| --- | --- |
| **Unpin** or **Pin to Dashboard** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` | Move the control between the top of the dashboard and the dashboard body. For details, refer to [Pinned and unpinned controls](dashboard-controls.md#pinned-unpinned-controls). |
| **Edit** | Change the control's query, variable name, label, and other settings in the control's flyout. You can also update a control by editing the {{esql}} query that references it. |
| **Display settings** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` | For pinned controls, set the minimum width and whether the control expands to fill the available space. Resize an unpinned control by dragging it, like any other panel. In earlier versions, set the width directly in the control's settings when you add or edit it. |
| **Remove** or **Delete** | Delete the control from the dashboard. |

:::{note}
If you delete a variable control that's used in an {{esql}} visualization, the visualization breaks. Edit the visualization query and remove or update the control reference.
:::
