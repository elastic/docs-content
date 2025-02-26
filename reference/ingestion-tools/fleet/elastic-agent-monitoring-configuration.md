---
navigation_title: "Monitoring"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-monitoring-configuration.html
---

# Configure monitoring for standalone {{agent}}s [elastic-agent-monitoring-configuration]


{{agent}} monitors {{beats}} by default. To turn off or change monitoring settings, set options under `agent.monitoring` in the `elastic-agent.yml` file.

This example configures {{agent}} monitoring:

```yaml
agent.monitoring:
  # enabled turns on monitoring of running processes
  enabled: true
  # enables log monitoring
  logs: true
  # enables metrics monitoring
  metrics: true
  # exposes /debug/pprof/ endpoints for Elastic Agent and Beats
  # enable these endpoints if the monitoring endpoint is set to localhost
  pprof.enabled: false
  # specifies output to be used
  use_output: monitoring
  http:
    # exposes a /buffer endpoint that holds a history of recent metrics
    buffer.enabled: false
```

To turn off monitoring, set `agent.monitoring.enabled` to `false`. When set to `false`, {{beats}} monitoring is turned off, and all other options in this section are ignored.

To enable monitoring, set `agent.monitoring.enabled` to `true`. Also set the `logs` and `metrics` settings to control whether logs, metrics, or both are collected. If neither setting is specified, monitoring is turned off. Set `use_output` to specify the output to which monitoring events are sent.

You can also add the setting `agent.monitoring.http.enabled: true` to expose a `/liveness` endpoint. By default, the endpoint returns a `200` OK status as long as {{agent}}'s internal main loop is responsive and can process configuration changes. It can be configured to also monitor the component states and return an error if anything is degraded or has failed.

The `agent.monitoring.pprof.enabled` option controls whether the {{agent}} and {{beats}} expose the `/debug/pprof/` endpoints with the monitoring endpoints. It is set to `false` by default. Data produced by these endpoints can be useful for debugging but present a security risk. It is recommended that this option remains `false` if the monitoring endpoint is accessible over a network.

The `agent.monitoring.http.buffer.enabled` option controls whether the {{agent}} and {{beats}} collect metrics into an in-memory buffer and expose these through a `/buffer` endpoint. It is set to `false` by default. This data can be useful for debugging or if the {{agent}} has issues communicating with {{es}}. Enabling this option may slightly increase process memory usage.

