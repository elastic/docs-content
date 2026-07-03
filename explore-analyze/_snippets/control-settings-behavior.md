Chaining
:   By default, making a selection in this control also narrows the options in the other controls. See [chaining](../visualize/dashboard-controls.md#controls-chaining).

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Set **Use global filters** on the control, in the **Additional settings** of its flyout. Turn it off to opt this control out of chaining.
    - {applies_to}`stack: ga 9.0-9.3` Set **Chain controls** in the dashboard-wide control settings. Changing it applies to all controls at once.

Validate selections
:   By default, selections that return no data are flagged.

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Set **Validate user selections** on the control, in the **Additional settings** of its flyout.
    - {applies_to}`stack: ga 9.0-9.3` Set **Validate user selections** in the dashboard-wide control settings. Changing it applies to all controls at once.

Auto apply selections
:   Choose whether the dashboard updates as soon as a selection is made, or only when you select **Apply**. This setting is dashboard-wide and applies to all controls.

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4` Set **Auto apply filters** in **Dashboard settings**.
    - {applies_to}`stack: ga 9.0-9.3` Set **Apply selections automatically** in the dashboard-wide control settings.

Other dashboard-wide settings {applies_to}`stack: ga 9.0-9.3`
:   In these versions, the dashboard-wide control settings also include:

    - **Label position**: show control labels **Inline** or **Above**.
    - **Apply global filters to controls**: whether controls obey the dashboard's main filter bar.
    - **Apply global time range to controls**: whether controls obey the dashboard's global time range. [Time slider controls](../visualize/add-time-slider-controls.md) need this on.
