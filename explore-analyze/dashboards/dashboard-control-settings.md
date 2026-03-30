---
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
:::{applies-item} { serverless: ga, stack: ga 9.4 }
 * **Label**: Overwrite the default field name with a clearer and self-explanatory label.
 - **Selections**:
   Select multiple values to filter with the control, or only one.
 - **Searching** (for Options list controls on *string* and *IP address* type fields):

   * **Prefix**: Show options that *start with* the entered value.
   * **Contains**: Show options that *contain* the entered value. This setting option is only available for *string* type fields. Results can take longer to show with this option.
   * **Exact**: Show options that are an *exact* match with the entered value.

   The search is not case sensitive. For example, searching for `ios` would still retrieve `iOS` if that value exists.
 - **Additional settings**:

   - **Use global filters**: A panel-level setting that applies to each individual control. It is enabled by default.
   - **Validate user selections**: Highlight control selections that result in no data.
   - **Ignore timeout for results**: Wait to display results until the list is complete.

:::
:::{applies-item} stack: ga 9.0-9.3
 - **Label**: Overwrite the default field name with a clearer and self-explanatory label.
 - **Minimum width**: Specify how much horizontal space does the control should occupy. The final width can vary depending on the other controls and their own width setting.
 - **Expand width to fit available space**: Expand the width of the control to fit the available horizontal space on the dashboard.

 - **Selections**:
   Select multiple values to filter with the control, or only one.

 - **Additional settings**:

   - **Ignore timeout for results**: Delays the display of the list of values until it is fully loaded. This option is useful for large data sets, to avoid missing some available options in case they take longer to load and appear when using the control.

   For Options list controls on *string* and *IP address* type fields, you can define how the control's embedded search should behave:

   * **Prefix**: Show options that *start with* the entered value.
   * **Contains**: Show options that *contain* the entered value. This setting option is only available for *string* type fields. Results can take longer to show with this option.
   * **Exact**: Show options that are an *exact* match with the entered value.

   The search is not case sensitive. For example, searching for `ios` would still retrieve `iOS` if that value exists.
:::

::::

## Range slider settings [range-slider-settings]

::::{applies-switch}

:::{applies-item} { serverless: ga, stack: ga 9.4 }
 - **Label**: Overwrite the default field name with a clearer and self-explanatory label.
 - **Step size**: Determine the slider's number of steps. The smaller a slider's step size, the more steps it has.
 - **Additional settings**:
   - **Use global filters**: A panel-level setting that applies to each individual control. It is enabled by default.
   - **Validate user selections**: Highlight control selections that result in no data.

:::

:::{applies-item} stack: ga 9.0-9.3
 - **Label**: Overwrite the default field name with a clearer and self-explanatory label.
 - **Minimum width**: Specify how much horizontal space does the control should occupy. The final width can vary depending on the other controls and their own width setting.
 - **Expand width to fit available space**: Expand the width of the control to fit the available horizontal space on the dashboard.
 - **Step size**: Determine the slider's number of steps. The smaller a slider's step size, the more steps it has.

:::
::::

## Shared control settings [configure-controls-settings]

::::{applies-switch}

:::{applies-item} { serverless: ga, stack: ga 9.4 }
Controls are always chained: a change in one control narrows the options available in all other controls on the dashboard. The exception is controls inside a [collapsible section](arrange-panels.md#collapsible-sections), which only chain with other controls in the same section. To opt a control out of chaining, turn off its **Use global filters** setting.

Per-control settings such as label, selections, search options, and additional settings are configured when you [create or edit a control](add-controls.md#create-and-add-options-list-and-range-slider-controls).

For pinned controls, click the Settings {icon}`gear` icon on the control to customize its display:

- **Minimum width**: Specify how much horizontal space the control should occupy. The final width can vary depending on the other controls and their own width setting.
- **Expand width to fit available space**: Expand the width of the control to fit the available horizontal space on the dashboard.

**Auto apply filters**: When enabled (default), the dashboard updates as soon as options are selected in controls. When disabled, you must click the unified search **Apply** button to apply pending control selections. This option is available from the **Dashboard settings** panel.

:::

:::{applies-item} stack: ga 9.0-9.3

1. Configure the control settings.

    * {applies_to}`stack: ga 9.2-9.3` In **Edit** mode, select **Add** > **Controls** > **Settings** in the toolbar.
    * {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Settings**.

2. On the **Control settings** flyout, configure the following settings:

    * **Label position** — Specify where the control label appears.
    * **Filtering** settings:

        * **Apply global filters to controls** — Define whether controls should ignore or apply any filter specified in the main filter bar of the dashboard.
        * **Apply global time range to controls** — Define whether controls should ignore or apply the main time range specified for the dashboard. Note that [time slider controls](add-controls.md#add-time-slider-controls) rely on the global time range and don't work properly when this option is disabled.

    * **Selections** settings:

        * **Validate user selections** — When selected, any selected option that results in no data is ignored.
        * **Chain controls** — When selected, controls are applied sequentially from left to right, and line by line. Any selected options in one control narrows the available options in the next control.
        * **Apply selections automatically** — The dashboard is updated dynamically when options are selected in controls. When this option is disabled, users first need to **Apply** their control selection before they are applied to the dashboard.

    * To remove all controls from the dashboard, select **Delete all**.

3. Select **Save** to apply the changes.

:::

::::
