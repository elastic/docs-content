---
navigation_title: Using Discover
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Turn an {{esql}} query in Discover into a {{alerting-v2}} rule with pre-filled evaluation and lookback."
---

# Create rules using Discover [create-rules-discover-v2]

$$$create-rules-discover-v2$$$

Create {{alerting-v2}} rules directly from Discover. When you build an {{esql}} query that surfaces interesting patterns, you can convert it into a rule without rewriting the query. For the full rule form including preview, alert mode settings, and YAML toggle, see [Create rules using the rule builder](create-rule-from-rule-builder.md).

:::{admonition} What gets pre-populated
When you create a rule from Discover:

- The full {{esql}} query from your current Discover session is placed into the rule's base query field.
- The index pattern is inferred from the `FROM` command in your query.
- The time range is converted into the rule's lookback window.

You can modify any of these values in the rule form before saving.
:::

## Create a rule from Discover

1. Open Discover and switch to {{esql}} mode.
2. Write and run an {{esql}} query that returns the data you want to monitor.
3. Open the **Rules** menu on the Discover toolbar and choose **Create v2 ES|QL rule**.
4. The rule creation form opens with the {{esql}} query pre-populated in the evaluation field.
5. Configure the remaining rule settings. For details on each setting, see [Configure a rule](configure-a-rule.md).
6. Click **Save**.
