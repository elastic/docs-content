---
navigation_title: Using the rule builder
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Create a {{alerting-v2}} rule with the interactive rule builder: open the form, configure settings, preview, and save."
---

# Create rules using the rule builder [create-rules-rule-builder-v2]

$$$create-rules-rule-builder-v2$$$
$$$create-rules-ui-v2$$$

Create {{alerting-v2}} rules using the interactive rule creation form. The form provides a guided experience for all rule settings, with the option to toggle between interactive and YAML modes.

1. Navigate to **{{manage-app}} > V2 Alerting Preview > Rules**.
2. Click **Create rule**.
3. Set up the rule. Refer to [](configure-a-rule-v2.md) to learn about the available settings.
4. Click **Preview** to evaluate the query against recent data before saving. The preview shows how many rows the query returns, how many alert events would be generated, sample alert event documents, and a bar chart of matching row counts over time.
5. Click **Save**. The rule starts executing on its configured schedule.
