---
navigation_title: Create an ES|QL rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write ES|QL detection queries for rules in Kibana's experimental alerting system using the rule form or YAML editor, with a live query sandbox for previewing results."
---

# Create an ES|QL rule in the {{alerting-v2-system}} [create-esql-rule]

The ES|QL rule path lets you write the detection query directly. Two ways to define it are available:

- **Rule form** - Fill in the step-by-step form with a live preview of results.
- **YAML mode** - Switch to YAML and edit the raw rule definition. You can switch between form and YAML at any point; edits are preserved.

For descriptions of what each rule setting does, refer to [Configure a rule](configure-a-rule.md). For a full list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

## Preview query results in the sandbox [rule-builder-query-sandbox]

The query sandbox lets you run your {{esql}} query against current data and preview the results before applying them to the rule form. Use the time field selector and date picker to control the time range, then select **Search** (or press ⌘↵) to execute. When the results look correct, select **Apply changes** to populate the form.

Use the sandbox to:

- **Confirm grouping** - Check that your `BY` clause produces the series you intend, for example, one distinct series per host or per service, not a single undifferentiated result.
- **Catch unexpected output** - Verify that the query returns data in the right shape for the alert condition you plan to set. A query that returns zero rows or an unexpected field name won't behave as expected once the rule runs on a schedule.
- **Refine before committing** - Edit the query and re-run it as many times as needed without leaving the rule creation form.

## Using the YAML editor [yaml-editor]

Use the YAML editor when you want to copy or adapt a rule quickly without re-entering settings by hand, or provision many rules at once. The YAML editor isn't available within the Threshold Alert builder.

### YAML-only mode when editing rules [yaml-only-edit]

When you reopen a rule for editing, the form/YAML toggle is disabled if the rule's YAML configuration contains settings the form cannot represent. The rule opens in YAML-only mode. This prevents the form from silently dropping fields it doesn't know how to display on save. The YAML editor remains fully functional, and all fields round-trip without loss.

The following configurations force YAML-only mode when editing:

| Configuration | Why the form can't represent it |
| --- | --- |
| `query.format: standalone` with `kind: alert` | The form is built around the composed query format (base query plus condition blocks). Standalone format rules cannot be loaded into the form editor. |
| `recovery_strategy: no_breach` or `recovery_strategy: none` | The form only supports custom recovery queries. The no-breach and none strategies have no form equivalent. |
| `no_data_strategy` (any active value) | The form has no controls for no-data handling. |
| `query.no_data` block | The form has no UI for inline no-data query definitions. |

If the toggle is disabled and you want to use the form, you must remove the non-representable configuration from the YAML before saving, then reopen the rule.
