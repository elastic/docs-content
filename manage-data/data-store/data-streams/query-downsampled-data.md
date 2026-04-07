---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Querying"
products:
  - id: elasticsearch
---

# Querying downsampled data [querying-downsampled-indices]

To query a downsampled index, use the [`_query`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-esql-query) endpoint. The [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [`_async_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) endpoints are also supported but not optimized for time series processing.

## {{esql}} `TS` command
```{applies_to}
stack: preview 9.2-9.3, ga 9.4+
```

You can use the {{esql}} [`TS` command](elasticsearch://reference/query-languages/esql/commands/ts.md) to query time series data streams. The `TS` command is optimized for processing time series data efficiently and enables the use of time series [aggregation functions](elasticsearch://reference/query-languages/esql/functions-operators/time-series-aggregation-functions.md) with window support.

## _search aggregations

* You can query multiple raw data and downsampled indices in a single request, and a single request can include downsampled indices with multiple downsampling intervals (for example, `15m`, `1h`, `1d`).
* When you run queries in {{kib}} and through Elastic solutions, a standard response is returned, with no indication that some of the queried indices are downsampled.
* [Date histogram aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md) support `fixed_intervals` only (not calendar-aware intervals).
* Time-based histogram aggregations use a uniform bucket size, without regard to the downsampling time interval specified in the request.

## Time zone offsets

Date histograms are based on UTC values. Some time zone situations require offsetting (shifting the time buckets) when downsampling:
     
* For time zone `+5:30` (India), offset by 30 minutes -- for example, `2020-01-01T10:30:00.000` instead of `2020-03-07T10:00:00.000`. Or use a downsampling interval of 15 minutes instead of offsetting.
* For intervals based on days rather than hours, adjust the buckets to the appropriate time zone -- for example, `2020-03-07T19:00:00.000` instead of `2020-03-07T00:00:00.000` for `America/New_York`. 

When offsetting is applied, responses include the field `downsampled_results_offset: true`.

For more details, refer to [Date histogram aggregation: Time zone](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md#datehistogram-aggregation-time-zone).

