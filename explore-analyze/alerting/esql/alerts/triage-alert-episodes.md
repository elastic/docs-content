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

Use the **Alerts** page in {{alerting-v2-system}} to triage alerts individually or in bulk. You can mark alerts as seen, silence their notifications, close or reopen them, and tag or assign them. To open the page, go to **Alerting** → **Alerts** in the Observability navigation menu, or find **Alerts** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

For deeper investigation of a specific alert, refer to [Investigate alerts](investigate-alert-episodes.md).

## Track review status [track-review-status]

Mark an alert as seen, or flag it again for follow-up, without changing its lifecycle state.

| Action | Description | Scope |
|---|---|---|
| Acknowledge | Marks the alert as seen and stops its notifications. | Alert |
| Unacknowledge | Removes the seen marker and restores notifications. | Alert |

## Silence notifications [silence-notifications]

Temporarily silence notifications for an alert's series, without disabling the rule.

| Action | Description | Scope |
|---|---|---|
| Snooze | Silences notifications for the alert's series for a set duration, for example during a scheduled maintenance window. The rule continues to evaluate and the alert remains visible. | Series |
| Unsnooze | Ends the active snooze and restores notifications immediately. Clears the snooze for all alerts sharing the same `group_hash`, not only the one you acted on. | Series |

Snooze is one of several silencing mechanisms in {{alerting-v2-system}}, each with a different scope. For the full comparison, refer to [Reduce notification noise](../action-policies/reduce-notification-noise.md).

## Close and reopen alerts [close-and-reopen-episodes]

Close an alert once the underlying problem is fixed, or reopen it if it turns out the problem wasn't resolved.

| Action | Description | Scope |
|---|---|---|
| Resolve | Closes the alert immediately, without waiting for the rule to detect recovery. | Alert |
| Unresolve | Reopens an inactive alert as active, for example when the problem recurs. It continues as the same alert instead of opening a new one. | Alert |

After you resolve an alert, its notifications stop and the rule doesn't reopen it. If the rule's condition still matches on its next run, a new alert starts for the series. The new alert follows the normal lifecycle, and action policies can send notifications for it.

$$$override-automatic-lifecycle$$$

An alert you unresolve stays active on every rule run, even when the rule detects recovery. It closes only when you resolve it again.

## Organize and assign alerts [organize-and-assign-episodes]

Add context to an alert for filtering, routing, or ownership.

| Action | Description | Scope |
|---|---|---|
| Edit alert tags or Edit Tags (depending on your {{stack}} version) | Adds or removes tags on the alert. | {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` Alert<br>{applies_to}`stack: experimental =9.5` Series |
| Edit assignee | Assigns the alert to a specific user, so others know who owns the investigation. | Alert |

## Investigate the underlying data [investigate-underlying-data]

Go to Discover to check whether the data behind an alert shows a genuine problem.

| Action | Description | Scope |
|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the alert opened. | Alert |

## Triage alerts from {{alerting-v1-system}} [triage-classic-alerts]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

To act on alerts with **Classic** in the **Source** column, your role needs [privileges in both alerting systems](../manage/configure-access.md#alerting-classic-alert-privileges).

### How actions affect alerts from {{alerting-v1-system}} [classic-triage-action-results]

You can't unresolve or assign {{alerting-v1-system}} alerts, or open them in Discover. The other actions use the matching {{alerting-v1-system}} feature, so some results differ from the same action on a {{alerting-v2-system}} alert:

| Action | What happens to a {{alerting-v1-system}} alert |
|---|---|
| Acknowledge, Unacknowledge | Adds or removes the [acknowledged](/explore-analyze/alerting/alerts/view-alerts.md#acknowledge-alerts) marker. Unlike a {{alerting-v2-system}} alert, the alert keeps sending notifications. |
| Snooze, Unsnooze | [Snoozes](/explore-analyze/alerting/alerts/view-alerts.md#snooze-alerts) or unsnoozes this alert only. Other alerts from the same rule keep sending notifications. A snooze lasts until the time you set. If you select **Indefinitely**, the snooze lasts until you unsnooze the alert. For **Condition based** snooze, use the {{alerting-v1-system}} alerts pages. |
| Resolve | Marks the alert as [untracked](/explore-analyze/alerting/alerts/view-alerts.md#alert-status). Its status changes to **Inactive**, its notifications stop, and its status no longer updates. You can't undo this. |
| Edit alert tags | Adds or removes tags on the alert. |

### Add alerts from {{alerting-v1-system}} to a case [classic-alerts-to-cases]

To add a {{alerting-v1-system}} alert from an Observability rule to a case, turn on the [**Show V1 Observability alerts table**](../setup.md#alerting-setup-v1-alerts-page) advanced setting in the space, then add the alert from the **Alerts (V1)** page. You can't add {{alerting-v1-system}} alerts to cases from the **Alerts** page.
