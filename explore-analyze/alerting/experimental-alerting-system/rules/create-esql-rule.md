---
navigation_title: Create an ES|QL rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write ES|QL detection queries for rules in Kibana's experimental alerting system using the rule form or YAML editor, with a live query sandbox for previewing results."
---

# Create an {{esql}} rule in the {{alerting-v2-system}} [create-esql-rule]

Creating an {{esql}} rule lets you write the detection query directly instead of going through the rule builder's structured inputs. There are two ways to define the rule:

- **Rule form** - Fill in the step-by-step form with a live preview of results. For details on configurable rule settings and guidance on how to configure them, refer to [Configure a rule](configure-a-rule.md).
- **YAML editor** - Edit the raw rule definition directly instead of using the form. You can switch between form and YAML at any time. Invalid YAML that can't be translated to a valid form state locks you into the YAML editor until it's fixed. For a list of supported YAML fields, refer to [YAML rule schema reference](yaml-rule-schema-reference.md).

Go to the **Rules** page (go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md) > **Rules**), then start creating a rule. When choosing a creation path, select the one that lets you write the query directly as {{esql}}.

:::{note}
**Rule form** and **YAML editor** are the names used in this documentation, not necessarily exact UI labels. Look for the equivalent options when creating or editing a rule.
:::

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

By default, applying changes in the sandbox automatically splits your query into a base query and alert condition. If you want full manual control over the split, use the toggle in the sandbox to switch to separate Base and Alert editors. If auto-split fails, a callout on the alert condition step lets you open the sandbox directly in manual split mode. For what each part of the split does, refer to [{{esql}} query](configure-rule-query.md).
