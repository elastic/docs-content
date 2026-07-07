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

The settings available depend on the control type. Find the settings for your control type below. Unless an entry says otherwise, you set a setting on the individual control, in the **Create control** flyout when you [add or edit](add-controls.md#create-and-add-options-list-and-range-slider-controls) it. Some settings apply to all controls at once, and for a few the location depends on your version; those entries tell you where to go.

## Options list settings [options-list-settings]

Label
:   Overwrite the default field name with a clearer label.

:::{include} ../_snippets/control-settings-selections.md
:::

:::{include} ../_snippets/control-settings-searching.md
:::

Ignore timeout for results
:   Wait to display results until the list is complete. Set it in the **Additional settings** of the control's flyout. Useful for large data sets, but results can take longer to populate.

:::{include} ../_snippets/control-display-settings.md
:::

:::{include} ../_snippets/control-settings-behavior.md
:::

## Range slider settings [range-slider-settings]

Label
:   Overwrite the default field name with a clearer label.

Step size
:   Set the slider's step granularity. The smaller the step size, the more steps the slider has.

:::{include} ../_snippets/control-display-settings.md
:::

:::{include} ../_snippets/control-settings-behavior.md
:::
