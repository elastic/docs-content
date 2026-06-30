---
navigation_title: Use the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create Threshold Alert rules in Kibana's experimental alerting system using a guided form that generates ES|QL automatically."
---

# Use the rule builder in the {{alerting-v2-system}} [use-rule-builder]

The rule builder provides a guided form for creating rules without writing {{esql}} by hand. The builder generates the {{esql}} query automatically from structured inputs for the data source, aggregation, filters, and alert conditions.

## Threshold Alert [use-threshold-alert-builder]

Threshold Alert is the only rule type available in the rule builder. Use it to monitor one or more metrics and alert when they cross a threshold, with multi-condition support and custom aggregations.
