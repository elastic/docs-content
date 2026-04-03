---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/add-controls.html
type: how-to
description: Add interactive filter controls to your Kibana dashboards to help users explore data with options lists, range sliders, and time sliders.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add controls to dashboards [add-controls]

Add interactive filter [controls](dashboard-controls.md) to your dashboards to help viewers filter and display only the data they want to explore. This page covers how to add, edit, and delete options list, range slider, and time slider controls.

To add {{esql}}-powered variable controls, refer to [Add variable controls with ES|QL](add-variable-controls.md).

## Before you begin [add-controls-requirements]

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) configured with fields available for filtering

## Add Options list and Range slider controls [create-and-add-options-list-and-range-slider-controls]

To add interactive Options list and Range slider controls, create the controls, then add them to your dashboard.

1. Open or create a new dashboard.
2. Add a control.

    ::::{applies-switch}
    :::{applies-item} { serverless: ga, stack: ga 9.4 }
    - Add as pinned control: In **Edit** mode, select **Add** > **Controls** > **Control**. The control is pinned and applies to the whole dashboard.
    - Add as free panel: Select **Add new panel** > **Controls**, then place the control on the dashboard. If you place a control inside a [collapsible section](arrange-panels.md#collapsible-sections), its filters apply only to panels in that section. To move a control between the header and the dashboard body, open the control's panel menu and select **Pin to Dashboard** or **Unpin**.
    :::
    :::{applies-item} stack: ga 9.2-9.3
    In **Edit** mode, select **Add** > **Controls** > **Control** in the toolbar.
    :::
    :::{applies-item} stack: ga 9.0-9.1
    In **Edit** mode, select **Controls** > **Add control** in the dashboard toolbar.
    :::
    ::::

3. On the **Create control** flyout, from the **Data view** dropdown, select the data view that contains the field you want to use for the control.
4. In the **Field** list, select the field you want to filter on.
5. Under **Control type**, select whether the control should be an **Options list** or a **Range slider**.
   ::::{tip}
   Range sliders are for Number type fields only.
   ::::

6. Configure the control's label, selections, search, and additional settings. For a full list of available settings, refer to [Dashboard control settings](dashboard-control-settings.md).
7. Select **Save**. The control can now be used.
8. Consider control order when you have several controls.

    ::::{applies-switch}
    :::{applies-item} { serverless: ga, stack: ga 9.4 }
    A change in one control will impact all other controls on the dashboard, regardless of their positioning in the grid, including pinned controls. The only exception to this is controls within a collapsible section. These controls will only chain with other controls in their section. To change this default behaviour, turn off the **Use global filters** setting.
    :::
    :::{applies-item} stack: ga 9.0-9.3
    Controls are applied from left to right; when the [Chain controls](dashboard-control-settings.md#configure-controls-settings) setting is enabled, their position changes the options available in the next control.
    :::
    ::::

9. Save the dashboard.

## Add time slider controls [add-time-slider-controls]

You can add one interactive time slider control to a dashboard.

1. Open or create a new dashboard.
2. Add a time slider control.

    ::::{applies-switch}
    :::{applies-item} { serverless: ga, stack: ga 9.2 }
    In **Edit** mode, select **Add** > **Controls** > **Time slider control** in the toolbar.
    :::
    :::{applies-item} stack: ga 9.0-9.1
    In **Edit** mode, select **Controls** > **Add time slider control**.
    :::
    ::::

3. The time slider control uses the time range from the global time filter. To change the time range in the time slider control, [change the global time filter](../query-filter/filtering.md).
4. Save the dashboard. The control can now be used.

:::{warning}
:applies_to: { serverless: ga, stack: ga 9.4 }
The time slider can only be added as a pinned control to the header. It is not available as a free panel.
:::

## Edit control settings [edit-controls]

Change the settings for Options list and Range slider controls.

::::{applies-switch}
:::{applies-item} { serverless: ga, stack: ga 9.4 }
1. Open the control's panel menu and select **Edit**.
2. In the **Edit control** flyout, change the options, then select **Save**.
:::
:::{applies-item} stack: ga 9.0-9.3
1. Hover over the control you want to edit, then select ![The Edit control icon that opens the Edit control flyout](/explore-analyze/images/kibana-dashboard_controlsEditControl_8.3.0.png "").
2. In the **Edit control** flyout, change the options, then select **Save**.
:::
::::

:::{tip}
To reset a control's current selections without editing its settings, hover over the control and click the **Clear** {icon}`eraser` icon.
:::

For the full list of available settings, refer to [Dashboard control settings](dashboard-control-settings.md).

## Delete controls [remove-controls]

::::{applies-switch}
:::{applies-item} { serverless: ga, stack: ga 9.4 }
To remove a control from view without deleting it, use **Unpin** from the control's panel menu; the control moves into the dashboard body. To remove it from the dashboard entirely, click **Remove** from the control's menu.
:::
:::{applies-item} stack: ga 9.0+
1. Hover over the control you want to delete, then select ![The Remove control icon that removes the control from the dashboard](/explore-analyze/images/kibana-dashboard_controlsRemoveControl_8.3.0.png "").
2. In the **Delete control?** window, select **Delete**.
:::
::::
:::{note}
If you delete a variable control that's used in an {{esql}} visualization, the visualization will break. You must edit the visualization query and remove or update the control reference.
:::
