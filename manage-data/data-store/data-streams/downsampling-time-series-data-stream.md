---
navigation_title: "Downsample a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsample a time series data stream [downsampling]

:::{admonition} Page status
🟢 Ready for review
:::

Downsampling reduces the footprint of your [time series data](time-series-data-stream-tsds.md) by storing it at reduced granularity.

Metrics tools and solutions collect large amounts of time series data over time. As the data ages, it becomes less relevant to the current state of the system. _Downsampling_ lets you reduce the resolution and precision of older data, in exchange for decreased storage space.

The downsampling process rolls up documents within a fixed time interval into a single summary document. Each summary document includes statistical representations of the original data: the `min`, `max`, `sum`, and `value_count` for each metric. Data stream [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension) are stored as is, with no changes.

:::{tip}
You can include downsampling in an [{{ilm}} ({{ilm-init}})](../../lifecycle/index-lifecycle-management.md) policy to automatically manage the volume and associated cost of your metrics data at it ages.
:::

This section explains the available downsampling options and helps you understand the process.

% TODO add subsection links and conceptual links after restructuring

## Next steps
% TODO confirm patterns

* [](downsampling-concepts.md)
* [](run-downsampling.md)