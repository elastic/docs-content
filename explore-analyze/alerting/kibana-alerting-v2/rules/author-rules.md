---
navigation_title: Author rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Write ES|QL queries for {{alerting-v2}} rules: modes, query structure, base query, alert condition, thresholds, and severity."
---

# Author {{alerting-v2}} rules [author-rules-v2]

$$$author-rules-v2$$$

Every {{alerting-v2}} rule is an {{esql}} query. Instead of choosing from a catalog of fixed rule types, you write {{esql}} directly. Describe what to look for, what counts as a breach, and which fields to store on each event.

This page covers the query concepts behind a rule definition. For settings beyond the query (such as schedules, grouping, and lifecycle thresholds), refer to [Configure a rule](configure-a-rule.md). Once you understand what goes into a rule, you can write one using the [rule builder](create-rule-from-rule-builder.md), [YAML editor](create-rule-with-yaml.md), or [a Discover session](create-rule-from-discover.md).

## Choose a rule mode

Before creating the rule, decide what you want it to do:

| Mode | What it does |
| --- | --- |
| Detect (`kind: signal`) | Records query matches as signals. No episodes, no notifications. Good for testing a query or building a data history without alerting anyone. |
| Alert (`kind: alert`) | Records matches and maintains alert episodes with lifecycle states. Episodes appear on the **Alerts** page and can be matched by action policies for notifications. |

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

## Data sources

Use `FROM` to point the rule at the indices or data streams to read. The query itself defines the scope; there is no separate data source step.

```esql
FROM logs-checkout-service-*
| WHERE http.response.status_code >= 500
| STATS error_count = COUNT(*) BY service.name
| KEEP service.name, error_count
```

The [{{esql}} reference](elasticsearch://reference/query-languages/esql.md) covers all available commands and processing functions.

## Conditions and thresholds [conditions-and-thresholds]

The alert condition in {{esql}} defines what counts as a breach in each evaluation.

The activation and recovery thresholds on the rule are separate from the query. They control how many consecutive breaches must occur, or how long the condition must persist, before an episode becomes active or moves back to inactive. Those settings are in [Configure a rule](configure-a-rule.md#activation-recovery-thresholds-v2).

For how alert states connect to episodes, refer to [Alert lifecycle](../alerts.md#alert-lifecycle-v2).

## Severity levels [severity-levels]

Severity is carried by convention as a field under `data.*`, for example `data.severity` or `data.priority`. Include it in your `KEEP` so it is available as a matcher field on action policies, for example `data.severity: "critical"` in a policy KQL matcher.

There is no required severity field name or fixed value set. Use whatever convention your team aligns on, and reference those same field names in your action policies.

## Rule templates [rule-templates-v2]

[CONTENT NEEDED: List supported rule template types, what each template pre-fills in ES|QL or YAML, and how templates relate to user-authored queries once the product catalog is finalized.]
