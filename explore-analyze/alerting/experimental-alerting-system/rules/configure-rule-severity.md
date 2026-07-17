---
navigation_title: Severity
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Assign severity levels to alert episodes in Kibana's experimental alerting system using a severity column in ES|QL query output."
---

# Severity in the {{alerting-v2-system}} [rule-severity]

Severity is an optional setting for rules in the {{alerting-v2-system}}. To set it, include a column named `severity` in your {{esql}} query output and add it to your `KEEP` list. The framework reads that column after each evaluation and maps it to one of five fixed levels.

| Value | Description | Urgency |
| --- | --- | --- |
| `info` | Informational event worth recording. | No action required. |
| `low` | Minor condition that might need monitoring. | Review when convenient. |
| `medium` | Notable condition that warrants investigation. | Investigate soon. |
| `high` | Serious condition requiring prompt attention. | Address promptly. |
| `critical` | Severe condition requiring immediate action. | Act immediately. |

## When to configure severity [severity-when-to-use]

Configure severity when:

* You want to route different urgency levels to different notification channels, for example, send `critical` episodes to an on-call channel and `low` episodes to a review queue.
* You want to filter the Alerts UI by urgency to help triage during incidents.
* The rule's detection logic can meaningfully distinguish between urgency levels through a computed metric, such as burn rate, error count, or latency percentile.

Skip severity when:

* All breaches from the rule are equally urgent. A fixed label in the rule's tags is simpler and doesn't require query changes.
* The underlying data doesn't produce a reliable metric to grade urgency. Severity that's frequently wrong generates more noise than routing by severity resolves.

## Severity behavior and usage [severity-behavior]

Keep the following in mind when configuring severity.

- **Matching is case-insensitive** - `critical`, `Critical`, and `CRITICAL` are all treated the same. You can use any casing in your `EVAL` expression.
- **Unrecognized values are silently ignored** - If the `severity` column contains a value that doesn't match one of the five levels, the alert episode is still created but `severity` is not set. If severity isn't appearing as expected, check the exact string your query is producing.
- **Severity only applies to breached events** - `recovered` and `no_data` events don't carry a severity value. Action policy matchers that filter by severity only match open episodes.

<!-- TODO - After action policies docs PR #6525 merge, uncomment the following list items: 
- **Severity can change mid-episode** — An alert episode can escalate or de-escalate without reopening. Action policy matching picks up the new value on the next dispatcher cycle. Refer to [Manage severity escalation notifications](../action-policies/severity-escalation.md) for routing examples.
- **The `severity` field is available in action policy matchers** - Once set, the value is stored on the alert episode and can be used to route episodes by urgency — for example, sending `critical` episodes to an on-call channel while `low` episodes go to a review queue. Refer to [Rule event field reference](../alerts/field-reference.md) for the full field reference.
-->

## Examples

### Static severity for a fixed threshold rule

Create a rule that alerts when a service logs more than 100 5xx errors in the lookback window. Every breach of this rule is equally urgent, so assign a fixed severity rather than computing it dynamically. The `EVAL` command adds a constant `severity` column to every row the query returns.

Every breach from this rule produces a `critical` episode.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name
| WHERE error_count > 100
| EVAL severity = "critical"
| KEEP service.name, error_count, severity
```

### Dynamic severity based on burn rate

Create a rule that grades each service's error rate against its SLO error budget. Use `CASE` to map the computed burn rate to different severity levels: services consuming error budget at 14.4× baseline or above are `critical`, those between 6× and 14.4× are `high`, and so on. Only services above 1× are returned, so below-threshold services don't generate alert rows.

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

Here's what the severity-specific steps do:

- **`EVAL burn_rate`**: Computes the error rate as failures over total requests.
- **`EVAL severity`**: Maps the burn rate to a severity level.
- **`KEEP`**: Keeps `severity` in the output so the {{alerting-v2-system}} reads and stores it.
