---
navigation_title: Create rules using the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create Threshold Alert rules in Kibana's experimental alerting system using a guided form that generates ES|QL automatically."
---

# Create a rule using the rule builder in the {{alerting-v2-system}} [use-rule-builder]

The rule builder provides a guided form for creating rules without writing {{esql}} by hand. The builder generates the {{esql}} query automatically from structured inputs for the data source, aggregation, filters, and alert conditions.

For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md). 

## Threshold Alert [use-threshold-alert-builder]

Threshold Alert is the rule type currently available in the rule builder. Use it to monitor one or more metrics and alert when they cross a threshold, with multi-condition support and custom aggregations.
