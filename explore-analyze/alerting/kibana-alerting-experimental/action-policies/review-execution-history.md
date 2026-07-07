---
navigation_title: Review execution history
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Monitor action policy dispatch activity from the execution history. Understand dispatched, throttled, and unmatched outcomes, search and filter records, and query the event log in Discover."
---

# Review action policy execution history in the {{alerting-v2-system}} [review-execution-history]

The execution history for action policies shows dispatcher decisions from the last 24 hours across all action policies in the space. Each row covers one dispatcher run for each action policy evaluated against a rule:

| Column | Description |
|---|---|
| **Timestamp** | When the dispatcher ran. |
| **Policy** | The action policy that was evaluated. |
| **Rule** | The rule whose alert episodes the policy processed. |
| **Outcome** | Whether the dispatcher acted on the episode: `dispatched`, `throttled`, or `unmatched`. Definitions are in [Dispatch outcomes](#dispatch-outcomes). |
| **Episodes** | The number of alert episodes processed in this run. |
| **Action groups** | The number of action groups involved. |
| **Workflows** | The workflows invoked, if any. |

You can search records by policy name, rule name, or saved-object ID, and filter by outcome to view only dispatched or throttled records.

## Dispatch outcomes [dispatch-outcomes]

After each dispatcher run, {{kib}} records one of three outcomes for each policy:

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched a policy but was rate-limited by the frequency setting, so no workflow ran. This is expected behavior, not an error. |
| `unmatched` | No action policy matched the alert episode. No workflow ran. |

`unmatched` is recorded in the event log but isn't available as an outcome filter in the execution history. To find those records, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"` and `event.action: "unmatched"`.

:::{note}
Episodes that are acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) are suppressed before the dispatcher runs and don't appear in the execution history.
:::

## Related pages

- [Manage action policies](manage-action-policies.md) to enable, disable, snooze, edit, or rotate API keys for action policies.
- [Action policy reference](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md) to understand how the dispatcher evaluates action policies against alert episodes.