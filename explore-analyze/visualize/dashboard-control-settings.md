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

[Dashboard controls](dashboard-controls.md) have settings at two levels:

- **Control-level settings** apply to a single control. You set most of them in the **Create control** flyout when you [add or edit](add-controls.md#create-and-add-options-list-and-range-slider-controls) the control.
- **General settings** apply to all controls on the dashboard at once.

Which settings are available, and where you set them, depends on the control type and your version.

## Control-level settings [control-level-settings]

You set these on a single control, in the **Create control** flyout when you [add or edit](add-controls.md#create-and-add-options-list-and-range-slider-controls) it. The available settings depend on the control type.

### Options list [options-list-settings]

Label
:   Overwrite the default field name with a clearer label.

:::{include} ../_snippets/control-settings-selections.md
:::

:::{include} ../_snippets/control-settings-searching.md
:::

Additional settings {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`
:   These extra options appear at the bottom of the flyout:

    :::{include} ../_snippets/control-settings-additional.md
    :::

    - **Ignore timeout for results**: wait to display results until the list is complete. Useful for large data sets, but results can take longer to populate.

You set the control's width in its {icon}`gear` **Display settings** ({applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`), or in the control editor in earlier versions:

:::{include} ../_snippets/control-display-settings.md
:::

### Range slider [range-slider-settings]

Label
:   Overwrite the default field name with a clearer label.

Step size
:   Set the slider's step granularity. The smaller the step size, the more steps the slider has.

Additional settings {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`
:   These extra options appear at the bottom of the flyout:

    :::{include} ../_snippets/control-settings-additional.md
    :::

You set the control's width in its {icon}`gear` **Display settings** ({applies_to}`serverless: ga` {applies_to}`stack: ga 9.4`), or in the control editor in earlier versions:

:::{include} ../_snippets/control-display-settings.md
:::

## General settings [configure-controls-settings]

These settings apply to all controls on the dashboard at once. Where you find them depends on your version.

::::{applies-switch}
:::{applies-item} {"serverless": "ga", "stack": "ga 9.4"}
The only dashboard-wide control setting is auto apply. Filtering and value validation are now set on each control instead, in its [Options list](#options-list-settings) or [Range slider](#range-slider-settings) settings.

Auto apply filters
:   By default, the dashboard updates as soon as a selection is made in a control. To require an explicit apply step, open **Dashboard settings** and turn off **Auto apply filters**. Pending selections are then applied only when you select **Apply** in the search bar.
:::
:::{applies-item} {"stack": "ga 9.0-9.3"}
These settings apply to all controls at once. To open them, in **Edit** mode:

- {applies_to}`stack: ga 9.2-9.3` Select **Add** > **Controls** > **Settings** in the application menu.
- {applies_to}`stack: ga 9.0-9.1` Select **Controls** > **Settings**.

Label position
:   Set where the control label appears, **Inline** or **Above**.

Filtering
:   - **Apply global filters to controls**: define whether controls apply or ignore filters from the dashboard's main filter bar.
    - **Apply global time range to controls**: define whether controls apply or ignore the dashboard's global time range. [Time slider controls](add-time-slider-controls.md) rely on the global time range and don't work properly when this option is off.

Selections
:   - **Validate user selections**: when on, any selection that returns no data is ignored.
    - **Chain controls** (on by default): controls apply sequentially from left to right and line by line, so a selection in one control narrows the options in the next.
    - **Apply selections automatically**: the dashboard updates as soon as a selection is made in a control. When off, users must select **Apply** to apply pending selections.

To remove all controls from the dashboard, select **Delete all**.
:::
::::
