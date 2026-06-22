---
navigation_title: Troubleshoot rule behavior
applies_to:
  stack: ga 9.5
  serverless: ga
description: Use the rule query inspector to view the Elasticsearch query a rule ran, confirm it targeted the right data, and diagnose why a rule ran or didn't run.
---

# Troubleshoot rule behavior with the rule query inspector [troubleshoot-rule-behavior]

The rule query inspector gives you direct visibility into the {{es}} queries that your rules run. When a rule fires unexpectedly, stays silent, or runs slowly, use the inspector to see exactly what query ran and what data it returned.

The inspector is available from two places: the rule details page and the alert details page. From the rule details page, you can find out how the rule is configured _now_. From the alert details page, you can find out how the rule was configured _when a specific alert was generated_. If you've modified a rule, the two views may show different queries.

## Supported rule types [inspect-supported-rule-types]

Currently, the rule query inspector is only available for [custom threshold rules](/solutions/observability/incident-management/create-custom-threshold-rule.md).

## Access the inspector [inspect-access]

* **Rule details page**: Open **{{stack-manage-app}}** > **{{rules-ui}}**, find your rule, and click its name to open its details page. Click **Rule query inspector**. The inspector builds the query from the rule's _current_ parameters. Use this view to verify that the rule is configured correctly and would match the data you expect.

* **Alert details page**: Go to the **Alerts** page, then open an individual alert. Click **Rule query inspector**. The inspector uses the rule parameters _as they existed when that specific alert was generated_, including the exact evaluation time range. Use this view to understand why a particular alert was triggered.

## What the inspector shows [inspect-tabs]

The inspector displays the {{es}} query made by the rule, the most recent raw response the rule received, and how long the query took to run.

| Element | Description |
| --- | --- |
| **Criterion dropdown** | Appears when a rule has multiple criteria. Each entry is labeled with its criterion number and metric (for example, `Criterion 1: avg(system.cpu.total.norm.pct)`). Selecting a criterion updates both the **Request** and **Response** tabs to show the query and results for that specific condition. |
| **Request** | Shows the full {{es}} query that the rule sends when it evaluates your data. Use it to verify the index pattern, time range, query filter, and aggregations match what you configured in the rule. |
| **Response** | Shows the raw {{es}} response. Use it to confirm whether data was found, whether the groups you expect are present, and what values the rule was working with when it made its alerting decision. |
| **Request time** | Shows how long {{es}} took to execute the query. This measures the query portion of rule execution only. It doesn't include time spent waiting in the task queue or processing actions after the query returns. Use it to identify whether the query itself is the bottleneck when a rule is slow. |

## Using the inspector [inspect-troubleshoot]

Expand the following to learn how the inspector can help.

:::{dropdown} Confirm why an alert was generated
Open the inspector from the alert details page. Review the time range to confirm it matches the evaluation period. Check the response to confirm the results met the rule's conditions during that window. If they did, the alert was correctly generated.
:::

:::{dropdown} Investigate why a rule didn't run
Open the inspector from the rule details page and confirm the query targets the right index pattern and time range. Also check the query filter for uncessary restrictions. If the response returns data but the results don't meet the rule's conditions, the rule evaluated your data correctly but didn't generate an alert because the rule's conditions were not satisfied during that evaluation window.
:::

:::{dropdown} Compare the current rule configuration to a historical alert
If you've modified the rule since the alert was generated, open the inspector from the _alert details page_ rather than the rule details page. The alert inspector uses the parameters that were active at the time the alert was generated, so the query will reflect the older configuration.
:::

:::{dropdown} Find out why a rule's query returns no results
The query matched no documents. Check whether the index pattern in the data view is correct, whether your time range is appropriate, and whether any query filter is too restrictive. Also verify that the data stream or index has data in the expected time period by running the same query in [Discover](/explore-analyze/discover.md) or [Dev Tools](/explore-analyze/query-filter/tools/console.md).
:::

:::{dropdown} Find out why a rule isn't detecting a specific group
If a group you expected (such as a specific host) doesn't appear in the buckets, no documents for that group matched the query during the evaluation window. This can happen when the group was inactive, when a filter excluded its documents, or when the field used for grouping has a different value in the actual documents than you expected.
:::

:::{dropdown} Find out why a rule is slow or times out
Check the request time in the inspector. A high request time indicates that the {{es}} query is the likely bottleneck. To reduce query execution time, shorten the evaluation time window, add a KQL filter to reduce the number of documents scanned, or group by a lower-cardinality field. If the rule has multiple conditions, use the criterion dropdown to compare request times across conditions and identify which one takes the longest to execute.

If the request time is near zero, the query isn't the bottleneck. The rule may be waiting too long before it starts running, which can happen when {{kib}} is handling too many rules or tasks at the same time. For broader investigation, including how to identify long-running rules using the event log and how to adjust timeout settings, refer to [Rules take a long time to run](alerting-common-issues.md#rules-long-run-time).
:::
