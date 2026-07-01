---
navigation_title: Triage alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Take triage actions on alert episodes in Kibana's experimental alerting system. Acknowledge, snooze, resolve, activate, tag, and assign episodes individually or in bulk."
---

# Triage alert episodes [triage-alert-episodes]

In the {{alerting-v2-system}}, you can take the following triage actions on alert episodes individually or in bulk. For deeper investigation of a specific episode, refer to [Investigate alert episodes](investigate-alert-episodes.md).

## Available actions [row-level-actions]

- **Acknowledge / Unacknowledge:** Marks the episode as seen. Applies to the individual episode.
- **Snooze / Unsnooze:** Suppresses notifications for the episode's series for a set duration. Applies to all episodes sharing the same `group_hash`.
- **Resolve / Unresolve:** Closes the episode. Applies to the episode's series.
- **Activate:** Manually moves the episode to `active` state without waiting for the activation threshold to be met.
- **Edit tags:** Adds or removes tags on the episode.
- **Assign:** Assigns the episode to a specific user. Available from the episode detail page.

## Bulk actions [bulk-actions]

All available actions can be applied to multiple episodes at once. Scope rules still apply: acknowledge and activate apply per episode, while snooze and resolve apply per series. When snoozing episodes across different series, each series is snoozed independently.

## Snooze [snooze-episode]

Snoozing suppresses notifications for an alert series for a defined period. The rule continues to evaluate and the episode remains visible, but no notifications are sent until the snooze expires.

Use snooze when a known condition is expected to persist for a fixed time and you want to stop the noise without disabling the rule entirely, for example, during a scheduled maintenance window.

## Unsnooze [unsnooze-episode]

Ending a snooze clears it for all episodes sharing the same `group_hash`, not just the one you acted on. Notifications resume immediately for the entire series.

## Open in Discover [open-episode-in-discover]

The **Discover** action opens the rule's base {{esql}} query scoped to the time window around when the episode opened. Use it to verify what data the rule was evaluating or to investigate whether a condition is a genuine problem.

## Action scope reference [alert-actions]

Some actions apply to the individual episode; others apply to every episode in the same series (same rule and `group_hash`). Snoozing one episode silences the whole series, not only that service.

| Action | Scope |
|---|---|
| Acknowledge / Unacknowledge | Episode |
| Activate | Episode |
| Edit tags | Episode |
| Assign | Episode |
| Snooze / Unsnooze | Series |
| Resolve / Unresolve | Series |
