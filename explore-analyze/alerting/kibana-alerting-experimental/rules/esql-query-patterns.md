---
navigation_title: ES|QL query patterns
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Advanced ES|QL query patterns for rules in the experimental alerting system: SLO burn rate, no-data detection, persistent breach, and unsupported operations."
---

# {{esql}} query patterns for rules in the {{alerting-v2-system}} [esql-query-patterns]


ES|QL query patterns for rules are part of the {{alerting-v2-system}} in {{kib}}. Some detection problems can't be expressed as a single metric compared to a fixed threshold. You might need to know whether an SLO is burning through its error budget across multiple time windows at once. Or whether a specific host has gone silent, rather than whether the query returned nothing. Or whether a condition has persisted continuously across consecutive time buckets rather than appearing once. These are structurally different problems that require different query shapes.

This page covers query patterns for SLO burn rate detection across multiple windows, no-data detection for silent hosts or stopped sources, and persistent breach detection using bucket-level continuity checks. Use it when a basic `STATS ... WHERE` pattern isn't enough. If you're still learning how rules in the {{alerting-v2-system}} work, start with [Author rules](author-rules.md) first.

## Basic threshold query [threshold-query]

A threshold query evaluates one metric over one lookback window and fires if a value crosses a limit. It is the simplest rule shape: a `STATS` aggregation followed by a `WHERE` condition.

```esql
FROM logs-*
| STATS
    // Count only error responses; count all requests for the denominator
    error_count = COUNT_IF(http.response.status_code >= 500),
    total_count = COUNT(*)
  BY service.name
| EVAL error_rate = error_count / total_count  // Compute the error rate as a fraction (0–1)
| WHERE error_rate > 0.10                      // Alert condition: services above 10% error rate are breaches
| KEEP service.name, error_rate, error_count, total_count
```

One window, one aggregate, one threshold check. The result is either a breach or no breach for each series.

## SLO burn rate query [slo-burn-rate-query]

An SLO burn rate query asks a different question than a basic threshold: are you consuming your error budget faster than you can afford to? Rather than checking a single metric at a fixed limit, it calculates error rates across multiple time windows simultaneously and returns a severity level.

### Why multiple windows

Checking both a short window (for example, 5 minutes) and a long window (for example, 1 hour) together filters out brief spikes that don't represent a real budget threat. A `critical`-severity alert episode fires only when *both* the short and long burn rates exceed the threshold. The two-window requirement is what separates a genuine budget emergency from a momentary blip.

### Query structure

A single {{esql}} query handles all window pairs at once using conditional aggregation:

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 3 days   // Lookback must cover the longest window pair used below.
                                       // Keep this value in sync with the rule's lookback setting.
| STATS
    // CRITICAL window pair: 5 min catches the fast signal, 1 hour confirms it's sustained
    errors_5m   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 5  minutes),
    total_5m    = COUNT_IF(@timestamp >= NOW() - 5  minutes),
    errors_1h   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 1  hour),
    total_1h    = COUNT_IF(@timestamp >= NOW() - 1  hour),
    // HIGH window pair: 30 min fast signal, 6 hours sustained confirmation
    errors_30m  = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 30 minutes),
    total_30m   = COUNT_IF(@timestamp >= NOW() - 30 minutes),
    errors_6h   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 6  hours),
    total_6h    = COUNT_IF(@timestamp >= NOW() - 6  hours)
  BY slo.id                            // Each SLO is evaluated independently
| EVAL
    // Compute error rates (errors as a fraction of total requests) for each window
    burn_5m  = errors_5m  / total_5m,
    burn_1h  = errors_1h  / total_1h,
    burn_30m = errors_30m / total_30m,
    burn_6h  = errors_6h  / total_6h
| EVAL severity = CASE(
    // critical: both the fast and sustained windows exceed 14.4x the baseline error rate.
    // Requiring both prevents a single brief spike from triggering a critical alert.
    burn_5m  > 14.4 AND burn_1h  > 14.4, "critical",
    // high: same two-window logic at a lower threshold
    burn_30m > 6.0  AND burn_6h  > 6.0,  "high",
    "none"
  )
| WHERE severity != "none"             // Only breaching SLOs become alert rows
| KEEP slo.id, severity, burn_5m, burn_1h, burn_30m, burn_6h  // Store fields needed for routing and triage
```

The burn rate multipliers (14.4×, 6×) reflect standard SLO error budget consumption rates. Adjust them to match your SLO targets.

Because the query computes several window pairs in one pass, the lookback window on the rule must cover the longest window in the query (3 days in the example above).

The `severity` column in `KEEP` maps directly to `episode.severity` on each resulting alert episode. For the accepted values and matching rules, refer to [Severity levels](author-rules.md#severity-levels).

## No-data detection [no-data-esql-query]

No-data detection inverts the normal pattern. Instead of filtering for data that meets a condition, you query for when data was *last seen* and flag sources that have gone silent.

The technique uses a broad lookback to find all known hosts, then surfaces only those that have not reported recently:

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 12 hours         // Broad lookback: must be wide enough that all known hosts
                                               // have at least one event in the window under normal conditions
| STATS last_seen = MAX(@timestamp) BY host.name  // Find the most recent event timestamp per host
| WHERE last_seen < NOW() - 15 minutes         // Keep only hosts that have NOT reported in the last 15 minutes
| KEEP host.name, last_seen                    // Each returned row is a silent host — the query result itself is the alert
```

Every row returned is a host that has gone silent, so the base query itself drives the alert. No separate alert condition is needed.

### Variants

| Variant | What it detects |
|---|---|
| Host-specific | Each host that stops reporting generates its own alert series (use `BY host.name` for grouping). |
| Global | No data from any source. Omit the `BY` clause and check whether the query returns any rows at all. |
| Combined | Flags both a high-metric condition *and* silent hosts in one query using a `CASE` expression to assign a `status` field (`"alert"`, `"no data"`, or `"ok"`), then filters to only the problematic rows. |

### Lookback window sizing

The lookback must be wide enough that known hosts appear in the result set. If the lookback is too short, a silent host falls outside the window and is never checked. However, large lookback windows on high-frequency data streams increase query cost significantly. Start with a lookback that comfortably covers the longest expected reporting gap for your hosts, not the full history of the index.

For no-data behavior when the entire base query returns zero rows (as opposed to detecting specific silent sources), refer to [No-data handling](configure-a-rule.md#no-data-handling).

<!--[CONTENT NEEDED for M2: M2 introduces Track By and a `series.*` block that gives the system a stable, explicit identity for each monitored series. Once series identity is formalized, the system may support native detection of when a known series stops producing events, which is the same problem this query solves manually today. Verify whether M2 adds a built-in no-data detection option at the series level, and if so, document it here as the preferred approach and move this manual `MAX(@timestamp)` pattern to a "how it works" explanation or a workaround note for cases the native approach does not cover.]
-->

## Limitations and workarounds [esql-limitations]

Some patterns from the classic alerting aggregation API are not directly available in {{esql}}, and some require workarounds.

### Persistent breach detection [persistent-breach]

A persistent breach condition detects a metric that stays above a threshold across several consecutive time buckets (for example, "CPU above 90% in all 10 of the last 10 five-minute windows"). {{esql}} can express this with bucket counting:

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 50 minutes       // Lookback must cover all 10 buckets (10 × 5 min = 50 min)
| EVAL bucket = BUCKET(@timestamp, 5 minutes)  // Assign each event to its 5-minute time bucket
| STATS
    total_buckets     = COUNT_DISTINCT(bucket),          // How many distinct buckets exist in the window
    exceeding_buckets = COUNT_DISTINCT(
      CASE(system.cpu.total.pct > 0.90, bucket, null)    // Count only buckets where CPU exceeded the threshold;
    )                                                    // null values are excluded by COUNT_DISTINCT
  BY host.name
| WHERE total_buckets >= 10                    // Require a full window of data before firing —
    AND exceeding_buckets == total_buckets     // guards against gaps making a partial breach look persistent;
                                               // every bucket in the window must have breached
| KEEP host.name, total_buckets, exceeding_buckets
```

The rule's lookback window must cover all the buckets you want to check (50 minutes for 10 five-minute buckets in this example). If any bucket is missing from the data because the host stopped reporting briefly mid-window, `total_buckets` drops below 10 and the condition doesn't fire. Design the query so that gaps in reporting produce the behavior you want: either treating partial coverage as a non-breach or adjusting the `WHERE` filter to allow it.

<!--[CONTENT NEEDED for M2: M2's Track By feature gives the system a native concept of series identity and may provide a way to track how many consecutive evaluations a series has been breaching. If this lands, persistent breach detection could become a rule configuration option rather than something expressed entirely in the {{esql}} query. Verify whether M2 adds consecutive-breach tracking at the series level, and if so, document the configuration approach here alongside or instead of this workaround.]
-->

### Derivative aggregation [derivative-aggregation]

{{esql}} does not have a `DERIVATIVE` function. In the {{es}} aggregations API, a derivative pipeline aggregation calculates the rate of change between consecutive time buckets (for example, "how fast is this counter increasing per minute?"). There is no equivalent in {{esql}}.

Use cases that require true per-bucket deltas (such as detecting a sudden acceleration in error rate) cannot be expressed as an {{esql}} rule at this time. Consider pre-computing deltas in an ingest pipeline or using a transform to write derived metrics to a separate index that your rule can then query with a standard threshold pattern.
