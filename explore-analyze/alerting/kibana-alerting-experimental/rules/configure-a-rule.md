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


Rule configuration is part of the {{alerting-v2-system}} in {{kib}}. The {{esql}} query defines what a rule detects. The settings on this page determine whether it behaves correctly in production. For query authoring, refer to [Author rules](author-rules.md).
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
For notification routing, refer to [Notifications](../notifications.md).
-->

This page covers how to configure a rule's mode, schedule, grouping, activation and recovery thresholds, and no-data behavior.

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

Several settings on this page apply only when the rule is in Alert mode.

## {{esql}} query [esql-query-rule]

The rule's {{esql}} query defines what to evaluate. It has a base query and an optional alert condition. Together they drive which rows become alert events and how no-data behavior applies. Refer to [{{esql}} query structure](author-rules.md#esql-query-structure) for how those pieces interact with no-data behavior and `KEEP`.

### Query parameters [query-parameters]

Two types of parameters are available in {{esql}} rule queries: reserved runtime parameters and UI form variables.

**Reserved runtime parameters**

The executor automatically binds `?_tstart` and `?_tend` to the lookback window start and end timestamps on every rule evaluation. Use these to filter your query to the evaluation window:

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT(*) BY service.name
| WHERE error_count > 10
```

These are the only parameters supported across all rule creation methods (rule form, YAML editor, and API).

**Rule form variables**

The rule form supports additional `?param` placeholders — for example, `?threshold` — through ES|QL Control variables. The form resolves these variables and inlines their values into the query string before saving. The stored rule and any API or YAML representation contain the resolved values, not the placeholder tokens.

## Severity [rule-severity]

Severity is optional. To set it, include a column named `severity` in your {{esql}} query output and add it to your `KEEP` list. The framework reads that column after each evaluation and maps it to one of five fixed levels:

| Value | Meaning |
| --- | --- |
| `info` | Informational; lowest urgency |
| `low` | Low-severity condition |
| `medium` | Moderate-severity condition |
| `high` | High-severity condition |
| `critical` | Critical; highest urgency |

### How the {{alerting-v2-system}} reads severity values

The {{alerting-v2-system}} reads the `severity` column after each evaluation and applies the following rules:

- Matching is case-insensitive.
- Values that don't match one of the five levels are silently ignored. The alert episode is still created, but `severity` isn't set.
- Severity is only set on `breached` events. `recovered` and `no_data` events don't carry a severity value.

### Stored fields

When severity is set, the {{alerting-v2-system}} stores the following field on the alert episode, available to action policy matchers:

| Field | Description |
| --- | --- |
| `severity` | The severity value from the most recent breached event. |

Refer to [Rule event and field reference](rule-event-field-reference.md#episode-fields) for more information about this field.

### Example

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Bind to the rule's configured lookback window
| STATS
    errors = COUNT_IF(outcome == "failure"),
    total  = COUNT(*)
  BY service.name
| EVAL burn_rate = errors / total
| EVAL severity = CASE(
    burn_rate > 14.4, "critical",
    burn_rate > 6.0,  "high",
    burn_rate > 1.0,  "medium",
    "low"
  )
| WHERE burn_rate > 1.0
| KEEP service.name, burn_rate, severity
```

- **`WHERE`** (time filter) - Scopes the query to the rule's configured lookback window using the reserved `?_tstart` and `?_tend` parameters.
- **`STATS`** - Counts failures and total requests, grouped by service.
- **`EVAL burn_rate`** - Computes the error rate as a fraction of failures to total requests.
- **`EVAL severity`** - Maps the burn rate to a severity level.
- **`WHERE burn_rate`** - Only services above the minimum threshold count as breaches.
- **`KEEP`** - Includes `severity` in the output so the {{alerting-v2-system}} reads and stores it.

## Rule grouping [rule-grouping]

Rule grouping lets a single rule track multiple things independently. For example, a rule monitoring CPU usage across hosts can produce a separate alert series for each host, rather than one alert for everything combined.

Each group tracks its own lifecycle, recovery, and snooze state.

Rule grouping controls how alert series are created. Notification grouping (configured on an action policy) controls how those alert episodes are batched into messages. These are separate settings.

### Aligning `BY` fields with your rule's query

The `BY` fields you specify for grouping must match the columns in the `BY` clause of your {{esql}} `STATS` command. If they don't match, the grouping configuration won't work as expected.

:::{tip}
Write the query first, then set the group fields. That way the `BY` columns are already defined and you can select them directly. If you later add or remove a `BY` field in the query, update the group fields to match.
:::

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

These settings are only available for Alert-mode rules.

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

Recovery thresholds control when an active alert episode transitions back to inactive. The same delay modes available for activation — consecutive recoveries required, minimum recovery duration, or both — apply here.

| Field | Description |
| --- | --- |
| `recovering_count` | Consecutive recoveries required |
| `recovering_timeframe` | Minimum duration for recovery |
| `recovering_operator` | How to combine count and timeframe (`AND` or `OR`) |

Time frame fields use the same 5 seconds to 365 days bounds as activation timeframes.

:::{note}
The `recovery_strategy` field controls how recovery is detected, separately from how many recoveries are required. When creating a rule through the UI, `recovery_strategy` defaults to `no_breach`, which recovers the alert episode when its active group no longer appears in the breach batch.

When creating a rule through Agent Builder, you can omit `recovery_strategy` entirely to suppress recovery events and keep alert episodes active until closed manually. For the full field reference, go to [YAML rule schema reference](yaml-rule-schema-reference.md#recovery-strategy).
:::

## No-data handling [no-data-handling]

No-data handling controls what happens when a rule executes and the base query returns no results. Proper configuration prevents false recoveries and misleading `no_data` events when data sources stop reporting.

### Behaviors

Set `no_data_strategy` to one of the following values:

| Behavior | Effect |
| --- | --- |
| `emit` | Record a no-data event |
| `last_known_status` | Carry forward the previous status |
| `recover` | Treat absence as recovery |
| `none` | Disable no-data detection |

These behaviors apply when the base query returns zero rows. They don't help when you want to *detect* that a specific host or data source has gone silent. That requires a different query approach. See [No-data detection](esql-query-patterns.md#no-data-esql-query) in the authoring guide for an {{esql}} pattern that surfaces silent sources as alert rows.

## Tags and runbooks [tags-investigation]

Alert-mode rules support two optional metadata fields:

- **Tags** - Free-form labels for filtering and organization.
- **Runbooks** - An investigation guide stored with the rule so responders have context when alerts are generated.

## Evaluate rule output [evaluate-rule-output]

Before relying on a rule in production, evaluate it against recent data by running a preview. A full evaluation surfaces how many rows the query returns, how many alert events would be generated, sample alert event documents, and a histogram of matching row counts over time.
