---
navigation_title: Control settings
type: reference
description: Reference for all available dashboard control settings in Kibana, including options list, range slider, and shared control settings.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Dashboard control settings [dashboard-control-settings]

This page lists all available settings for [dashboard controls](dashboard-controls.md). Settings vary by control type and version. For instructions on adding controls to your dashboards, refer to [Add controls to dashboards](add-controls.md).

## Options list settings [options-list-settings]

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
- **Label**: Overwrite the default field name with a clearer label.
- **Selections**: Allow multiple selections, or restrict the control to a single selection.
- **Searching** (for string and IP address fields): Choose how the control's embedded search matches values.

  - **Prefix** (default for IP address fields): Match values that start with the entered text.
  - **Contains** (default for string fields): Match values that contain the entered text. Only available for string fields. Results can take longer to populate.
  - **Exact**: Match values that exactly equal the entered text.

  Searches are not case sensitive. For example, searching for `ios` still returns `iOS`.

- **Additional settings**:

  - **Use global filters**: When enabled (default), the control responds to the dashboard's filter chain. Turn it off to opt the control out of chaining.
  - **Validate user selections**: Highlight selections that return no data.
  - **Ignore timeout for results**: Wait to display results until the list is complete.

:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
- **Label**: Overwrite the default field name with a clearer label.
- **Minimum width**: Set how much horizontal space the control occupies. The final width can vary depending on the other controls and their width settings.
- **Expand width to fit available space**: Expand the control's width to fill the remaining horizontal space on the dashboard.
- **Selections**: Allow multiple selections, or restrict the control to a single selection.
- **Additional settings**:

  - **Ignore timeout for results**: Wait to display the list of values until it is fully loaded. Useful for large data sets, where some options might otherwise be missed if they take longer to appear.

  For Options list controls on string and IP address fields, choose how the control's embedded search matches values:

  - **Prefix**: Match values that start with the entered text.
  - **Contains**: Match values that contain the entered text. Only available for string fields. Results can take longer to populate.
  - **Exact**: Match values that exactly equal the entered text.

  Searches are not case sensitive. For example, searching for `ios` still returns `iOS`.
:::
::::

## Range slider settings [range-slider-settings]

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
- **Label**: Overwrite the default field name with a clearer label.
- **Step size**: Set the slider's step granularity. The smaller the step size, the more steps the slider has.
- **Additional settings**:
  - **Use global filters**: When enabled (default), the control responds to the dashboard's filter chain. Turn it off to opt the control out of chaining.
  - **Validate user selections**: Highlight selections that return no data.

:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
- **Label**: Overwrite the default field name with a clearer label.
- **Minimum width**: Set how much horizontal space the control occupies. The final width can vary depending on the other controls and their width settings.
- **Expand width to fit available space**: Expand the control's width to fill the remaining horizontal space on the dashboard.
- **Step size**: Set the slider's step granularity. The smaller the step size, the more steps the slider has.

:::
::::

## Shared control settings [configure-controls-settings]

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}

**Chaining**

Controls are chained by default: a selection in one control narrows the options available in all other controls on the dashboard. The exception is controls inside a [collapsible section](../dashboards/arrange-panels.md#collapsible-sections), which only chain with other controls in the same section. To opt a control out of chaining, turn off its **Use global filters** setting when you [create or edit it](add-controls.md#create-and-add-options-list-and-range-slider-controls).

**Pinned control display**

For pinned controls, select the {icon}`gear` **Settings** icon on the control to customize its display:

- **Minimum width**: Set how much horizontal space the control occupies. The final width can vary depending on the other controls and their width settings.
- **Expand width to fit available space**: Expand the control's width to fill the remaining horizontal space on the dashboard.

**Auto apply filters**

By default, the dashboard updates as soon as a selection is made in a control. To require an explicit apply step instead, open **Dashboard settings** and turn off **Auto apply filters**. When **Auto apply filters** is off, pending control selections are applied only when you select **Apply** in the unified search bar.
:::
:::{applies-item} {"stack": "ga 9.0-9.3"}

In versions earlier than 9.4, these settings apply to all controls on the dashboard at once. To open them, in **Edit** mode:

- {applies_to}`stack: ga 9.2-9.3` Select **Add** > **Controls** > **Settings** in the application menu.
- {applies_to}`stack: ga 9.0-9.1` Select **Controls** > **Settings**.

Available settings:

- **Label position**: Set where the control label appears.
- **Filtering**:
  - **Apply global filters to controls**: Define whether controls apply or ignore filters from the dashboard's main filter bar.
  - **Apply global time range to controls**: Define whether controls apply or ignore the dashboard's global time range. [Time slider controls](add-controls.md#add-time-slider-controls) rely on the global time range and don't work properly when this option is off.
- **Selections**:
  - **Validate user selections**: When on, any selection that returns no data is ignored.
  - **Chain controls**: On by default. When on, controls apply sequentially from left to right and line by line, so a selection in one control narrows the options in the next.
  - **Apply selections automatically**: When on, the dashboard updates as soon as a selection is made in a control. When off, users must select **Apply** to apply pending selections.

To remove all controls from the dashboard, select **Delete all**.
:::
::::
