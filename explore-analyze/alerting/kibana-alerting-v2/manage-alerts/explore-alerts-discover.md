---
navigation_title: Explore alerts and signals in Discover
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Query Kibana alerting v2 alert events in Discover with ES|QL for trend analysis, operational reporting, and on-demand investigation."
---

# Explore {{kib}} alerting v2 alerts and signals in Discover [explore-alerts-discover-v2]

**What this page is for:** {{kib}} alerting v2 stores rule output in **`.rule-events`** and user or system actions in **`.alert-actions`**. Both are ordinary {{es}} data you query with **{{esql}}** in **Discover**. **When you land here**, use the examples to **investigate** what rules produced (recent rows, status mix, hourly volume), **drill into** one rule or one alert series, **track** breach trends over days, and **support operational metrics** such as mean time to acknowledge (MTTA) from acknowledgment rows.

**How to use it:** Open Discover, choose **{{esql}}**, paste a query, then adjust time ranges and placeholders (`YOUR_RULE_ID`, `YOUR_GROUP_HASH`) to match your environment. Save views, export results, or reuse clauses in dashboards and reports.

The examples below follow that workflow: they start with **broad** views of **`.rule-events`**, move to **narrow** filters (single rule, single `group_hash`), add a **daily breach trend**, then switch to **`.alert-actions`** for acknowledgment history.

## Query alert events

These queries target **`.rule-events`**: signal and alert documents from rule evaluations. Use them before the **alert actions** section when you care about rule output and episode fields, not action audit rows.

### Example: Recent alert and signal events

This example shows a **non-aggregated** sample of the newest documents in **`.rule-events`**: one row per evaluation output, with core fields so you can scan what happened in roughly the **last day**. The results are capped at **100** rows so the query stays responsive in Discover.

```esql
// ═══════════════════════════════════════════════════════════════
// LATEST ROWS — Sample across rules (raw timeline)
// Why: See what ran recently without aggregating; spot spikes or odd episode state
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 1 day                            // Rolling last 24 hours
| KEEP @timestamp, rule.id, status, type, episode.status       // When, rule id, status, signal or alert type, episode state
| SORT @timestamp DESC
| LIMIT 100                                                     // Cap rows for a quick scan
```

### Example: Event counts by status

This example **aggregates** all events from the **last seven days** and counts how many documents fall into each **`status`** value (for example `breached`, `recovered`, or `no_data`). Use it to see whether the stream is mostly healthy transitions or dominated by a single status.

```esql
// ═══════════════════════════════════════════════════════════════
// STATUS MIX — How many events per status over the week
// Why: Health check; see if no_data dominates (data or query issues)
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 7 days
| STATS event_count = COUNT(*) BY status                        // One bucket per status value
| SORT event_count DESC
```

### Example: Hourly event volume

This example buckets events by **clock hour** over the **last 24 hours** using `DATE_TRUNC` and counts events per hour. It highlights **when** volume rises or falls, which helps correlate activity with rule schedules, deployments, or incidents.

```esql
// ═══════════════════════════════════════════════════════════════
// THROUGHPUT — Event counts per clock hour
// Why: Compare quiet versus busy windows; correlate with schedules or incidents
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE @timestamp > NOW() - 24 hours
| STATS c = COUNT(*) BY hour = DATE_TRUNC(1 hour, @timestamp)  // Bucket by hour
| SORT hour ASC
```

### Example: Events for a specific rule

This example filters **`.rule-events`** to a **single rule** by **`rule.id`**. Replace **`YOUR_RULE_ID`** with the id from the rule’s details or API. It keeps **`data`**, which holds the fields your {{esql}} rule selected—useful for validating field names and shapes. The window is **seven days**.

```esql
// ═══════════════════════════════════════════════════════════════
// SINGLE RULE — All events for one rule id (replace YOUR_RULE_ID)
// Why: Validate the data field payload; isolate volume for one definition
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE rule.id == "YOUR_RULE_ID"                              // Narrow to one rule
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, group_hash, status, type, data              // Series key and query output fields
| SORT @timestamp DESC
```

### Example: Group hash series for an episode

This example follows **one alert series** (`group_hash`) over **seven days**, sorted **oldest to newest**, so you can read the timeline for that series. Replace **`YOUR_GROUP_HASH`** with the value from an event or the rule details. **Episode** fields show how state changed across evaluations.

```esql
// ═══════════════════════════════════════════════════════════════
// ONE SERIES — Timeline for a single group_hash (replace YOUR_GROUP_HASH)
// Why: Replay how an episode progressed (same series key as in the rule and alert UI)
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE group_hash == "YOUR_GROUP_HASH"
  AND @timestamp > NOW() - 7 days
| KEEP @timestamp, status, episode.id, episode.status          // Chronological episode story
| SORT @timestamp ASC
```

### Example: Breached rows trend

This example counts only rows where **`status`** is **`breached`** (the condition was met for that evaluation), then totals **breaches per calendar day** for the **last week**. It is suited to **trend** questions (getting louder or quieter over days), not to total signal volume.

```esql
// ═══════════════════════════════════════════════════════════════
// BREACH TREND — Daily breach counts (condition met rows only)
// Why: Day-over-day trend; noisy rules; validate a change after deploy
// ═══════════════════════════════════════════════════════════════
FROM .rule-events
| WHERE status == "breached" AND @timestamp > NOW() - 7 days
| STATS breaches = COUNT(*) BY day = DATE_TRUNC(1 day, @timestamp)
| SORT day ASC
```

## Query alert actions (for example, MTTA)

Earlier on this page, the **`.rule-events`** examples covered **what the rule wrote**; this section covers **what people did** to alerts. Operational metrics such as **mean time to acknowledge (MTTA)** build on action documents in **`.alert-actions`** (for example acknowledgments), often combined with episode or `fire` timestamps in a separate step.

### Example: Acknowledgment events for MTTA-style analysis

This example reads **`.alert-actions`** (not **`.rule-events`**) and returns rows where **`action.type`** is **`acknowledge`**, limited to **30 days** of history. It is a typical **starting point** for MTTA: you still need timestamps for “start” (for example first `fire` or episode start) and your own definition of acknowledge time, which may require a second query or aggregation.

```esql
// ═══════════════════════════════════════════════════════════════
// ACKNOWLEDGMENTS — Rows users acknowledged (MTTA anchor)
// Why: Pair with fire or episode start in a follow-up query for your organization's MTTA definition
// ═══════════════════════════════════════════════════════════════
FROM .alert-actions
| WHERE action.type == "acknowledge"
  AND @timestamp > NOW() - 30 days
| KEEP @timestamp, episode.id, rule.id, action.type
| SORT @timestamp DESC
```

Adjust filters and aggregations to match how your organization defines MTTA (for example, time from first `fire` to first `acknowledge` for an episode).
