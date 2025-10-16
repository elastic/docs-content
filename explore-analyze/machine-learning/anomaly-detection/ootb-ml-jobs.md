---
navigation_title: Supplied configurations
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Supplied configurations [ootb-ml-jobs]

{{anomaly-jobs-cap}} contain the configuration information and metadata necessary to perform an analytics task. {{kib}} can recognize certain types of data and provide specialized wizards for that context. This page lists the categories of the {{anomaly-jobs}} that are ready to use via {{kib}} in **Machine learning**. Refer to [Create {{anomaly-jobs}}](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-create-job) to learn more about creating a job by using supplied configurations. Logs and Metrics supplied configurations are available and can be created via the related solution UI in {{kib}}.

* [Apache](/reference/machine-learning/ootb-ml-jobs-apache.md)
* [APM](/reference/machine-learning/ootb-ml-jobs-apm.md)
* [{{auditbeat}}](/reference/machine-learning/ootb-ml-jobs-auditbeat.md)
* [Logs](/reference/machine-learning/ootb-ml-jobs-logs-ui.md)
* [{{metricbeat}}](/reference/machine-learning/ootb-ml-jobs-metricbeat.md)
* [Metrics](/reference/machine-learning/ootb-ml-jobs-metrics-ui.md)
* [Nginx](/reference/machine-learning/ootb-ml-jobs-nginx.md)
* [Security](/reference/machine-learning/ootb-ml-jobs-siem.md)
* [Uptime](/reference/machine-learning/ootb-ml-jobs-uptime.md)

::::{note}
The configurations are only available if data exists that matches the queries specified in the manifest files. These recognizer queries are linked in the descriptions of the individual configurations.
::::

## Model memory considerations [ootb-ml-model-memory]

By default, these jobs have `model_memory_limit` values that are deemed appropriate for typical user environments and data characteristics. If your environment or your data is atypical and your jobs reach a memory status value of `soft_limit` or `hard_limit`, you might need to update the model memory limits. For more information, see [Working with {{anomaly-detect}} at scale](anomaly-detection-scale.md#set-model-memory-limit).
