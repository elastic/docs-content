---
navigation_title: Author rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Write {{alerting-v2}} rules: rule modes, what a rule contains, {{esql}} query structure, conditions, and how to configure and create rules."
---

# Write and configure {{alerting-v2}} rules [author-rules-v2]

$$$author-rules-v2$$$

A {{alerting-v2}} rule is an {{esql}} query that runs on a schedule. There are no fixed rule types to choose from. You write {{esql}} directly to describe what to detect, what counts as a breach, and which fields to store on each event.

This page covers what goes into a rule and how the {{esql}} query works. Use the sections below to understand the structure before creating or configuring your rule.

## Choose a rule mode

Every rule runs in one of two modes. Choose the mode before writing the query, as it affects which features are available.

| Mode | What it does |
|---|---|
| Detect (`kind: signal`) | Records query matches as signals. No episodes, no notifications. Useful for testing a query or building a data history without alerting anyone. |
| Alert (`kind: alert`) | Records matches and maintains alert episodes with lifecycle states. Episodes appear on the **Alerts** page and can be matched by action policies for notifications. |

You can switch a rule's mode after creation from the rule list or rule detail page.

## What a rule contains

A rule definition includes the following sections:

| Section | Purpose |
|---|---|
| **Metadata** | Name, description, tags, owner |
| **Evaluation** | {{esql}} query (base query + optional alert condition) |
| **Schedule** | Execution interval and lookback window |
| **Grouping** | Fields to split alert events by (for example, `host.name`, `service.name`) |
| **State transition** | Activation and recovery thresholds (Alert mode only) |
| **Recovery policy** | How recovery is detected (Alert mode only) |
| **No-data handling** | Behavior when the query returns no results |
| **Action policies** | Policies that control how alerts are routed (global; not stored on the rule). See [Notifications](../notifications.md#action-policies-v2). |
| **Workflows** | Direct workflow links for rule-triggered automation. See [Workflows for {{alerting-v2}}](../workflows-alerting-v2.md#workflows-v2). |

## {{esql}} query structure [esql-query-structure]

The {{esql}} query is the core of every rule. It has two parts:

**Base query** (required)
:   The main {{esql}} expression that selects, aggregates, and transforms your data. The base query always runs, even when no breach occurs, which enables no-data detection and recovery.

**Alert condition** (optional)
:   A `WHERE` clause applied after the base query. Only rows that pass the alert condition are treated as breaches. Without one, every row returned by the base query is a breach.

```esql
-- Base query
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name

-- Alert condition (applied as a WHERE clause)
WHERE avg_cpu > 0.9
```

The `KEEP` command controls which fields are stored in each alert event document. Only the fields you `KEEP` are available for policy matchers, grouping keys, and triage in the Alerts UI.

Use `FROM` to point the rule at the indices or data streams to read. The query itself defines the scope — there is no separate data source step. The [{{esql}} reference](elasticsearch://reference/query-languages/esql.md) covers all available commands and functions.

## Conditions and thresholds [conditions-and-thresholds]

The alert condition in {{esql}} defines what counts as a breach in each evaluation. Activation and recovery thresholds on the rule are separate from the query: they control how many consecutive breaches must occur, or how long the condition must persist, before an episode becomes active or returns to inactive.

For the threshold settings, refer to [Configure a rule](configure-a-rule.md#activation-recovery-thresholds-v2). For how states connect to episodes, refer to [Alert lifecycle](../alerts.md#alert-lifecycle-v2).

## Severity levels [severity-levels]

Severity is carried by convention as a field under `data.*`, for example `data.severity` or `data.priority`. Include it in your `KEEP` so it is available as a matcher field on action policies, for example `data.severity: "critical"` in a policy KQL matcher.

There is no required severity field name or fixed value set. Use whatever convention your team aligns on, and reference those same field names in your action policies.

## Configure the rule

After you know what the rule should evaluate, configure how it runs and manages state. These settings live on the rule itself and are separate from the {{esql}} query:

- **Schedule and lookback**: how often the rule runs and how far back each evaluation looks.
- **Grouping**: which fields split alert event generation into separate series.
- **Activation and recovery thresholds**: how many consecutive breaches or how long a condition must hold before an episode opens or closes.
- **No-data handling**: what happens when the query returns no rows.
- **Tags and investigation guide**: optional metadata attached to Alert-mode rules.

For the full field reference and configuration procedures, refer to [Configure a rule](configure-a-rule.md).

## Choose how to create a rule

Pick the creation path that fits how you work:

- [Create using the rule builder](create-rule-from-rule-builder.md): Interactive form with a live preview before saving. Best for exploring a new rule.
- [Create with YAML](create-rule-with-yaml.md): Version-controlled definitions for repeatable or bulk deployments.
- [Create from Discover](create-rule-from-discover.md): Promote an existing {{esql}} session from Discover into a rule.

## Rule templates [rule-templates-v2]

[CONTENT NEEDED: List supported rule template types, what each template pre-fills in ES|QL or YAML, and how templates relate to user-authored queries once the product catalog is finalized.]
