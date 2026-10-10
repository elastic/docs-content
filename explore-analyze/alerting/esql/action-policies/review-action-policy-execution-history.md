---
navigation_title: Review action policy execution history
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Monitor action policy dispatch activity from the execution history. Understand dispatched, throttled, and unmatched outcomes, search and filter records, and query the event log in Discover."
---

# Review action policy execution history [review-action-policy-execution-history]

In {{alerting-v2-system}}, action policy execution history shows dispatcher decisions from the last 24 hours across all action policies in the space, so you can confirm notifications are dispatching as expected or investigate unexpected notification behavior.

Go to **Execution history** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Policies** tab. Each row covers one dispatcher run for one action policy, grouped by the rule whose alerts it processed:

| Column | Description |
|---|---|
| **Timestamp** | When the dispatcher ran. |
| **Policy** | The action policy that was evaluated. |
| **Outcome** | Whether the dispatcher acted on the alert: `dispatched`, `throttled`, or `unmatched`. Definitions are in [Dispatch outcomes](#dispatch-outcomes). |
| **Rules** | The rule whose alerts the action policy processed. |
| **Alerts** | The number of alerts processed in this run. |
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

You can search records by action policy name, rule name, or saved-object ID, and filter by outcome to view only dispatched or throttled records.

## Dispatch outcomes [dispatch-outcomes]

After each dispatcher run, {{kib}} records one of three outcomes for each action policy:

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert. |
| `throttled` | The alert matched an action policy but was rate-limited by the frequency setting, so no workflow ran. This is expected behavior, not an error. |
| `unmatched` | No action policy matched the alert. No workflow ran. |

`unmatched` is recorded in the event log but isn't available as an outcome filter in the execution history. To find those records, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"` and `event.action: "unmatched"`.

:::{note}
Alerts that are acknowledged, snoozed, resolved, or covered by a [maintenance window](../../alerts/maintenance-windows.md) fail the eligibility check, so the dispatcher doesn't evaluate action policies for them. They don't appear in the execution history.
:::

## Event-log outcomes and .alert-actions action types [outcome-vocab-mapping]

The `dispatched`, `throttled`, and `unmatched` outcomes are the **event-log terms** written to `.kibana-event-log-*`. The `.alert-actions` data stream records the same events using different terms. The mapping is:

| Event-log outcome (`event.action`) | `.alert-actions` `action_type` | Meaning |
|---|---|---|
| `dispatched` | `fire` and `notified` | Policy matched, frequency cleared, workflow invoked. {{kib}} writes `fire` for each dispatched alert and `notified` for each workflow invocation. |
| `throttled` | `suppress` | Policy matched but frequency limit not yet cleared. No workflow invoked. |
| `unmatched` | `unmatched` | No action policy matched the alert. No workflow invoked. |

`.alert-actions` also records triage actions (`ack`, `unack`, `assign`, `tag`, `snooze`, `unsnooze`, `activate`, `deactivate`). These have no event-log counterpart, because they aren't dispatcher outcomes. For the full field reference, refer to [Action type values](../alerts/field-reference.md#action-type-values).

:::{note}
The `suppress` action type covers more than the `throttled` outcome does, because the dispatcher also writes `suppress` for alerts that fail the eligibility check. To tell the cases apart, check the `reason` field. Throttled alerts have `suppressed by throttled policy <policy ID>`, and alerts that failed the eligibility check have `ack`, `snooze`, `deactivate`, or `maintenance_window:<window ID>`.
:::

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, or rotate API keys for your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand how the dispatcher evaluates action policies against alerts.