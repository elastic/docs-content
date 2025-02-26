---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-metricbeat.html
---

# {{metricbeat}} {{anomaly-detect}} configurations [ootb-ml-jobs-metricbeat]

These {{anomaly-job}} wizards appear in {{kib}} if you use the [{{metricbeat}} system module](beats://docs/reference/metricbeat/metricbeat-module-system.md) to monitor your servers. For more details, see the {{dfeed}} and job definitions in GitHub.


## {{metricbeat}} system [metricbeat-system-ecs]

Detect anomalies in {{metricbeat}} System data (ECS).

These configurations are only available if data exists that matches the recognizer query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/manifest.json#L8).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| high_mean_cpu_iowait_ecs | Detect unusual increases in cpu time spent in iowait (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/high_mean_cpu_iowait_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/datafeed_high_mean_cpu_iowait_ecs.json) |
| max_disk_utilization_ecs | Detect unusual increases in disk utilization (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/max_disk_utilization_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/datafeed_max_disk_utilization_ecs.json) |
| metricbeat_outages_ecs | Detect unusual decreases in metricbeat documents (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/metricbeat_outages_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metricbeat_system_ecs/ml/datafeed_metricbeat_outages_ecs.json) |

