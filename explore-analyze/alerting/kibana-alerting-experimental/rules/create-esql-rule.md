---
navigation_title: Create an ES|QL rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write ES|QL detection queries for rules in Kibana's experimental alerting system using the rule form or YAML editor, with a live query sandbox for previewing results."
---

# Create an {{esql}} rule in the {{alerting-v2-system}} [experimental-alerting-system-create-esql-rule]

The {{esql}} rule path lets you write the detection query directly. There are two ways to define the rule: 

- **Rule form** - Fill in the step-by-step form with a live preview of results.
- **YAML mode** - Edit the raw rule definition. You can switch between form and YAML at any time, unless the YAML can't be translated to a valid form state, in which case you must stay in YAML.

For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md). For a list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

## Preview query results in the sandbox [rule-builder-query-sandbox]

The query sandbox lets you run your {{esql}} query against current data and preview the results before applying them to the rule form. Use the time field selector and date picker to control the time range, then select **Search** (or press ⌘↵) to execute. When the results look correct, select **Apply changes** to populate the form.

:::{note}
In the query sandbox, the time field selector and date picker control the query results only. They do not set the rule's schedule or lookback period.
:::

Use the sandbox to:

- **Confirm grouping** - Check that your `BY` clause produces the series you intend, for example, one distinct series per host or per service, not a single undifferentiated result.
- **Catch unexpected output** - Verify that the query returns data in the right shape for the alert condition you plan to set. A query that returns zero rows or an unexpected field name won't behave as expected once the rule runs on a schedule.
- **Refine before committing** - Edit the query and re-run it as many times as needed without leaving the rule creation form.

While the sandbox is open, switching between rule form and YAML or between rule modes (Alert and Signal) is not available. Close the sandbox first if you need to change authoring mode.

### Control how your query splits [sandbox-split-editor]

By default, applying changes automatically splits your query into a [base query and alert condition](configure-rule-query.md). If you want full manual control over the split, use the toggle in the sandbox to switch to separate Base and Alert editors. If auto-split fails, a callout on the alert condition step lets you open the sandbox directly in manual split mode.

## Using the YAML editor [yaml-editor]

Use the YAML editor when you want to copy or adapt a rule quickly without re-entering settings by hand, or provision many rules at once. The YAML editor isn't available within the Threshold Alert builder.
