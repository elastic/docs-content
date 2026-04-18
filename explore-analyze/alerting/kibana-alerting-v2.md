---
applies_to:
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: Learn what {{alerting-v2}} offers, who it is for, and where to go next in the documentation.
---

# {{alerting-v2}} [alerting-overview-v2]

{{alerting-v2}} is a redesigned alerting framework built on [ES|QL](elasticsearch://reference/query-languages/esql.md). Rules evaluate source data on a configurable schedule using ES|QL queries and produce immutable alert event documents. You control exactly what data each alert carries by writing the query that computes it.

It runs next to [Kibana alerting v1](kibana-alerting-v1.md). You can adopt {{alerting-v2}} at your own pace. There is no forced migration.

## What is {{alerting-v2}} [alerting-v2-what]

{{alerting-v2}} is a rules-based system that checks your data on a schedule, stores a clear record of what happened over time, and can send notifications through shared settings that apply across many rules. You can start with guided setup and grow into more advanced options when you are ready.

## Why use {{alerting-v2}} [alerting-v2-why]

Detection alone is not always enough. Teams often need a **record they can search later**, **notifications that do not repeat the same setup on every rule**, and a **consistent way to track an issue** from first occurrence through resolution. {{alerting-v2}} is aimed at those needs.

It helps with challenges such as:

* **Limited visibility**: Store outcomes over time so you can review trends and past behavior, not only what is open right now.
* **Notification overload**: Reuse how and when messages go out instead of configuring each rule in isolation.
* **Rigid rule types**: Define what to watch with queries and carry the fields that matter for your responders.
* **Siloed tools**: Use one query language for exploration and for alerting so skills transfer.

## Core concepts

{{alerting-v2}} introduces a layered model that separates detection from notification:

Signals
:   Immutable documents produced each time a rule evaluates and its query returns results. Signals are the raw output of every rule, written to an append-only data stream. Use signals for exploration, dashboards, and retroactive analysis.

Alerts
:   Signals with lifecycle tracking. When a rule runs in alert mode, the system tracks state transitions for each alert series: `inactive` → `pending` → `active` → `recovering` → `inactive`. Alerts are the primary operational unit for triage and response.

Episodes
:   A full lifecycle arc of an alert, from first breach to final recovery. Each episode groups the state transitions for a single alert series and is identified by an `episode_id`.

Series
:   A grouped time series of signals for a given rule and grouping key. Identified by a `group_hash` computed from the rule ID and grouping field values. Series are the unit for per-group snooze and recovery detection.

Action policies
:   Standalone, reusable entities that control how and when alerts reach people and systems. Policies define matching conditions, grouping, throttling, and routing to workflow destinations. One policy can apply across multiple rules.

Workflows
:   User-defined automated sequences of tasks for delivering notifications and integrating with external systems. Action policies reference workflows as destinations.

## Who should use {{alerting-v2}} [alerting-v2-who]

{{alerting-v2}} is a good fit on {{stack}} 9.4+ or in {{serverless-full}} when you want query-driven alerting, shared notification behavior through action policies, and searchable history.

## How {{alerting-v2}} differs from Kibana alerting v1 [alerting-v2-diff-v1]

| Aspect | Kibana alerting v1 | {{alerting-v2}} |
|---|---|---|
| Query language | Rule type defines what data is evaluated | You write the ES\|QL query directly |
| Alert persistence | Mutable documents updated in place | Immutable, append-only event documents |
| Alert queryability | Limited; alerts live in system indices | Full ES\|QL access in Discover and dashboards |
| Notification control | Per-action frequency and throttle on each rule | Action policies: centralized matching, grouping, throttling, suppression |
| Noise reduction | Snooze per rule; limited grouping | Per-series snooze, acknowledgment per episode, activation thresholds, matcher-based routing, rules on alerts |
| Rule definition | Plugin-registered rule types with fixed schemas | ES\|QL queries with `KEEP` to control what data is stored |
| Recovery detection | Rule-type specific | Group hash comparison between consecutive evaluations |

## Key concepts [alerting-v2-concepts]

These topics are explained in depth on dedicated pages:

* **Rules and queries**: How you define what to evaluate, optional detect vs alert behavior, schedules, and authoring from the UI, Discover, or YAML. Refer to [Author rules](kibana-alerting-v2/author-rules.md).
* **Notifications**: How shared settings decide who gets notified and how messages are grouped or throttled. Refer to [Action policies](kibana-alerting-v2/author-rules/rule-settings/action-policies.md).
* **Alerts and investigation**: How to view, filter, and work with findings in the product and in Discover. Refer to [Manage alerts](kibana-alerting-v2/manage-alerts.md).
* **Noise and lifecycle**: Snooze, grouping, thresholds, maintenance windows, and related controls. Refer to [Reduce noise](kibana-alerting-v2/reduce-noise.md).
* **Fields and storage**: Names and meanings of fields written for rules and actions. Refer to [Rule event and action field reference](kibana-alerting-v2/alert-event-field-reference.md).

## How detection and alert modes work

Every rule operates in one of two modes:

Detect mode (`kind: signal`)
:   The rule produces signal events for every query result. Signals are written to the alert events data stream and are available for exploration in Discover, but no lifecycle tracking or notifications occur. Use detect mode for broad monitoring with zero noise.

Alert mode (`kind: alert`)
:   The rule produces alert events with full lifecycle management. Alerts transition through episode states, trigger action policies, and support triage actions like acknowledge and snooze. Use alert mode when you need actionable alerts.

You can switch a rule between modes at any time. Switching from alert to detect stops lifecycle tracking and notifications but continues producing signal events.

## What happens when a rule runs

From your perspective, a rule does the following on each run:

- It evaluates your ES|QL query over the lookback window you configured.
- It appends new rows to the `.rule-events` data stream: signal rows in detect mode, or signal and alert rows with episode fields in alert mode.
- In alert mode, it updates episode lifecycle (for example pending, active, recovering) according to your activation, recovery, and no-data settings.
- When an episode is ready for notifications, action policies decide whether and how it is routed to workflows. Policies apply after lifecycle and thresholds; a short delay between “episode ready” and “notification sent” is normal when many policies or episodes are in play.

You can inspect raw history in Discover on `.rule-events` at any time, independent of whether notifications were sent.

## What you can do with {{alerting-v2}}

- Write rules using any ES|QL query pattern: thresholds, change detection, ratios, no-data, SLO burn rate, and more.
- Create rules from the UI, from Discover, or with YAML for infrastructure-as-code workflows.
- Preview rule results against existing data before saving.
- Use action policies to control routing, grouping, and throttling independently of rules.
- Investigate alerts in a dedicated inbox with filtering by status, severity, and custom fields.
- Explore alert history in Discover using ES|QL for trend analysis and operational reporting.
- Write rules on alerts: use the alert events index as a data source for correlation and escalation patterns.

## Learn more

* [Before you begin](kibana-alerting-v2/before-you-begin.md) for concepts, access, and setup before you author rules.
* [Author rules](kibana-alerting-v2/author-rules.md) to create and tune rules end to end.
* [Manage rules](kibana-alerting-v2/manage-rules.md) for day-to-day operations.

For a high-level comparison with Kibana alerting v1 and Watcher, read [Alerting overview](../alerting-overview.md). To pick a system by goal, read [Choose an alerting system](choose-an-alerting-system.md).
