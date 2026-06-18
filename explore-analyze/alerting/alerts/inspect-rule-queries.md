---
navigation_title: Inspect rule queries
description: Use the rule query inspector to view the Elasticsearch request a rule used, confirm it targeted the right data, and diagnose why alerts were or weren't generated.
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
---

# Inspect rule queries [inspect-rule-queries]

The rule query inspector lets you view the {{es}} request that a rule sent when it evaluated your data. Use it to understand the query structure, confirm the rule targeted the right data, and diagnose why an alert was or wasn't generated.

::::{note}
:applies_to: {"stack": "ga 9.5", "serverless": "ga"}
Currently, the rule query inspector is only available for **custom threshold rules**. 
::::

## Access the inspector [inspect-access]

The inspector is available from two places, each showing a different query:

* **Rule details page**: Open **{{stack-manage-app}}** > **{{rules-ui}}**, find your rule, and click its name to open its details page. Click **Rule query inspector**. The inspector builds the query from the rule's _current_ parameters. Use this view to verify that the rule is configured correctly and would match the data you expect.

* **Alert details page**: Go to the **Alerts** page, then open an individual alert. Click **Rule query inspector**. The inspector uses the rule parameters _as they existed when that specific alert was generated_, including the exact evaluation time range. Use this view to understand why a particular alert was or wasn't triggered.

The key difference is that the rule details page reflects the rule as it is _now_, while the alert details page reflects the rule as it was _then_. If you've edited the rule since an alert was generated, the two inspectors will show different queries.

## What the inspector shows [inspect-tabs]

The inspector displays the {{es}} query made by the rule, the most recent raw response the rule received, and how long the query took to run.

| Element | Description |
| --- | --- |
| **Criterion dropdown** | Appears when a rule has multiple criteria. Each entry is labeled with its criterion number and metric (for example, `Criterion 1: avg(system.cpu.total.norm.pct)`). Selecting a criterion updates both the **Request** and **Response** tabs to show the query and results for that specific condition. |
| **Request** | Shows the full {{es}} query that the rule sends when it evaluates your data. Use it to verify the index pattern, time range, query filter, and aggregations match what you configured in the rule. |
| **Response** | Shows the raw {{es}} response. Use it to confirm whether data was found, whether the groups you expect are present, and what values the rule was working with when it made its alerting decision. |
| **Request time** | Shows how long {{es}} took to execute the query. This measures the query portion of rule execution only. It doesn't include time spent waiting in the task queue or processing actions after the query returns. Use it to identify whether the query itself is the bottleneck when a rule is slow. |

## Factors that affect request time [inspect-request-time-factors]

The request time can be affected by the following factors. When optimizing for performance, verify that any changes don't affect the rule's detection logic, for example, a shorter time window or tighter filter may prevent the rule from catching the conditions it was designed to detect.

| Factor | Why it increases execution time | How to reduce it |
| --- | --- | --- |
| **Index size** | Rules that search indices with more documents take longer to execute. | Add a KQL filter to narrow the documents the rule searches. |
| **Query complexity** | Metric aggregations such as average, rate, or percentile are heavier than a simple count. | Simplify criteria or swap a complex aggregation for a lighter one where possible. |
| **Number of criteria** | Each criterion is a separate {{es}} query. | Reduce the number of criteria in the rule. |
| **Group-by cardinality** | Grouping by a high-cardinality field (such as `host.name` with thousands of hosts) significantly increases query cost. | Choose a lower-cardinality field, or apply a KQL filter to narrow the population before grouping. |
| **Shard count and cluster load** | Query time increases when {{es}} is under heavy load. | This is outside the rule configuration. If high cluster load is consistent, consider reviewing your cluster sizing or spreading rule evaluation across off-peak hours. |
| **Time window size** | A longer window means {{es}} must scan more data. | Shorten the time window in the rule configuration. |

## Using the inspector [inspect-troubleshoot]

Expand the following to learn how the inspector can help.

:::{dropdown} Confirm why an alert was generated
Open the inspector from the alert details page. Review the time range to confirm it matches the evaluation period. Find the aggregation bucket for your group and check the value against the threshold. If the value exceeds the threshold, the alert was generated correctly.
:::

:::{dropdown} Investigate why an alert wasn't generated
Open the inspector from the rule details page and confirm the query targets the right index pattern and time range. Check the query filter for unintended restrictions. If the aggregation values in the response are below the threshold, the rule evaluated correctly but your data didn't breach the threshold during that window.
:::

:::{dropdown} Compare the current rule configuration to a historical alert
If you've modified the rule since the alert was generated, open the inspector from the _alert details page_ rather than the rule details page. The alert inspector uses the parameters that were active at the time the alert was generated, so the query will reflect the older configuration.
:::

:::{dropdown} Identify why the response shows no data
The query matched no documents. Check whether the index pattern in the data view is correct, whether your time range is appropriate, and whether any query filter is too restrictive. Also verify that the data stream or index has data in the expected time period by running the same query in [Discover](/explore-analyze/discover.md) or [Dev Tools](/explore-analyze/query-filter/tools/console.md).
:::

:::{dropdown} Find out why a group is missing from the results
If a group you expected (such as a specific host) doesn't appear in the buckets, no documents for that group matched the query during the evaluation window. This can happen when the group was inactive, when a filter excluded its documents, or when the field used for grouping has a different value in the actual documents than you expected.
:::

:::{dropdown} Diagnose a slow or timing-out rule
Check the request time in the inspector. A high request time means the Elasticsearch query is likely the cause. To reduce it, simplify the query by reducing the number of criteria, shortening the time window, adding a tighter KQL filter, or reducing group-by cardinality. If the rule has multiple criteria, use the dropdown to compare request times across criteria and identify which condition is the most expensive.

If the request time is near zero, the query isn't the bottleneck and the timeout is likely caused by something else, such as task manager queue pressure or scheduling overhead. For broader investigation, including how to identify long-running rules using the event log and how to adjust timeout settings, refer to [Rules take a long time to run](alerting-common-issues.md#rules-long-run-time).
:::
