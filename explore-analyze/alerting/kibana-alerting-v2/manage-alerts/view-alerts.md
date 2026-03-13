---
navigation_title: View alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Filter, sort, and search Kibana alerting v2 alerts in the alert inbox using quick filters, severity, tags, and custom fields."
---

# View Kibana alerting v2 alerts [view-alerts-v2]

The alert inbox shows all Kibana alerting v2 alert episodes with filtering, sorting, and quick actions for efficient triage.

## Alert list

The alert list displays alert episodes with the following columns:

| Column | Description |
|---|---|
| **Rule name** | The rule that generated the alert |
| **Grouping key** | The group field values for this alert series |
| **Duration** | How long the alert has been in its current state |
| **Alert status** | Current lifecycle status: active, pending, recovering, inactive |
| **Alert severity** | Severity level if configured on the rule |

By default, the list is pre-filtered on **Active** alerts and sorted by descending severity and timestamp.

## Quick filters

Use quick filters to switch between alert views:

| Filter | Description |
|---|---|
| **All** | All alert episodes with a count |
| **Active** | Currently active alerts |
| **Resolved** | Alerts that have completed recovery |
| **Snoozed** | Alerts with active snooze |
| **Acknowledged** | Alerts that have been acknowledged |
| **Pending** | Alerts in pending state (activation threshold not yet met) |
| **Recovering** | Alerts in recovering state (recovery threshold not yet met) |

## Additional filters

Filter alerts by:

- **Alert severity** — critical, high, medium, low.
- **Rule name** — specific rules.
- **Tags** — rule tags or alert tags.
- **Assigned to** — team member assignment.
- **Grouping key** — specific group field values.

## Search

Use the search bar to search across all alert fields, including data fields from the ES|QL query payload.

## Alert timeline chart

A stacked line chart at the top of the inbox shows alert series and their event status over time. By default, it shows the last 30 minutes for alert series with active episodes, sorted by descending severity and limited to the top 20 series.

You can use the chart to filter the time range for the alert list below.

## Alert actions

From the alert list, you can perform the following actions on individual alerts:

- **View alert detail** — open the alert flyout.
- **View rule detail** — navigate to the rule that generated the alert.
- **Edit tags** — add or modify alert tags.
- **Assign** — assign the alert to a team member.
- **Acknowledge / Unacknowledge** — mark the alert as acknowledged to suppress notifications for this episode.
- **Resolve / Activate** — manually change the alert state.
- **Snooze** — suppress notifications for this alert series for a configured duration.
- **View alert events in Discover** — open Discover with a pre-populated query for this alert's events.
- **Add to Cases** — link the alert to a case for tracking.

## Pagination

The alert list paginates automatically. Click **Load more** to continuously load additional alert episodes.
