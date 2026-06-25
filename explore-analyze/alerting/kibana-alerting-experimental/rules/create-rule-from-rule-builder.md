---
navigation_title: Using the rule builder
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create ES|QL rules, AI-assisted rules, and Threshold Alert rules in Kibana's experimental alerting system using the rule builder flyout."
---

# Create rules in the {{alerting-v2-system}} [create-rules-rule-builder]

The rule builder is part of the {{alerting-v2-system}} in {{kib}}. This page covers the three creation paths available from the rules list, how to configure an ES|QL rule, and how the Threshold Alert builder works. For descriptions of what each setting does, refer to [Configure a rule](configure-a-rule.md).

## Creation paths [rule-creation-paths]

All rules are created through a flyout that opens from the **Create rule** button in the rules list. Three options are available:

| Option | What it does | When to use |
| --- | --- | --- |
| **Create ES\|QL rule** | Write the detection query as {{esql}} directly. Includes a query sandbox for previewing results and a YAML editor. If you already have a query working in Discover, you can [start from there instead](create-rule-from-discover.md). | When you want full control over the query. |
| **Create with AI Agent** | Describe what you want to detect in plain language. The AI agent generates a rule definition and walks you through reviewing and saving it. | When you know the problem but aren't sure how to write the {{esql}}. |
| **Start from a rule builder** | Choose a structured rule type and fill in a guided form. The builder generates the {{esql}} query automatically. | When you want to create a standard rule type without writing {{esql}} by hand. |

## Create an {{esql}} rule [rule-builder-form-yaml]

The **Create ES|QL rule** path gives you two ways to define the query:

- **Rule form** - Fill in the step-by-step form with a live preview of results.
- **YAML mode** - Switch to YAML and edit the raw rule definition. You can switch between form and YAML at any point; edits are preserved.

The YAML editor isn't available within the Threshold Alert builder or other rule builder types. For a list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

### Preview query results in the sandbox [rule-builder-query-sandbox]

The query sandbox lets you run your {{esql}} query against current data and preview the results before applying them to the rule form. Use the time field selector and date picker to control the time range, then select **Search** (or press ⌘↵) to execute. When the results look correct, select **Apply changes** to populate the form.

Use the sandbox to:

- **Confirm grouping** - Check that your `BY` clause produces the series you intend, for example, one distinct series per host or per service, not a single undifferentiated result.
- **Catch unexpected output** - Verify that the query returns data in the right shape for the alert condition you plan to set. A query that returns zero rows or an unexpected field name won't behave as expected once the rule runs on a schedule.
- **Refine before committing** - Edit the query and re-run it as many times as needed without leaving the rule creation form.

## Create a rule with AI Agent [create-rule-ai-agent]

The **Create with AI Agent** option opens the Elastic AI agent pre-loaded with rule management knowledge. Describe what you want to monitor in plain language and the agent resolves the relevant data source and builds a rule proposal.

The proposal appears as an inline attachment card in the conversation showing the rule name, type, schedule, and tags. Select the card to open a flyout with three tabs:

- **Conditions** - The full rule configuration, including query, thresholds, grouping, and schedule.
- **Query preview** - Runs the {{esql}} query and shows results inline so you can verify the detection logic without leaving the conversation.
- **Runbook** - A free-text runbook associated with the rule.

The agent doesn't save the rule automatically. When the proposal looks correct, select **Save as rule** from the flyout header to persist it. After saving, you can ask the agent to configure notifications, which creates an action policy scoped to that rule.

:::{note}
Signal-mode rules don't support notifications. If you ask the agent to set up notifications on a signal rule, the agent will explain the limitation and offer to convert the rule to Alert mode or create a new Alert-mode rule.
:::

### Example prompts for creating rules [ai-agent-sample-prompts]

Use these prompts as a starting point, then adjust them to your data and thresholds:

- Create an error threshold rule on my checkout service data. Alert when there are more than 3 HTTP 5xx errors in the past 5 minutes, grouped by URL path.
- Monitor average CPU usage across all hosts. Alert when any host exceeds 90% for more than 10 minutes.
- Alert me when log volume from the payments service drops below 100 events in a 5-minute window. This likely means data has stopped flowing.
- Set up a rule that tracks error rate by service. Alert at medium severity when the rate exceeds 1%, and critical when it exceeds 5%.

## Use the rule builder [use-rule-builder]

The **Start from a rule builder** option provides a guided form for creating rules without writing {{esql}} by hand. The builder generates the {{esql}} query automatically from structured inputs for the data source, aggregation, filters, and alert conditions.

### Threshold Alert [use-threshold-alert-builder]

Threshold Alert is the only rule type available in the rule builder. Use it to monitor one or more metrics and alert when they cross a threshold, with multi-condition support and custom aggregations.

