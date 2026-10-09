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
| Edit alert tags (**Edit Tags** in earlier versions) | Adds or removes tags on the alert. | You want to categorize alerts for routing, filtering, or reporting. | Series |
| Edit assignee | Assigns the alert to a specific user. | You want to establish clear ownership during investigation or prevent duplicate work. | Alert |

## Investigate the underlying data [investigate-underlying-data]

Go to Discover to inspect the data behind an alert.

| Action | Description | When to use | Scope |
|---|---|---|---|
| Open in Discover | Opens the rule's base {{esql}} query scoped to the time window around when the alert opened. | You want to verify what data the rule was evaluating or investigate whether the condition is a genuine problem. | Alert |

## Triage {{alerting-v1-system}} alerts [triage-classic-alerts]
```{applies_to}
serverless: ga
stack: experimental 9.6+
```

The **Alerts** page also lists [alerts from {{alerting-v1-system}} rules](view-and-manage-alerts.md#alerts-from-both-systems), which show **Classic** in the **Source** column. You can take most of the same actions on them, individually or in bulk. Each action uses the matching {{alerting-v1-system}} feature, so the results differ from those for {{alerting-v2-system}} alerts:

| Action | What happens to a {{alerting-v1-system}} alert |
|---|---|
| Acknowledge, Unacknowledge | Adds or removes the [acknowledged](/explore-analyze/alerting/alerts/view-alerts.md#acknowledge-alerts) marker. The alert's notifications keep running. Acknowledging a {{alerting-v2-system}} alert [stops its notifications](../action-policies/reduce-notification-noise.md#silencing-mechanisms). |
| Snooze | [Snoozes](/explore-analyze/alerting/alerts/view-alerts.md#snooze-alerts) this alert only. Other alerts from the same rule keep running their actions. The snooze lasts until the time you set, or until you unsnooze the alert if you select **Indefinitely**. Condition-based snooze isn't available on this page. |
| Unsnooze | Ends the snooze, so the alert's actions run again. |
| Resolve | Marks the alert as [untracked](/explore-analyze/alerting/alerts/view-alerts.md#alert-status). Its status changes to **Inactive**, its actions stop, and its status no longer updates. You can't undo this. |
| Edit alert tags | Adds or removes tags on this alert only. |

Some actions aren't available for {{alerting-v1-system}} alerts on this page:

- **Unresolve**, **Edit assignee**, and **Open in Discover** work only on {{alerting-v2-system}} alerts.
- You can't add the alert to a case. To add a {{alerting-v1-system}} alert from an Observability rule to a case, use the **Alerts (V1)** page instead. To show that page, turn on the **Show V1 Observability alerts table** advanced setting in the space.

To act on {{alerting-v1-system}} alerts from this page, your role needs two sets of privileges:

- The {{alerting-v2-system}} **Alerts** privilege set to **All**. With **Read**, you can't triage {{alerting-v1-system}} alerts from this page. Refer to [Configure access](../manage/configure-access.md#alerting-triage-privileges).
- The {{alerting-v1-system}} privileges for the alert's rule type. Refer to [Give access to triage alerts without managing rules](/explore-analyze/alerting/alerts/alerting-setup.md#_give_access_to_triage_alerts_without_managing_rules).
