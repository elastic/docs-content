---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-metrics-ui.html
---

# Metrics {{anomaly-detect}} configurations [ootb-ml-jobs-metrics-ui]

These {{anomaly-jobs}} can be created in the [{{infrastructure-app}}](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) in {{kib}}. For more information about their usage, refer to [Inspect metric anomalies](/solutions/observability/infra-and-hosts/detect-metric-anomalies.md).


## Metrics hosts [metrics-ui-hosts]

Detect anomalous memory and network behavior on hosts.

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| hosts_memory_usage | Identify unusual spikes in memory usage across hosts. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/hosts_memory_usage.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/datafeed_hosts_memory_usage.json) |
| hosts_network_in | Identify unusual spikes in inbound traffic across hosts. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/hosts_network_in.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/datafeed_hosts_network_in.json) |
| hosts_network_out | Identify unusual spikes in outbound traffic across hosts. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/hosts_network_out.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_hosts/ml/datafeed_hosts_network_out.json) |


## Metrics Kubernetes [metrics-ui-k8s]

Detect anomalous memory and network behavior on Kubernetes pods.

| Name | Description | Job (JSON) | Datafeed |
| --- | --- | --- | --- |
| k8s_memory_usage | Identify unusual spikes in memory usage across Kubernetes pods. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/k8s_memory_usage.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/datafeed_k8s_memory_usage.json) |
| k8s_network_in | Identify unusual spikes in inbound traffic across Kubernetes pods. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/k8s_network_in.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/datafeed_k8s_network_in.json) |
| k8s_network_out | Identify unusual spikes in outbound traffic across Kubernetes pods. | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/k8s_network_out.json) | [code](https://github.com/elastic/kibana/blob/master/x-pack/plugins/ml/server/models/data_recognizer/modules/metrics_ui_k8s/ml/datafeed_k8s_network_out.json) |

