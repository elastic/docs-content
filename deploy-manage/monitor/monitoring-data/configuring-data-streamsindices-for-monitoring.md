---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-indices.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# Configuring data streams/indices for monitoring [config-monitoring-indices]

Monitoring data is stored in data streams or indices in {{es}}. The default data stream or index settings may not work for your situation. For example, you might want to change index lifecycle management (ILM) settings, add custom mappings, or change the number of shards and replicas. The steps to change these settings depend on the monitoring method:

* [Configuring data streams created by {{agent}}](config-monitoring-data-streams-elastic-agent.md)
* [Configuring data streams created by {{metricbeat}} 8](config-monitoring-data-streams-metricbeat-8.md) (the default for version 8 {{ech}} deployments on {{ecloud}})
* [Configuring indices created by {{metricbeat}} 7 or internal collection](config-monitoring-indices-metricbeat-7-internal-collection.md)

::::{important} 
Changing mappings or settings can cause your monitoring dashboards to stop working correctly.
::::





