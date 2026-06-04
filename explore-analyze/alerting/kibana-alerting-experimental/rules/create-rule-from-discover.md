---
navigation_title: Using Discover
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Turn an {{esql}} query in Discover into a rule in the {{alerting-v2}} with pre-filled evaluation and lookback."
---

# Create rules from Discover in {{alerting-v2}} [create-rules-discover]


Creating rules from Discover is part of the {{alerting-v2}} in {{kib}}. When you build an {{esql}} query that surfaces interesting patterns, you can convert it into a rule without rewriting the query. For the full rule form including schedule and lifecycle settings, refer to [Configure a rule](configure-a-rule.md).

## Entry points [discover-rule-entry-points]

Two paths lead to Discover-based rule creation:

- **Discover Alerts menu**: When you're in Discover with an active {{esql}} query and the {{alerting-v2}} is enabled, the Alerts menu includes a **Create ES|QL rule** option. The rule creation flyout opens pre-populated with the current query. This path is only available in ES|QL mode.
- **Rules list**: From the rules list, selecting the option to create a rule from Discover opens the Discover-based rule creation experience directly. The flyout embeds a live Discover session so you can compose and test the query before saving the rule. After saving, you return to the rules list.

## How it works [discover-rule-flow]

Starting a rule from Discover means your query is already tested and returns the shape you expect before the rule is ever saved. Instead of drafting a query in the rule builder and hoping it works, you iterate in Discover (where you can see real results immediately) and then create the rule when the query is ready.

When you trigger rule creation from Discover, your {{esql}} query pre-fills the **Create ES|QL rule** form. The rule creation form also shows a preview panel that reflects how your query partitions results into alert series. If your query uses a `BY` clause, the preview shows the series that would be evaluated on each run. This lets you verify grouping logic against live data before committing to a schedule.

## Form and YAML editing [discover-form-yaml]

The rule creation flyout supports both a step-by-step form and a YAML editing mode. You can switch between them at any point — edits in YAML mode are preserved when you return to the form view. To discard YAML edits and return to the prior form state, use the **Cancel YAML** option. The YAML editor includes {{esql}} autocomplete in the query field.

Use YAML mode when you want to fine-tune the raw rule definition, copy a pattern from an existing rule, or work faster than filling in individual form fields allows.

## Preview query results before creating the rule [preview-query-discover]


The query preview in the rule creation flow runs your {{esql}} query against current data and displays the resulting rows. Use this to:

- **Confirm grouping**: Check that your `BY` clause produces the series you intend — for example, one distinct series per host or per service, not a single undifferentiated result.
- **Catch unexpected output**: Verify that the query returns data in the right shape for the alert condition you plan to set. A query that returns zero rows or an unexpected field name won't behave as expected once the rule runs on a schedule.
- **Refine before committing**: Edit the query in the preview panel and re-run it without leaving the rule creation form. Once the preview looks correct, proceed to fill in the remaining settings.

<!--[CONTENT NEEDED: UI. Add a step-by-step procedure once the Discover-to-rule workflow is confirmed in the shipped UI.

Section heading: "Create a rule from Discover" (anchor: create-rule-discover-procedure-v2). The procedure should cover: (1) the exact entry point and menu item name for triggering rule creation from an ES|QL query in Discover; (2) what pre-fills in the rule form (query, lookback, schedule defaults); (3) how to use the query preview panel — running the preview, reading grouping output, and editing the query inline; (4) how to complete the remaining settings and save.

Verify all button labels, panel names, and navigation paths against the shipped UI before publishing. Draft content is in source control for reference.]
-->