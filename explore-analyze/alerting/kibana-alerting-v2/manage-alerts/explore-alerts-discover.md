---
navigation_title: Explore alerts and signals in Discover
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Query Kibana alerting v2 alert events in Discover using ES|QL for trend analysis, operational reporting, and ad hoc investigation."
---

# Explore Kibana alerting v2 alerts and signals in Discover [explore-alerts-discover-v2]

Because Kibana alerting v2 alert events are stored as queryable data in standard {{es}} indices, you can explore them in Discover using ES|QL.

## Query alert events

Run ES|QL in Discover against the **`.rule-events`** data stream to analyze signal and alert documents written by rule executions.

### Example: Recent alert and signal events

**What it does:** Returns the most recent rows from `.rule-events`, with timestamps, rule id, breach/recovery/no-data **status**, whether the row is a **signal** or **alert**, and current **episode** state.

**Why use it:** Start here for ad hoc investigation—see what your rules produced today without aggregating, so you can spot spikes, wrong rules, or unexpected episode states in raw order.

```esql
FROM .rule-events
| WHERE @timestamp > NOW() - 1 day
| KEEP @timestamp, rule.id, status, type, episode.status
| SORT @timestamp DESC
| LIMIT 100
```

### Example: Event counts by status

**What it does:** Counts how many events fall into each **status** value (`breached`, `recovered`, `no_data`, and so on) over the last seven days.

**Why use it:** Understand the mix of breach vs recovery vs no-data at a glance—useful for health checks, reporting, and seeing whether no-data dominates (query or data-source issues).

```esql
FROM .rule-events
| WHERE @timestamp > NOW() - 7 days
| STATS event_count = COUNT(*) BY status
| SORT event_count DESC
```

### Example: Hourly event volume

**What it does:** Buckets events by hour with `DATE_TRUNC` and counts events per hour for the last 24 hours.

**Why use it:** Spot time-of-day patterns, rule schedule effects, or incident windows—compare quiet hours vs bursts without picking a single rule yet.

```esql
FROM .rule-events
| WHERE @timestamp > NOW() - 24 hours
| STATS c = COUNT(*) BY hour = DATE_TRUNC(1 hour, @timestamp)
| SORT hour ASC
```

### Example: Events for a specific rule

**What it does:** Filters to one **rule id**, keeps time, **group_hash**, status, type, and the **data** payload from your ES|QL rule output.

**Why use it:** Drill into a single rule you care about—validate field shapes in `data`, follow one rule’s volume, or share a reproducible slice with another engineer (replace `YOUR_RULE_ID` with the real id).

```esql
FROM .rule-events
| WHERE rule.id == "YOUR_RULE_ID"
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, group_hash, status, type, data
| SORT @timestamp DESC
```

### Example: Group hash series for an episode

**What it does:** Selects all events for one **group_hash** (one alert series) and keeps time, status, and **episode** identifiers and state, sorted oldest to newest.

**Why use it:** Reconstruct the timeline for a single series—how an episode opened, changed state, and recovered—using the same key the executor uses for grouping.

```esql
FROM .rule-events
| WHERE group_hash == "YOUR_GROUP_HASH"
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, status, episode.id, episode.status
| SORT @timestamp ASC
```

### Example: Breached rows trend

**What it does:** Counts only rows where **status** is `breached`, aggregated by calendar day for the last week.

**Why use it:** Track whether breach volume is trending up or down day over day—useful for capacity, noisy rules, or validating a change after a deployment.

```esql
FROM .rule-events
| WHERE status == "breached" AND @timestamp > NOW() - 7 days
| STATS breaches = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp)
| SORT day ASC
```

## Query alert actions (for example, MTTA)

Operational metrics such as **mean time to acknowledge (MTTA)** use action documents in **`.alert-actions`**.

### Example: Acknowledgment events for MTTA-style analysis

**What it does:** Reads **`.alert-actions`** and returns rows where **action.type** is `acknowledge`, with time, episode, and rule identifiers.

**Why use it:** Acknowledgments are the usual anchor for MTTA-style metrics; from here you can join or compare against `fire` actions or episode start times in your own aggregations to match your org’s definition of “time to acknowledge.”

```esql
FROM .alert-actions
| WHERE action.type == "acknowledge"
  AND @timestamp > NOW() - 30 days
| KEEP @timestamp, episode.id, rule.id, action.type
| SORT @timestamp DESC
```

Adjust filters and aggregations to match how your organization defines MTTA (for example, time from first `fire` to first `acknowledge` for an episode).
