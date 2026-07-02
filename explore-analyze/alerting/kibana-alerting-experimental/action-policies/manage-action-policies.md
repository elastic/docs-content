---
navigation_title: Manage action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "View policy details, enable, disable, snooze, review execution history, and rotate API keys for action policies in the experimental alerting system."
---

# Manage action policies for the {{alerting-v2-system}}

Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page covers how to view policy details, enable and disable policies, snooze them during planned outages, rotate their API keys, and review execution history.

## View and edit a policy

From the **Action policies** list, you can open a policy to see its full configuration, including match conditions, grouping mode, frequency, and destinations. The list also shows the display name of the user who created the policy and the user who last updated it. You can also edit, clone, delete, enable, disable, snooze, or update its API key without leaving the list page.

## Review dispatch records and outcomes

After each dispatcher run, {{kib}} writes one event log entry per policy to the `.kibana-event-log-*` index. {{kib}} retains records for 24 hours. Each entry covers one policy's full dispatcher cycle and includes the policy name, rule name, outcome, episode count, action group count, and any workflows invoked.

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched a policy but was rate-limited by the frequency setting. No workflow ran. |
| `unmatched` | No action policy matched the alert episode. No workflow ran. |

The dispatcher drops episodes that are acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) before running and writes no record for them.

To query records directly or find records older than 24 hours, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"`. Use `event.action` to filter by outcome (`dispatched`, `throttled`, or `unmatched`).

## Enable, disable, and snooze a policy

You can disable a policy so the dispatcher doesn't evaluate it for new alert episodes. You can snooze a policy for a defined window so it doesn't dispatch notifications during that period. The dispatcher skips policies that aren't enabled or are snoozed.

:::{note}
Snoozing a policy differs from [snoozing an alert episode](reduce-notification-noise.md#snooze-scope). When you snooze a policy, the dispatcher pauses and silences every alert series the policy processes. When you snooze an alert episode, you target one specific series before policy matching runs, silencing it regardless of which policy handles it. Use alert snooze when you want to quiet a specific recurring alert without affecting other series handled by the same policy.
:::

### Pause dispatch during a maintenance window [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop dispatching notifications automatically. You don't need to configure the policy. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. Configure {{maint-windows-cap}} separately, not on the action policy.

## Rotate a policy's API key

You can rotate the API key used to run a policy's workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies.

::::{important} 

**Production considerations**

When you update or delete an action policy, previous API keys used for execution are queued for removal on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::

## Manage multiple policies at once

On the action policies list, select one or more policies to enable, disable, snooze, and do more in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.

## Related pages

- [Reduce notification noise in {{alerting-v2-system}}](reduce-notification-noise.md) to silence individual alert episodes by acknowledging, snoozing, or marking them inactive.
- [Action policy reference in {{alerting-v2-system}}](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
- [Create and configure an action policy](create-configure-action-policy.md) to set up or update the policies you manage here.
