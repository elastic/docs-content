---
navigation_title: Create and manage action policies
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Create, configure, and manage Kibana alerting v2 action policies, including matching conditions, grouping, throttling, destinations, and snooze."
---

# Create and manage Kibana alerting v2 action policies [create-manage-action-policies-v2]

Create action policies to control which alerts trigger notifications, how alerts are grouped, how frequently notifications are sent, and where they are routed. Policies are **global**: you create and edit them from the **Action Policies** area, not from the rule form. Rules do not “link” to policies. Scoping is defined on the policy with **`rule_labels`** and matchers. Refer to [Action policies](../action-policies.md).

## Create an action policy

1. Navigate to **Management > Alerts and Insights > Rules V2 > Action Policies**.
2. Click **Create policy**.
3. Configure the policy settings: matching, grouping, throttling, destinations, and optional snooze.
4. Click **Save**.

## Policy list columns

| Column | Description |
|---|---|
| **Name** | Policy display name |
| **Status** | Whether the policy is active |
| **Rule labels** | Label selector used to scope which rules this policy can apply to |
| **Last updated** | Last save time |

There is **no “linked rule count”** in the global model. Policies are not attached to a fixed set of rules. Use **rule labels** and matcher behavior to understand effective coverage. For the evaluation flow, refer to [How action policies are evaluated](how-action-policies-are-evaluated.md).

## Destinations

Destinations route matching episodes to workflows and channels. Instead of choosing from a static list, the UI provides a **search field** that queries available workflows through the **`/api/workflows/search`** endpoint. Type to search and select the workflow to use for this policy.

## Snooze and maintenance

You can snooze a policy for a defined window so that it does not dispatch notifications during that period.

::::{important} Production considerations
When you **update** or **delete** an action policy, API keys used for execution are **invalidated** by a background task named `invalidateApiKeysTask`. Allow for brief propagation delay before new keys are used for dispatch. For intervals and delays, refer to [Set up](../../../before-you-begin/set-up.md).
::::

## Bulk actions

On the action policies list, select one or more policies to **enable**, **disable**, or **delete** in bulk. **Select all** selects every policy on the current page of results. Clear the selection before changing filters if you need a different set.
