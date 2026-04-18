---
navigation_title: View and manage rules
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Use the {{alerting-v2}} rules list and rule details page: filters, search, sorting, bulk actions, snooze vs disable, and configuration including Conditions and Runbook."
---

# View and manage {{alerting-v2}} rules [manage-rules-v2]

$$$manage-rules-v2$$$

The {{alerting-v2}} rules list and the **rule details** page are where you review rule configuration, open the rule form to edit, and run bulk or per-rule actions such as **`Enable`**, **`Disable`**, **`Clone`**, and **`Delete`**.

**Managing rules** is separate from **authoring** definitions. Refer to [Author rules](author-rules.md) to create or edit the {{esql}} query, schedule, and mode.

## Rules list

### Open the list

1. Open **{{manage-app}}**.
2. Go to **V2 Alerting Preview** > **{{rules-ui}}**.

If your deployment still surfaces the same experience under **Alerts and Insights** > **{{rules-ui}}** (v2), you can use that entry instead. Labels vary slightly by version.

### Columns

Typical columns include:

- **Name:** Rule name. Select the name to open the rule details page (often with a normal link so you can open in a new tab).
- **Source:** Data source inferred from the rule {{esql}} query (for example the index or pattern from the `FROM` clause).
- **Labels:** Tags applied to the rule for filtering and action policy scoping.
- **Mode:** Whether the rule runs in **alert** mode or **detect-only** mode, where applicable.
- **Enabled:** Whether the rule is on and scheduled.

Your build may add or rename columns. Use table controls if your UI exposes them.

### Filters, search, and sorting

- Use **filters** to narrow by whether the rule is running, mode (alert versus detect-only), and labels or tags.
- Use **search** to match rule **names** and **labels** (server-side).
- Use **column headers** to sort where sorting is supported (for example by name, mode, or status).

### Open rule details

Select a rule **name** to open the **rule details** page. There you can read full configuration, use **Edit** to change the rule, and use the actions menu for **`Enable`**, **`Disable`**, **`Clone`**, and **`Delete`**.

The details view includes a **Rule conditions** section ({{esql}} base query, alert condition when applicable, schedule, grouping, recovery, and related fields). If the rule defines a runbook artifact, a **Runbook** tab shows the runbook content next to **Conditions**.

## Bulk actions

From the rules list, select one or more rows to run bulk operations:

- **`Enable`:** Selected rules schedule again.
- **`Disable`:** Selected rules stop scheduling until you run **`Enable`** again.
- **`Delete`:** Remove selected rules. Confirm when prompted.

**Select all** (including select-all for the full filtered result set) applies bulk actions to the rules that match your **current filters and search**, not only the rows on one page. Large filter-based selections are **capped** (for example at 10,000 rules per operation). If the cap applies, the UI explains that only the first portion of the matching rules is included.

For actions on a single rule, open the rule details page or use the row actions menu if your build provides it.

## Stop a rule from running

Use **`Disable`** on a rule when you want it to stop running on its schedule until you **`Enable`** it again. That is different from **snoozing**, which usually suppresses notifications or quiets work for a **series** or **policy** without removing the rule from the schedule.

### From the rules list

1. Open the rules list as described in [Open the list](#open-the-list).
2. Find the rule using search and filters if needed.
3. Use the row actions or selection checkboxes, then select **`Disable`**, or use bulk **`Disable`** when multiple rules are selected.

### From the rule details page

1. Open the rule from the list (select the rule **name**).
2. Open the actions menu on the details page.
3. Select **`Disable rule`** (or equivalent). The page should show that the rule is not running.

To start the rule again, use **`Enable`** from the same places.

## Snooze and other ways to reduce noise

- **Snooze or silence alert episodes and series** (for example per `group_hash`) is handled from the alert episodes experience and related flows. See [Investigate and respond](manage-alerts/investigate-respond.md#alert-actions-v2) and [View and manage alert episodes](manage-alerts.md).
- **Snooze or stop action policies** (notification policies) is configured on the action policy, not on the rule list. See [Send notifications](send-notifications.md#action-policies-v2).

If you are unsure whether to stop the rule or snooze a series, start with [Reduce noise](reduce-noise.md) for an overview of scopes.

## Related

- [View and manage alert episodes](manage-alerts.md): Triage and respond to alerts produced by rules.
