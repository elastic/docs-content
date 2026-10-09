---
navigation_title: Triage alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Take triage actions on alerts. Acknowledge, snooze, resolve, activate, deactivate, tag, and assign alerts individually or in bulk."
---

# Triage alerts [triage-alert-episodes]

To open the **Alerts** page in {{alerting-v2-system}}, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

From the **Alerts** page, you can take the following triage actions on alerts individually or in bulk. For deeper investigation of a specific alert, refer to [Investigate alerts](investigate-alert-episodes.md).

## Track review status [track-review-status]

Mark an alert as seen, or flag it again for follow-up, without changing its lifecycle state.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Acknowledge | Marks the alert as seen. | You've reviewed the alert and want to track that it's been seen without taking further action. | Alert |
| Unacknowledge | Removes the seen marker from the alert. | You want to re-flag an alert for follow-up. | Alert |

## Silence notifications [silence-notifications]

Temporarily silence notifications for an alert's series, without disabling the rule.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Snooze | Silences notifications for the alert's series for a set duration. The rule continues to evaluate and the alert remains visible. | A known condition is expected to persist for a fixed time and you want to reduce noise without disabling the rule, for example during a scheduled maintenance window. | Series |
| Unsnooze | Ends the active snooze, restoring notifications immediately. Clears the snooze for all alerts sharing the same `group_hash`, not only the one you acted on. | The condition has changed and you want notifications to resume before the snooze expires. | Series |

Snooze is one of several silencing mechanisms in {{alerting-v2-system}}, each with a different scope. For the full comparison, refer to [Reduce notification noise](../action-policies/reduce-notification-noise.md).

## Close and reopen alerts [close-and-reopen-episodes]

Close an alert once the underlying problem is fixed, or reopen it if it turns out the problem wasn't resolved.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Resolve | Closes the alert. | The underlying problem is fixed and the alert should be closed. | Series |
| Unresolve | Reopens a resolved alert. | The problem has recurred or was closed prematurely. | Series |

## Override the automatic lifecycle [override-automatic-lifecycle]

Take manual control of an alert's lifecycle state. 

| Action | Description | When to use | Scope |
|---|---|---|---|
| Activate | Manually moves the alert to `active` state without waiting to meet the activation threshold. | Another signal already confirms the problem, or the metric recovered but the problem persists. | Alert |
| Deactivate | Returns a manually activated alert to normal behavior. | You want to restore automatic recovery behavior for a previously activated alert. | Alert |

:::{note}
**Activate** ignores automatic recoveries once triggered. The alert stays open until you manually close it with Resolve or Deactivate.

**Deactivate** resumes automatic recovery detection. The alert can close on its own the next time the rule evaluates as recovered, but deactivating alone doesn't close the current alert.
:::

## Organize and assign alerts [organize-and-assign-episodes]

Add context to an alert for filtering, routing, or ownership.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Edit tags | Adds or removes tags on the alert. | You want to categorize alerts for routing, filtering, or reporting. | Series |
| Edit assignee | Assigns the alert to a specific user. | You want to establish clear ownership during investigation or prevent duplicate work. | Alert |

## Investigate the underlying data [investigate-underlying-data]

Go to Discover to inspect the data behind an alert.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the alert opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Alert |
