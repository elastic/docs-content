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

Customize your dashboard layout by arranging panels into logical groups and adjusting their size and position. When panels are well organized, your dashboard becomes easier to read, faster to load, and helps viewers locate important information more quickly.

## Requirements [arrange-panels-requirements]

To organize dashboard panels, you need **Edit** permissions for the **Dashboard** feature in {{product.kibana}}.

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

![Collapsible sections](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt8c368aecdd095010/685e8fcb9c34ed3c353812a5/collapsible_panels.gif)

## Move and resize panels [resizing-containers]

Compare the data in your panels side-by-side, organize panels by priority, resize the panels so they all appear immediately on the dashboard, and more.

In the toolbar, click **Edit**, then use the following options:

* To move, hover over the panel, click and hold ![The move control icon](/explore-analyze/images/kibana-move-control.png "The move control icon =4%x4%") and drag to the new location. Your screen scrolls automatically when you drag above or below the visible parts of the dashboard.
* To resize, click and hold the bottom right corner of the panel and drag to the new dimensions.
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

1. In the toolbar, click **Edit**.
2. Open the panel menu and select **Duplicate**.


### Copy panels [copy-to-dashboard]

Copy panels from one dashboard to another dashboard.

1. Open the panel menu and select **Copy to dashboard**.
2. On the **Copy to dashboard** window, select the dashboard, then click **Copy and go to dashboard**.

    ![Copy a panel to another dashboard](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt48304cb3cd1ee2e6/6753879eb7c4663812148d47/copy-to-dashboard-8.17.0.gif "")



