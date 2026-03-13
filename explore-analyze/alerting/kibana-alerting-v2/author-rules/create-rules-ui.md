---
navigation_title: Using the UI
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Create and configure Kibana alerting v2 rules using the rule creation form with interactive and YAML editing modes."
---

# Create Kibana alerting v2 rules in the UI [create-rules-ui-v2]

Create and configure Kibana alerting v2 rules using the rule creation form. The form supports both interactive (GUI) and YAML editing modes, and lets you preview rule results against existing data before saving.

## Open the rule creation form

1. Navigate to **Management > Alerts and Insights > Rules V2**.
2. Click **Create rule**.

You can also create rules from within a notification policy or from Discover. Refer to [Create rules in Discover](create-rules-discover.md) for the Discover workflow.

## Configure the rule

### Name and description

Give the rule a meaningful name and optional description. These appear in the rules list and alert details.

### Mode

Choose the rule mode:

- **Detect** (`kind: signal`) — produces signal events for exploration. No lifecycle tracking or notifications.
- **Detect and alert** (`kind: alert`) — produces alert events with lifecycle management and notification support.

You can switch modes after creation.

### ES|QL query

Write the ES|QL query that defines what the rule evaluates. The query has two parts:

- **Base query** (required) — the main ES|QL query that selects, aggregates, and transforms data.
- **Alert condition** (optional) — a `WHERE` clause that filters to breaching rows. Setting a separate alert condition enables the system to distinguish "data exists but doesn't breach" from "no data."

Use the **YAML mode** toggle to switch between the interactive form and a YAML editor for the full rule definition.

### Grouping

Define one or more group key fields to split alert event generation. Each unique combination of field values produces its own alert series. For example, grouping by `host.name` creates a separate alert series for each host.

### Schedule

Configure the execution interval (for example, every 1 minute, 5 minutes, or 1 hour) and the lookback window that determines how far back the ES|QL query evaluates.

### Alert mode settings

When the rule is in alert mode, additional settings are available:

- **Alert delay** (activation threshold) — require the condition to be met a specified number of consecutive times or for a minimum duration before an alert becomes active.
- **Recovery conditions** — define how recovery is detected: by the absence of breaching results (`no_breach`) or by a separate recovery query.
- **No-data handling** — configure behavior when the query returns no results: record a no-data status, carry forward the previous status, or treat as recovery.
- **Notification policies** — link one or more notification policies to route alerts to workflow destinations.
- **Tags** — add free-form tags for filtering and organization.
- **Investigation guide** — attach a runbook or investigation guide to the rule.

### Preview results

Before saving, click **Preview** to evaluate the query against recent data. The preview shows:

- How many rows the query returns.
- How many alert events would be generated.
- Sample alert event documents.

Use the preview to tune the query and thresholds before the rule starts running in production.

## Save the rule

Click **Save** to create the rule. The rule starts executing on its configured schedule. Results appear in the rules list and, for alert-mode rules, in the alert inbox.
