---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rollup-agg-limitations.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---

# Rollup aggregation limitations [rollup-agg-limitations]

::::{admonition} Deprecated in 8.11.0.
:class: warning

Rollups will be removed in a future version. [Migrate](migrating-from-rollup-to-downsampling.md) to [downsampling](../../data-store/data-streams/downsampling-time-series-data-stream.md) instead.
::::


There are some limitations to how fields can be rolled up / aggregated. This page highlights the major limitations so that you are aware of them.


## Limited aggregation components [_limited_aggregation_components] 

The Rollup functionality allows fields to be grouped with the following aggregations:

* Date Histogram aggregation
* Histogram aggregation
* Terms aggregation

And the following metrics are allowed to be specified for numeric fields:

* Min aggregation
* Max aggregation
* Sum aggregation
* Average aggregation
* Value Count aggregation

