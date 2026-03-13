---
navigation_title: No-data handling
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Prevent false recoveries and false alerts when data sources stop reporting by configuring Kibana alerting v2 no-data behavior."
---

# Kibana alerting v2 no-data handling [reduce-noise-no-data-v2]

Proper no-data handling prevents false recoveries and false alerts when data sources stop reporting. By default, if a rule returns no results, the system cannot determine whether the condition is resolved or whether data has simply stopped arriving.

## The problem

Consider a rule that monitors CPU usage per host. If `host-a` stops sending metrics:

- Without no-data handling, the rule sees no breaching rows for `host-a` and treats it as recovery — a false recovery.
- With no-data handling configured to `no_data`, the system detects the absence and records a no-data event instead.

## Behaviors

| Behavior | Effect | Use when |
|---|---|---|
| `no_data` | Records a no-data event. The alert does not recover or activate. | Missing data is a condition you want to track |
| `last_status` | Carries forward the previous status. No new event is written. | Data gaps are expected (batch ingestion) |
| `recover` | Treats absence as recovery. Alert transitions to recovering. | You are confident that no data means the issue is resolved |

## How to configure

Refer to [No-data handling (rule settings)](/explore-analyze/alerting/kibana-alerting-v2/author-rules/rule-settings/no-data-handling.md) for configuration details and examples.

## Noise reduction impact

Choosing the right no-data behavior reduces two types of noise:

1. **False recoveries** — prevented by using `no_data` or `last_status` instead of `recover`.
2. **False no-data alerts** — prevented by using `last_status` when gaps are expected.

For the strongest noise reduction, use `no_data` behavior with a combined metric and no-data rule that handles both conditions in a single ES|QL query.
