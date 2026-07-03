---
navigation_title: Add a time slider control
type: how-to
description: Add a time slider control to a Kibana dashboard to filter time-based data across a range that viewers can adjust and animate.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add a time slider control to a dashboard [add-time-slider-controls]

A time slider control filters a dashboard's time-based data to a range that viewers can adjust, and advance or animate backward and forward. Unlike [Options list and Range slider controls](add-controls.md), the time slider is a separate option in the control menu, and a dashboard supports only one. It uses the dashboard's [global time filter](../query-filter/filtering.md) as its initial range.

## Before you begin [add-time-slider-requirements]

To add a time slider control to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) with a time field, so the dashboard has time-based data to filter

## Add the control [add-time-slider-steps]

:::{warning}
:applies_to: {"serverless": "ga", "stack": "ga 9.4"}
The time slider must be pinned to the dashboard header. It is not available as a free panel.
:::

1. Open or create a dashboard.
2. Add a time slider control:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** > **Controls** > **Time slider**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Add time slider control**.

3. Save the dashboard. Viewers can now use the control. To change its range, [change the global time filter](../query-filter/filtering.md).

To remove a time slider control, follow the steps to [manage controls](add-controls.md#manage-controls). The same panel menu and hover actions apply to all control types.
