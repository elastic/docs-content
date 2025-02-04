---
navigation_title: "Supplied configurations"
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs.html
---

# Supplied configurations [ootb-ml-jobs]

{{anomaly-jobs-cap}} contain the configuration information and metadata necessary to perform an analytics task. {{kib}} can recognize certain types of data and provide specialized wizards for that context. This page lists the categories of the {{anomaly-jobs}} that are ready to use via {{kib}} in **Machine learning**. Refer to [Create {{anomaly-jobs}}](https://www.elastic.co/guide/en/machine-learning/current/create-jobs.html) to learn more about creating a job by using supplied configurations. Logs and Metrics supplied configurations are available and can be created via the related solution UI in {{kib}}.

* [Apache](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-apache.html)
* [APM](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-apm.html)
* [{{auditbeat}}](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-auditbeat.html)
* [Logs](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-logs-ui.html)
* [{{metricbeat}}](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-metricbeat.html)
* [Metrics](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-metrics-ui.html)
* [Nginx](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-nginx.html)
* [Security](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-siem.html)
* [Uptime](https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-uptime.html)

::::{note}
The configurations are only available if data exists that matches the queries specified in the manifest files. These recognizer queries are linked in the descriptions of the individual configurations.
::::

## Model memory considerations [ootb-ml-model-memory]

By default, these jobs have `model_memory_limit` values that are deemed appropriate for typical user environments and data characteristics. If your environment or your data is atypical and your jobs reach a memory status value of `soft_limit` or `hard_limit`, you might need to update the model memory limits. For more information, see [Working with {{anomaly-detect}} at scale](anomaly-detection-scale.md#set-model-memory-limit).
