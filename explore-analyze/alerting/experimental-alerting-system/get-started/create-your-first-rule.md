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
5. **Watch the episode open and recover** - Open the alert episode's details page to watch the episode move from `pending` to `active` as the breach persists, then trigger the recovery condition directly to see it close.

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

Run the following in **Dev Tools** to create the index that your rule will query. This index requires explicit creation because it uses a custom mapping.

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

Expand the drop-down below to copy the full bulk request, then run it in Dev Tools. It populates the index with synthetic latency data for a `checkout` service covering three phases, all within a single hour:

- **Healthy** (`:00`–`:15`): P95 well under 2 seconds
- **Degraded** (`:16`–`:30`): P95 well over 2 seconds across 3 consecutive 5-minute windows
- **Recovered** (`:31`–`:40`): P95 returns to healthy levels

The response should show `errors: false` for all documents.

:::{note}
The timestamps are fixed to `2026-07-02T21`. Before running this request, replace `2026-07-02T21` with today's date and the current UTC hour in `YYYY-MM-DDTHH` format (for example, `2026-07-14T09`), keeping the minutes and seconds unchanged.

The rule can only see data that's already in the past, so each phase won't appear until real time reaches its minute mark.
:::

::::{dropdown} Bulk request: 82 synthetic latency events (healthy → degraded → recovered)
```json
POST checkout-service-logs/_bulk
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:00:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":468}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:00:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":336}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:01:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":367}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:01:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":372}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:02:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":497}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:02:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":305}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:03:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":384}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:03:31.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":406}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:04:01.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":427}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:04:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":461}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:05:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":448}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:05:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":527}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:06:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":272}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:06:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":477}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:07:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":355}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:07:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":466}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:08:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":528}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:08:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":280}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:09:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":278}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:09:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":252}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:10:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":443}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:10:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":447}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:11:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":504}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:11:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":260}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:12:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":353}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:12:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":508}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:13:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":381}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:13:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":315}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:14:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":284}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:14:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":261}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:15:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":371}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:15:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":329}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:16:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2704}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:16:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2909}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:17:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2898}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:17:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3094}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:18:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3701}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:18:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3977}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:19:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2368}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:19:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3954}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:20:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2610}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:20:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2491}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:21:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3751}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:21:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3909}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:22:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3903}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:22:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3905}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:23:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2292}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:23:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4429}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:24:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4147}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:24:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2462}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:25:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2733}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:25:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2869}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:26:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4323}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:26:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3802}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:27:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3105}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:27:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2335}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:28:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3649}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:28:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":4320}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:29:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2671}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:29:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3438}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:30:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":2251}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:30:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":3235}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:31:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":525}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:31:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":458}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:32:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":448}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:32:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":453}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:33:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":435}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:33:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":463}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:34:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":319}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:34:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":421}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:35:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":353}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:35:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":378}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:36:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":369}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:36:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":490}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:37:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":284}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:37:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":359}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:38:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":468}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:38:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":292}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:39:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":427}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:39:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":423}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:40:02.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":259}
{"index":{"_index":"checkout-service-logs"}}
{"@timestamp":"2026-07-02T21:40:32.000Z","service.name":"checkout","transaction.name":"POST /checkout","latency_ms":309}
```
::::

::::

:::::

## Create the rule [create-the-rule]

You'll build a rule that detects when P95 latency for a service exceeds 2 seconds. The rule queries the synthetic data you just loaded, so you can see the breach and recovery cycle play out in real time.

:::::{stepper}

::::{step} Open the rule form

Go to **Rules** (**Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md) > **Rules**), create a new rule, then select **Create ES|QL rule** to open the rule authoring flyout.

::::

::::{step} Write and test the detection query

1. Paste the following {{esql}} query into the **Query sandbox**. It finds the slowest 5% of requests for each service (P95 latency), labels how severe that is, and keeps only the services where that value is above 2 seconds. You don't need to add a time filter yourself. The sandbox and the rule both apply one automatically based on the date range or schedule you choose.

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

2. Set the sandbox date range to the **Today** preset (from the **Commonly used** list) and run the query. **Today** covers the full calendar day, so it finds the sample data no matter what time it is right now.

3. Confirm the query results. You should see one row for `service.name: checkout` with `p95_latency_ms` above 2000 and `severity: high` or `critical`.

4. Select **Apply changes** to populate the rule form, then select **Next**.

   :::{note}
   The sandbox time controls set the preview range only. They don't carry over to the rule's schedule or lookback window once the rule is running.
   :::

::::

::::{step} Configure the alert condition

The query you applied from the sandbox auto-fills **Mode**, **Time field**, and **Group fields**. Set the remaining fields:

- **Alert delay**: `Breaches: 2` (The breach must persist across 2 consecutive evaluations before the episode moves to `active`.)
- **Schedule**: `Every 5 minutes`
- **Lookback Window**: `Last 45 minutes` (Ensures the rule can reach the pre-loaded sample data regardless of when you complete the tutorial.)

Select **Next**.

::::

::::{step} Configure the recovery condition

Confirm the default settings:

- **Recovery**: `Default recovery`
- **Recovery delay**: `Immediate` (no delay, recovers on first non-breach)

These default settings will produce the automatic recovery behavior this tutorial demonstrates. As soon as a scheduled run finds that the service's P95 latency is back under the 2-second threshold, the episode will close.

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

:::::{stepper}

::::{step} Open Execution history

Open **Execution history** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::

::::{step} Select the rule

On the **Rules** tab, select **Checkout Service Latency**.

::::

::::{step} Wait for an execution

Wait one schedule interval (5 minutes) after saving the rule, then check the table for a recent entry.

::::

::::{step} Confirm success

Confirm the **Response** column shows `success` and the **Timestamp** matches a recent time. If no entries appear, confirm at least one 5-minute interval has elapsed since you saved the rule.

::::

:::::

## Observe the episode lifecycle [observe-episode-lifecycle]

With the rule running, you can watch the full alert lifecycle play out on the **Alerts** page and in the episode's details page. It stays active until the recovery condition is met.

:::::{stepper}

::::{step} Open the Alerts page

Open **Alerting v2 preview** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the **Alerts** page.

::::

::::{step} Find the episode

The episode won't appear until the current UTC time passes 16 minutes past the hour, which is the start of the degraded window. After the first two evaluations following that point (about 10 minutes), you'll see an episode appear and move from `pending` to `active`.

::::

::::{step} Inspect the episode details

Select the episode to open its details. Use the metric trend to see how P95 latency compared to the threshold over the episode's lifetime, and confirm the grouping value (`checkout`) that triggered it.

::::

::::{step} Force recovery

Run the following in **Dev Tools** to rewrite the degraded documents' `latency_ms` values to a healthy level. This triggers the rule's recovery condition directly, so you see the episode close because the condition resolved.

```json
POST checkout-service-logs/_update_by_query
{
  "query": {
    "range": { "latency_ms": { "gt": 2000 } }
  },
  "script": {
    "source": "ctx._source.latency_ms = 300"
  }
}
```

Wait for the next scheduled run (within 5 minutes), then go to the **Alerts** page and open the episode's details again to confirm it moved to `inactive`.

::::

:::::

## Key concepts demonstrated [create-rule-key-concepts]

By completing this tutorial, you learned:

- **Rules** - A rule's schedule and lookback window control how often it evaluates and how much history each evaluation considers.
- **Severity tiers** - An {{esql}} `CASE()` expression can classify each breach by severity, and those labels are recorded in `.rule-events` and shown on the episode's details page.
- **Episode lifecycle** - **Alert delay** requires a breach to persist across consecutive evaluations before an episode opens, so transient spikes don't trigger it.
- **Automatic recovery** - With default recovery, an episode closes as soon as a scheduled run finds the alert condition is no longer met, which is exactly what happened right after rewriting the latency values.
