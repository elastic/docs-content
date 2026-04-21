---
navigation_title: Configure a rule
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Configure {{alerting-v2}} rules: mode, ES|QL, grouping, schedule, lookback, activation and recovery, no-data handling, tags, and evaluation."
---

# Configure a rule [rule-settings-v2]

$$$rule-settings-v2$$$

Use this page to configure how a {{alerting-v2}} rule evaluates data and manages its alert lifecycle. These settings live on the rule itself.

For writing the {{esql}} query, refer to [Author rules](author-rules.md). For notification routing (matchers, grouping, throttling, maintenance windows), refer to [Notifications](../notifications.md) and [Manage action policies](../notifications/manage-action-policies.md).

:::{note}
Action policies are not configured on the rule form. You create them separately in the **Action policies** area and use KQL matchers to scope them to the episodes you want to route. The rule form does not link to policies.
:::

## Rule mode [rule-mode-v2]

Choose a mode that matches how you want to use results:

| Mode | Behavior |
| --- | --- |
| Detect | Signals only: the rule produces detections without alert lifecycle tracking or notifications. |
| Alert | Lifecycle tracking and notifications: alerts move through states (pending, active, recovering, and so on), and you can attach action policies so episodes dispatch through workflows. |

Several settings on this page apply only when the rule is in Alert mode (`kind: alert`).

## {{esql}} query [esql-query-rule-v2]

The rule's {{esql}} query defines what to evaluate. It has a base query and an optional alert condition. Together they drive which rows become alert events and how no-data behavior applies. See [{{esql}} query structure](author-rules.md#esql-query-structure) for how those pieces interact with no-data behavior and `KEEP`.

## Rule grouping [rule-grouping-v2]

$$$rule-grouping-v2$$$

Rule grouping splits alert event generation by one or more group key fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

Group key fields must align with the `BY` clause in your {{esql}} query's `STATS` command. See [Author rules](author-rules.md) for query patterns.

Note that rule grouping is separate from notification grouping on an action policy, which controls how episodes batch into messages.

## Schedule and lookback [schedule-lookback-v2]

$$$schedule-lookback-v2$$$

The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

### Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates.

{{kib}} enforces a minimum interval of 5 seconds and a maximum of 365 days for duration fields (including this one). Values outside that range are rejected.

### Lookback window

The lookback window (`schedule.lookback`) determines the time range that the {{esql}} query covers.

The lookback must not exceed 365 days. If the lookback is shorter than the execution interval, evaluations can miss data between runs. Use a lookback at least as long as the execution interval unless you have a deliberate reason not to.

## Activation and recovery thresholds [activation-recovery-thresholds-v2]

$$$activation-recovery-thresholds-v2$$$

Activation and recovery thresholds control when alerts transition between lifecycle states. They reduce noise from short spikes and from rapid flapping between active and recovered.

These settings are only available for Alert-mode rules (`kind: alert`).

### Activation thresholds

Configure activation using count, timeframe, or both:

| Field | Description |
| --- | --- |
| pending_count | Consecutive breaches required |
| pending_timeframe | Minimum duration the condition must persist |
| pending_operator | How to combine count and timeframe (`AND` or `OR`) |

Each timeframe value must be between 5 seconds and 365 days.

### Recovery thresholds

| Field | Description |
| --- | --- |
| recovering_count | Consecutive recoveries required |
| recovering_timeframe | Minimum duration for recovery |
| recovering_operator | How to combine count and timeframe (`AND` or `OR`) |

Timeframe fields use the same 5 seconds to 365 days bounds as activation timeframes.

## No-data handling [no-data-handling-v2]

No-data handling controls what happens when a rule executes and the base query returns no results. Proper configuration prevents false recoveries and misleading `no_data` events when data sources stop reporting.

### Behaviors

| Behavior | Effect |
| --- | --- |
| no_data (default) | Record a no-data event |
| last_status | Carry forward the previous status |
| recover | Treat absence as recovery |

## Tags and investigation guide [tags-investigation-v2]

Alert-mode rules support two optional metadata fields:

- **Tags**: Free-form labels for filtering and organization.
- **Investigation guide**: A runbook stored with the rule so responders have context when an alert fires.

## Evaluate rule output [evaluate-rule-output-v2]

Before relying on a rule in production, evaluate it against recent data. A full evaluation surfaces:

- How many rows the query returns.
- How many alert events would be generated.
- Sample alert event documents.
- A histogram of matching row counts over time (for evaluation and, when recovery logic applies, for recovery-oriented previews).

In the rule builder, click **Preview** before saving to run this evaluation against your current query and settings.
