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

Go to **Execution history** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Policies** tab. Each row covers one dispatcher run for each action policy evaluated against a rule:

| Column | Description |
|---|---|
| **Timestamp** | When the dispatcher ran. |
| **Policy** | The action policy that was evaluated. |
| **Outcome** | Whether the dispatcher acted on the episode: `dispatched`, `throttled`, or `unmatched`. Definitions are in [Dispatch outcomes](#dispatch-outcomes). |
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

You can search records by action policy name, rule name, or saved-object ID, and filter by outcome to view only dispatched or throttled records.

## Dispatch outcomes [dispatch-outcomes]

After each dispatcher run, {{kib}} records one of three outcomes for each action policy:

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched an action policy but was rate-limited by the frequency setting, so no workflow ran. This is expected behavior, not an error. |
| `unmatched` | No action policy matched the alert episode. No workflow ran. |

`unmatched` is recorded in the event log but isn't available as an outcome filter in the execution history. To find those records, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"` and `event.action: "unmatched"`.

:::{note}
Episodes that are acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) are excluded before the dispatcher runs and don't appear in the execution history.
:::

<!--
TODO (after PR #6527 merges): uncomment this section and verify field values against field-reference.md.

## Event-log outcomes and .alert-actions action types [outcome-vocab-mapping]

The three outcomes above (`dispatched`, `throttled`, `unmatched`) are the **event-log terms** written to `.kibana-event-log-*`. PR #6527 introduces a parallel data stream (`.alert-actions`) that uses a different vocabulary for the same events. The mapping is:

| Event-log outcome (`event.action`) | `.alert-actions` `action_type` | Meaning |
|---|---|---|
| `dispatched` | `notified` | Policy matched, frequency cleared, workflow invoked. |
| `throttled` | `suppress` | Policy matched but frequency limit not yet cleared; no workflow invoked. |
| `unmatched` | `unmatched` | No action policy matched the episode; no workflow invoked. |

Note: `.alert-actions` also records alert-lifecycle events (`fire`, `activate`, `deactivate`, `ack`, `unack`)
that have no event-log counterpart in this context — they are not dispatcher outcomes.

Caution on naming: `suppress` in `.alert-actions` means **rate-limited by frequency** (same as `throttled`
in the event log). It is unrelated to the eligibility gate (acknowledged/snoozed/maintenance-window episodes).
Cross-reference this note from `action-policy-reference.md` Frequency section.
-->

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, or rotate API keys for your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand how the dispatcher evaluates action policies against alert episodes.