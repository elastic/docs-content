---
navigation_title: Create a rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create rules in Kibana's experimental alerting system using the ES|QL editor, AI Agent, rule builder, or directly from a Discover session."
---

# Create a rule in the {{alerting-v2-system}} [create-a-rule]

The {{alerting-v2-system}} in {{kib}} provides several ways to create rules. For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md).

| Option | Best for |
| --- | --- |
| [Create an ES\|QL rule](create-esql-rule.md) | Full control over the query. Supports both a step-by-step form and a YAML editor. |
| [Create using {{agent-builder}}](create-rules-action-policies-agent-builder.md) | When you know what you want to detect but aren't sure how to write the ES\|QL. |
| [Use the rule builder](use-rule-builder.md) | Rules that follow a guided, form-based setup. |
| [Create from Discover](create-rule-from-discover.md) | When you already have an ES\|QL query working in Discover and want to convert it into a rule. |

:::{note}
For query examples ranging from a basic event filter to SLO burn rate and persistent breach detection, refer to [ES|QL query patterns](esql-query-patterns.md).
:::