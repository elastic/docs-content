---
navigation_title: Author rules
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Create Kibana alerting v2 rules using ES|QL queries from the UI, Discover, or YAML in detect or alert mode."
---

# Author Kibana alerting v2 rules [author-rules-v2]

A Kibana alerting v2 rule defines what to look for in your data. It evaluates source data such as logs, metrics, traces, or alert events from other rules on a configurable schedule using an ES|QL query and produces alert event documents when conditions are met.

## Rule modes

Every rule operates in one of two modes:

- **Detect mode** (`kind: signal`): produces signal events for exploration and analysis. No lifecycle tracking, no notifications. Use detect mode for broad monitoring without noise.
- **Alert mode** (`kind: alert`): produces alert events with full lifecycle management. Alerts transition through episode states (`inactive` → `pending` → `active` → `recovering` → `inactive`), trigger notification policies, and support triage actions. Use alert mode when conditions require human response.

You can switch between modes at any time from the rule list or rule details page.

## Ways to create a rule

You can create rules in three ways:

- **[From the UI](author-rules/create-rules-ui.md)**: use the rule creation form with interactive controls and YAML mode toggle. Preview results before saving.
- **[From Discover](author-rules/create-rules-discover.md)**: convert an ES|QL query you've built in Discover directly into a rule. The query pre-populates the rule definition.
- **[With YAML](author-rules/create-rules-yaml.md)**: define rules as YAML documents for infrastructure-as-code workflows, version control, and bulk provisioning.

## What a rule contains

A rule definition includes:

| Section | Purpose |
|---|---|
| **Metadata** | Name, description, tags, owner |
| **Evaluation** | ES\|QL query (base query + optional alert condition) |
| **Schedule** | Execution interval and lookback window |
| **Grouping** | Fields to split alert events by (for example, `host.name`, `service.name`) |
| **State transition** | Activation and recovery thresholds (alert mode only) |
| **Recovery policy** | How recovery is detected (alert mode only) |
| **No-data handling** | Behavior when the query returns no results |
| **Notification policies** | References to policies that control how alerts are routed |
| **Workflows** | Direct workflow links for rule-triggered actions |

## ES|QL query structure

The ES|QL query is the core of every rule. It has two parts:

**Base query** (required)
:   The main ES|QL query that selects, aggregates, and transforms your data. The base query always runs, even when no alert condition is met. This enables no-data detection and recovery.

**Alert condition** (optional)
:   A `WHERE` clause that filters the base query results to only the rows that represent a breach. When the alert condition is set, the system can distinguish between "data exists but doesn't breach" and "no data at all."

```esql
-- Base query
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name

-- Alert condition (applied as a WHERE clause)
WHERE avg_cpu > 0.9
```

The `KEEP` command controls which fields are stored in each alert event document. Only the fields you `KEEP` appear in the `data` field of the alert event.
