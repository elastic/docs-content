---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-logs-ui.html
---

# Logs {{anomaly-detect}} configurations [ootb-ml-jobs-logs-ui]

These {{anomaly-jobs}} appear by default in the [{{logs-app}}](/solutions/observability/logs/explore-logs.md) in {{kib}}. For more information about their usage, refer to [Categorize log entries](/solutions/observability/logs/categorize-log-entries.md) and [Inspect log anomalies](/solutions/observability/logs/inspect-log-anomalies.md).


## Log analysis [logs-ui-analysis]

Detect anomalies in log entries via the Logs UI.

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| log_entry_rate | Detects anomalies in the log entry ingestion rate | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/logs_ui_analysis/ml/log_entry_rate.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/logs_ui_analysis/ml/datafeed_log_entry_rate.json) |


## Log entry categories [logs-ui-categories]

Detect anomalies in count of log entries by category.

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| log_entry_categories_count | Detects anomalies in count of log entries by category | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/logs_ui_categories/ml/log_entry_categories_count.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/logs_ui_categories/ml/datafeed_log_entry_categories_count.json) |

