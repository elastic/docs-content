---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-algorithms.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Anomaly detection algorithms [ml-ad-algorithms]

The {{anomaly-detect}} {{ml-features}} use a bespoke amalgamation of different techniques such as clustering, various types of time series decomposition, Bayesian distribution modeling, and correlation analysis. These analytics provide sophisticated real-time automated {{anomaly-detect}} for time series data.

The {{ml}} analytics statistically model the time-based characteristics of your data by observing historical behavior and adapting to new data. The model represents a baseline of normal behavior and can therefore be used to determine how anomalous new events are.

{{anomaly-detect-cap}} results are written for each [bucket span](ml-ad-run-jobs.md#ml-ad-bucket-span). These results include scores that are aggregated in order to reduce noise and normalized in order to rank the most mathematically significant anomalies.
