---
navigation_title: Control settings
type: reference
description: Reference for all available dashboard control settings in Kibana, including options list, range slider, variable, and time slider controls.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Dashboard control settings [dashboard-control-settings]

The settings available depend on the control type.

## Options list and range slider settings [options-list-range-slider-settings]

Options lists and range sliders share most settings. A few are specific to one type: **Selections**, **Searching**, and **Ignore timeout for results** apply only to options lists, and **Step size** applies only to range sliders.

### Control settings [data-control-settings]

Set these in the control's editor: when you add the control, or later by hovering over the control and selecting **Edit**.

**Label**
:   Overwrite the default field name with a clearer label.

**Selections**
:   Options list only. Let viewers select multiple values (default), or restrict them to a single value where a new selection replaces the previous one.

**Searching**
:   Options list only. For text and IP address fields, how the search matches values: **Contains** (default for text, and text only), **Prefix** (default for IP address), or **Exact**. Searches aren't case sensitive.

**Step size**
:   Range slider only. Set the slider's step granularity. The smaller the step size, the more steps the slider has.

**Use global filters**
:   Whether the control's available options honor the dashboard's global filters, query, and time range, including the selections in other controls (chaining). Turn it off to always offer all values, independent of the rest of the dashboard. On by default.

    {applies_to}`stack: ga 9.0-9.3` In these versions, this behavior is set once for the whole dashboard, not per control, as three separate toggles: **Chain controls**, **Apply global filters to controls**, and **Apply global time range to controls**. Open the control settings dialog with **Add** → **Controls** → **Settings**; in 9.0 and 9.1, select **Controls** → **Settings** instead.

**Validate user selections**
:   Flag a selected value that returns no data once the dashboard's other filters and control selections are applied, so viewers can tell the selection is empty. On by default.

    {applies_to}`stack: ga 9.0-9.3` In these versions, this is set once for the whole dashboard in the same control settings dialog, applying to all controls.

**Ignore timeout for results**
:   Options list only. Wait to display results until the list is complete. Useful for large data sets, but the results might take longer to populate.

### Display settings [data-display-settings]

Display settings apply to pinned controls: hover over the control and select {icon}`gear` **Display settings**. Resize an unpinned control by dragging it, like any other panel.

**Width**
:   Set a minimum width, and whether the control expands to fill the available horizontal space.

    {applies_to}`stack: ga 9.0-9.3` In these versions, set the minimum width and expand option in the control's own settings.

### Dashboard settings [data-dashboard-settings]

In **Edit** mode, select **Settings** in the dashboard toolbar, then find the **Control panels** section.

**Auto apply filters** or **Apply selections automatically**
:   Choose whether the dashboard updates as soon as a selection is made, or only when you select **Apply**. Applies to all controls. Updates automatically by default.

    {applies_to}`stack: ga 9.0-9.3` In these versions, this is set in the control settings dialog, opened with **Add** → **Controls** → **Settings**; in 9.0 and 9.1, select **Controls** → **Settings** instead.

## Variable control settings [variable-control-settings]
```{applies_to}
serverless: preview
stack: preview 9.0
```

[Variable controls](add-variable-controls.md) get their values, variable name, and type when you create them. After that, these settings are available.

### Control settings [variable-editor-settings]

Set these in the control's editor: when you add the control, or later by hovering over the control and selecting **Edit**.

**Label**
:   Overwrite the default variable name with a clearer label.

**Selections**
:   Let viewers select a single value.

    {applies_to}`serverless: preview` {applies_to}`stack: preview 9.3` You can also allow multiple values.

### Display settings [variable-display-settings]

Display settings apply to pinned controls: hover over the control and select {icon}`gear` **Display settings**. Resize an unpinned control by dragging it, like any other panel.

**Width**
:   Set a minimum width, and whether the control expands to fill the available horizontal space.

    {applies_to}`stack: preview 9.0-9.3` In these versions, set the minimum width and expand option in the control's own settings.

Variable controls chain by referencing another control's variable in their {{esql}} query, not through a setting. For details, refer to [Chain variable controls](add-variable-controls.md#chain-variable-controls).

## Time slider settings [time-slider-settings]

A [time slider](add-time-slider-controls.md) has no field or value settings to configure. Its range comes from the dashboard's [global time range](../query-filter/filtering.md), and you can pin the start of the range so it stays fixed while the end extends. For details, refer to [Add a time slider control](add-time-slider-controls.md).
