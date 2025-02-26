---
navigation_title: "Managed integrations content"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/managed-integrations-content.html
---

# Managed integrations content [managed-integrations-content]


Most integration content installed by {{fleet}} isn't editable. This content is tagged with a **Managed** badge in the {{kib}} UI. Managed content itself cannot be edited or deleted, however managed visualizations, dashboards, and saved searches can be cloned.

:::{image} images/system-managed.png
:alt: An image of the new managed badge.
:class: screenshot
:::

When a managed dashboard is cloned, any linked or referenced panels become part of the clone without relying on external sources. The panels are integrated into the cloned dashboard as stand alone components. For example, with a cloned dashboard, the cloned panels become entirely self-contained copies without any dependencies on the original configuration. Clones can be customized and modified without accidentally affecting the original.

::::{note}
The cloned managed content retains the managed badge, but is independent from the original.

::::

You can make a complete clone of a whole managed dashboard. If you clone a panel within a managed dashboard, you're prompted to save the changes as a new dashboard, which is unlinked from the original managed content.

% The following details are copied from https://www.elastic.co/guide/en/kibana/8.17/fleet.html
To clone a dashboard:

1. Go to **Dashboards**.
2. Click on the name of the managed dashboard to view the dashboard.
3. Click **Clone** in the toolbar.
4. Click **Save and return** after editing the dashboard.
5. Click **Save**.

With managed content relating to specific visualization editor such as Lens, TSVB, and Maps, the clones retain the original reference configurations. To clone the visualization, view it in the editor then begin to make edits. Once finished editing you are prompted to save the edits as a new visualization. The same applies to editing any saved searches in a managed visualization.
