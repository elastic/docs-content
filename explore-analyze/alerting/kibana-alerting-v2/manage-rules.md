---
navigation_title: Manage rules
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "View, filter, and manage Kibana alerting v2 rules from the rules list."
---

# Manage Kibana alerting v2 rules [manage-rules-v2]

View, filter, and manage your Kibana alerting v2 rules from a single entry point. The rules list provides an overview of all rules with their status, execution state, and alert counts.

## Access the rules list

Navigate to **Management > Alerts and Insights > Rules V2**. The rules list shows Kibana alerting v2 rules in a dedicated tab alongside the Kibana alerting v1 rules tab.

## Rules list columns

Each rule in the list displays:

| Column | Description |
|---|---|
| **Rule name** | The rule name defined in metadata |
| **Mode** | Detect (signal) or Alert |
| **Status** | Enabled or disabled |
| **Last run** | Timestamp of the most recent execution |
| **Execution state** | Succeeded, failed, or warning |
| **Alert events** | Count of alert events generated (last 7 days) |
| **Tags** | Tags assigned to the rule |
| **Source** | Data source from the rule's ES\|QL query |

## Filter, sort, and search

- **Filter** by rule name, mode, tags, status, source, and execution state.
- **Sort** by any column.
- **Search** across all rule attributes using the search bar.

## Rule actions

### Inline actions

Click the actions menu on any rule row to:

- **View details** — open the full rule details page.
- **Edit** — open the rule form with current settings.
- **Enable/Disable** — toggle rule execution.
- **Clone** — create a copy with all settings pre-filled.
- **Run** — execute the rule once immediately.
- **Update API key** — refresh the API key used for execution.
- **Delete** — remove the rule.

### Bulk actions

Select multiple rules to:

- Enable or disable in bulk.
- Update API keys in bulk.
- Delete in bulk.

## Switch rule mode

You can switch a rule between detect and alert modes from the rules list or the rule details page:

- **Alert → Detect**: stops lifecycle tracking and notifications. The rule continues producing signal events.
- **Detect → Alert**: begins lifecycle tracking. New episodes are created for breaching conditions.
