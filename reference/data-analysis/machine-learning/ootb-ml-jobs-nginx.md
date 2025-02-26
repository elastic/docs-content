---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-nginx.html
---

# Nginx {{anomaly-detect}} configurations [ootb-ml-jobs-nginx]

These {{anomaly-job}} wizards appear in {{kib}} if you use the Nginx integration in {{fleet}} or you use {{filebeat}} to ship access logs from your [Nginx](http://nginx.org/) HTTP servers to {{es}}. The jobs assume that you use fields and data types from the Elastic Common Schema (ECS).


## Nginx access logs [nginx-access-logs]

Find unusual activity in HTTP access logs.

These jobs are available in {{kib}} only if data exists that matches the query specified in the [manifest file](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| low_request_rate_nginx | Detect low request rates | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L215) | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L370) |
| source_ip_request_rate_nginx | Detect unusual source IPs - high request rates | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L176) | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L349) |
| source_ip_url_count_nginx | Detect unusual source IPs - high distinct count of URLs | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L136) | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L328) |
| status_code_rate_nginx | Detect unusual status code rates | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L90) | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L307) |
| visitor_rate_nginx | Detect unusual visitor rates | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L47) | [code](https://github.com/elastic/integrations/blob/main/packages/nginx/kibana/ml_module/nginx-Logs-ml.json#L260) |


## Nginx access logs ({{filebeat}}) [nginx-access-logs-filebeat]

These legacy {{anomaly-jobs}} find unusual activity in HTTP access logs. For the latest versions, install the Nginx integration in {{fleet}}; see [Nginx access logs](ootb-ml-jobs-nginx.md#nginx-access-logs).

These jobs exist in {{kib}} only if data exists that matches the recognizer query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/manifest.json).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| low_request_rate_ecs | Detect low request rates (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/low_request_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/datafeed_low_request_rate_ecs.json) |
| source_ip_request_rate_ecs | Detect unusual source IPs - high request rates (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/source_ip_request_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/datafeed_source_ip_request_rate_ecs.json) |
| source_ip_url_count_ecs | Detect unusual source IPs - high distinct count of URLs (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/source_ip_url_count_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/datafeed_source_ip_url_count_ecs.json) |
| status_code_rate_ecs | Detect unusual status code rates (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/status_code_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/datafeed_status_code_rate_ecs.json) |
| visitor_rate_ecs | Detect unusual visitor rates (ECS) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/visitor_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/nginx_ecs/ml/datafeed_visitor_rate_ecs.json) |

