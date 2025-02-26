---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-delayed-data-detection.html
---

# Handling delayed data [ml-delayed-data-detection]

Delayed data are documents that are indexed late. That is to say, it is data related to a time that your {{dfeed}} has already processed and it is therefore never analyzed by your {{anomaly-job}}.

When you create a {{dfeed}}, you can specify a [`query_delay`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-datafeed) setting. This setting enables the {{dfeed}} to wait for some time past real-time, which means any "late" data in this period is fully indexed before the {{dfeed}} tries to gather it. However, if the setting is set too low, the {{dfeed}} may query for data before it has been indexed and consequently miss that document. Conversely, if it is set too high, analysis drifts farther away from real-time. The balance that is struck depends upon each use case and the environmental factors of the cluster.

::::{important}
If you get an error that says `Datafeed missed XXXX documents due to ingest latency`, consider increasing the value of query_delay. If it doesn’t help, investigate the ingest latency and its cause. You can do this by comparing event and ingest timestamps. High latency is often caused by bursts of ingested documents, misconfiguration of the ingest pipeline, or misalignment of system clocks.
::::
