---
navigation_title: Create an action policy
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Create action policies in the {{alerting-v2}}, configure match conditions, Notify per, Frequency, and workflow destinations."
---

# Create and configure an action policy [create-manage-action-policies]


Action policies are part of the {{alerting-v2}} in {{kib}}. This page covers how to configure match conditions, set grouping and frequency, and attach workflow destinations. Where rules define what counts as a problem, action policies define what happens when one is detected — which episodes generate notifications, how they batch for dispatch, and where they're routed.

Because policies are separate from rules and global within a space, you can update notification behavior across many rules at once without touching detection logic, and you can route the same alerts differently depending on severity or source. You create and manage policies from the **Action policies** page, not from the rule form.

For match conditions fields, grouping modes, frequency options, and dispatch outcomes, refer to [Action policy reference](action-policy-reference.md).

<!--
## Create an action policy

[CONTENT NEEDED for M2: UI. Once the navigation and action policy settings have been confirmed, add instructions for creating an action policy.]
-->

## Policy fields [policy-fields]

### Match conditions [matcher]


An optional KQL expression that filters which episodes this policy applies to. An empty match condition matches every episode in the space.

Use match conditions to route different episodes to different policies, for example, one policy for `data.severity: "critical"` episodes routed to PagerDuty and another for warnings routed to Slack. For available fields and examples, refer to [Match conditions fields](action-policy-reference.md#matcher-fields).

<!--[CONTENT NEEDED for M2: The `data.severity: "critical"` example above will become the legacy approach once M2 ships. M2 promotes severity to `episode.severity` and `episode.severity_max` as first-class episode fields. Update this example to use `episode.severity: "CRITICAL"` and update the cross-reference to include the new fields. Also decide whether to retain `data.severity` as an alternative for rules that haven't migrated, or to remove it from guidance entirely.]
-->

### Grouping and frequency [reduce-noise-grouping]


**Notify per** controls how episodes batch into notifications. **Frequency** controls how often the policy can notify for each batch.

:::{table}
:widths: 4-4-4

| Notify per | What it does | Available Frequency options |
|---|---|---|
| Episode | One notification per episode. | - On status change <br> - On status change + repeat at interval <br> - Every evaluation |
| Group | Bundle episodes that share a field value. Specify **Group by** (for example `data.service.name` or `data.host.name`). | - At most once every… <br> - Every evaluation |
| Digest | One notification for all matching episodes combined. | Every evaluation |

:::

For detailed descriptions, frequency options, and examples for each mode, refer to [Notify per options](action-policy-reference.md#notification-grouping).

### Frequency [throttle]


**Frequency** limits how often the policy can fire for a given notification group. The interval resets from the last time the policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`. For available options by **Notify per** mode, refer to [Frequency](action-policy-reference.md#throttle-strategies).

### Destinations

One or more workflows to invoke when the policy matches. Use the search field to find and attach workflows.

### Snooze

An optional time window during which the policy doesn't dispatch. Useful for planned maintenance or quiet periods without disabling the policy entirely.
