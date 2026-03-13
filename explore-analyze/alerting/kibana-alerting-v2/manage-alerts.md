---
navigation_title: Manage alerts
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "View, triage, and respond to alerts produced by Kibana alerting v2 rules using the alert inbox."
---

# Manage Kibana alerting v2 alerts [manage-alerts-v2]

View, triage, and respond to alerts produced by Kibana alerting v2 rules. The alert inbox provides a centralized view of all active and recent alerts with filtering, investigation, and action capabilities.

## Alert inbox

The alert inbox is the primary interface for working with Kibana alerting v2 alerts. It shows alert episodes with their status, severity, rule information, and timeline.

### What you can do

- **View alerts** — see all alert episodes with status, severity, rule name, grouping key, and duration.
- **Filter and search** — narrow the list by status, severity, rule, tags, assignee, and any alert field.
- **Investigate** — open the alert flyout to review the timeline, rule condition, related alerts, and metadata.
- **Take action** — acknowledge, snooze, resolve, assign, tag, and more.
- **Explore in Discover** — query alert events with ES|QL for trend analysis and operational reporting.

### Learn more

- [View alerts](manage-alerts/view-alerts.md) — filtering, sorting, and navigating the alert inbox.
- [Investigate and respond to alerts](manage-alerts/investigate-respond.md) — using the alert flyout and detail pages.
- [Explore alerts and signals in Discover](manage-alerts/explore-alerts-discover.md) — querying alert data with ES|QL.
