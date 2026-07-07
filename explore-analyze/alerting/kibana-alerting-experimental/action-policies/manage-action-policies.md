---
navigation_title: Manage action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "View policy details, enable, disable, snooze, monitor dispatch activity on the Execution History Policies tab, and rotate API keys for action policies in the experimental alerting system."
---

# Manage action policies for the {{alerting-v2-system}}

Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page covers how to view policy details, enable and disable policies, snooze them during planned outages, rotate their API keys, and monitor dispatch activity on the Execution History **Policies** tab.

## View and edit a policy

From the **Action policies** list, you can open a policy to see its full configuration, including match conditions, grouping mode, frequency, and destinations. The list also shows the display name of the user who created the policy and the user who last updated it. You can also edit, clone, delete, enable, disable, snooze, or update its API key without leaving the list page.

## Review dispatch records and outcomes [execution-history]

The **Execution History** page provides a paginated, filterable log of dispatcher activity across all action policies in the space. Select the **Policies** tab to see dispatch records for the last 24 hours. Each row covers one (policy, rule) pair per dispatcher run:

| Column | Description |
|---|---|
| **Timestamp** | When the dispatcher ran. |
| **Policy** | The action policy that was evaluated. |
| **Rule** | The rule whose alert episodes the policy processed. |
| **Outcome** | Whether the dispatcher acted: `dispatched` means a workflow was invoked; `throttled` means the episode matched a policy but was rate-limited and no workflow ran. |
| **Episodes** | The number of alert episodes processed in this run. |
| **Action groups** | The number of action groups involved. |
| **Workflows** | The workflows invoked, if any. |

Use the search bar to find records by policy name, rule name, or saved-object ID. Use the **Outcome** filter to narrow results to **Dispatched** or **Throttled**. 

The `unmatched` outcome (which is when no policy matched the episode) is written to the event log but isn't available as a filter. To find those records, open Discover and query `.kibana-event-log-*` with `event.provider: "alerting_v2"` and `event.action: "unmatched"`.

Episodes that are acknowledged, snoozed, marked inactive, or covered by a [maintenance window](../../alerts/maintenance-windows.md) are dropped before the dispatcher runs and produce no record.

## Enable, disable, and snooze a policy

You can disable a policy so the dispatcher doesn't evaluate it for new alert episodes. You can snooze a policy for a defined window so it doesn't dispatch notifications during that period. The dispatcher skips policies that aren't enabled or are snoozed.

:::{note}
Snoozing a policy differs from [snoozing an alert episode](reduce-notification-noise.md#snooze-scope). When you snooze a policy, the dispatcher pauses and silences every alert series the policy processes. When you snooze an alert episode, you target one specific series before policy matching runs, silencing it regardless of which policy handles it. Use alert snooze when you want to quiet a specific recurring alert without affecting other series handled by the same policy.
:::

### Pause dispatch during a maintenance window [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop dispatching notifications automatically. You don't need to configure the policy. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. Configure {{maint-windows-cap}} separately, not on the action policy.

## Rotate a policy's API key

You can rotate the API key used to run a policy's workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies.

<!-- TODO: Verify accuracy before publishing — is the API key rotation behavior still accurate?
::::{important} 

**Production considerations**

When you update or delete an action policy, previous API keys used for execution are queued for removal on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::
-->

## Manage multiple policies at once

On the action policies list, select one or more policies to enable, disable, snooze, and do more in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.

## Related pages

- [Reduce notification noise in {{alerting-v2-system}}](reduce-notification-noise.md) to silence individual alert episodes by acknowledging, snoozing, or marking them inactive.
- [Action policy reference in {{alerting-v2-system}}](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
- [Create and configure an action policy](create-configure-action-policy.md) to set up or update the policies you manage here.
