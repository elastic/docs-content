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

Go to the **Rules** page, then start creating a rule. When choosing a creation path, select the one that lets you build the rule using a guided form instead of writing {{esql}} by hand. The rule builder generates the {{esql}} query automatically from structured inputs for the data source, aggregation, filters, and alert conditions.

For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md).

## Threshold Alert [use-threshold-alert-builder]

Threshold Alert is the only rule type available in the rule builder. Use it to monitor metrics against one or more threshold conditions. Custom aggregations let you control how metric values are computed before they are compared to the threshold.