---
navigation_title: Create your first rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Step-by-step tutorial for creating your first rule in Kibana's experimental alerting system: load sample latency data, write an ES|QL detection query, configure the rule, and observe the alert episode lifecycle from breach to automatic recovery."
---

# Create your first rule [alerting-quick-start]

In this tutorial, you'll create an index of synthetic latency data, build a rule that detects when P95 latency for a service exceeds 2 seconds, and watch the episode lifecycle — from breach detection through automatic recovery. Along the way, you'll learn how the {{alerting-v2-system}} tracks conditions over time.

## Prerequisites [alerting-quick-start-prerequisites]

- **Enable the {{alerting-v2-system}}:** The feature must be turned on in your space before you can create rules or view the UI. Refer to [Set up the {{alerting-v2-system}}](setup.md) for instructions.
- **Configure access:** Your role must include the following privileges to complete this tutorial. Refer to [{{kib}} role management](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for instructions on creating or updating a role.
  - **Rules: All** (under **Alerting** in {{kib}} role management) to create and manage rules
  - **Discover: Read** and `read` index privilege on `.rule-events` to query rule output in Discover

## Tutorial [alerting-quick-start-tutorial]

:::::{stepper}

::::{step} Create the index

Run the following in **Dev Tools** to create the index that your rule will query. Unlike data streams, this index requires explicit creation because it uses a custom mapping.

```json
PUT checkout-service-logs
{
  "mappings": {
    "properties": {
      "@timestamp": { "type": "date" },
      "service.name": { "type": "keyword" },
      "transaction.name": { "type": "keyword" },
      "latency_ms": { "type": "float" }
    }
  }
}
```

Confirm the response shows `"acknowledged": true` before proceeding.

::::

::::{step} Load the sample data

Expand the drop-down below (at the end of this step) to copy the full bulk request, then run it in Dev Tools. It populates the index with ~40 minutes of synthetic latency data for a `checkout` service covering three phases:

- **Healthy** (first ~16 minutes): P95 well under 2 seconds
- **Degraded** (next ~15 minutes): P95 well over 2 seconds, spanning 3 consecutive 5-minute windows
- **Recovered** (final ~10 minutes): P95 returns to healthy levels

The response should show `errors: false` for all documents. The dataset gives you: healthy through `22:12`, degraded `22:13`–`22:27` (spanning 3 consecutive 5-minute windows), recovered from `22:28` onward.

:::{note}
The timestamps in this request are fixed to `2026-07-02`. For the full episode lifecycle to play out as described, load this data and create the rule within 60 minutes, or adjust the timestamps to a recent window before running. For example, open the request in a text editor and use find-and-replace to substitute `2026-07-02` with today's date in `YYYY-MM-DD` format, keeping the time portion (`T21:57` through `T22:37`) intact so the degraded window (`T22:13`–`T22:27`) falls within the past 60 minutes in UTC.
:::

::::{dropdown} Bulk request: 80 synthetic latency events (healthy → degraded → recovered)
```json
POST checkout-service-logs/_bulk
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:57:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":468}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:57:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":336}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:58:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":367}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:58:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":372}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:59:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":497}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:59:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":305}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:00:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":384}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:00:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":406}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:01:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":427}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:01:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":461}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:02:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":448}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:02:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":527}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:03:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":272}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:03:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":477}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:04:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":355}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:04:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":466}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:05:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":528}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:05:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":280}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:06:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":278}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:06:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":252}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:07:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":443}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:07:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":447}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:08:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":504}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:08:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":260}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:09:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":353}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:09:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":508}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:10:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":381}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:10:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":315}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:11:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":284}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:11:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":261}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:12:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":371}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:12:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":329}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:13:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2704}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:13:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2909}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:14:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2898}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:14:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3094}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:15:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3701}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:15:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3977}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:16:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2368}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:16:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3954}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:17:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2610}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:17:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2491}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:18:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3751}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:18:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3909}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:19:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3903}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:19:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3905}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:20:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2292}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:20:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4429}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:21:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4147}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:21:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2462}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:22:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2733}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:22:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2869}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:23:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4323}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:23:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3802}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:24:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3105}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:24:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2335}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:25:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3649}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:25:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4320}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:26:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2671}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:26:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3438}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:27:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2251}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:27:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3235}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:28:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":525}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:28:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":458}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:29:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":448}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:29:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":453}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:30:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":435}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:30:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":463}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:31:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":319}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:31:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":421}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:32:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":353}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:32:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":378}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:33:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":369}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:33:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":490}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:34:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":284}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:34:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":359}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:35:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":468}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:35:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":292}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:36:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":427}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:36:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":423}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:37:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":259}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T22:37:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":309}
```
::::


::::

::::{step} Create the rule

Go to **Alerting V2 Preview** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the rules list, select the option to create a new rule. When the rule creation panel opens, select **Create ES|QL rule** to open the rule authoring flyout.

1. Paste the following {{esql}} query into the **Query sandbox**. The query computes P95 latency per service, assigns a severity tier (`critical`, `high`, or `low`) based on the result, and returns only rows where P95 exceeds 2000 ms. An empty result means no breach.

   ```esql
   FROM checkout-service-logs
   | STATS p95_latency_ms = PERCENTILE(latency_ms, 95) BY service.name
   | EVAL severity = CASE(
       p95_latency_ms >= 4000, "critical",
       p95_latency_ms >= 2000, "high",
       "low"
     )
   | WHERE p95_latency_ms > 2000 
   ```

   :::{note}
   Do not add a `WHERE @timestamp` clause to this query. Both the query sandbox and the rule executor automatically inject the time-window filter based on the date range you select in the sandbox or the rule's schedule and lookback once it's running.
   :::

2. Set the sandbox date range to **Last 1 hour** and run the query. This preset gives comfortable coverage of the full dataset without being wide enough to pull in data from a previous run-through.

3. Confirm the query results. You should see one row for `service.name: checkout` with `p95_latency_ms` above 2000 and `severity: high` or `critical`. When you narrow the range to cover only the healthy periods before or after the degraded window, the row disappears. P95 drops below the threshold, which is the `no_breach` recovery condition.

4. When the results look correct, select **Apply changes** to populate the rule form, then select **Next**. 

   :::{note}
   The sandbox time controls set the preview range only. They don't carry over to the rule's schedule or lookback window once the rule is running.
   :::

5. Complete the **Alert Condition** step (pane 1 of 4). The query you applied from the sandbox auto-fills **Mode**, **Time field**, and **Group fields**. Set the remaining fields, then select **Next**:

   - Under **Alert delay**, select **Breaches** and set the count to `2`. This requires the breach to persist across 2 consecutive evaluations before the episode moves to `active`.
   - Set **Schedule** to every `5` minutes.
   - Set **Lookback Window** to the last `2` hours. This ensures the rule can reach the pre-loaded sample data regardless of when you complete the tutorial. A shorter lookback would only work if the data timestamps fell within the last few minutes.

6. On the **Recovery Condition** step, confirm the defaults, then select **Next**:

   - **Recovery**: `Default recovery`
   - **Recovery delay**: `Immediate` (No delay, recovers on first non-breach)

   These defaults produce the automatic recovery behavior this tutorial demonstrates: the episode closes as soon as a scheduled run returns no breaching rows.

7. On the **Details & Artifacts** step, enter the following, then select **Next**:

   - **Name**: Checkout Service Latency
   - **Description**: `Detects when P95 latency for the checkout service exceeds 2 seconds. Groups by service name and assigns severity: critical at 4000 ms, high at 2000 ms.`

8. On the **Actions** step, do not create an action policy (rules can run without notifications or actions setup). Select **Create rule** to create and enable the rule.

::::

::::{step} Confirm the rule is evaluating

1. Open Discover and switch to {{esql}} mode.

2. Set the date range to **Today** or **Last 1 hour**. The default "Last 15 minutes" is often too narrow to catch the first evaluation.

3. Wait one schedule interval (5 minutes), then run the following query. Replace `<your-rule-id>` with the ID from the rule's detail page URL.

   ```esql
   FROM .rule-events
   | WHERE rule.id == "<your-rule-id>"
   | SORT @timestamp DESC
   | LIMIT 10
   ```

   :::{tip}
   Open the rule's detail page. The rule ID is the last path segment in the browser URL. If you see 0 results, confirm the date range is wide enough and that at least one schedule interval has elapsed since you created the rule.
   :::

4. Check these fields in the results:

   | Field | What to look for |
   |---|---|
   | `@timestamp` | A recent timestamp confirming the rule has run |
   | `status` | `breached` when the query found rows above the threshold; `no_breach` when it found none |
   | `episode.status` | `pending` for the first two consecutive breaching runs; `active` once the breach persists |
   | `data.service.name` | `checkout` — confirms the grouping field was captured |
   | `data.severity` | `high` or `critical` depending on the P95 value in the evaluated window |

::::

::::{step} Observe the episode lifecycle

1. As the rule continues to run every 5 minutes, its lookback window slides forward in time. Once the degraded data at `22:13`–`22:27` is no longer within the 2-hour window, the rule returns no breach and the episode recovers automatically.

2. Run the following in Discover to track the episode:

   ```esql
   FROM .rule-events
   | WHERE rule.id == "<your-rule-id>"
   | STATS latest = MAX(@timestamp) BY episode.id, episode.status, data.service.name
   | SORT latest DESC
   ```

3. Confirm the episode moves from `active` to `inactive` without any manual intervention. This is the `no_breach` recovery strategy in action.

::::

:::::

## Key concepts demonstrated

- **Rules**: Run an {{esql}} query on a schedule and detect when the results meet a condition. Each run computes P95 latency over the lookback window and finds a breach when the result exceeds 2000 ms.
- **Severity tiers**: The `CASE()` expression assigns `high` or `critical` based on the P95 value. These values are stored in `.rule-events` as `data.severity` and are queryable from Discover.
- **Episode lifecycle**: Episodes don't open on the first breach. With **Alert delay** set to **Breaches: 2**, the condition must persist for two consecutive evaluations before the episode moves to `active`. This filters out transient spikes.
- **Automatic recovery**: With **Recovery** set to **Default recovery**, the episode closes as soon as a scheduled run returns no breaching rows. No separate recovery query or manual step was required.
- **Rule events**: Every evaluation writes a document to `.rule-events`, giving you a full queryable history of what the rule found, when the episode opened, and when it recovered.

<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
## What's next
- **[Add notifications](../notifications-actions.md):** Create a workflow and action policy to route alerts when an episode opens or recovers. Use `rule.tags: "checkout" AND severity: ("high" OR "critical")` as the matcher to skip low-severity episodes.
-->
<!-- TODO: Uncomment when PR #6523 (rules) is merged:
- **[Use your own data](../rules/create-a-rule.md):** Swap `checkout-service-logs` for a real data source and update the breach condition to match your use case.
-->
<!-- TODO: Uncomment when PR #6527 (alerts) is merged:
- **[Query rule output in Discover](../alerts/query-alerts-and-signals-in-discover.md):** Track trends, compare episode durations, and identify which services breach most frequently.
-->
