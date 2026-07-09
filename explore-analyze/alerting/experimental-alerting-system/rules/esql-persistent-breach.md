---
navigation_title: Persistent breach detection
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Detect conditions that persist across consecutive time buckets in Kibana's experimental alerting system using ES|QL bucket counting."
---

# Persistent breach detection in the {{alerting-v2-system}} [persistent-breach]

A persistent breach condition detects a metric that stays above a threshold across several consecutive time buckets, for example CPU above 90% in all 10 of the last 10 five-minute windows. This filters out transient spikes and fires only when a problem has been sustained.

{{esql}} can express this with bucket counting:

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 50 minutes       // Lookback must cover all 10 buckets (10 × 5 min = 50 min)
| EVAL bucket = BUCKET(@timestamp, 5 minutes)  // Assign each event to its 5-minute time bucket
| STATS
    total_buckets     = COUNT_DISTINCT(bucket),          // How many distinct buckets exist in the window
    exceeding_buckets = COUNT_DISTINCT(
      CASE(system.cpu.total.pct > 0.90, bucket, null)    // Count only buckets where CPU exceeded threshold;
    )                                                    // null values are excluded by COUNT_DISTINCT
  BY host.name
| WHERE total_buckets >= 10                    // Require a full window of data before firing;
    AND exceeding_buckets == total_buckets     // every bucket must have breached
| KEEP host.name, total_buckets, exceeding_buckets
```

The rule's lookback window must cover all the buckets you want to check. In this example, 10 five-minute buckets requires at least 50 minutes of lookback.

## Handling gaps in data

If any bucket is missing because the host stopped reporting briefly mid-window, `total_buckets` drops below 10 and the condition doesn't fire. This is a deliberate safety check: a host that went silent for one bucket is treated as "we don't have enough data to confirm persistence" rather than "breach."

If you want to allow some gaps, replace `exceeding_buckets == total_buckets` with a ratio or a minimum count:

```esql
| WHERE total_buckets >= 8               // Tolerate up to 2 missing buckets
    AND exceeding_buckets >= total_buckets * 0.9  // 90% of present buckets must have breached
```

Design the query so that gaps in reporting produce the behavior you want before deploying it.
