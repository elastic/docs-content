---
navigation_title: Create your first rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Create your first Kibana rule using the experimental alerting features: enable the feature flag, write an ES|QL query in the YAML editor, and verify the rule is running by querying the rule events data stream."
---

# Create your first rule [alerting-quick-start]

In this tutorial, you'll load sample error logs, create a rule that detects errors by service, and watch the alert lifecycle play out — from breach to recovery. Along the way, you'll learn the core concepts of the {{alerting-v2-system}}.

## Prerequisites [alerting-quick-start-prerequisites]

- **Enable the {{alerting-v2-system}}:** The feature must be turned on in your space before you can create rules or view the UI. Refer to [Turn on the {{alerting-v2-system}}](setup.md) for instructions.
- **Configure access:** Your role must include the following privileges to complete this tutorial:
  - **Rules: All** (under **Alerting** in Kibana role management) to create and manage rules
  - **Discover: Read** and `read` index privilege on `.rule-events` to query rule output in Discover

  For a full breakdown of privilege requirements, refer to [{{alerting-v2-system-cap}} privileges](configure-access.md).

## Tutorial [alerting-quick-start-tutorial]

:::::{stepper}

::::{step} Create a sample data stream

Run this in Dev Tools to create a data stream called `logs-tutorial` and populate it with sample error logs. This is the data your rule will query.

```json
POST logs-tutorial/_bulk
{ "index": {} }
{ "@timestamp": "2026-04-21T21:50:00.000Z", "log_level": "ERROR", "service_name": "checkout", "message": "Connection timeout" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:51:00.000Z", "log_level": "ERROR", "service_name": "checkout", "message": "Database query failed" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:52:00.000Z", "log_level": "ERROR", "service_name": "checkout", "message": "Null pointer exception" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:50:00.000Z", "log_level": "ERROR", "service_name": "payments", "message": "Payment gateway unreachable" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:51:00.000Z", "log_level": "ERROR", "service_name": "payments", "message": "Transaction rollback failed" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:50:00.000Z", "log_level": "INFO", "service_name": "checkout", "message": "Request received" }
{ "index": {} }
{ "@timestamp": "2026-04-21T21:51:00.000Z", "log_level": "INFO", "service_name": "payments", "message": "Health check passed" }
```

:::{note}
`logs-tutorial` is automatically created as a data stream because the `logs-*` naming pattern matches Elasticsearch's default index template. You don't need to create it manually beforehand.
:::

Confirm the data was indexed. You should see `errors: false` and `result: "created"` for each document in the response.

::::

::::{step} Create the rule

Go to **Alerting V2 Preview** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the rules list, select the option to create a new rule. When the rule creation panel opens, select **Create ES|QL rule**.

Next, paste the following {{esql}} query into the **Query sandbox** textbox:

```esql
FROM logs-tutorial
| WHERE log_level == "ERROR"
| STATS error_count = COUNT() BY service_name
| WHERE error_count >= 2
```

Use the query sandbox to verify the query returns the results you expect before applying it to the rule form. The sandbox lets you run the query against current data using the time field selector and date picker to control the time range. Select **Search** (or press ⌘↵) to execute. When the results look correct, select **Apply changes** to populate the form.

After applying the query, set the remaining fields in the form:

| Field | Value |
|---|---|
| Time field | `@timestamp` |
| Schedule | `5s` |
| Lookback | `24h` |
| Group by | `service_name` |

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
For a full walkthrough of the rule creation flyout, refer to [Create an ES|QL rule](../rules/create-esql-rule.md). For a complete reference of YAML fields if using YAML mode, refer to [YAML rule schema reference](../rules/yaml-rule-schema-reference.md).
-->

Click **Save**. The rule is enabled automatically.

::::

::::{step} Confirm the rule is running

Wait 5 seconds, then run the following in Discover using the ES|QL mode. Replace `<your-rule-id>` with the `tutorial-error-rate` rule ID.

:::{tip}
After saving the rule, open its details page. The rule ID is the string at the end of the browser URL.
:::

```esql
FROM .rule-events
| WHERE rule.id == "<your-rule-id>"
| SORT @timestamp DESC
| LIMIT 10
```

Check the following in the query results:

| Field | What you should see |
|---|---|
| `@timestamp` | Recent timestamps updating every 5 seconds |
| `status` | `breached` confirms the query is finding matches |
| `episode.status` | `active` confirms episodes have opened for both services |
| `data.service_name` | `checkout` and `payments` confirms grouping is working |

::::

::::{step} Confirm two episodes are open

In Discover, run:

```esql
FROM .rule-events
| WHERE rule.id == "<your-rule-id>"
| STATS latest = MAX(@timestamp) BY episode.id, episode.status, data.service_name
| SORT latest DESC
```

You should see two rows: one episode for `checkout` and one for `payments`, both with `episode.status: active`.

::::

::::{step} Trigger recovery

Delete the test data to clear the breach condition. Run the following in Dev Tools:

```json
POST logs-tutorial/_delete_by_query
{
  "query": { "match_all": {} }
}
```

Wait up to 5 seconds, then re-run the query from the previous step in Discover. Both episodes should now show `episode.status: inactive`.

::::

:::::

## Key concepts demonstrated

This tutorial introduces the core concepts of the {{alerting-v2-system}}:

* **Rules**: Query your data on a schedule and detect when conditions are met. Your rule ran every 5 seconds, checking for services with 2 or more errors in the last 24 hours.
* **Grouping**: Creates independent tracked series from a single rule. Because the rule grouped by `service_name`, `checkout` and `payments` were tracked separately — each with its own episode.
* **Episodes**: Follow a lifecycle driven by the rule's findings. Both episodes moved to `active` when errors existed, and recovered to `inactive` automatically when the data was deleted.
* **Rule events**: The underlying record of every evaluation. Every run wrote documents to `.rule-events`, giving you a full queryable history of what the rule found and when.

## What's next

<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- **[Add notifications](../notifications-actions.md):** Create a workflow and action policy to route alerts when an episode opens or recovers.
-->
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
- **[Use your own data](../rules/create-a-rule.md):** Swap `logs-tutorial` for a real data source and update the breach condition to match your use case.
-->
<!-- TODO: Uncomment when PR #6527 (alerts) is merged:
- **[Query rule output in Discover](../alerts/query-alerts-and-signals-in-discover.md):** Track trends, compare episode durations, and identify which services breach most frequently.
-->
