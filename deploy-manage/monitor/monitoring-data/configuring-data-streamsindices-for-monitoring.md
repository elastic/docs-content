---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-indices.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Configuring monitoring data streams and indices [config-monitoring-indices]

Monitoring data is stored in data streams or indices in {{es}}. The default data stream or index settings may not work for your situation. For example, you might want to change index lifecycle management (ILM) settings, add custom mappings, or change the number of shards and replicas. The steps to change these settings depend on the monitoring method:

* [Configuring data streams created by {{agent}}](config-monitoring-data-streams-elastic-agent.md)
* [Configuring data streams created by {{metricbeat}}](config-monitoring-data-streams-metricbeat.md)
* {applies_to}`self: deprecated 7.16, removed 10.0` [Configuring indices created by internal collection](config-monitoring-indices-internal-collection.md)

::::{important} 
Changing mappings or settings can cause your monitoring dashboards to stop working correctly.
::::
