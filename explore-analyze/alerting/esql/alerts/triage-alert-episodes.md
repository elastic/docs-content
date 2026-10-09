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

To open the **Alerts** page in {{alerting-v2-system}}, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

From the **Alerts** page, you can take triage actions on alerts individually or in bulk. For deeper investigation of a specific alert, refer to [Investigate alerts](investigate-alert-episodes.md).

## What you can do by alert source [triage-actions-by-source]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

The **Alerts** page lists [alerts from both alerting systems](view-and-manage-alerts.md#alerts-from-both-systems). The **Source** column shows where each alert comes from, and the source determines which actions you can take:

| Action | Universal | Classic |
|---|:---:|:---:|
| Acknowledge, Unacknowledge | ✓ | ✓ |
| Snooze, Unsnooze | ✓ | ✓ |
| Resolve | ✓ | ✓ |
| Unresolve | ✓ | — |
| Edit alert tags | ✓ | ✓ |
| Edit assignee | ✓ | — |
| Open in Discover | ✓ | — |

On a {{alerting-v1-system}} alert, some actions have different results, and your role needs extra privileges. Refer to [Triage {{alerting-v1-system}} alerts](#triage-classic-alerts).

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
| Resolve | Closes the alert immediately, without waiting for the rule to detect recovery. | The underlying problem is fixed and the alert should be closed. | Alert |
| Unresolve | Reopens an inactive alert as active. It continues as the same alert instead of opening a new one. | The problem has recurred, or the alert closed while the problem persists. | Alert |

After you resolve an alert, its notifications stop and the rule doesn't reopen it. If the rule's condition still matches on its next run, a new alert starts for the series. The new alert follows the normal lifecycle, and action policies can send notifications for it.

$$$override-automatic-lifecycle$$$

An alert you unresolve stays active on every rule run, even when the rule detects recovery. It closes only when you resolve it again.

## Organize and assign alerts [organize-and-assign-episodes]

Add context to an alert for filtering, routing, or ownership.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Edit alert tags (**Edit Tags** in earlier versions) | Adds or removes tags on the alert. | You want to categorize alerts for routing, filtering, or reporting. | Series |
| Edit assignee | Assigns the alert to a specific user. | You want to establish clear ownership during investigation or prevent duplicate work. | Alert |

## Investigate the underlying data [investigate-underlying-data]

Go to Discover to inspect the data behind an alert.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the alert opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Alert |

## Triage alerts from {{alerting-v1-system}} [triage-classic-alerts]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

To act on {{alerting-v1-system}} alerts from the **Alerts** page, your role needs two sets of privileges:

- The {{alerting-v2-system}} **Alerts** privilege set to **All**. With **Read**, you can't triage {{alerting-v1-system}} alerts from this page. Refer to [Configure access](../manage/configure-access.md#alerting-triage-privileges).
- The {{alerting-v1-system}} privileges for the alert's rule type. Refer to [Give access to triage alerts without managing rules](/explore-analyze/alerting/alerts/alerting-setup.md#_give_access_to_triage_alerts_without_managing_rules).

Each action on a {{alerting-v1-system}} alert uses the matching {{alerting-v1-system}} feature, so the result differs from the same action on a {{alerting-v2-system}} alert:

| Action | What happens to a {{alerting-v1-system}} alert |
|---|---|
| Acknowledge, Unacknowledge | Adds or removes the [acknowledged](/explore-analyze/alerting/alerts/view-alerts.md#acknowledge-alerts) marker. The alert's notifications keep running. Acknowledging a {{alerting-v2-system}} alert [stops its notifications](../action-policies/reduce-notification-noise.md#silencing-mechanisms). |
| Snooze, Unsnooze | [Snoozes](/explore-analyze/alerting/alerts/view-alerts.md#snooze-alerts) or unsnoozes this alert only. Other alerts from the same rule keep running their actions. A snooze lasts until the time you set, or until you unsnooze the alert if you select **Indefinitely**. Condition-based snooze isn't available on this page. |
| Resolve | Marks the alert as [untracked](/explore-analyze/alerting/alerts/view-alerts.md#alert-status). Its status changes to **Inactive**, its actions stop, and its status no longer updates. You can't undo this. |
| Edit alert tags | Adds or removes tags on this alert only, not on every alert in its series. |

You can't add a {{alerting-v1-system}} alert to a case from this page. To add one from an Observability rule, use the **Alerts (V1)** page instead. To show that page, turn on the **Show V1 Observability alerts table** advanced setting in the space.
