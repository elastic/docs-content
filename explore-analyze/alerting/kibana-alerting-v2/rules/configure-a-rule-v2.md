---
navigation_title: Configure a rule
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Configure {{alerting-v2}} rules: mode, ES|QL, grouping, schedule, lookback, activation and recovery, no-data handling, tags, and evaluation."
---

# Configure a {{alerting-v2}} rule [rule-settings-v2]

$$$rule-settings-v2$$$

The {{esql}} query defines what a rule detects. The settings on this page determine whether it behaves correctly in production: how often it runs, how it groups related problems, when it opens and closes alerts, and what it does when data stops arriving.

For query authoring, refer to [Author rules](author-rules-v2.md). For notification routing, refer to [Notifications](../notifications-v2.md).

:::{note}
Action policies are not configured on the rule form. You create them separately in the **Action policies** area and use KQL matchers to scope them to the episodes you want to route. The rule builder form does not link to policies.
:::

## Rule mode [rule-mode-v2]

Choose a mode that matches how you want to use results:

| Mode | Behavior |
| --- | --- |
| Detect | Signals only: the rule produces detections without alert lifecycle tracking or notifications. |
| Alert | Lifecycle tracking and notifications: alerts move through states (pending, active, recovering, and so on), and you can attach action policies so episodes dispatch through workflows. |

Several settings on this page apply only when the rule is in Alert mode (`kind: alert`).

## {{esql}} query [esql-query-rule-v2]

The rule's {{esql}} query defines what to evaluate. It has a base query and an optional alert condition. Together they drive which rows become alert events and how no-data behavior applies. See [{{esql}} query structure](author-rules-v2.md#esql-query-structure) for how those pieces interact with no-data behavior and `KEEP`.

## Rule grouping [rule-grouping-v2]

$$$rule-grouping-v2$$$

Rule grouping splits alert event generation by one or more group key fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

Group key fields must align with the `BY` clause in your {{esql}} query's `STATS` command. See [Author rules](author-rules-v2.md) for query patterns.

Note that rule grouping is separate from notification grouping on an action policy, which controls how episodes batch into messages.

[CONTENT NEEDED for M2: M2 replaces the current `grouping.fields` approach with a `track_by` concept and introduces a `series.*` block that gives each series a stable, explicit identity. Update this section to document the `track_by` configuration, explain how the `series.*` block differs from the current `group_hash` approach, and revise any references to `grouping.fields` or the `BY` clause alignment requirement once the M2 schema is finalized.]

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

These behaviors apply when the base query returns zero rows. They do not help when you want to *detect* that a specific host or data source has gone silent — that requires a different query approach. See [No-data detection](esql-query-patterns-v2.md#no-data-esql-query-v2) in the authoring guide for an ES|QL pattern that surfaces silent sources as alert rows.

## Tags and investigation guide [tags-investigation-v2]

Alert-mode rules support two optional metadata fields:

- **Tags**: Free-form labels for filtering and organization.
- **Investigation guide**: A runbook stored with the rule so responders have context when an alert fires.

## Evaluate rule output [evaluate-rule-output-v2]

Before relying on a rule in production, evaluate it against recent data by running a preview. A full evaluation surfaces how many rows the query returns, how many alert events would be generated, sample alert event documents, and a histogram of matching row counts over time.
