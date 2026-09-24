---
navigation_title: Create a rule
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Create rules using the ES|QL editor, AI Agent, rule builder, or directly from a Discover session."
---

# Create a rule [create-a-rule]

:::{include} /explore-analyze/alerting/v2/_snippets/v2-system-note.md
:::

{{kib}} provides several ways to create rules. Compare the options below and pick the one that best fits your workflow and how comfortable you are writing {{esql}}.

| Option | Best for |
| --- | --- |
| [Create an ES\|QL rule](create-esql-rule.md) | Full control over the query. Supports both a step-by-step form and a YAML editor. |
| [Create using {{agent-builder}}](create-rules-action-policies-agent-builder.md) | When you know what you want to detect but aren't sure how to write the ES\|QL. |
| [Use the rule builder](use-rule-builder.md) | Selecting a rule type (currently Threshold Alert) and configuring it through structured inputs, without writing {{esql}} by hand. |
| [Create from Discover](create-rule-from-discover.md) | When you already have an ES\|QL query working in Discover and want to convert it into a rule. |