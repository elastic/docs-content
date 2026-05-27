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

## Anatomy of the query [inspect-query-anatomy]

The following sections describe the query structure for **custom threshold rules**. As support for additional rule types is added, this reference will expand.

The inspector displays the full {{es}} request. Each part of the query maps to a setting in your rule configuration.

### Index and time range [inspect-anatomy-index-time]

The top-level index and `range` filter reflect your rule's data source and time window:

```json
{
  "index": ["<your-data-view-index-pattern>"],
  "body": {
    "query": {
      "bool": {
        "filter": [
          {
            "range": {
              "@timestamp": {           <1>
                "gte": "...",           <2>
                "lte": "..."            <3>
              }
            }
          }
        ]
      }
    }
  }
}
```

1. The time field from your data view.
2. The start of the evaluation window (`now` minus your rule's **time window** setting).
3. The end of the evaluation window. From an alert details page, this matches the exact moment the alert was evaluated, not the current time.

If the time range looks unexpected from an alert details page, this confirms the exact window {{es}} searched when the alert fired. This can help explain alerts that seem outdated or cover an unexpected period.

### Query filter [inspect-anatomy-query-filter]

If you set a **query filter** on the rule, it appears as an additional clause in the `bool` filter:

```json
{
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { ... } } },
        { "query_string": { "query": "host.name: host-1" } }   <1>
      ]
    }
  }
}
```

1. The KQL query filter you set on the rule, translated to a `query_string` or `term` clause. If this filter excludes more data than expected, the rule won't find the documents you intended.

If the filter is missing or different from what you set, double-check the rule configuration.

### Aggregations [inspect-anatomy-aggregations]

Each criterion you defined in the rule becomes an aggregation in the query. A rule with two criteria (for example, Aggregation A and Aggregation B) produces two sub-aggregations:

```json
{
  "aggs": {
    "A": {                                     <1>
      "avg": { "field": "system.cpu.user.pct" }
    },
    "B": {
      "avg": { "field": "system.cpu.system.pct" }
    }
  }
}
```

1. The letter label matches the criterion label shown in the rule configuration (**A**, **B**, and so on).

| Rule criterion | Aggregation in query |
| --- | --- |
| **Average** of a field | `avg` |
| **Max** of a field | `max` |
| **Min** of a field | `min` |
| **Sum** of a field | `sum` |
| **Count** (all docs) | `value_count` or `filter` + `value_count` |
| **Cardinality** of a field | `cardinality` |
| **95th percentile** of a field | `percentiles` with `{ "percents": [95] }` |
| **Rate** of a field | Two `max` aggregations plus a bucket script |

If you set a **KQL filter** on a criterion ({applies_to}`stack: ga 9.4+`), it appears as a `filter` aggregation wrapping the metric aggregation.

### Group-by fields [inspect-anatomy-group-by]

If your rule uses **Group alerts by**, the aggregations are wrapped in a `composite` aggregation that partitions results by those fields:

```json
{
  "aggs": {
    "groupBy": {
      "composite": {
        "sources": [
          { "host.name": { "terms": { "field": "host.name" } } }   <1>
        ],
        "size": 10000
      },
      "aggs": {
        "A": { "avg": { "field": "system.cpu.user.pct" } }
      }
    }
  }
}
```

1. One entry per **Group alerts by** field. Multiple group-by fields produce multiple `sources`.

Without group-by, the aggregations run over all matched documents and return a single value.

## Reading the response [inspect-response]

The inspector also shows the Elasticsearch response alongside the request. Match each aggregation bucket back to your rule configuration to understand what value was computed.

### No group-by: single-value response [inspect-response-no-group]

When there are no group-by fields, the response contains a single set of aggregation values under `aggregations`:

```json
{
  "aggregations": {
    "A": { "value": 0.82 },      <1>
    "B": { "value": 0.15 }
  }
}
```

1. Aggregation `A` returned `0.82`. If your rule equation is `(A + B) / C * 100` with threshold `IS ABOVE 95`, you'd compute the equation value with these numbers to confirm whether the threshold was met.

If the response value is below the threshold and no alert fired, this confirms the rule evaluated correctly. If you _expected_ an alert and the value is below the threshold, review your aggregations and KQL filters.

### With group-by: bucketed response [inspect-response-group]

When group-by fields are used, the response returns one bucket per group under `aggregations.groupBy.buckets`:

```json
{
  "aggregations": {
    "groupBy": {
      "buckets": [
        {
          "key": { "host.name": "host-1" },
          "doc_count": 342,
          "A": { "value": 0.97 }       <1>
        },
        {
          "key": { "host.name": "host-2" },
          "doc_count": 58,
          "A": { "value": 0.42 }       <2>
        }
      ]
    }
  }
}
```

1. `host-1` had a value of `0.97`. If the threshold is `IS ABOVE 0.95`, this group breached it and an alert should have fired for `host-1`.
2. `host-2` had a value of `0.42` — below the threshold, so no alert fired for this group.

If a group you expected to appear is missing from the buckets, it had no matching documents during the evaluation window. This can happen when `doc_count` is 0 or when the query filter excluded all documents for that group.

### What a "no data" response looks like [inspect-response-no-data]

If {{es}} returned no documents, the aggregation values will be `null` or the buckets array will be empty:

```json
{
  "aggregations": {
    "A": { "value": null }
  }
}
```

A `null` value means no data matched the query during the evaluation window. If you have **no data** alerts configured, this is the state that triggers them. Check the time range and query filter to confirm no documents were genuinely present, or investigate whether an index or data view configuration issue is preventing data from being found.

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
