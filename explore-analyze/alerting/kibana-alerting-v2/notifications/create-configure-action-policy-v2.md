---
navigation_title: Create an action policy
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Create {{alerting-v2}} action policies, configure matchers, Dispatch per, Frequency, and workflow destinations."
---

# Create and configure an action policy [create-manage-action-policies-v2]

$$$create-manage-action-policies-v2$$$

An action policy controls which alert episodes trigger notifications, how the policy groups episodes, how often it sends notifications, and where it routes them. Policies are global within a space. You create and manage them from the **Action policies** page, not from the rule form.

For matcher fields, grouping modes, throttle strategies, frequency options, and dispatch outcomes, refer to [Action policy reference](action-policy-reference-v2.md).

## Create an action policy

1. Open **{{manage-app}} > V2 Alerting Preview > Action Policies**.
2. Select **Create policy**.
3. Fill in the policy fields described in [Policy fields](#policy-fields).
4. Select **Save**. Kibana validates the matcher expression on save and rejects any KQL that isn't valid.

## Policy fields [policy-fields]

### Matcher [matcher-v2]

$$$matcher-v2$$$

An optional KQL expression that filters which episodes this policy applies to. An empty matcher matches every episode in the space.

Use matchers to route different episodes to different policies, for example, one policy for `data.severity: "critical"` episodes routed to PagerDuty and another for warnings routed to Slack. For available fields and examples, refer to [Matcher fields](action-policy-reference-v2.md#matcher-fields).

[CONTENT NEEDED for M2: The `data.severity: "critical"` example above will become the legacy approach once M2 ships. M2 promotes severity to `episode.severity` and `episode.severity_max` as first-class episode fields. Update this example to use `episode.severity: "CRITICAL"` and update the cross-reference to include the new fields. Also decide whether to retain `data.severity` as an alternative for rules that haven't migrated, or to remove it from guidance entirely.]

### Grouping and frequency [reduce-noise-grouping-v2]

$$$reduce-noise-grouping-v2$$$

**Dispatch per** controls how episodes batch into notifications. **Frequency** controls how often the policy can notify for each batch.

:::{table}
:widths: 4-4-4

| Dispatch per | What it does | Available Frequency options |
|---|---|---|
| **Episode** | One notification per episode. | - On status change <br> - On status change + repeat at interval <br> - Every evaluation |
| **Group** | Bundle episodes that share a field value. Specify **Group by** (for example `data.service.name` or `data.host.name`). | - At most once every… <br> - Every evaluation |
| **Digest** | One notification for all matching episodes combined. | Every evaluation |

:::

For detailed descriptions, frequency options, and examples for each mode, refer to [Dispatch per options](action-policy-reference-v2.md#notification-grouping).

### Throttling [throttle-v2]

$$$throttle-v2$$$

Throttling limits how often the policy can fire for a given group. The interval resets from the last time the policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`. For available throttle strategies, refer to [Throttle strategies](action-policy-reference-v2.md#throttle-strategies).

### Destinations

One or more workflows to invoke when the policy matches. Use the search field to find and attach workflows.

### Snooze

An optional time window during which the policy doesn't dispatch. Useful for planned maintenance or quiet periods without disabling the policy entirely.
