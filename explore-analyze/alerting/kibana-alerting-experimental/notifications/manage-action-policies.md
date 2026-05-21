---
navigation_title: Manage action policies
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Enable, disable, snooze, bulk actions, and API key rotation for action policies in the {{alerting-v2}}."
---

# Manage action policies

Action policies are part of the {{alerting-v2}} in {{kib}}. This page covers how to enable and disable policies, snooze them during planned outages, and rotate their API keys.

## Enable and snooze

You can disable a policy so it is not evaluated for new episodes. You can snooze a policy for a defined window so that it does not dispatch notifications during that period. Policies that are not enabled or are snoozed are skipped when the dispatcher evaluates policies.

### Maintenance windows [maintenance-windows]

During a [maintenance window](../../alerts/maintenance-windows.md), action policies stop dispatching notifications automatically — no policy configuration is required. Rule evaluation continues and alert episodes are still recorded in `.rule-events`. Maintenance windows are configured separately, not on the action policy.

## Update API keys

You can rotate the API key used to run a policy's workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies.

::::{important} Production considerations
When you update or delete an action policy, previous API keys used for execution are marked for invalidation and removed on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::

## Bulk actions

On the action policies list, select one or more policies to enable, disable, snooze, and do more in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.
