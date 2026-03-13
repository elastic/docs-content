---
navigation_title: Alert actions
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Actions you can take on Kibana alerting v2 alerts: acknowledge, snooze, deactivate, assign, tag, resolve, and add to cases."
---

# Kibana alerting v2 alert actions [alert-actions-v2]

Alert actions are operations you perform on Kibana alerting v2 alerts to manage their lifecycle, suppress notifications, and organize your triage workflow. Each action is recorded in the `.alerts-actions` index for auditability and suppression tracking.

## Available actions

### Acknowledge and unacknowledge

**Scope**: per episode

Acknowledging an alert suppresses notifications for that specific episode. The alert continues through its lifecycle (the rule still evaluates and writes events), but the dispatcher records `suppress` with reason `ack` instead of dispatching to workflows.

Unacknowledge resumes notifications for the episode. If the alert is still active, notifications fire on the next dispatcher run.

### Snooze and unsnooze

**Scope**: per series

Snoozing suppresses notifications for a specific series (rule + group key combination) for a configured duration. Unlike acknowledge, snooze is time-bound and applies to all episodes in the series, including future ones that start during the snooze window.

When the snooze expires, notifications resume automatically.

### Deactivate and activate

**Scope**: per episode

Deactivating an episode stops lifecycle processing and notifications for that episode entirely. The rule continues running and can detect new episodes for the same series, but the deactivated episode is no longer tracked.

This is roughly analogous to "mark as untracked" in Kibana alerting v1.

Activate reverses a deactivation.

### Resolve

**Scope**: per episode

Manually transitions the alert to inactive, ending the episode. Use this when you have verified the underlying issue is resolved but the rule has not yet detected recovery automatically.

### Assign

**Scope**: per episode

Assign the alert to a team member for tracking and accountability. Assignment is visible in the alert inbox and can be used as a filter.

### Edit tags

**Scope**: per episode

Add or modify tags on the alert for organization and filtering. Tags set on alerts are separate from tags set on rules.

### Set severity

**Scope**: per episode

Manually override the alert severity. This affects sorting and filtering in the alert inbox.

### Add to Cases

**Scope**: per episode

Link the alert to a case for structured incident tracking and collaboration.

## Action recording

Every action is written to the `.alerts-actions` index with:

- **Action type** — `ack`, `unack`, `snooze`, `unsnooze`, `deactivate`, `activate`, `fire`, `suppress`, `notified`.
- **Scope identifiers** — `rule_id`, `group_hash`, `episode_id`.
- **Timestamp** — when the action was taken.
- **User** — who performed the action (for manual actions).

The dispatcher uses these records to determine suppression state during the notification pipeline.
