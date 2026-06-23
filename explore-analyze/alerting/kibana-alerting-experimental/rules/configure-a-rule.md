---
navigation_title: Configure a rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure rules in the experimental alerting system: mode, ES|QL, grouping, schedule, lookback, activation and recovery, no-data handling, tags, and evaluation."
---

# Configure a rule in {{alerting-v2-system}} [rule-settings]


Rule configuration is part of the {{alerting-v2-system}} in {{kib}}. The {{esql}} query defines what a rule detects. The settings on this page determine whether it behaves correctly in production: how often it runs, how it groups related problems, when it opens and closes alerts, and what it does when data stops arriving.

For query authoring, refer to [Author rules](author-rules.md).
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
For notification routing, refer to [Notifications](../notifications.md).
-->

:::{note}
For Alert-mode rules, you can create and attach action policies directly from the rule form's **Actions** step. Existing action policies that match the rule are listed on load. If none exist, an onboarding panel appears. Action policies are created or updated alongside the rule when you save. The **Actions** step is not shown for Signal-mode rules.

You can also manage action policies independently from the **Action policies** area, using KQL matchers to scope them to any episodes you want to route.
:::

## Rule mode [rule-mode]

Choose a mode that matches how you want to use results:

| Mode | Behavior |
| --- | --- |
| Signal | Signals only: the rule produces detections without alert lifecycle tracking or notifications. |
| Alert | Lifecycle tracking and actions. Alerts move through states (pending, active, recovering, and so on), and you can attach action policies so alert episodes dispatch through workflows. |

Several settings on this page apply only when the rule is in Alert mode (`kind: alert`).

## {{esql}} query [esql-query-rule]

The rule's {{esql}} query defines what to evaluate. It has a base query and an optional alert condition. Together they drive which rows become alert events and how no-data behavior applies. See [{{esql}} query structure](author-rules.md#esql-query-structure) for how those pieces interact with no-data behavior and `KEEP`.

## Rule grouping [rule-grouping]


Rule grouping splits alert event generation by one or more group key fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

Group key fields must align with the `BY` clause in your {{esql}} query's `STATS` command. See [Author rules](author-rules.md) for query patterns.

When writing a rule that uses grouping, writing the query first and then specifying group fields avoids mismatches between the query output and the grouping configuration. The group fields in the rule form reflect the columns produced by the `STATS ... BY` clause, so if you add or remove a `BY` field in the query, the corresponding group field must be updated to match.

Note that rule grouping is separate from notification grouping on an action policy, which controls how alert episodes batch into messages.

<!--[CONTENT NEEDED for M2: M2 replaces the current `grouping.fields` approach with a `track_by` concept and introduces a `series.*` block that gives each series a stable, explicit identity. Update this section to document the `track_by` configuration, explain how the `series.*` block differs from the current `group_hash` approach, and revise any references to `grouping.fields` or the `BY` clause alignment requirement once the M2 schema is finalized.]
-->

## Schedule and lookback [schedule-lookback]


The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

### Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates.

{{kib}} enforces a minimum interval of 5 seconds and a maximum of 365 days for duration fields (including this one). Values outside that range are rejected.

### Lookback window

The lookback window (`schedule.lookback`) determines the time range that the {{esql}} query covers.

The lookback must not exceed 365 days. If the lookback is shorter than the execution interval, evaluations can miss data between runs. Use a lookback at least as long as the execution interval unless you have a deliberate reason not to.

## Activation and recovery thresholds [activation-recovery-thresholds]


Activation and recovery thresholds control when alerts transition between lifecycle states. They reduce noise from short spikes and from rapid flapping between active and recovered.

These settings are only available for Alert-mode rules (`kind: alert`).

### Activation thresholds

Activation thresholds control when a breached rule transitions from pending to active. Three delay modes are available:

| Mode | Behavior | When to use |
| --- | --- | --- |
| Immediate | Opens an alert episode as soon as the threshold is breached on the first evaluation. | Use when any single breach warrants attention and latency matters. |
| Breaches | Opens an alert episode after the threshold is breached a set number of times in a row. | Use when a single breach isn't enough reason to act (for example, when brief spikes are normal and you only care if the condition keeps firing). |
| Duration | Opens an alert episode after the threshold has been continuously breached for a set time. | Use when duration of the problem matters more than how many evaluations caught it (for example, sustained high CPU rather than a momentary spike). |

You can also use Breaches and Duration together. For example, require the threshold to be breached five times in a row _and_ persist for at least two minutes before an alert episode opens. Use `pending_operator` to control whether both constraints must be met (`AND`) or either one is enough (`OR`).

Configure these modes using the following fields. Timeframe values must be between 5 seconds and 365 days.

| Field | Description |
| --- | --- |
| `pending_count` | Number of consecutive breach evaluations required before the alert episode opens. |
| `pending_timeframe` | How long the condition must remain breached before the alert episode opens. |
| `pending_operator` | When both `pending_count` and `pending_timeframe` are set, controls whether both must be satisfied (`AND`) or either one is enough (`OR`). |

### Recovery thresholds

| Field | Description |
| --- | --- |
| `recovering_count` | Consecutive recoveries required |
| `recovering_timeframe` | Minimum duration for recovery |
| `recovering_operator` | How to combine count and timeframe (`AND` or `OR`) |

Time frame fields use the same 5 seconds to 365 days bounds as activation timeframes.

:::{note}
The `recovery_policy` field controls how recovery is detected, separately from how many recoveries are required. When creating a rule through the UI, `recovery_policy.type` defaults to `no_breach`, which recovers the alert episode when its active group no longer appears in the breach batch. When creating a rule through the API or Agent Builder, you can omit `recovery_policy` entirely to suppress recovery events and keep alert episodes active until closed manually. For the full field reference, go to [YAML rule schema reference](yaml-rule-schema-reference.md#recovery-policy-fields).
:::

## No-data handling [no-data-handling]

No-data handling controls what happens when a rule executes and the base query returns no results. Proper configuration prevents false recoveries and misleading `no_data` events when data sources stop reporting.

### Behaviors

Set `no_data.behavior` to one of the following values:

| Behavior | Effect |
| --- | --- |
| `no_data` | Record a no-data event (default) |
| `last_status` | Carry forward the previous status |
| `recover` | Treat absence as recovery |

These behaviors apply when the base query returns zero rows. They don't help when you want to *detect* that a specific host or data source has gone silent. That requires a different query approach. See [No-data detection](esql-query-patterns.md#no-data-esql-query) in the authoring guide for an {{esql}} pattern that surfaces silent sources as alert rows.

## Tags and investigation guide [tags-investigation]

Alert-mode rules support two optional metadata fields:

- **Tags**: Free-form labels for filtering and organization.
- **Investigation guide**: A runbook stored with the rule so responders have context when an alert fires.

## Evaluate rule output [evaluate-rule-output]

Before relying on a rule in production, evaluate it against recent data by running a preview. A full evaluation surfaces how many rows the query returns, how many alert events would be generated, sample alert event documents, and a histogram of matching row counts over time.
