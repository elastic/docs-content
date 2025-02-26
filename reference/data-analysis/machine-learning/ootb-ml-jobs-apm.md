---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-apm.html
---

# APM {{anomaly-detect}} configurations [ootb-ml-jobs-apm]

This {{anomaly-job}} appears in the {{apm-app}} and the {{ml-app}} app when you have data from APM Agents or an APM Server in your cluster. It is available only if data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/apm_transaction/manifest.json).

For more information about {{anomaly-detect}} in the {{apm-app}}, refer to [{{ml-cap}} integration](/solutions/observability/apps/integrate-with-machine-learning.md).


## Transactions [apm-transaction-jobs]

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| apm_tx_metrics | Detects anomalies in transaction latency, throughput and error percentage for metric data. | [code](https://github.com/elastic/kibana/blob/main/x-pack/plugins/ml/server/models/data_recognizer/modules/apm_transaction/ml/apm_tx_metrics.json) | [code](https://github.com/elastic/kibana/blob/main/x-pack/plugins/ml/server/models/data_recognizer/modules/apm_transaction/ml/datafeed_apm_tx_metrics.json) |

