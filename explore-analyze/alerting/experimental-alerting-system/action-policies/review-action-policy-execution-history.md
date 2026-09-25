---
navigation_title: Review action policy execution history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Monitor action policy dispatch activity from the execution history. Understand dispatched, throttled, and unmatched outcomes, search and filter records, and query the event log in Discover."
---

# Review action policy execution history in the {{alerting-v2-system}} [review-action-policy-execution-history]

Action policy execution history shows dispatcher decisions from the last 24 hours across all action policies in the space, so you can confirm notifications are dispatching as expected or investigate unexpected notification behavior.

Go to **Execution history** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Policies** tab. Each row covers one dispatcher run for one action policy, grouped by the rule whose alert episodes it processed:

| Column | Description |
|---|---|
| **Timestamp** | When the dispatcher ran. |
| **Policy** | The action policy that was evaluated. |
| **Outcome** | Whether the dispatcher acted on the alert episode. Definitions are in [Dispatch outcomes](#dispatch-outcomes). |
| **Rules** | The rule whose alert episodes the action policy processed. |
| **Episodes** | The number of alert episodes processed in this run. |
| **Action groups** | The number of action groups involved. |
| **Workflows** | The workflows invoked, if any. |

<!-- TODO: "Action groups" is unexplained jargon — elaborate before publishing.
     Working hypothesis from code review: refers to the distinct groupBy buckets that
     fired in a given dispatcher run. For example, if the policy groups by host.name
     and host-1 and host-3 matched, the value would be 2. Confirm exact meaning and
     add a plain-language description (e.g. "The number of distinct groups that
     triggered a workflow in this run. Only relevant when the policy uses Group mode;
     otherwise 1."). Verify with the Alerting v2 team before uncommenting.
-->

You can search records by action policy name, rule name, or saved-object ID, and filter by outcome to narrow the list.

{applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` To review the dispatcher's decisions for a single alert episode across its whole lifetime, open the [**Policy history** tab](../alerts/investigate-alert-episodes.md#policy-history) on that alert episode's details page.

## Dispatch outcomes [dispatch-outcomes]

After each dispatcher run, {{kib}} records one of the following outcomes for each action policy:

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched an action policy but was rate-limited by the frequency setting, so no workflow ran. This is expected behavior, not an error. |
| `unmatched` | No action policy matched the alert episode. No workflow ran. |
| `dispatch_failed` | {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` The alert episode matched an action policy and wasn't throttled, but {{kib}} couldn't invoke the workflow. The table and the outcome filter show this outcome as **Failed**. |

### Find out why a dispatch failed [dispatch-failure-reasons]
```{applies_to}
serverless: experimental
stack: experimental 9.6+
```

In the **Outcome** column, each **Failed** badge has a second badge with the failure reason. Hover over the badges to see the full error message. {{kib}} also stores the reason in the `kibana.alerting_v2.dispatcher.failure_reason` event log field, so you can group failures in Discover without parsing error messages.

| Reason | What happened |
|---|---|
| `missing_api_key` | The action policy has no API key that {{kib}} can use, so {{kib}} skipped the whole action group. To fix this, rotate the action policy's API key. Refer to [Manage action policies](manage-action-policies.md). |
| `workflow_not_found` | The action policy points to a workflow that doesn't exist, for example because someone deleted the workflow after attaching it to the policy. |
| `workflow_disabled` | The action policy's workflow exists but is disabled. |
| `schedule_error` | {{kib}} couldn't schedule the workflow run, for example because of a Task Manager error. |

`unmatched` is recorded in the event log but isn't available as an outcome filter in the execution history. To find those records, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"` and `event.action: "unmatched"`.

:::{note}
Alert episodes that are acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) are excluded before the dispatcher runs and don't appear in the execution history.
:::

## Event-log outcomes and .alert-actions action types [outcome-vocab-mapping]

The `dispatched`, `throttled`, and `unmatched` outcomes are the **event-log terms** written to `.kibana-event-log-*`. The `.alert-actions` data stream records the same events using different terms. The mapping is:

| Event-log outcome (`event.action`) | `.alert-actions` `action_type` | Meaning |
|---|---|---|
| `dispatched` | `notified` | Policy matched, frequency cleared, workflow invoked. |
| `throttled` | `suppress` | Policy matched but frequency limit not yet cleared. No workflow invoked. |
| `unmatched` | `unmatched` | No action policy matched the alert episode. No workflow invoked. |

`.alert-actions` also records triage actions (`ack`, `unack`, `assign`, `tag`, `snooze`, `unsnooze`, `activate`, `deactivate`, `resolve`, `unresolve`) and the `fire` action type, which marks that an alert episode opened or continued. These have no event-log counterpart in this context, because they aren't dispatcher outcomes. For the full field reference, refer to [Action type values](../alerts/field-reference.md#action-type-values).

:::{note}
`suppress` in `.alert-actions` means the same thing as `throttled` in the event log: the action policy matched but the frequency setting hadn't cleared yet, so no notification was sent. It's unrelated to the eligibility gate that excludes acknowledged, snoozed, or maintenance-window alert episodes before the dispatcher runs.
:::

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, or rotate API keys for your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand how the dispatcher evaluates action policies against alert episodes.