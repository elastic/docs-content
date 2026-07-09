---
navigation_title: Triage alert episodes
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Take triage actions on alert episodes in Kibana's experimental alerting system. Acknowledge, snooze, resolve, activate, deactivate, tag, and assign episodes individually or in bulk."
---

# Triage alert episodes [triage-alert-episodes]

In the {{alerting-v2-system}}, you can take the following triage actions on alert episodes individually or in bulk. For deeper investigation of a specific episode, refer to [Investigate alert episodes](investigate-alert-episodes.md).

| Action | Description | When to use | Scope |
|---|---|---|---|
| Acknowledge | Marks the episode as seen. | You've reviewed the episode and want to track that it's been seen without taking further action. | Episode |
| Unacknowledge | Removes the seen marker from the episode. | You want to re-flag an episode for follow-up. | Episode |
| Snooze | Suppresses actions for the episode's series for a set duration. The rule continues to evaluate and the episode remains visible. | A known condition is expected to persist for a fixed time and you want to suppress noise without disabling the rule, for example during a scheduled maintenance window. | Series |
| Unsnooze | Ends the active snooze, restoring action execution immediately. Clears the snooze for all episodes sharing the same `group_hash`, not only the one you acted on. | The condition has changed and you want notifications to resume before the snooze expires. | Series |
| Resolve | Closes the episode. | The underlying problem is fixed and the episode should be closed. | Series |
| Unresolve | Reopens a resolved episode. | The problem has recurred or was closed prematurely. | Series |
| Activate | Manually moves the episode to `active` state without waiting to meet the activation threshold. Once activated, the engine ignores automatic recoveries. It stays open until you manually close it using Resolve or Deactivate. | A metric drops below the threshold but the underlying problem isn't resolved and you want to keep the episode open. | Episode |
| Deactivate | Returns a manually activated episode to normal behavior. The engine resumes automatic recovery detection, and the episode can close on its own the next time the rule evaluates as recovered. Deactivating does not close the current episode. | You want to restore automatic recovery behavior for a previously activated episode. | Episode |
| Edit tags | Adds or removes tags on the episode. | You want to categorize episodes for routing, filtering, or reporting. | Series |
| Edit assignee | Assigns the episode to a specific user. | You want to establish clear ownership during investigation or prevent duplicate work. | Episode |
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the episode opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Episode |
