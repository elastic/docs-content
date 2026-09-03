---
navigation_title: Cardinality and dimensions
description: Understand and manage high-cardinality metrics in Elastic, including TSDS dimension limits and mitigation strategies.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Cardinality and dimensions in Elastic metrics [metrics-cardinality-dimensions]

:::{note}
This page is a stub. Detailed cardinality guidance is coming soon.
:::

High cardinality — a large number of unique label or dimension combinations — is a common cause of unexpected storage growth and query slowness in metrics systems. This page will cover how cardinality works in Elastic's TSDS storage model, how to identify high-cardinality metrics, and strategies to reduce cardinality without losing signal.

## What is cardinality in this context [metrics-cardinality-what]

In Elastic, cardinality refers to the number of unique combinations of dimension fields (labels) on a metric. For example, a metric with three labels — `host`, `region`, and `status_code` — can generate up to `hosts × regions × status_codes` unique time series. As cardinality grows, so does storage consumption and query cost.

TSDS manages cardinality differently from regular data streams by tracking dimension combinations explicitly, which makes high-cardinality data more efficient to store but also more visible when it becomes a problem.

## Related [metrics-cardinality-related]

- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
- [Time Series Data Streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
