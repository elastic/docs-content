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

A time slider control filters a dashboard's time-based data to a range that viewers can adjust, and advance or animate backward and forward. It uses the dashboard's [global time filter](../query-filter/filtering.md) as its initial range.

## Before you begin [add-time-slider-requirements]

To add a time slider control to a dashboard, you need:

* **All** privilege for the **Dashboard** feature in {{product.kibana}}
* An existing dashboard open in **Edit** mode
* A [data view](../find-and-organize/data-views.md) with a time field, so the dashboard has time-based data to filter

A dashboard supports only one time slider control, and it can't be placed freely on the dashboard's grid: it always stays pinned to the top of the dashboard.

## Add a time slider control [add-time-slider-steps]

1. Open or create a dashboard.
2. Add a time slider control:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2` In **Edit** mode, select **Add** → **Controls** → **Time slider**.
    - {applies_to}`stack: ga 9.0-9.1` In **Edit** mode, select **Controls** → **Add time slider control**.

3. Optional: Choose how the range moves as viewers advance or animate it. By default, the time slider covers a fixed-width range that slides along the timeline. To anchor the start instead, open the time slider and select {icon}`pin` **Pin start**, so the start stays fixed while the end extends. Select **Unpin start** to return to a sliding range. Viewers can also change this while using the control.
4. Save the dashboard. Viewers can now use the control.

## Manage the time slider control [manage-time-slider-control]

To change the range the time slider covers, [change the dashboard's global time filter](../query-filter/filtering.md).

To clear the current selection or remove the control, hover over the control to reveal its action icons, then select an action:

| Action | Description |
| --- | --- |
| **Clear** | Reset the time slider's selected range. Available only when a range is selected. |
| **Remove** or **Delete** | Delete the time slider control from the dashboard. |
