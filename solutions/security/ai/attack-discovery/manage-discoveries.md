---
navigation_title: Attack Discovery page
applies_to:
  stack: ga 9.1
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage discoveries from the Attack Discovery page [manage-discoveries]

This page describes how to change status, share, bulk-act on, and search saved discoveries directly from the **Attack Discovery** page. For a unified, alert-correlated view that also supports triage actions like assignment and tagging, use the [Attacks page](/solutions/security/ai/attack-discovery/attacks-page.md) instead. To compare what each page offers, refer to [Manage saved discoveries](/solutions/security/ai/attack-discovery/manage-saved-discoveries.md#compare-pages).

## Change a discovery's status [discovery-status]

You can set a discovery's status to indicate that it's under active investigation or that it's been resolved:

| Status | Meaning |
|--------|---------|
| Open | Needs investigation (default) |
| Acknowledged | Under active investigation |
| Closed | Resolved |

Attacks on the [Attacks page](/solutions/security/ai/attack-discovery/attacks-page.md) use this same status lifecycle.

To change a discovery's status, click **Take action**, then select **Mark as acknowledged** or **Mark as closed**. You can choose to change the status of only the discovery, or of both the discovery and the alerts associated with it.

## Share discoveries [share-attack-discoveries]

By default, scheduled discoveries are shared with all users in a {{kib}} space.

Manually generated discoveries are private by default. To share them, change **Not shared** to **Shared** next to the discovery's name.

:::{note}
Once a discovery is shared, its visibility cannot be changed.
:::

## Take bulk actions [take-bulk-actions]

You can take bulk actions on multiple discoveries, such as bulk-changing their status or adding them to a case. To do this, select the checkboxes next to each discovery, then click **Selected *x* Attack discoveries** and choose the action you want to take.

## Search and filter saved discoveries [search-filter-discoveries]

You can search and filter saved discoveries to help locate relevant findings.

* Use the search box to perform full-text searches across your generated discoveries.

* **Visibility**: Use this filter to, for example, show only [shared](#share-attack-discoveries) discoveries.

* **Status**: Filter discoveries by their [current status](#discovery-status).

* **Connector**: Filter discoveries by connector name. Connectors that are deleted after discoveries have been generated are shown with a **Deleted** tag.

* Time filter: Adjust the time filter to view discoveries generated within a specific timeframe.
