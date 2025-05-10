---
navigation_title: Finding anomalies
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-finding-anomalies.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Finding anomalies [ml-ad-finding-anomalies]

The {{ml}} {{anomaly-detect}} features automate the analysis of time series data by creating accurate baselines of normal behavior in your data. These baselines then enable you to identify anomalous events or patterns. Data is pulled from {{es}} for analysis and anomaly results are displayed in {{kib}} dashboards. For example, the **{{ml-app}}** app provides charts that illustrate the actual data values, the bounds for the expected values, and the anomalies that occur outside these bounds.

The typical workflow for performing {{anomaly-detect}} is as follows:

* [Plan your analysis](ml-ad-plan.md)
* [Run a job](ml-ad-run-jobs.md)
* [View the results](ml-ad-view-results.md)
* [Forecast future behavior](ml-ad-forecast.md)