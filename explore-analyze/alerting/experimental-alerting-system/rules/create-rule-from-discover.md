---
navigation_title: Create from Discover
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Convert an ES|QL query from a Discover session into a rule in Kibana's experimental alerting system, with the query pre-filled and a preview panel for verifying grouping."
---

# Create a rule from Discover in the {{alerting-v2-system}} [create-from-discover]

Convert an {{esql}} query you've already built in Discover directly into a rule, without rewriting it. Because you test the query against live data in Discover first, you know it returns the shape you expect before the rule is ever saved.

## Entry points [discover-rule-entry-points]

Two paths lead to Discover-based rule creation:

- **Discover Alerts menu**: When you're in Discover with an active {{esql}} query and the {{alerting-v2-system}} is enabled, the Alerts menu includes a **Create ES|QL rule** option. The rule creation flyout opens pre-populated with the current query. This path is only available in ES|QL mode.
- **Rules list**: Go to the **Rules** page, then start creating a rule. When choosing a creation path, select the one that opens a flyout embedding a live Discover session, so you can compose and test the query before saving the rule.

## How it works [discover-rule-flow]

When you trigger rule creation from Discover, your {{esql}} query pre-fills the **Create ES|QL rule** form. The rule creation form also shows a preview panel that reflects how your query partitions results into alert series. If your query uses a `BY` clause, the preview shows the series that would be evaluated on each run, letting you verify grouping logic against live data before committing to a schedule.

The rule creation flyout supports both a step-by-step form and a YAML editor. You can switch between them at any point. Edits are preserved when you return to the form view. The YAML editor includes {{esql}} autocomplete in the query field.

For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md).
