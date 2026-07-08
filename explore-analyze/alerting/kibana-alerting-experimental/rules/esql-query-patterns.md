---
navigation_title: ES|QL query patterns
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "ES|QL query patterns for rules in Kibana's experimental alerting system, from basic event filters to SLO burn rates, silent source detection, and persistent breach checks."
---

# {{esql}} query patterns for rules in the {{alerting-v2-system}} [experimental-alerting-system-esql-query-patterns]

The following pages cover {{esql}} query patterns for rules in the {{alerting-v2-system}}, ordered from the simplest starting point to advanced use cases. Start with [Your first rule query](esql-first-rule-query.md) if you're new, or jump to the pattern you need.

| Pattern | What it solves | Complexity |
| --- | --- | --- |
| [Your first rule query](esql-first-rule-query.md) | Alert on any individual event that matches a condition. No aggregation needed. | Beginner |
| [Threshold queries](esql-threshold-queries.md) | Alert when a metric crosses a limit. Covers single-series and grouped (per-host, per-service) rules. | Beginner |
| [No-data detection](esql-no-data-detection.md) | Alert when a specific host or data source stops reporting. | Intermediate |
| [SLO burn rate](esql-slo-burn-rate.md) | Alert when error budget consumption exceeds safe rates across multiple time windows. | Advanced |
| [Persistent breach detection](esql-persistent-breach.md) | Alert when a condition has been continuously true across consecutive time buckets. | Advanced |
