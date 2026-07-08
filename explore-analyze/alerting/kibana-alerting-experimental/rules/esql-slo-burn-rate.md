---
navigation_title: SLO burn rate
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Detect SLO error budget burn across multiple time windows in Kibana's experimental alerting system using ES|QL conditional aggregation."
---

# SLO burn rate detection in the {{alerting-v2-system}} [experimental-alerting-system-slo-burn-rate-query]

An SLO burn rate query asks a different question than a basic threshold: are you consuming your error budget faster than you can afford to? Rather than checking a single metric at a fixed limit, it calculates error rates across multiple time windows simultaneously and assigns a severity level based on how fast the budget is being consumed.

## Single-tier query

This version checks one window pair and fires only at `critical` severity. It shows the core two-window pattern with the minimum number of moving parts.

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 1 hour    // Cover the longest window in the pair
| STATS
    errors_5m = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 5 minutes),
    total_5m  = COUNT_IF(@timestamp >= NOW() - 5 minutes),
    errors_1h = COUNT_IF(outcome == "failure"),
    total_1h  = COUNT(*)
  BY slo.id                             // Each SLO is evaluated independently
| EVAL
    burn_5m = errors_5m / total_5m,
    burn_1h = errors_1h / total_1h
| WHERE burn_5m > 14.4 AND burn_1h > 14.4  // Both windows must exceed the threshold to fire;
                                            // the short window detects the spike, the long window confirms it's sustained
| EVAL severity = "critical"
| KEEP slo.id, severity, burn_5m, burn_1h
```

The 14.4× multiplier reflects the rate at which a service would exhaust a 99.9% monthly error budget in one hour. Adjust it to match your SLO target.

## Multi-tier query

This version extends the single-tier pattern to detect both `critical` and `high` severity in one pass. Each severity level uses its own window pair with different time scales and thresholds.

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 3 days   // Cover the longest window pair used below.
                                       // Keep this in sync with the rule's lookback setting.
| STATS
    // CRITICAL window pair: 5 min fast signal, 1 hour sustained confirmation
    errors_5m   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 5  minutes),
    total_5m    = COUNT_IF(@timestamp >= NOW() - 5  minutes),
    errors_1h   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 1  hour),
    total_1h    = COUNT_IF(@timestamp >= NOW() - 1  hour),
    // HIGH window pair: 30 min fast signal, 6 hours sustained confirmation
    errors_30m  = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 30 minutes),
    total_30m   = COUNT_IF(@timestamp >= NOW() - 30 minutes),
    errors_6h   = COUNT_IF(outcome == "failure" AND @timestamp >= NOW() - 6  hours),
    total_6h    = COUNT_IF(@timestamp >= NOW() - 6  hours)
  BY slo.id
| EVAL
    burn_5m  = errors_5m  / total_5m,
    burn_1h  = errors_1h  / total_1h,
    burn_30m = errors_30m / total_30m,
    burn_6h  = errors_6h  / total_6h
| EVAL severity = CASE(
    burn_5m  > 14.4 AND burn_1h  > 14.4, "critical",
    burn_30m > 6.0  AND burn_6h  > 6.0,  "high",
    "none"
  )
| WHERE severity != "none"
| KEEP slo.id, severity, burn_5m, burn_1h, burn_30m, burn_6h
```

The rule's lookback window must cover the longest window in the query. In this example that's 3 days, driven by the 6-hour window pair.

The `severity` column in `KEEP` maps directly to the `severity` field on each resulting alert episode. For accepted values and matching rules, refer to [Severity](configure-rule-severity.md).
