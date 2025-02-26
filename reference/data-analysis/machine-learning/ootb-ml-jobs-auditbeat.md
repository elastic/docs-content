---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-auditbeat.html
---

# {{auditbeat}} {{anomaly-detect}} configurations [ootb-ml-jobs-auditbeat]

These {{anomaly-job}} wizards appear in {{kib}} if you use [{{auditbeat}}](beats://docs/reference/auditbeat/auditbeat.md) to audit process activity on your systems. For more details, see the {{dfeed}} and job definitions in GitHub.


## Auditbeat docker processes [auditbeat-process-docker-ecs]

Detect unusual processes in docker containers from auditd data (ECS).

These configurations are only available if data exists that matches the recognizer query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/auditbeat_process_docker_ecs/manifest.json#L8).

| Name | Description | Job (JSON)| Datafeed |
| --- | --- | --- | --- |
| docker_high_count_process_events_ecs | Detect unusual increases in process execution rates in docker containers (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/auditbeat_process_docker_ecs/ml/docker_high_count_process_events_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/auditbeat_process_docker_ecs/ml/datafeed_docker_high_count_process_events_ecs.json) |
| docker_rare_process_activity_ecs | Detect rare process executions in docker containers (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/auditbeat_process_docker_ecs/ml/docker_rare_process_activity_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/auditbeat_process_docker_ecs/ml/datafeed_docker_rare_process_activity_ecs.json) |

