---
navigation_title: Manage action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Manage action policies in the experimental alerting system: turn them on or off, snooze them so they don't invoke workflows, and rotate API keys."
---

# Manage action policies for the {{alerting-v2-system}} [manage-action-policies]

This page covers how to view action policy details in the {{alerting-v2-system}}, enable and disable action policies, snooze them during planned outages, and rotate their API keys. To monitor dispatcher activity and review execution outcomes, refer to [Review action policy execution history](review-action-policy-execution-history.md).

To find your action policies, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Action Policies**.

## View and edit an action policy

The action policy list shows who created and last updated each policy, along with quick actions to clone or delete one. Open a policy to view or edit its scope, grouping mode, frequency, and destinations.

Deleting a rule doesn't delete the action policies that applied to its alert episodes. Delete those policies separately when no remaining rule needs them.

{applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` The **Matcher** field in a policy's details states its [scope](create-configure-action-policy.md#matcher) as a sentence, such as **Matches alerts where Rule tagged with** `checkout` **and Matches query** `severity: "critical"`. A policy with an empty scope shows **Matches all alerts**.

## Enable, disable, and snooze an action policy

You can disable an action policy so the dispatcher doesn't evaluate it for new alert episodes. You can snooze an action policy for a defined window so it doesn't invoke workflows during that period. The dispatcher skips action policies that aren't enabled or are snoozed.

:::{note}
Snoozing an action policy differs from [snoozing an alert episode](reduce-notification-noise.md#snooze-scope). When you snooze an action policy, the dispatcher pauses and silences every alert series the action policy applies to. When you snooze an alert episode, you target one specific series before action policy evaluation runs, silencing it regardless of which action policy applies to it. Use alert snooze when you want to quiet a specific recurring alert without affecting other series the same action policy applies to.
:::

### Pause dispatch during a maintenance window [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop invoking workflows automatically. You don't need to configure the action policy. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. Configure {{maint-windows-cap}} separately, not on the action policy.

## Rotate an action policy's API key

You can rotate the API key used to run an action policy's workflows without changing its scope or destinations. Use the **Update API key** action on one action policy or for multiple selected action policies.

## Manage multiple action policies at once

On the action policies list, select one or more action policies to enable, disable, snooze, and do more in bulk. **Select all** selects every action policy on the current page of results. Clear the selection before changing filters if you need a different set.

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Set up or update the action policies you manage here.
- [Review action policy execution history](review-action-policy-execution-history.md): Check dispatcher outcomes and investigate unexpected notification behavior.
- [Reduce notification noise](reduce-notification-noise.md): Silence alert episodes with acknowledgment, snooze, or deactivation.
