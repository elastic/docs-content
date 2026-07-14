---
navigation_title: Create your first rule
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
  - id: cloud-serverless
description: "Tutorial for creating an ES|QL rule in Kibana's experimental alerting system. Covers how alert delay controls when an episode opens, how .rule-events records each evaluation, and how default recovery closes an episode automatically when no breach is detected."
---

# Create a rule and observe the alert lifecycle [create-first-rule]

In this tutorial, you'll use the {{alerting-v2-system}} to detect a real-world performance problem and watch what happens next. You'll see how the system decides when a condition is serious enough to open an alert, how it tracks that alert over time, and how it closes automatically when things return to normal, without any manual intervention.

Here's what you'll do:

1. **Load sample data** - Create an index and populate it with synthetic latency data that moves through healthy, degraded, and recovered phases. This gives you a realistic dataset to work with without needing a live service.
2. **Write a detection query** - Use the query sandbox to build and preview an {{esql}} query that computes P95 latency and flags breaches. The sandbox lets you verify the logic before the rule ever runs.
3. **Configure the rule** - Set the alert condition, schedule, lookback window, and recovery behavior. You'll see how each setting shapes the alert lifecycle.
4. **Confirm the rule is running** - Check the **Execution history** page to see that the rule is evaluating on schedule and its runs are succeeding.
5. **Watch the episode open and recover** - Open the alert episode's details page to watch the episode move from `pending` to `active` as the breach persists, then close automatically when the degraded data ages out of the lookback window.

## Requirements [create-rule-requirements]

Before you start, make sure you have the following:

- **One of the following deployment types**:
  - **{{serverless-short}}** - A {{serverless-full}} project. [Create a serverless project](/deploy-manage/deploy/elastic-cloud/serverless.md) if you don't have one.
  - **{{ech}}** - An {{ech}} deployment running version 9.5 or later. Refer to [Create an Elastic Cloud hosted deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) if you don't have one. {applies_to}`stack: experimental 9.5`
  - **Self-managed** - An {{stack}} deployment running version 9.5 or later. Refer to the [local development quickstart](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md) if you don't have one. {applies_to}`stack: experimental 9.5`

- **The {{alerting-v2-system}} enabled**: The {{alerting-v2-system}} must be turned on in your space before you can use any of its features. Refer to [Set up the {{alerting-v2-system}}](setup.md) for instructions.

- **The required access**: Your [role](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) must give you access to:

  | Task | Required privilege |
  |---|---|
  | Create and manage rules | **Rules: All** (under **Alerting**) |
  | View and triage alert episodes | **Alerts: Read** (under **Alerting**); also automatically grants {{es}} `read` access to `.rule-events`, no separate index privilege needed |
  | Review execution history | **Execution history: Read** (under **Alerting**) |
  | Create the tutorial index and load sample data | `create_index` and `write` index privileges on `checkout-service-logs` |

## Prepare your environment [prepare-your-environment]

Before creating the rule, set up the index and load the sample data it will query.

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

Expand the drop-down below to copy the full bulk request, then run it in Dev Tools. It populates the index with synthetic latency data for a `checkout` service covering three phases:

- **Healthy** (`21:57`–`22:12`): P95 well under 2 seconds
- **Degraded** (`22:13`–`22:27`): P95 well over 2 seconds across 3 consecutive 5-minute windows
- **Recovered** (`22:28`–`22:37`): P95 returns to healthy levels

The response should show `errors: false` for all documents.

:::{note}
The timestamps are fixed to `2026-07-02`, which is in the past. Before running this request, open it in a text editor and replace `2026-07-02` with today's date in `YYYY-MM-DD` format, keeping the time values unchanged. Once you load the data, complete the tutorial within 2 hours to see the full episode lifecycle.

Because the times of day are fixed (`21:57`–`22:37` UTC), the data only looks "recent" once the current UTC time has passed `22:37`. If you load the data before then, the documents are technically timestamped in the future. This doesn't affect the query sandbox in the next section, which uses an absolute time range, but it does affect the rule's lookback window (which is always relative to now) once the rule is running. See the note in **Observe the episode lifecycle** for what this means for the rest of the tutorial.
:::

::::{dropdown} Bulk request: 82 synthetic latency events (healthy → degraded → recovered)
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

:::::

## Create the rule [create-the-rule]

You'll build a rule that detects when P95 latency for a service exceeds 2 seconds. The rule queries the synthetic data you just loaded, so you can see the breach and recovery cycle play out in real time.

:::::{stepper}

::::{step} Open the rule editor

Go to **Alerting v2 preview** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the **Rules** page, select the option to create an {{esql}} rule.

::::

::::{step} Write and test the detection query

1. Paste the following {{esql}} query into the **Query sandbox**. It computes the 95th percentile latency per service, assigns a severity label based on the result, and filters to show only services where P95 exceeds 2 seconds. Each pipe (`|`) passes the output of one step to the next.

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
   You don't need to add a `WHERE @timestamp` clause to this query. Both the query sandbox and the rule executor automatically inject the time-window filter based on the date range you select in the sandbox or the rule's schedule and lookback once it's running.
   :::

2. Set the sandbox date range to the **Today** preset (from the **Commonly used** list) and run the query.

   :::{note}
   Use **Today** rather than a relative preset like **Last 1 hour**. Because the sample data uses fixed times of day, a relative range only includes data once the current time has passed the data's last timestamp (`22:37` UTC, after you substitute today's date). **Today** covers the full calendar day, so it finds the data regardless of what time it is right now.
   :::

3. Confirm the query results. You should see one row for `service.name: checkout` with `p95_latency_ms` above 2000 and `severity: high` or `critical`.

   You can also use the sandbox to preview what recovery looks like. If you narrow the range to a healthy window (before `22:13` or after `22:28`), the row disappears. No rows means no breach, and when a scheduled evaluation returns the same, the episode closes. You'll configure this behavior in the **Recovery Condition** step.

4. Select **Apply changes** to populate the rule form, then select **Next**.

   :::{note}
   The sandbox time controls set the preview range only. They don't carry over to the rule's schedule or lookback window once the rule is running.
   :::

::::

::::{step} Configure the alert condition

The query you applied from the sandbox auto-fills **Mode**, **Time field**, and **Group fields**. Set the remaining fields:

- Set **Alert delay** to **Breaches: 2**. The breach must persist across 2 consecutive evaluations before the episode moves to `active`.
- Set **Schedule** to every `5` minutes.
- Set **Lookback Window** to the last `2` hours. This ensures the rule can reach the pre-loaded sample data regardless of when you complete the tutorial.

   :::{note}
   Unlike the sandbox, the rule's **Lookback Window** is always a relative range (the last 2 hours as of each evaluation). It can't use an absolute range like **Today**. If the current UTC time hasn't yet passed the start of the degraded window (`22:13`, after you substitute today's date), the rule won't see the degraded data until real time catches up. This doesn't block you from continuing the tutorial. You can go ahead and finish configuring and saving the rule. Refer to the note in **Observe the episode lifecycle** for when the episode will actually appear.
   :::

Select **Next**.

::::

::::{step} Configure the recovery condition

Confirm the default settings:

- **Recovery**: `Default recovery`
- **Recovery delay**: `Immediate` (no delay, recovers on first non-breach)

These default settings will produce the automatic recovery behavior this tutorial demonstrates. As soon as a scheduled run returns no breaching rows, the episode will close.

Select **Next**.

::::

::::{step} Name and save the rule

1. On the **Details & Artifacts** step, enter the following:

   - **Name**: Checkout Service Latency
   - **Description**: Detects when P95 latency for the checkout service exceeds 2 seconds. Groups by service name and assigns severity: critical at 4 seconds, high at 2 seconds.

   Select **Next**.

2. On the **Actions** step, do not create an action policy (rules can run without notifications or an action policy configured). Select **Create rule** to create and enable the rule.

::::

:::::

## Confirm the rule is evaluating [confirm-rule-evaluating]

The sandbox showed that your query *can* find a breach. This step confirms the rule is actually running on schedule. The **Execution history** page gives you a real-time log of every rule run and its outcome.

1. Open **Execution history** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

2. On the **Rules** tab, select **Checkout Service Latency**.

3. Wait one schedule interval (5 minutes) after saving the rule, then check the table for a recent entry.

4. Confirm the **Response** shows `success` and the **Timestamp** matches a recent time. If no entries appear, confirm at least one 5-minute interval has elapsed since you saved the rule.

## Observe the episode lifecycle [observe-episode-lifecycle]

With the rule running, you can watch the full alert lifecycle play out on the **Alerts** page and in the episode detail view. The episode opens once the breach persists across consecutive evaluations, stays active while the degraded data is in the lookback window, and closes automatically when no breaching data remains.

Because you set **Alert delay** to 2 consecutive breaches, the episode starts as `pending` and only moves to `active` once the breach persists across a second evaluation. This prevents transient spikes from opening an episode right away.

:::{note}
If your current UTC time hadn't yet passed `22:13` (the start of the degraded window, after you substitute today's date) when you loaded the sample data, no episode will appear here until real time reaches that point. The rule's lookback window only looks backward, so it needs the degraded window to be in the past before it can flag a breach. Once real time passes `22:13`, expect the episode to appear within about 10–15 minutes, after two consecutive evaluations confirm the breach.
:::

1. Open **Alerting v2 preview** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the **Alerts** page.

2. If you have other rules in this cluster, filter by **Rule** to show only episodes for **Checkout Service Latency**. After the first two evaluations (about 10 minutes), you'll see an episode appear and move from `pending` to `active`.

3. Select the episode to open its details page. Use the metric trend to see how P95 latency compared to the threshold over the episode's lifetime, and confirm the grouping value (`checkout`) that triggered it.

4. Wait for the rule's lookback window to advance past the degraded data. Once no breaching rows fall within the 2-hour window, the episode status changes to `inactive` automatically. No manual action is required. This is default recovery in action.

## Key concepts demonstrated [create-rule-key-concepts]

This tutorial put four core concepts into practice:

- **Rules** - The query you wrote runs every 5 minutes and computes P95 latency over a 2-hour lookback window. Each run checks whether the result exceeds 2000 ms. The schedule and lookback you configured determined how often the rule checked and how much history it analyzed each time.
- **Severity tiers** - The `CASE()` expression you wrote classified each breach as `high` or `critical` based on the P95 value. Those labels are stored in `.rule-events` and visible in the episode detail view.
- **Episode lifecycle** - Setting **Alert delay** to **Breaches: 2** meant the episode didn't open on the first breach. You watched it start as `pending` on the Alerts page, then move to `active` after a second consecutive breaching evaluation confirmed the condition wasn't transient.
- **Automatic recovery** - Because you kept the default recovery settings, the episode closed on its own once the degraded data aged out of the lookback window. The rule detected the absence of a breach and moved the episode to `inactive`. 
