---
navigation_title: Manage action policies
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Enable, disable, snooze, maintenance windows, bulk actions, and API key rotation for action policies in the {{alerting-v2}}."
---

# Manage action policies

Managing action policies is part of the {{alerting-v2}} in Kibana. After you create an action policy, you can control when it runs, pause it temporarily, and keep its credentials current. This page covers those management tasks.

## Enable, snooze, and maintenance

You can disable a policy so it is not evaluated for new episodes. You can snooze a policy for a defined window so that it does not dispatch notifications during that period. Policies that are not enabled or are snoozed are skipped when the dispatcher evaluates policies.

### Maintenance windows [maintenance-windows]


Maintenance windows are scheduled periods during which a policy does not dispatch notifications. They are configured on the action policy alongside snooze and other policy controls, not on the rule. Rule evaluation continues and alert episodes can still be recorded in `.rule-events`. Only dispatch through that policy pauses. Use maintenance windows for planned deployments, infrastructure changes, or recurring quiet periods.

## Update API keys

You can rotate the API key used to run a policy's workflows without changing matchers or destinations. Use the **Update API key** action on one policy or for multiple selected policies.

::::{important} Production considerations
When you update or delete an action policy, previous API keys used for execution are marked for invalidation and removed on a schedule managed by {{kib}}. Allow for a short delay before new keys are used for dispatch.
::::

## Bulk actions

On the action policies list, select one or more policies to enable, disable, snooze, and do more in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.
