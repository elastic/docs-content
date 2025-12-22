---
navigation_title: "Downsampling"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Downsampling a time series data stream [downsampling]

Downsampling reduces the footprint of your [time series data](time-series-data-stream-tsds.md) by storing it at reduced granularity.

Metrics tools and solutions collect large amounts of time series data over time. As the data ages, it becomes less relevant to the current state of the system. You can _downsample_ older data to reduce its resolution and precision, freeing up storage space.

This section explains the available downsampling options and helps you understand the process.

* [](downsampling-concepts.md)
* [](run-downsampling.md)