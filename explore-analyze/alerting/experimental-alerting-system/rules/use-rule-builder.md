---
navigation_title: Create rules using the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create rules in Kibana's experimental alerting system by selecting a rule type and configuring it through a guided form that generates ES|QL automatically."
---

# Create a rule using the rule builder in the {{alerting-v2-system}} [use-rule-builder]

Go to the **Rules** page, then start creating a rule. When choosing a creation path, select the one that lets you build the rule by selecting a rule type and configuring it through structured inputs, instead of writing {{esql}} directly. Behind the scenes, the rule builder generates the {{esql}} query for you from the data source, aggregation, filters, and alert conditions you set.

:::{note}
The rule builder differs from the **Rule form** described in [Create an {{esql}} rule](create-esql-rule.md). The Rule form is for writing an {{esql}} query directly, with a live preview of results. The rule builder instead has you select a rule type, then fills in the query for you based on the structured inputs you provide for that type.
:::

For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md).

## Threshold Alert [use-threshold-alert-builder]

Threshold Alert is the only rule type available in the rule builder. Use it to monitor metrics against one or more threshold conditions. Custom aggregations let you control how metric values are computed before they are compared to the threshold.