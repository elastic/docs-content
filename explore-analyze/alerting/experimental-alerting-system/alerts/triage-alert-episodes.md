---
navigation_title: Triage alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Take triage actions on alert episodes in the experimental alerting system. Acknowledge, snooze, resolve, activate, deactivate, tag, and assign episodes individually or in bulk."
---

# Triage alert episodes in the {{alerting-v2-system}} [triage-alert-episodes]

From the **Alerts** page (find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts**), you can take the following triage actions on alert episodes individually or in bulk. For deeper investigation of a specific episode, refer to [Investigate alert episodes](investigate-alert-episodes.md).

## Track review status [track-review-status]

Mark an episode as seen, or flag it again for follow-up, without changing its lifecycle state.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Acknowledge | Marks the episode as seen. | You've reviewed the episode and want to track that it's been seen without taking further action. | Episode |
| Unacknowledge | Removes the seen marker from the episode. | You want to re-flag an episode for follow-up. | Episode |

## Silence notifications [silence-notifications]

Temporarily silence notifications for an episode's series, without disabling the rule.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Snooze | Silences notifications for the episode's series for a set duration. The rule continues to evaluate and the episode remains visible. | A known condition is expected to persist for a fixed time and you want to reduce noise without disabling the rule, for example during a scheduled maintenance window. | Series |
| Unsnooze | Ends the active snooze, restoring notifications immediately. Clears the snooze for all episodes sharing the same `group_hash`, not only the one you acted on. | The condition has changed and you want notifications to resume before the snooze expires. | Series |

Snooze is one of several silencing mechanisms in the {{alerting-v2-system}}, each with a different scope. For the full comparison, refer to [Reduce notification noise](../action-policies/reduce-notification-noise.md).

## Close and reopen episodes [close-and-reopen-episodes]

Close an episode once the underlying problem is fixed, or reopen it if it turns out the problem wasn't resolved.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Resolve | Closes the episode. | The underlying problem is fixed and the episode should be closed. | Series |
| Unresolve | Reopens a resolved episode. | The problem has recurred or was closed prematurely. | Series |

## Override the automatic lifecycle [override-automatic-lifecycle]

Take manual control of an episode's lifecycle state. 

| Action | Description | When to use | Scope |
|---|---|---|---|
| Activate | Manually moves the episode to `active` state without waiting to meet the activation threshold. | Another signal already confirms the problem, or the metric recovered but the problem persists. | Episode |
| Deactivate | Returns a manually activated episode to normal behavior. | You want to restore automatic recovery behavior for a previously activated episode. | Episode |

:::{note}
**Activate** ignores automatic recoveries once triggered. The episode stays open until you manually close it with Resolve or Deactivate.

**Deactivate** resumes automatic recovery detection. The episode can close on its own the next time the rule evaluates as recovered, but deactivating alone doesn't close the current episode.
:::

## Organize and assign episodes [organize-and-assign-episodes]

Add context to an episode for filtering, routing, or ownership.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Edit tags | Adds or removes tags on the episode. | You want to categorize episodes for routing, filtering, or reporting. | Series |
| Edit assignee | Assigns the episode to a specific user. | You want to establish clear ownership during investigation or prevent duplicate work. | Episode |

## Investigate the underlying data [investigate-underlying-data]

Go to Discover to inspect the data behind an episode.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the episode opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Episode |
