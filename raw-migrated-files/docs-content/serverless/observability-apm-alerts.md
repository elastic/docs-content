---
navigation_title: "Create rules and alerts"
---

# Create APM rules and alerts [observability-apm-alerts]


The Applications UI allows you to define **rules** to detect complex conditions within your APM data and trigger built-in **actions** when those conditions are met.


## APM rules [_apm_rules] 

The following APM rules are supported:

|     |     |
| --- | --- |
| **APM Anomaly** | Alert when either the latency, throughput, or failed transaction rate of a service is anomalous.Anomaly rules can be set at the environment level, service level, and/or transaction type level. Read more in [APM Anomaly rule →](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md) |
| **Error count threshold** | Alert when the number of errors in a service exceeds a defined threshold. Error count rules can be set at theenvironment level, service level, and error group level. Read more in [Error count threshold rule →](../../../solutions/observability/incident-management/create-an-error-count-threshold-rule.md) |
| **Failed transaction rate threshold** | Alert when the rate of transaction errors in a service exceeds a defined threshold. Read more in [Failed transaction rate threshold rule →](../../../solutions/observability/incident-management/create-failed-transaction-rate-threshold-rule.md) |
| **Latency threshold** | Alert when the latency or failed transaction rate is abnormal.Threshold rules can be as broad or as granular as you’d like, enabling you to define exactly when you want to be alerted—​whether that’s at the environment level, service name level, transaction type level, and/or transaction name level. Read more in [Latency threshold rule →](../../../solutions/observability/incident-management/create-latency-threshold-rule.md) |

