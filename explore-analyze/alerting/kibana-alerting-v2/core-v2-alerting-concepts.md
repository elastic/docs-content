---
navigation_title: Core concepts
applies_to:
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "A short tour of {{alerting-v2}} vocabulary and mental model: rules, schedules vs policies, data flow, where execution runs, and availability."
---

# {{alerting-v2}} overview [kibana-alerting-v2-overview]

This page introduces the core vocabulary and how {{alerting-v2}} fits together. 

## How {{alerting-v2}} works

A {{alerting-v2}} rule defines what to look for in your data. It evaluates source data such as logs, metrics, traces, or alert events from other rules on a configurable schedule using an ES|QL query and produces alert event documents when conditions are met.

Each rule is set to **Detect** or **Alert** mode. Detect mode saves what the rule found each run. You can use it to try out a query without opening issues or sending notifications. Alert mode does that too, but also keeps an ongoing problem you can work in **Alerts**, which is what action policies hook into.

Besides mode, a typical rule includes the following:

| Part | What it does |
|------|----------------|
| **Query** | An ES\|QL query that defines what to look at and what counts as a match. |
| **Schedule** | How often the rule runs and how far back each run looks. |
| **Grouping** (optional) | Fields that split results so each value (for example, each host) is tracked on its own. |
| **Action policies and workflows** | In Alert mode, policies decide when an episode should notify someone; workflows are the concrete steps, such as sending email. |

These parts work together when a rule runs. Each run looks roughly like this:

1. The rule runs its query over the lookback window.
2. The system writes signals, one saved result per match. In Alert mode it also updates alert and episode information for each series (each grouped track you care about).
3. In Alert mode, the dispatcher decides whether an action policy that is **enabled** and not **snoozed** applies, whether throttling allows a send, and whether to run a workflow. Policies and workflows are resolved in the **same {{kib}} space** as the rule.
4. You work from the Alerts UI, Discover, or dashboards. You can add more rules later that build on the same data.

In Detect mode, step 3 does not apply because there are no episodes for policies to target.

## Core concepts

Core concepts about {{alerting-v2}}.

### ES|QL rules replace fixed rule types

{{alerting-v2}} does not ask you to pick a plugin **rule type** with a fixed form. You write an [ES|QL](elasticsearch://reference/query-languages/esql.md) query: a **base query** (required) that selects and aggregates your data, an optional **alert condition** (typically a `WHERE` on those results), and **`KEEP`** so you control which fields are stored on each event.

Every rule is in **Detect** or **Alert** mode:

- **Detect** (`kind: signal`) records **signals**—append-only rows when the query matched—so you can validate behavior in Discover without lifecycle or notifications.
- **Alert** (`kind: alert`) still writes signals, and also maintains **alerts** with lifecycle so episodes can open, change state, and drive action policies.

### Evaluation separated from notification [detection-and-notification-v2]

Think in two layers: **evaluation** (what the rule does on its clock) and **dispatch** (what happens when an episode is ready for outreach).

#### Schedules and thresholds

The **schedule** and **lookback** control how often the rule runs and which slice of time each run evaluates. **Activation** and **recovery** thresholds control how long a breach must persist—or how many consecutive evaluations must agree—before an episode becomes active or returns to inactive. **No-data** handling defines how empty query results affect state.

#### Action policies

**Action policies** are separate saved objects in the space. They do not live on the rule document. A policy’s **matcher** (optional KQL), **grouping**, **throttling**, and **{{maint-windows-cap}}** decide whether a matching episode **dispatches** and which **workflow** runs. The rule describes the signal; the policy describes who gets notified and how often.

### Immutable events and episodes

Each evaluation **appends** documents—you do not mutate yesterday’s row when a condition clears. **Signals** are the raw saved outcomes. When you **group** by fields (for example `host.name`), each distinct combination is a **series** (identified by `group_hash`). An **episode** is one full incident on that series, from first breach through recovery, tied together across many runs by `episode_id`.

That history lives in **`.rule-events`** (and related streams) so Discover, dashboards, and follow-on rules can query the same facts operators see in the inbox.