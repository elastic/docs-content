---
navigation_title: Create with AI Agent
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Use the Elastic AI Agent to generate ES|QL rules from plain-language descriptions in Kibana's experimental alerting system."
---

# Create a rule with AI Agent in the {{alerting-v2-system}} [create-rule-ai-agent]

The AI Agent option opens the Elastic AI agent pre-loaded with rule management knowledge. Describe what you want to monitor in plain language and the agent resolves the relevant data source and builds a rule proposal.

The proposal appears as an inline attachment card in the conversation showing the rule name, type, schedule, and tags. Select the card to open a flyout with three tabs:

- **Conditions** - The full rule configuration, including query, thresholds, grouping, and schedule.
- **Query preview** - Runs the {{esql}} query and shows results inline so you can verify the detection logic without leaving the conversation.
- **Runbook** - A free-text runbook associated with the rule.

The agent doesn't save the rule automatically. When the proposal looks correct, select **Save as rule** from the flyout header to persist it. After saving, you can ask the agent to configure notifications, which creates an action policy scoped to that rule.

:::{note}
Signal-mode rules don't support notifications. If you ask the agent to set up notifications on a signal rule, the agent will explain the limitation and offer to convert the rule to Alert mode or create a new Alert-mode rule.
:::

## Example prompts [ai-agent-sample-prompts]

Use these prompts as a starting point, then adjust them to your data and thresholds:

- Create an error threshold rule on my checkout service data. Alert when there are more than 3 HTTP 5xx errors in the past 5 minutes, grouped by URL path.
- Monitor average CPU usage across all hosts. Alert when any host exceeds 90% for more than 10 minutes.
- Alert me when log volume from the payments service drops below 100 events in a 5-minute window. This likely means data has stopped flowing.
- Set up a rule that tracks error rate by service. Alert at medium severity when the rate exceeds 1%, and critical when it exceeds 5%.
