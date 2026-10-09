---
navigation_title: Triage alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Take triage actions on alerts. Acknowledge, snooze, resolve, reopen, tag, and assign alerts individually or in bulk."
---

# Triage alerts [triage-alert-episodes]

To open the **Alerts** page in {{alerting-v2-system}}:

* {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` In the Observability navigation menu, go to **Alerting** > **Alerts**, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* {applies_to}`stack: experimental =9.5` Go to **Alerting V2 Preview** in the navigation menu or global search, then go to **Alerts**.

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
| Resolve | Closes the alert immediately, without waiting for the rule to detect recovery. Action policies stop sending notifications for the alert. | The underlying problem is fixed and the alert should be closed. | Alert |
| Unresolve | Reopens a closed alert and keeps it `active`. The rule no longer closes the alert automatically. | The problem has recurred or the alert was closed prematurely, and you want it to stay open until someone confirms the fix. | Alert |

Resolving and unresolving also change how the rule treats the series on later runs:

* **After you resolve an alert**, the rule doesn't reopen it. If the rule's condition still matches on its next run, a new alert starts for the series. The new alert follows the normal lifecycle, and action policies can send notifications for it.
* **After you unresolve an alert**, the alert stays `active` on every run, even when the rule's condition recovers. It closes only when you resolve it again.

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
