---
navigation_title: Create an action policy
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Create {{alerting-v2}} action policies, configure matchers, Dispatch per, Frequency, and workflow destinations."
---

# Create and configure an action policy [create-manage-action-policies-v2]

$$$create-manage-action-policies-v2$$$

An action policy controls which alert episodes trigger notifications, how episodes are grouped, how often notifications are sent, and where they are routed. Policies are global within a space. You create and manage them from the **Action policies** page, not from the rule form.

For API values, Dispatch per and Frequency mappings, throttle strategies, dispatch outcomes, and matcher field examples, refer to [Action policy reference](action-policy-reference.md#action-policy-reference-v2).

## Create an action policy

1. Open **{{manage-app}}** > **V2 Alerting Preview** > **Action policies**.
2. Click **Create policy**.
3. Fill in the policy fields described in [Policy fields](#policy-fields) below.
4. Click **Save**. The matcher expression is validated on save, so invalid KQL is rejected before dispatch runs.

## Policy fields [policy-fields]

### Matcher [matcher-v2]

$$$matcher-v2$$$

An optional KQL expression that filters which episodes this policy applies to. An empty matcher matches every episode in the space.

Use matchers to route different episodes to different policies — for example, one policy for `data.severity: "critical"` episodes routed to PagerDuty and another for warnings routed to Slack. Typical matcher fields and examples are listed in [Action policy reference](action-policy-reference.md#matcher-fields-typical-kql).

### Grouping and frequency [reduce-noise-grouping-v2]

$$$reduce-noise-grouping-v2$$$

**Dispatch per** controls how episodes batch into notifications. **Frequency** controls how often the policy can notify for each batch.

| Dispatch per | What it does | Available Frequency options |
|---|---|---|
| **Episode** | One notification per episode. | On status change; On status change + repeat at interval; Every evaluation |
| **Group** | Bundle episodes that share a field value. Specify **Group by** (for example `data.service.name` or `data.host.name`). | At most once every…; Every evaluation |
| **Digest** | One notification for all matching episodes combined. | Every evaluation |

Episode works for most rules. Use Group when a rule produces many series-level episodes and you want to batch by a shared field. Use Digest for periodic summaries on longer schedules.

For Frequency to API strategy mappings, refer to [Action policy reference](action-policy-reference.md#frequency-ui-when-episode-per_episode).

### Throttling [throttle-v2]

$$$throttle-v2$$$

Throttling limits how often the policy can fire for a given group. The interval resets from the last time the policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`.

For throttle strategy API values, refer to [Action policy reference](action-policy-reference.md#throttle-strategies-api).

### Destinations

One or more workflows to invoke when the policy matches. Use the **workflow search** field in the policy editor to find and attach workflows. Only workflow-type destinations are supported in the current UI.

### Snooze

An optional time window during which the policy does not dispatch. Useful for planned maintenance or quiet periods without disabling the policy entirely.
