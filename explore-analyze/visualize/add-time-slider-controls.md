---
navigation_title: Add time slider controls
type: how-to
description: Add a time slider control to a Kibana dashboard to filter time-based data across a range that viewers can adjust and animate.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Add a time slider control to dashboards [add-time-slider-controls]

A time slider control filters a dashboard's time-based data to a range that viewers can adjust, and advance or animate backward and forward. Unlike [Options list and Range slider controls](add-controls.md), the time slider is a separate option in the control menu. It uses the dashboard's [global time filter](../query-filter/filtering.md) as its initial range.

## Before you begin [add-time-slider-requirements]

To add a time slider control to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) with a time field, so the dashboard has time-based data to filter

A dashboard supports only one time slider control, and it can't be placed freely: it always stays pinned to the dashboard header.

## Add a time slider control [add-time-slider-steps]

1. Open or create a dashboard.
2. Add a time slider control:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** > **Controls** > **Time slider**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** > **Add time slider control**.

3. Save the dashboard. Viewers can now use the control.

## Manage the time slider control [manage-time-slider-control]

The time slider appears on your dashboard like other controls, so you edit and remove it the same way. Refer to [Manage Options list and Range slider controls](add-controls.md#manage-controls).

To change the time slider's range, [change the global time filter](../query-filter/filtering.md).
