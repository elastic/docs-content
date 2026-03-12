---
navigation_title: Maintenance windows
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Schedule periods during which Kibana alerting v2 notifications are paused for planned deployments or recurring maintenance."
---

# Kibana alerting v2 maintenance windows [maintenance-windows-v2]

Maintenance windows are scheduled periods during which notifications are paused. Use them for planned deployments, infrastructure changes, or recurring maintenance that you know will trigger alerts.

## How maintenance windows work

During a maintenance window:

- Rules continue to execute and produce alert events.
- Alert lifecycle tracking continues (pending, active, recovering transitions still occur).
- Notifications through notification policies are suppressed.
- The dispatcher records suppressed outcomes for auditability.

When the maintenance window ends, notifications resume automatically.

## Create a maintenance window

1. Navigate to the maintenance windows management area.
2. Click **Create maintenance window**.
3. Configure:
   - **Name** and **description**.
   - **Schedule** — start time, end time, and optional recurrence (daily, weekly, monthly).
   - **Scope** — which rules or notification policies are affected.

### Scoping options

Maintenance windows can be scoped by:

- **Linked rules** — suppress notifications for specific rules.
- **Match conditions** — suppress notifications for alerts matching specific attributes (for example, `env: production AND service: checkout`).
- **Notification policies** — suppress all notifications from specific policies.

## Manage maintenance windows

The maintenance windows list shows all windows with:

- Window name and schedule.
- Status (active, scheduled, or expired).
- Linked rules and policies.

## Maintenance windows on notification policies

Notification policies can reference maintenance windows directly. From the notification policy form:

1. Go to the **Maintenance windows** section.
2. Select one or more maintenance windows to apply.

When a linked maintenance window is active, the policy's notifications are suppressed.

## Relationship to snooze

| Mechanism | Scope | Trigger | Recurrence |
|---|---|---|---|
| **Maintenance window** | Rule, policy, or attribute-based | Scheduled | Supports recurring schedules |
| **Snooze** | Per series | Manual (ad hoc) | One-time only |

Use maintenance windows for planned, recurring events. Use snooze for ad hoc suppression.
