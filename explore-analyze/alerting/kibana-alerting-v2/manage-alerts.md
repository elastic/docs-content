---
navigation_title: View and manage alert episodes
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Open the {{alerting-v2}} alert episodes table from {{manage-app}}, filter and sort episodes, search, open Discover from a row, and run triage actions."
---

# View and manage {{alerting-v2}} alert episodes [manage-alerts-v2]

$$$manage-alerts-v2$$$

The **alert episodes** table is the main place to see {{alerting-v2}} episodes in your space, narrow them with filters and search, sort columns, and start triage. The primary path is **{{manage-app}}** under **Alerts and Insights**.

## Open the alert episodes list

1. Open the **{{manage-app}}** app.
2. Go to **Alerts and Insights** > **Rules V2** > **Alert episodes**.

If your organization enabled {{alerting-v2}} but you do not see **Rules V2** or **Alert episodes**, ask an administrator. Some deployments also surface the same experience from **{{observability}}** (for example under **Alerts**); use whichever entry your layout provides.

## Time range

The table respects the **time range** control on the page. Narrow the range when you have many episodes or when filters return too many rows.

## Filter and search

- **Rule.** Limit rows to one or more rules (searchable list).
- **Status.** Limit by episode lifecycle state (for example active, recovered, pending, inactive).
- **Tags.** Limit to episodes whose **last** tag set matches any of the tags you select (OR logic). Tag choices come from tag actions in the selected time range; very large tag sets may show a capped list in the filter.
- **Search.** Text search runs over fields stored on alert event documents. It may not match every column you see (for example some rule metadata comes from separate fetches), so combine search with **Rule** or **Tags** when you need to find a specific rule or label.

You can use several filters together. Change the time range to refresh tag options and results.

## Sorting and table size

Select a column header to sort. Clearing sort on a column restores the default sort (typically newest first by time). The table loads up to a **large fixed number of rows** for the current query; if you reach that limit, narrow filters, search, or the time range. Pagination may not be available in all builds.

## Row actions and status

Actions appear on each row (and may be grouped in an overflow menu). Depending on state and permissions you can:

- **Acknowledge** and **Unacknowledge**: Per **episode**.
- **Snooze** and **Unsnooze**: Per **group** (`group_hash`). Snoozing affects the series group, not only one row if several rows share that group.
- **Resolve** and **Unresolve**: Per **group**. The UI may show episode status as inactive when resolved even if underlying lifecycle data differs. See [Investigate and respond](manage-alerts/investigate-respond.md#alert-actions-v2).
- **Edit tags**: Opens a flyout to add tags and select from suggestions (top tags in the product).

Icons in the status column can indicate snooze (for example a bell with expiry) or acknowledge state. Hover tooltips may show details such as snooze end time.

## Open in Discover

Use **Discover** (or the control labeled to open Discover) on a row to investigate source data. Discover opens with the rule **ES|QL** query and a **short time window** around the episode time so you can inspect matching documents in context.

## Open episode details

Open an episode’s **detail** page from the row (for example the episode identifier, title, or row action your build provides). The detail page shares the same triage actions and adds lifecycle context, related episodes, and grouping. See [Investigate and respond](manage-alerts/investigate-respond.md#alert-episode-details-v2).

## Learn more

- [Investigate and respond](manage-alerts/investigate-respond.md)
- [Explore alerts in Discover](manage-alerts/explore-alerts-discover.md)
