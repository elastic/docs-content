---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-controls.html
navigation_title: Add controls
type: how-to
description: Add interactive filter controls to your Kibana dashboards to help users explore data with options lists and range sliders.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add Options list and Range slider controls to dashboards [add-controls]

Add interactive [controls](dashboard-controls.md) to your dashboards to help viewers filter data without writing queries. This page covers how to add, edit, and remove Options list and Range slider controls.

To add other control types, refer to [Add time slider controls](add-time-slider-controls.md) or [Add variable controls](add-variable-controls.md).

:::{tip}
:applies_to: {"stack": "preview 9.5", "serverless": "preview"}
You can also ask [{{agent-builder}}](/explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md) to add Options list and Range slider controls when it creates or updates a dashboard through chat.
:::

## Before you begin [add-controls-requirements]

To add Options list and Range slider controls to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

:::{include} ../_snippets/control-limits.md
:::

## Add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

1. Open or create a dashboard.
2. Open the **Create control** flyout:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** → **Controls** → **Control**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** → **Add control** in the dashboard toolbar.

3. Choose how to populate the values available in the control:

    - **Select a field**: base the control on a [data view](../find-and-organize/data-views.md) field. The control offers the values found in that field.

        1. From the **Data view** dropdown, select the data view that contains the field you want to use.
        2. In the **Field** list, select the field you want to filter on.

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5` **Write a query**: populate the control with the results of an {{esql}} query. Use this for high-cardinality fields, where listing every value isn't practical, or when you want to filter or otherwise shape the values the control offers.

        1. Write an {{esql}} query that returns a single column. The column determines the field the control filters on and the values it offers. Use a command such as `STATS BY` to return a single column.
        2. Run the query to preview the values it returns under **Values preview**. If the query returns more than one column, select a column or narrow the query. If it returns no values, edit the query and run it again.

        :::{tip}
        Because the values come from a query, you can also chain the control to a [variable control](add-variable-controls.md) by referencing its variable with the `?variable_name` syntax.
        :::

4. Under **Control type**, select **Options list** or **Range slider**. Range sliders are only compatible with numeric fields. The slider's minimum and maximum come from the data: the field's values, or the query results if you populate it with a query.

5. Configure how the control looks and behaves. You can give it a clearer label, allow single or multiple selections, adjust how its search matches values, and set whether it [chains with other controls](dashboard-controls.md#controls-chaining). The available settings depend on the control type. For the complete list, refer to [Dashboard control settings](dashboard-control-settings.md).
6. Select **Save** to add the control to the dashboard. The control appears right away in **Edit** mode, where you can test it and adjust its settings before viewers see it.
7. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Choose where the control appears. New controls are pinned to the top of the dashboard by default, where they apply to all panels. To move a control into the dashboard body, hover over the control and select **Unpin**. To move it back, select **Pin to dashboard**. Once unpinned, you can move, resize, and arrange the control on the dashboard like any other panel, including placing it inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections) to scope it to that section's panels. Placement changes which panels a control filters. For details, refer to [How controls affect the dashboard](dashboard-controls.md#controls-scope).
8. Save the dashboard. The control becomes a permanent part of it, and viewers can use it to filter the relevant panels.

:::{note}
When a dashboard has more than one control, the controls interact:

* By default, selecting a value in one control updates the others to show only values that still return data. This behavior is called [chaining](dashboard-controls.md#controls-chaining). You can turn it off for a control with its **Use global filters** setting.
* If a value you already selected no longer matches any data, the control marks it as invalid, as long as **Validate user selections** is on (the default).
:::

## Manage Options list and Range slider controls [manage-controls]

After adding a control to your dashboard, you can change its settings, clear its values, move it, adjust its width, or delete it. How you access these actions depends on whether the control is pinned:

- **When pinned**, hover over the control to reveal its action icons.
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` **When unpinned**, hover over the control to reveal its action icons, or open its panel menu, which adds standard panel actions such as **Duplicate** and **Copy to dashboard**.

| Action | Description |
| --- | --- |
| **Clear** | Clear the selected values without changing the control's settings. Available only when a value is selected. |
| **Unpin** or **Pin to Dashboard** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` | Move the control between the top of the dashboard and the dashboard body. For details, refer to [Pinned and unpinned controls](dashboard-controls.md#pinned-unpinned-controls). |
| **Edit** | Change the control's field, type, query, and other settings in the **Edit control** flyout. For the full list, refer to [Dashboard control settings](dashboard-control-settings.md). |
| **Display settings** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` | For pinned controls, set the minimum width and whether the control expands to fill the available space. Resize an unpinned control by dragging it, like any other panel. In earlier versions, set the width directly in the control's settings when you add or edit it. |
| **Remove** or **Delete** | Delete the control from the dashboard. |
