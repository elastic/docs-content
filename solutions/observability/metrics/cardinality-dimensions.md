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

High cardinality, meaning a large number of unique label or dimension combinations, is a common cause of unexpected storage growth and query slowness in metrics systems.

## What is cardinality in this context [metrics-cardinality-what]

In the context of {{product.observability}}, cardinality refers to the number of unique combinations of dimension fields (labels) on a metric. For example, a metric with three labels (like )`host`, `region`, and `status_code`) can generate up to `hosts × regions × status_codes` unique time series. As cardinality grows, so does storage consumption and query cost.

TSDS manages cardinality differently from regular data streams by tracking dimension combinations explicitly, which makes high-cardinality data more efficient to store but also more visible when it becomes a problem.

## Related [metrics-cardinality-related]

- [Manage metrics storage](/solutions/observability/metrics/manage-storage.md)
- [Time Series Data Streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
