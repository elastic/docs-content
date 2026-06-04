---
navigation_title: Author rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Learn how to write ES|QL queries for rules. Choose a rule mode, structure a base query and alert condition, set thresholds, and assign severity levels."
---

# Rule authoring in the {{alerting-v2-system}} [author-rules]

Rule authoring is part of the {{alerting-v2-system}} in {{kib}}. Authoring a rule means deciding three things: what condition in your data counts as a problem, whether you want the rule to silently record matches or actively track issues through to resolution, and which fields to carry forward onto each alert event so you can route and triage effectively. Getting these decisions right in the query is what makes the difference between a rule that fires on everything and one that surfaces the problems that actually need attention.

This page covers the query concepts behind a rule definition. For settings beyond the query (such as schedules, grouping, and lifecycle thresholds), refer to [Configure a rule](configure-a-rule.md). Once you understand what goes into a rule, you can write one using the [rule builder](create-rule-from-rule-builder.md), [YAML editor](create-rule-with-yaml.md), or [a Discover session](create-rule-from-discover.md).

## Choose a rule mode

Before creating the rule, decide what you want it to do:

| Mode | What it does |
| --- | --- |
| Detect (`kind: signal`) | Records query matches as signals. No alert episodes, no notifications. Good for testing a query or building a data history without alerting anyone. |
| Alert (`kind: alert`) | Records matches and maintains alert episodes with lifecycle states. Alert episodes appear on the **Alerts** page and can be matched by action policies for notifications. |

You can switch a rule's mode after creation from the rule list or rule detail page.

## The {{esql}} query [esql-query-structure]

Every rule has two parts to its query: the base query and the alert conditions.

### Base query (required)  
The main {{esql}} expression. It runs on every evaluation, selects data from `FROM`, shapes results with `STATS`, `WHERE`, `EVAL`, and controls which fields are stored with `KEEP`. The base query always runs, even when no breach occurs, which is what enables no-data detection and recovery.

### Alert conditions (optional)  
A `WHERE` clause applied after the base query. Only rows that pass the alert condition are treated as breaches. Without an alert condition, every row returned by the base query is a breach.

```esql
-- Base query: compute average CPU per host
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name

-- Alert condition: only rows above the threshold count as breaches
WHERE avg_cpu > 0.9
```

The `KEEP` command controls which fields appear on each stored alert event. Only the fields you `KEEP` are available for policy matchers, grouping keys, and triage in the Alerts UI.

### Recovery condition [recovery-condition]

Recovery conditions are optional. They determine when an active alert episode closes.

Three recovery types are available:

| Type | Behavior |
| --- | --- |
| Default | The alert episode recovers automatically when the alert condition is no longer met. |
| Custom | Uses a separate {{esql}} expression you define. The alert episode recovers when that expression returns no rows. |
| No recovery | The alert episode stays active until manually closed. *(Coming soon.)* |

When no recovery condition is configured, Default recovery applies. Use a custom recovery condition when the absence of a breach isn't a reliable recovery indicator — for example, when the alert condition uses a narrow lookback window and you want recovery to require the condition to stay clear across a longer period, or when the recovery logic requires a different query shape than the alert detection.

## Data sources

Use `FROM` to point the rule at the indices or data streams to read. The query itself defines the scope. There's no separate data source step.

```esql
FROM logs-checkout-service-*
| WHERE http.response.status_code >= 500
| STATS error_count = COUNT(*) BY service.name
| KEEP service.name, error_count
```

The [{{esql}} reference](elasticsearch://reference/query-languages/esql.md) covers all available commands and processing functions.

## Conditions and thresholds [conditions-and-thresholds]

The alert condition in {{esql}} defines what counts as a breach in each evaluation.

The activation and recovery thresholds on the rule are separate from the query. They control how many consecutive breaches must occur, or how long the condition must persist, before an alert episode becomes active or moves back to inactive. Those settings are in [Configure a rule](configure-a-rule.md#activation-recovery-thresholds).

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
For how alert states connect to episodes, refer to [Alert lifecycle](../alerts.md#alert-lifecycle).
-->

## Severity levels [severity-levels]

Severity is a first-class field on alert episodes in the {{alerting-v2-system}}. To set severity, include a column named `severity` in your ES|QL query output and add it to your `KEEP` list. The framework reads that column after each evaluation and maps it to one of five fixed levels:

| Value | Meaning |
| --- | --- |
| `info` | Informational; lowest urgency |
| `low` | Low-severity condition |
| `medium` | Moderate-severity condition |
| `high` | High-severity condition |
| `critical` | Critical; highest urgency |

Severity matching is case-insensitive. Values that don't match one of the five levels are silently ignored — the alert episode is still created, but `episode.severity` is not set.

Severity is set only on `breached` rule events. `recovered` and `no_data` events don't carry a severity value.

When severity is set, the framework stores two fields on the alert episode:

- `episode.severity` — the severity value from the most recent breached event (current state).
- `episode.severity_max` — the highest severity level observed across the episode's lifetime. Useful for routing like "this episode peaked at critical."

Both fields are available for action policy matchers. For the full field reference, see [Rule event and field reference](rule-event-field-reference.md#episode-fields).

```esql
FROM metrics-*
| STATS
    errors_5m = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 5 minutes),
    total_5m   = COUNT_IF(@timestamp >= NOW() - 5 minutes)
  BY service.name
| EVAL burn_5m = errors_5m / total_5m
| EVAL severity = CASE(
    burn_5m > 14.4, "critical",
    burn_5m > 6.0,  "high",
    burn_5m > 1.0,  "medium",
    "low"
  )
| WHERE burn_5m > 1.0
| KEEP service.name, burn_5m, severity
```

The `severity` column in `KEEP` is what tells the framework to set `episode.severity` on each resulting alert episode.

## Next steps

Once you understand the query structure, explore [{{esql}} query patterns](esql-query-patterns.md) for advanced use cases including SLO burn rate queries, no-data detection, persistent breach detection, and unsupported operations.

<!--
## Rule forms [rule-forms]

[CONTENT NEEDED for M2: UI. This page needs a procedure once rule forms are finalized: what forms are available, what each one pre-fills in the ES|QL query or YAML, and how to start from a form versus authoring a rule from scratch. Verify the name "rule forms" and the available form types against the shipped product before publishing.]
-->
