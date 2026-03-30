---
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Overview of Kibana alerting v2: an ES|QL-based alerting framework with immutable alert events, notification policies, and alert lifecycle tracking."
---

# Kibana alerting v2 [alerting-overview-v2]

Kibana alerting v2 is a redesigned alerting framework built on [ES|QL](elasticsearch://reference/query-languages/esql.md). Rules evaluate source data on a configurable schedule using ES|QL queries and produce immutable alert event documents. You control exactly what data each alert carries by writing the query that computes it.

Kibana alerting v2 runs alongside [Kibana alerting v1](/explore-analyze/alerting/kibana-alerting-v1.md). There is no forced migration. You can adopt Kibana alerting v2 at your own pace and run both systems in parallel.

## Core concepts

Kibana alerting v2 introduces a layered model that separates detection from notification:

**Signals**
:   Immutable documents produced each time a rule evaluates and its query returns results. Signals are the raw output of every rule, written to an append-only data stream. Use signals for exploration, dashboards, and retroactive analysis.

**Alerts**
:   Signals with lifecycle tracking. When a rule runs in alert mode, the system tracks state transitions for each alert series: `inactive` → `pending` → `active` → `recovering` → `inactive`. Alerts are the primary operational unit for triage and response.

**Episodes**
:   A full lifecycle arc of an alert, from first breach to final recovery. Each episode groups the state transitions for a single alert series and is identified by an `episode_id`.

**Series**
:   A grouped time series of signals for a given rule and grouping key. Identified by a `group_hash` computed from the rule ID and grouping field values. Series are the unit for per-group snooze and recovery detection.

**Notification policies**
:   Standalone, reusable entities that control how and when alerts reach people and systems. Policies define matching conditions, grouping, throttling, and routing to workflow destinations. One policy can apply across multiple rules.

**Workflows**
:   User-defined automated sequences of tasks for delivering notifications and integrating with external systems. Notification policies reference workflows as destinations.

## How Kibana alerting v2 differs from Kibana alerting v1

| Aspect | Kibana alerting v1 | Kibana alerting v2 |
|---|---|---|
| **Query language** | Rule type defines what data is evaluated | You write the ES\|QL query directly |
| **Alert persistence** | Mutable documents updated in place | Immutable, append-only event documents |
| **Alert queryability** | Limited; alerts live in system indices | Full ES\|QL access in Discover and dashboards |
| **Notification control** | Per-action frequency and throttle on each rule | Notification policies: centralized matching, grouping, throttling, suppression |
| **Noise reduction** | Snooze per rule; limited grouping | Per-series snooze, acknowledgment per episode, activation thresholds, matcher-based routing, rules on alerts |
| **Rule definition** | Plugin-registered rule types with fixed schemas | ES\|QL queries with `KEEP` to control what data is stored |
| **Recovery detection** | Rule-type specific | Group hash comparison between consecutive evaluations |

## How detection and alert modes work

Every rule operates in one of two modes:

**Detect mode** (`kind: signal`)
:   The rule produces signal events for every query result. Signals are written to the alert events data stream and are available for exploration in Discover, but no lifecycle tracking or notifications occur. Use detect mode for broad monitoring with zero noise.

**Alert mode** (`kind: alert`)
:   The rule produces alert events with full lifecycle management. Alerts transition through episode states, trigger notification policies, and support triage actions like acknowledge and snooze. Use alert mode when you need actionable alerts.

You can switch a rule between modes at any time. Switching from alert to detect stops lifecycle tracking and notifications but continues producing signal events.

## What happens when a rule runs

From your perspective, a rule does the following on each run:

- It evaluates your ES|QL query over the lookback window you configured.
- It appends new rows to the **`.rule-events`** data stream: signal rows in detect mode, or signal and alert rows with episode fields in alert mode.
- In alert mode, it updates episode lifecycle (for example **pending**, **active**, **recovering**) according to your activation, recovery, and no-data settings.
- When an episode is ready for notifications, **notification policies** decide whether and how it is routed to workflows. Policies apply **after** lifecycle and thresholds; a short delay between “episode ready” and “notification sent” is normal when many policies or episodes are in play.

You can inspect raw history in Discover on **`.rule-events`** at any time, independent of whether notifications were sent.

## What you can do with Kibana alerting v2

- Write rules using any ES|QL query pattern: thresholds, change detection, ratios, no-data, SLO burn rate, and more.
- Create rules from the UI, from Discover, or with YAML for infrastructure-as-code workflows.
- Preview rule results against existing data before saving.
- Use notification policies to control routing, grouping, and throttling independently of rules.
- Investigate alerts in a dedicated inbox with filtering by status, severity, and custom fields.
- Explore alert history in Discover using ES|QL for trend analysis and operational reporting.
- Write rules on alerts: use the alert events index as a data source for correlation and escalation patterns.
