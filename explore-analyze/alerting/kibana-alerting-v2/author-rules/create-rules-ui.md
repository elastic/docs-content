---
navigation_title: Using the UI
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Create Kibana alerting v2 rules using the interactive rule creation form with query editor, preview, and YAML toggle."
---

# Create Kibana alerting v2 rules in the UI [create-rules-ui-v2]

Create Kibana alerting v2 rules using the interactive rule creation form. The form provides a guided experience for configuring all rule settings, with the option to toggle between interactive and YAML modes.

## Open the rule creation form

1. Navigate to Management > Alerts and Insights > Rules V2.
2. Click Create rule.

## Configure the rule

### Mode

Choose between Detect (signals only) and Alert (lifecycle tracking and notifications).

### ES|QL query

Write the ES|QL query that defines what to detect. The query has two parts:

- Base query (required): the main ES|QL query that selects, aggregates, and transforms data.
- Alert condition (optional): a `WHERE` clause that filters to breaching rows.

Use the YAML mode toggle to switch between the interactive form and a YAML editor for the full rule definition.

### Grouping

Define one or more group key fields to split alert event generation. Each unique combination of field values produces its own alert series.

### Schedule

Configure the execution interval and the lookback window that determines how far back the ES|QL query evaluates.

### Alert mode settings

When the rule is in alert mode, additional settings are available:

- Alert delay (activation threshold): require the condition to be met a specified number of consecutive times or for a minimum duration before an alert becomes active.
- Recovery conditions: define how recovery is detected.
- No-data handling: configure behavior when the query returns no results.
- Notification policies: policies are global. Scoping uses rule labels and matchers on the policy side, not links from this form. Configure policies under Notification Policies. For an overview, refer to [Notification policies](rule-settings/notification-policies.md).
- Tags: add free-form tags for filtering and organization.
- Investigation guide: attach a runbook or investigation guide to the rule.

### Preview results

Before saving, click Preview to evaluate the query against recent data. The preview shows:

- How many rows the query returns.
- How many alert events would be generated.
- Sample alert event documents.
- A Lens-powered bar chart histogram of matching row counts over time, for both evaluation previews and recovery previews (when recovery logic applies).

## Save the rule

Click Save to create the rule. The rule starts executing on its configured schedule.
