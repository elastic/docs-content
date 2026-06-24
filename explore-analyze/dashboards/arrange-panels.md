---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/arrange-panels.html
description: Organize and arrange dashboard panels using collapsible sections, resizing, positioning, and duplication to improve readability and performance.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Organize dashboard panels [arrange-panels]

Customize your dashboard layout by arranging panels into logical groups and adjusting their size and position. When panels are well organized, your dashboard becomes easier to read, loads faster, and helps viewers locate important information more quickly.

This page covers:

- [Dashboard grid layout and best practices](#dashboard-grid-layout)
- [Layout examples](#dashboard-layout-examples)
- [Collapsible sections](#collapsible-sections)
- [Moving and resizing panels](#resizing-containers)
- [Copying and duplicating panels](#duplicate-panels)

## Requirements [arrange-panels-requirements]

To organize dashboard panels, you need the **All** privilege for the **Dashboard** feature in {{product.kibana}}.

## Dashboard grid layout and best practices [dashboard-grid-layout]

Dashboards use a 48-column grid with rows of fixed height. When you move or resize a panel, it snaps to column and row boundaries on this grid. New panels are created at half width (24 columns) by default.

Size panels to match what they show. Use these as starting points and adjust for the density of your data:

| Chart type | Recommended width | Recommended height (rows) |
| ---------- | ----------------- | ------------------------- |
| Metric | Quarter (12) | 4–6 |
| Metric (on dense row) | Sixth (8) | 4–5 |
| Bar chart, gauge, pie | Half (24) | 8–12 |
| Line chart, area chart (time series) | Third (16) to full (48) | 12–15 |
| Heat map | Full (48) | 15–25 |
| Table | Half (24) to full (48) | 15+ |

Consider the following best practices to keep dashboards scannable as you add panels:

* **Place KPIs and key trends above the fold.** On a 1080p screen, roughly 20–24 rows are visible without scrolling. Put metrics in the top row so viewers see the most important information first. Aim for 8–12 panels above the fold.
* **Keep heights consistent within a row.** When several panels sit side by side, use the same height for all of them. Mismatched heights leave awkward gaps and make the row harder to read.
* **Match panel width to importance.** Give primary charts more horizontal room, and group compact KPI metrics into narrower panels along a single row.
* **Separate secondary content with collapsible sections.** When a dashboard accumulates supporting panels and detail tables, place them inside a [collapsible section](#collapsible-sections) so the primary view stays focused and the dashboard loads faster.
* **Don't use text panels as section headers.** They take up vertical space without showing data. Use collapsible section labels and descriptive panel titles instead.

### Layout examples [dashboard-layout-examples]

**Starting point**: a metric row, two half-width charts, and a detail table.

```text
┌──────────┬──────────┬──────────┬──────────┐
│  Metric  │  Metric  │  Metric  │  Metric  │  4 × 12 cols, ~5 rows
├──────────┴──────────┼──────────┴──────────┤
│  Chart              │  Chart              │  2 × 24 cols, ~10–12 rows
├─────────────────────┴─────────────────────┤
│  Table or distribution chart              │  48 cols, 15+ rows
└───────────────────────────────────────────┘
```

::::{dropdown} Screenshot
![A polished dashboard with metrics at the top, time series charts in the middle, and a bar chart and table at the bottom](/explore-analyze/images/kibana-learning-tutorial-dashboard-polished.png "")
::::

**Dense layout**: six compact metrics, two rows of three charts at third width, and a table.

```text
┌────────┬────────┬────────┬────────┬────────┬────────┐
│ Metric │ Metric │ Metric │ Metric │ Metric │ Metric │  6 × 8 cols, ~5 rows
├────────┴────────┼────────┴────────┼────────┴────────┤
│  Chart          │  Chart          │  Chart          │  3 × 16 cols, ~12 rows
├─────────────────┼─────────────────┼─────────────────┤
│  Chart          │  Chart          │  Chart          │  3 × 16 cols, ~12 rows
├─────────────────┴─────────────────┴─────────────────┤
│  Table                                              │  48 cols, 15+ rows
└─────────────────────────────────────────────────────┘
```

::::{dropdown} Screenshot
![A Kibana dashboard showing KPI metrics at the top, followed by charts and a data table](/explore-analyze/images/kibana-dashboard-overview.png "")
::::

When you use the [Dashboards API](create-dashboards-programmatically.md) to author dashboards, you specify `x`, `y`, `w`, and `h` as grid coordinates directly. The dashboard editor's automatic packing no longer applies, so the same guidelines apply in your panel definitions.

### Panel limits [dashboard-panel-limits]
```{applies_to}
stack: ga 9.4
serverless: ga
```

Each dashboard enforces the following limits:

- Up to 1,000 top-level items (panels, including unpinned controls, and sections combined)
- Up to 1,000 panels inside each section
- Up to 100 [pinned controls](add-controls.md)

These limits are independent of each other. For example, a single dashboard can have 100 pinned controls, 1,000 sections at the top level, and 1,000 panels inside each of those sections.

When you create or update a dashboard with the [Dashboards API](create-dashboards-programmatically.md), an additional combined limit applies: the total number of panels, sections, and pinned controls can't exceed 1,000. Requests that exceed this limit are rejected with a validation error.

## Arrange panels in collapsible sections [collapsible-sections]
```{applies_to}
stack: ga 9.1
serverless: ga
```

Organize your dashboard panels into collapsible sections to improve readability and navigation, especially for dashboards with many panels. Collapsible sections also help dashboards load faster by only loading the content from expanded sections.

To add a collapsible section:

1. Open the dashboard and make sure that you are in **Edit** mode.
2. Add a new panel and select **Collapsible section**. The collapsible section is added at the end of the dashboard.
3. Optionally, edit the label of the section.
4. Drag and drop any panels you want into the section.
   :::{tip}
   The section must be expanded in order to place panels into it.
   :::
5. Like any other panel, you can drag and drop the collapsible section to a different position in the dashboard.
6. Save the dashboard. 

Users viewing the dashboard will find the section in the same state as when you saved the dashboard. If you saved it with the section collapsed, then it will also be collapsed by default for users.

:::{note} 
:applies_to: stack: ga 9.4

**Filter controls and sections**: Controls placed inside a collapsible section apply their filters only to panels within that section. Controls placed outside sections, or [pinned to the dashboard header](dashboard-controls.md), have global scope and filter all relevant panels on the dashboard. Refer to [Dashboard controls](dashboard-controls.md) for more on pinned and unpinned controls.
:::

![Collapsible sections](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt8c368aecdd095010/685e8fcb9c34ed3c353812a5/collapsible_panels.gif)

## Move and resize panels [resizing-containers]

Compare the data in your panels side-by-side, organize panels by priority, resize the panels so they all appear immediately on the dashboard, and more.

In the application menu, click **Edit**, then use the following options:

* To move, hover over the panel, click and hold ![The move control icon](/explore-analyze/images/kibana-move-control.png "The move control icon =4%x4%") and drag to the new location. Your screen scrolls automatically when you drag above or below the visible parts of the dashboard.
* To resize, click and hold the bottom right corner of the panel and drag to the new dimensions. Panels snap to a [48-column grid](#dashboard-grid-layout).
* To maximize to full screen, open the panel menu and click **Maximize**.

  ::::{tip}
  If you [share](sharing.md) a dashboard while viewing a full screen panel, the generated link will directly open the same panel in full screen mode.
  ::::

### Move and resize panels using a keyboard
```{applies_to}
stack: ga 9.1
serverless: ga
```

To move a panel:

1. Using `Tab`, browse to the {icon}`move` panel action and press `Enter` or `Space` to lock the action.
2. Use `Arrow` keys to move the panel to the new location.
3. Press `Enter` or `Space` again to release the panel.
4. Save the dashboard.

To resize a panel:

1. Using `Tab`, browse to the {icon}`scale` panel action and press `Enter` or `Space` to lock the action.
2. Use `Arrow` keys to resize the panel to the new dimensions.
3. Press `Enter` or `Space` again to release the panel.
4. Save the dashboard.

:::{tip}
While moving or resizing a panel, you can cancel the action at any time by pressing `Escape`.
:::

## Copy and duplicate panels [duplicate-panels]

To duplicate a panel and its configured functionality, use the clone and copy panel options. Cloned and copied panels replicate all of the functionality from the original panel, including renaming, editing, and cloning.


### Duplicate panels [clone-panels]

Duplicated panels appear next to the original panel, and move the other panels to provide a space on the dashboard.

1. In the application menu, click **Edit**.
2. Open the panel menu and select **Duplicate**.


### Copy panels [copy-to-dashboard]

Copy panels from one dashboard to another dashboard.

1. Open the panel menu and select **Copy to dashboard**.
2. On the **Copy to dashboard** window, select the dashboard, then click **Copy and go to dashboard**.

    ![Copy a panel to another dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt48304cb3cd1ee2e6/6753879eb7c4663812148d47/copy-to-dashboard-8.17.0.gif "")



