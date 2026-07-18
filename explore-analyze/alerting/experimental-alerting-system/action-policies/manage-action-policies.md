---
navigation_title: Manage action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "View action policy details, enable, disable, snooze, and rotate API keys for action policies in the experimental alerting system."
---

# Manage action policies for the {{alerting-v2-system}} [manage-action-policies]

This page covers how to view action policy details in the {{alerting-v2-system}}, enable and disable action policies, snooze them during planned outages, and rotate their API keys. To monitor dispatcher activity and review execution outcomes, refer to [Review action policy execution history](review-action-policy-execution-history.md).

## View and edit an action policy

To find your action policies, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Action Policies**. From the list, you can open an action policy to view its full configuration, including match conditions, grouping mode, frequency, and destinations.

The list also shows the display name of the user who created the action policy and the user who last updated it, along with quick actions for common tasks, such as cloning or deleting an action policy, without leaving the list page. For enabling, disabling, snoozing, or rotating an API key, refer to the sections below.

## Enable, disable, and snooze an action policy

You can disable an action policy so the dispatcher doesn't evaluate it for new alert episodes. You can snooze an action policy for a defined window so it doesn't dispatch notifications during that period. The dispatcher skips action policies that aren't enabled or are snoozed.

:::{note}
Snoozing an action policy differs from [snoozing an alert episode](reduce-notification-noise.md#snooze-scope). When you snooze an action policy, the dispatcher pauses and silences every alert series the action policy processes. When you snooze an alert episode, you target one specific series before action policy matching runs, silencing it regardless of which action policy handles it. Use alert snooze when you want to quiet a specific recurring alert without affecting other series handled by the same action policy.
:::

### Pause dispatch during a maintenance window [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop dispatching notifications automatically. You don't need to configure the action policy. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. Configure {{maint-windows-cap}} separately, not on the action policy.

## Rotate an action policy's API key

You can rotate the API key used to run an action policy's workflows without changing matchers or destinations. Use the **Update API key** action on one action policy or for multiple selected action policies.

<!-- TODO: Verify accuracy before publishing — is the API key rotation behavior described below still accurate?
::::{important} 

**Production considerations**

When you update or delete an action policy, previous API keys used for execution are queued for removal on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::
-->

## Manage multiple action policies at once

On the action policies list, select one or more action policies to enable, disable, snooze, and do more in bulk. **Select all** selects every action policy on the current page of results. Clear the selection before changing filters if you need a different set.

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Set up or update the action policies you manage here.
- [Review action policy execution history](review-action-policy-execution-history.md): Check dispatcher outcomes and investigate unexpected notification behavior.
- [Reduce notification noise](reduce-notification-noise.md): Silence alert episodes with acknowledgment, snooze, or deactivation.
