---
navigation_title: Triage alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Take triage actions on alert episodes in Kibana's experimental alerting system. Acknowledge, snooze, resolve, activate, deactivate, tag, and assign episodes individually or in bulk."
---

# Triage alert episodes in the {{alerting-v2-system}} [triage-alert-episodes]

From the **Alerts** page (find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts**), you can take the following triage actions on alert episodes individually or in bulk. For deeper investigation of a specific episode, refer to [Investigate alert episodes](investigate-alert-episodes.md).

## Track review status [track-review-status]

Mark an episode as seen, or flag it again for follow-up, without changing its lifecycle state.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Acknowledge | Marks the episode as seen. | You've reviewed the episode and want to track that it's been seen without taking further action. | Episode |
| Unacknowledge | Removes the seen marker from the episode. | You want to re-flag an episode for follow-up. | Episode |

## Suppress notifications [suppress-notifications]

Temporarily stop actions from firing for an episode's series, without disabling the rule.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Snooze | Suppresses actions for the episode's series for a set duration. The rule continues to evaluate and the episode remains visible. | A known condition is expected to persist for a fixed time and you want to suppress noise without disabling the rule, for example during a scheduled maintenance window. | Series |
| Unsnooze | Ends the active snooze, restoring action execution immediately. Clears the snooze for all episodes sharing the same `group_hash`, not only the one you acted on. | The condition has changed and you want notifications to resume before the snooze expires. | Series |

## Close and reopen episodes [close-and-reopen-episodes]

Close an episode once the underlying problem is fixed, or reopen it if it turns out the problem wasn't resolved.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Resolve | Closes the episode. | The underlying problem is fixed and the episode should be closed. | Series |
| Unresolve | Reopens a resolved episode. | The problem has recurred or was closed prematurely. | Series |

## Override the automatic lifecycle [override-automatic-lifecycle]

Take manual control of an episode's lifecycle state when automatic recovery doesn't match what's actually happening.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Activate | Manually moves the episode to `active` state without waiting to meet the activation threshold. | A metric drops below the threshold but the underlying problem isn't resolved and you want to keep the episode open. | Episode |
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

Jump into Discover to inspect the data behind an episode.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the episode opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Episode |
