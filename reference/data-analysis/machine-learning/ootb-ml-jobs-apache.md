---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-apache.html
---

# Apache {{anomaly-detect}} configurations [ootb-ml-jobs-apache]

These {{anomaly-job}} wizards appear in {{kib}} if you use the Apache integration in {{fleet}} or you use {{filebeat}} to ship access logs from your [Apache](https://httpd.apache.org/) HTTP servers to {{es}}. The jobs assume that you use fields and data types from the Elastic Common Schema (ECS).


## Apache access logs [apache-access-logs]

These {{anomaly-jobs}} find unusual activity in HTTP access logs.

For more details, see the {{dfeed}} and job definitions in [GitHub](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json). Note that these jobs are available in {{kib}} only if data exists that matches the query specified in the [manifest file](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L11).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| low_request_rate_apache | Detects low request rates. | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L215) | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L370) |
| source_ip_request_rate_apache | Detects unusual source IPs - high request rates. | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L176) | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L349) |
| source_ip_url_count_apache | Detects unusual source IPs - high distinct count of URLs. | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L136) | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L328) |
| status_code_rate_apache | Detects unusual status code rates. | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L90) | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L307) |
| visitor_rate_apache | Detects unusual visitor rates. | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L47) | [code](https://github.com/elastic/integrations/blob/main/packages/apache/kibana/ml_module/apache-Logs-ml.json#L260) |


## Apache access logs ({{filebeat}}) [apache-access-logs-filebeat]

These legacy {{anomaly-jobs}} find unusual activity in HTTP access logs. For the latest versions, install the Apache integration in {{fleet}}; see [Apache access logs](ootb-ml-jobs-apache.md#apache-access-logs).

For more details, see the {{dfeed}} and job definitions in [GitHub](https://github.com/elastic/kibana/tree/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml).

These configurations are only available if data exists that matches the recognizer query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/manifest.json#L8).

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| low_request_rate_ecs | Detects low request rates (ECS). | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/low_request_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/datafeed_low_request_rate_ecs.json) |
| source_ip_request_rate_ecs | Detects unusual source IPs - high request rates (ECS). | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/source_ip_request_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/datafeed_source_ip_request_rate_ecs.json) |
| source_ip_url_count_ecs | Detect unusual source IPs - high distinct count of URLs (ECS). | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/source_ip_url_count_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/datafeed_source_ip_url_count_ecs.json) |
| status_code_rate_ecs | Detects unusual status code rates (ECS). | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/status_code_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/datafeed_status_code_rate_ecs.json) |
| visitor_rate_ecs | Detects unusual visitor rates (ECS). | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/visitor_rate_ecs.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apache_ecs/ml/datafeed_visitor_rate_ecs.json) |

