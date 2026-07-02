---
navigation_title: Quick start
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Create your first rule in the {{alerting-v2}}: enable the feature, write an {{esql}} query in the YAML editor, and confirm the rule is running by querying the rule events data stream."
---

# Quick start: Your first rule [alerting-quick-start]


This quick start is part of the {{alerting-v2}} in Kibana. It walks you through the core model in action. You'll load sample error logs, create a rule that groups results by service, watch episodes open as the rule finds breaches, and then trigger recovery by deleting the data. By the end, you'll have learned about rules, grouping, episodes, and the alert lifecycle play out from start to finish.

## Step 1: Create a sample data stream

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


## Step 2: Verify the data is queryable

Run this in Dev Tools to confirm the rule will find it:

```esql
FROM logs-tutorial
| WHERE log_level == "ERROR"
| STATS error_count = COUNT() BY service_name
| WHERE error_count >= 2
```

You should see two rows: one for `checkout` (3 errors) and one for `payments` (2 errors). If you see this, the rule will trigger for both services.

## Step 3: Create the rule

Go to **Management > V2 Alerting Preview** and create a new rule using the YAML editor with the following configuration:

<!--[CONTENT NEEDED: UI. "V2 Alerting Preview" is a development-phase navigation label that will change. Update all instances of this navigation path in this tutorial before publishing.]
-->

```yaml
kind: alert
metadata:
  name: tutorial-error-rate
  tags:
    - tutorial
time_field: '@timestamp'
schedule:
  every: 5s
  lookback: 24h
evaluation:
  query:
    base: |-
      FROM logs-tutorial
      | WHERE log_level == "ERROR"
      | STATS error_count = COUNT() BY service_name
      | WHERE error_count >= 2
grouping:
  fields:
    - service_name
```

<!--[CONTENT NEEDED for M2: The `grouping` key will be renamed to `track_by` in M2. Update this example to use `track_by: { fields: [service_name] }` once that change ships.]
-->

Save the rule. It will be enabled automatically.


## Step 4: Confirm the rule is running

Wait 5 seconds, then run the following in Discover using the ES|QL mode. Replace `<your-rule-id>` with the `tutorial-error-rate` rule ID.

```esql
FROM .rule-events
| WHERE rule.id == "<your-rule-id>"
| SORT @timestamp DESC
| LIMIT 10
```

:::{tip}
After saving the rule, open its details page. The rule ID is the string at the end of the browser URL.
:::

Check the following in the query results:

| Field | What you should see |
|---|---|
| `@timestamp` | Recent timestamps updating every 5 seconds |
| `status` | `breached` confirms the query is finding matches |
| `episode.status` | `active` confirms episodes have opened for both services |
| `data.service_name` | `checkout` and `payments` confirms grouping is working |


## Step 5: Confirm two episodes are open

In Discover, run: 

```esql
FROM .rule-events
| WHERE rule.id == "<your-rule-id>"
| STATS latest = MAX(@timestamp) BY episode.id, episode.status, data.service_name
| SORT latest DESC
```

You should see two rows: one episode for `checkout` and one for `payments`, both with `episode.status: active`.


## Step 6: Trigger recovery

Delete the test data to clear the breach condition. Run the following in Dev Tools:

```json
POST logs-tutorial/_delete_by_query
{
  "query": { "match_all": {} }
}
```

Wait up to 5 seconds, then re-run the query from Step 5 in Discover. Both episodes should now show `episode.status: inactive`.

## What you learned

By completing this tutorial, you saw the core experimental alerting model in action end to end:

- **Rules query your data on a schedule.** Your rule ran every 5 seconds, checking for services with 2 or more errors in the last 24 hours.
- **Grouping creates independent series.** Because the rule grouped by `service_name`, `checkout` and `payments` were tracked separately. Each got its own episode.
- **Episodes follow a lifecycle.** When the error logs existed, both episodes moved to `active`. When you deleted the logs, both recovered and moved to `inactive` automatically, no manual intervention required.
- **Rule events are the underlying record.** Every evaluation wrote documents to `.rule-events`, giving you a full queryable history of what the rule found and when.

## Next steps

<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- **Add notifications:** Create a workflow and action policy to route alerts when an episode opens or recovers. Refer to [Notifications](notifications.md).
-->
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
- **Use your own data:** Swap `logs-tutorial` for a real data source and update the breach condition to match your use case. Refer to [Author rules](rules/author-rules.md) to learn more.
-->
<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
- **Explore rule history in Discover:** Query `.rule-events` to track trends, compare episode durations, and identify which services breach most frequently. Refer to [Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover.md) to learn more.
-->