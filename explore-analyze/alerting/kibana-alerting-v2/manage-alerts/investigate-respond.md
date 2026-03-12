---
navigation_title: Investigate and respond to alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Investigate Kibana alerting v2 alerts using the alert flyout and detail pages — review timelines, metadata, related alerts, and take action."
---

# Investigate and respond to Kibana alerting v2 alerts [investigate-respond-v2]

When an alert requires investigation, use the alert flyout and detail pages to understand the condition, review the timeline, examine related alerts, and take action.

## Alert flyout

Click any alert row in the inbox to open the alert flyout. The flyout provides a compact investigation view with multiple tabs.

### Alert timeline

At the top of the flyout, a visual timeline shows alert events and their corresponding statuses since the beginning of the episode. Click on the timeline chart to navigate to the alert events tab on the full alert details page.

### Overview tab

The overview tab shows:

**Alert summary**
- Triggered timestamp
- Last updated timestamp
- Duration
- Alert status (active, pending, recovering, inactive)
- Alert severity
- Tags
- Assignee

**Rule summary**
- Rule name and description
- Rule condition (ES|QL query)
- Grouping key

**Alert event evaluation chart**
- A time series chart showing evaluation results since the beginning of the episode until resolution.

### Metadata tab

All alert metadata fields in a structured view, including the `data` payload from the ES|QL query.

### Attachments tab

Resources linked to the rule that generated the alert:
- Investigation guides (runbooks)
- Linked dashboards
- Saved searches

### Related tab

Related alerts from:
- Related rules (parent, child, sibling rules in rules-on-alerts chains).
- Past episodes from the same rule and series.

Click a related alert to open its flyout.

## Alert detail page

For deeper investigation, click **View details** in the flyout to open the full alert detail page. This page provides the same information as the flyout with additional space for timeline exploration and alert event history.

## Taking action

From the flyout or detail page, you can:

| Action | Scope | Effect |
|---|---|---|
| **Acknowledge** | Per episode | Suppresses notifications for this episode until unacknowledged |
| **Unacknowledge** | Per episode | Resumes notifications for this episode |
| **Snooze** | Per series | Suppresses notifications for a configured duration |
| **Resolve** | Per episode | Manually transitions the alert to inactive |
| **Assign** | Per episode | Assigns the alert to a team member |
| **Edit tags** | Per episode | Adds or modifies tags |
| **Set severity** | Per episode | Changes the alert severity |
| **Add to Cases** | Per episode | Links the alert to a case |
| **View in Discover** | — | Opens the alert events in Discover for ES\|QL exploration |

Refer to [Alert episode details](investigate-respond/alert-episode-details.md) and [Alert actions](investigate-respond/alert-actions.md) for more detail.
