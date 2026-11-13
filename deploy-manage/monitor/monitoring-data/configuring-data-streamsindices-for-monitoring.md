---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-indices.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Configuring stack monitoring data streams and indices

Monitoring data is stored in data streams or indices in {{es}}. The default data stream or index settings may not work for your situation. For example, you might want to change index lifecycle management (ILM) settings, add custom mappings, or change the number of shards and replicas. The steps to change these settings depend on the monitoring method:

* {applies_to}`self: ga` [](config-monitoring-data-streams-elastic-agent.md)
* [](config-monitoring-data-streams-metricbeat.md)
* {applies_to}`self: deprecated 7.16, removed 10.0` [](config-monitoring-indices-internal-collection.md)

::::{important} 
Changing mappings or settings can cause your monitoring dashboards to stop working correctly.
::::
