---
navigation_title: Using the rule builder
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Create a {{alerting-v2}} rule with the interactive rule builder: open the form, configure settings, preview, and save."
---

# Create rules using the rule builder [create-rules-rule-builder-v2]

$$$create-rules-ui-v2$$$

Create {{alerting-v2}} rules using the interactive rule creation form. The form provides a guided experience for all rule settings, with the option to toggle between interactive and YAML modes.

For how the {{esql}} query is structured and how the base query and alert condition fit together, see [Author rules](author-rules.md#esql-query-structure). For YAML-as-code and bulk definitions, see [Create rules with YAML](create-rule-with-yaml.md).

## Open the rule creation form

1. Navigate to **{{manage-app}}** > **Alerts and Insights** > **Rules V2**.
2. Click **Create rule**.

## Configure the rule

The form covers all settings described in [Configure a rule](configure-a-rule.md): mode, {{esql}} query, grouping, schedule, lookback, activation and recovery thresholds, no-data handling, tags, and investigation guide.

## Preview results

Before saving, click **Preview** to evaluate the query against recent data. The preview shows:

- How many rows the query returns.
- How many alert events would be generated.
- Sample alert event documents.
- A Lens-powered bar chart histogram of matching row counts over time, including recovery previews when recovery logic applies.

## Save the rule

Click **Save** to create the rule. The rule starts executing on its configured schedule.
