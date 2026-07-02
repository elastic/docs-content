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

## View policy details

From the **Action policies** list, you can open a policy to see its full configuration, including match conditions, grouping mode, frequency, and destinations. The list also shows the display name of the user who created the policy and the user who last updated it. You can also edit, clone, delete, enable, disable, snooze, or update its API key without leaving the list page.

## Execution history

The **Execution history** page shows records from the last 24 hours. Each row represents one rule processed by a policy in a single dispatcher cycle and shows the policy name, rule name, outcome, episode count, action group count, and the workflows invoked (for `dispatched` records).

After each dispatcher run, {{kib}} writes one event log entry per policy that ran. The UI denormalizes each entry into one row per rule reference, so a single dispatcher cycle produces as many rows as there are rules the policy evaluated.

| Outcome | What it means |
|---|---|
| `dispatched` | The dispatcher invoked a workflow for the alert episode. |
| `throttled` | The alert episode matched a policy but was rate-limited by the frequency setting. No workflow ran. |
| `unmatched` | No action policy matched the alert episode. No workflow ran. This outcome is recorded in the event log but is not available as a filter in the **Execution history** UI. Use Discover to find `unmatched` records. |

Episodes that were acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) are suppressed before the dispatcher runs and do not produce an execution history record.

Search records by policy name, rule name, or saved-object ID. Filter by outcome using the `dispatched` and `throttled` options in the UI.

:::{warning}
The **Execution history** page paginates at 100 log events per page. Each log event covers one policy's full dispatcher cycle and is then expanded into one row per rule — a single event matching 50 rules fills one page slot but renders 50 rows. A broad policy with no rule or severity scoping can generate hundreds of rows from a single event, pushing records from other policies off the visible page. Use match conditions to scope a policy to specific rules or severity levels to reduce this.
:::

Execution history records are retained for 24 hours. For older records, open Discover and query the `.kibana-event-log-*` index. Add a filter for `event.provider: "alerting_v2"` and use `event.action` to narrow by outcome (`dispatched`, `throttled`, or `unmatched`).

## Enable, disable, and snooze

You can disable a policy so it is not evaluated for new alert episodes. You can snooze a policy for a defined window so that it does not dispatch notifications during that period. Policies that are not enabled or are snoozed are skipped when the dispatcher evaluates policies.

:::{note}
Snoozing a policy differs from [snoozing an alert episode](reduce-notification-noise.md#snooze-scope). When you snooze a policy, the dispatch mechanism is paused and every series the policy processes is silenced. When you snooze an alert episode, you target one specific series before policy matching runs, silencing it regardless of which policy handles it. Use alert snooze when you want to quiet a specific recurring alert without affecting other series handled by the same policy.
:::

### {{maint-windows-cap}} [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop dispatching notifications automatically. No policy configuration is required. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. {{maint-windows-cap}} are configured separately, not on the action policy.

## Update API keys

You can rotate the API key used to run a policy's workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies.

::::{important} 

**Production considerations**

When you update or delete an action policy, previous API keys used for execution are queued for removal on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::

## Bulk actions

On the action policies list, select one or more policies to enable, disable, snooze, and do more in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.

## Related pages

- [Reduce notification noise in {{alerting-v2-system}}](reduce-notification-noise.md) to silence individual alert episodes by acknowledging, snoozing, or marking them inactive.
- [Action policy reference in {{alerting-v2-system}}](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
- [Create and configure an action policy](create-configure-action-policy.md) to set up or update the policies you manage here.
