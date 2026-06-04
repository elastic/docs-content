---
navigation_title: Diagnose rule behavior
description: Use the rule query inspector to view the Elasticsearch request behind a rule and diagnose why an alert did or didn't fire.
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
---

# Diagnose rule behavior with the rule query inspector [inspect-rule-queries]

The rule query inspector lets you view the {{es}} request that a rule sends when it evaluates your data. Use it to understand the query structure, confirm the rule is targeting the right data, and diagnose why an alert did or didn't fire.

::::{note}
:applies_to: {"stack": "ga 9.5", "serverless": "ga"}
Currently, the rule query inspector is only available for **custom threshold rules**. 
::::

## Access the inspector [inspect-access]

The inspector is available from two places, each showing a different query:

**From the rule details page (current rule parameters)**
:   Open **{{stack-manage-app}}** > **{{rules-ui}}**, find your rule, and click its name to open the rule details page. Click **Rule query inspector**. The inspector builds the query from the rule's _current_ parameters. Use this view to verify that the rule is configured correctly and would match the data you expect.

**From an alert details page (historical parameters)**
:   Go to the **Alerts** page, then open an individual alert. Click **Rule query inspector**. The inspector uses the rule parameters _as they existed when that specific alert fired_, including the exact evaluation time range. Use this view to understand why a particular alert was or wasn't triggered.

The key difference: the rule details page reflects the rule as it is _now_, while the alert details page reflects the rule as it was _then_. If you've edited the rule since an alert fired, the two inspectors will show different queries.

## What the inspector shows [inspect-tabs]

The inspector has two tabs:

**Request**
:   Shows the full {{es}} query that the rule sends when it evaluates your data. Use it to verify the index pattern, time range, query filter, and aggregations match what you configured in the rule.

**Response**
:   Shows the raw {{es}} response. Use it to confirm whether data was found, whether the groups you expect are present, and what values the rule was working with when it made its alerting decision.

## Common troubleshooting scenarios [inspect-troubleshoot]

:::{dropdown} Alert fired but I don't know why
Open the inspector from the alert details page. Review the time range to confirm it matches the evaluation period. Find the aggregation bucket for your group and check the value against the threshold. If the value exceeds the threshold, the alert fired correctly.
:::

:::{dropdown} Alert didn't fire when I expected it to
Open the inspector from the rule details page and confirm the query targets the right index pattern and time range. Check the query filter for unintended restrictions. If the aggregation values in the response are below the threshold, the rule evaluated correctly but your data didn't breach the threshold during that window.
:::

:::{dropdown} Rule looks correct now but the alert used different parameters
If you've modified the rule since the alert fired, open the inspector from the _alert details page_ rather than the rule details page. The alert inspector uses the parameters that were active at the time the alert fired, so the query will reflect the older configuration.
:::

:::{dropdown} Empty or null aggregation values
The query matched no documents. Check whether the index pattern in the data view is correct, whether your time range is appropriate, and whether any query filter is too restrictive. Also verify that the data stream or index has data in the expected time period by running the same query in [Discover](/explore-analyze/discover.md) or [Dev Tools](/explore-analyze/query-filter/tools/console.md).
:::

:::{dropdown} Unexpected group missing from results
If a group you expected (such as a specific host) doesn't appear in the buckets, no documents for that group matched the query during the evaluation window. This can happen when the group was inactive, when a filter excluded its documents, or when the field used for grouping has a different value in the actual documents than you expected.
:::
