---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-uptime.html
---

# Uptime {{anomaly-detect}} configurations [ootb-ml-jobs-uptime]

If you have appropriate {{heartbeat}} data in {{es}}, you can enable this {{anomaly-job}} in the [{{uptime-app}}](/solutions/observability/apps/synthetic-monitoring.md#monitoring-uptime) in {{kib}}. For more usage information, refer to [Inspect uptime duration anomalies](/solutions/observability/apps/inspect-uptime-duration-anomalies.md).


## Uptime: {{heartbeat}} [uptime-heartbeat]

Detect latency issues in heartbeat monitors.

These configurations are available in {{kib}} only if data exists that matches the recognizer query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/uptime_heartbeat/manifest.json).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| high_latency_by_geo | Identify periods of increased latency across geographical regions | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/uptime_heartbeat/ml/high_latency_by_geo.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/uptime_heartbeat/ml/datafeed_high_latency_by_geo.json) |

