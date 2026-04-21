---
navigation_title: Query alerts in Discover
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Use {{esql}} in Discover against `.rule-events` and `.alert-actions`: sample queries, trends, and MTTA-style analysis for {{alerting-v2}}."
---

# Query alerts and signals in Discover [explore-alerts-discover-v2]

$$$explore-alerts-discover-v2$$$

{{alerting-v2}} stores rule output in `.rule-events` and user or system actions in `.alert-actions`. Both are queryable with {{esql}} in Discover. Open Discover, select {{esql}}, paste a query, then adjust the time range and placeholders (`YOUR_RULE_ID`, `YOUR_GROUP_HASH`) to match your environment.

For field names, types, and episode fields, refer to [Alert states and fields reference](alert-states-and-fields-reference-v2.md#alert-states-reference-v2) and [Rule event and field reference](../rules/rule-event-field-reference-v2.md#rule-reference-v2). For triage in the product UI, refer to [View, manage, and reference alerts](view-manage-and-reference-alerts-v2.md).

## Rule events

Each write to `.rule-events` is one document. The `type` field is either `signal` (Detect mode, no `episode.*` fields) or `alert` (Alert mode, with episode lifecycle fields). Fields your {{esql}} rule selected are stored under `data` — confirm field names and types there until you know the full shape of your rule output.

### Example: Recent events

```esql
// ═══════════════════════════════════════════════════════════════
// LATEST ROWS - Sample across rules, raw timeline
// Why: Inspect recent runs without aggregating. Spot spikes or odd episode state
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 1 day
| KEEP @timestamp, rule.id, status, type, episode.status
| SORT @timestamp DESC
| LIMIT 100
```

### Example: Event counts by status

```esql
// ═══════════════════════════════════════════════════════════════
// STATUS MIX - How many events per status over the week
// Why: Health check. Check whether no_data dominates for data or query issues
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 7 days
| STATS event_count = COUNT(*) BY status
| SORT event_count DESC
```

### Example: Hourly event volume

```esql
// ═══════════════════════════════════════════════════════════════
// THROUGHPUT - Event counts per clock hour
// Why: Compare quiet versus busy windows. Correlate with schedules or incidents
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 24 hours
| STATS c = COUNT(*) BY hour = DATE_TRUNC(1 hour, @timestamp)
| SORT hour ASC
```

### Example: Events for a specific rule

Replace `YOUR_RULE_ID` with the ID from the rule's details or API.

```esql
// ═══════════════════════════════════════════════════════════════
// SINGLE RULE - All events for one rule id, replace YOUR_RULE_ID
// Why: Validate the data field payload. Isolate volume for one definition
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE rule.id == "YOUR_RULE_ID"
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, group_hash, status, type, data
| SORT @timestamp DESC
```

### Example: Timeline for one alert series

Replace `YOUR_GROUP_HASH` with the value from an event or the rule details.

```esql
// ═══════════════════════════════════════════════════════════════
// ONE SERIES - Timeline for a single group_hash, replace YOUR_GROUP_HASH
// Why: Replay how an episode progressed with the same series key as in the rule and alert UI
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE group_hash == "YOUR_GROUP_HASH"
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, status, episode.id, episode.status
| SORT @timestamp ASC
```

### Example: Lifecycle timeline for one episode

Replace `YOUR_EPISODE_ID` with the `episode.id` value from an alert event or the alert details UI. This query returns one row per rule evaluation, ordered chronologically, so you can trace exactly how the episode moved through its lifecycle from start to finish.

```esql
// ═══════════════════════════════════════════════════════════════
// ONE EPISODE - Full lifecycle timeline by episode.id, replace YOUR_EPISODE_ID
// Why: Replay how an episode progressed through pending → active → recovering → inactive
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE episode.id == "YOUR_EPISODE_ID"
| KEEP @timestamp, episode.status, episode.status_count, status
| SORT @timestamp ASC
```

### Example: Daily breach trend

```esql
// ═══════════════════════════════════════════════════════════════
// BREACH TREND - Daily breach counts, condition met rows only
// Why: Day-over-day trend, noisy rules, validate a change after deploy
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE status == "breached" AND @timestamp > NOW() - 7 days
| STATS breaches = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp)
| SORT day ASC
```

## Alert actions

Action records in `.alert-actions` capture what people did to episodes: acknowledge, snooze, resolve, and tag. Use them for operational metrics such as mean time to acknowledge (MTTA).

### Example: Acknowledgments for MTTA

To calculate MTTA, pair acknowledgment timestamps with episode start or first `fire` timestamps from a second query.

```esql
// ═══════════════════════════════════════════════════════════════
// ACKNOWLEDGMENTS - Rows users acknowledged, MTTA anchor
// Why: Pair with fire or episode start in a follow-up query for your organization's MTTA definition
// ═══════════════════════════════════════════════════════════════
FROM .alert-actions
| WHERE action.type == "acknowledge"
  AND @timestamp > NOW() - 30 days
| KEEP @timestamp, episode.id, rule.id, action.type
| SORT @timestamp DESC
```
