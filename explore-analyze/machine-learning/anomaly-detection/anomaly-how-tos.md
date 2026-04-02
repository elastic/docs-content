---
navigation_title: How-tos
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/anomaly-how-tos.html
  - https://www.elastic.co/guide/en/serverless/current/observability-aiops-tune-anomaly-detection-job.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
  - id: cloud-serverless
---

# How-tos [anomaly-how-tos]

Though it is quite simple to analyze your data and provide quick {{ml}} results, gaining deep insights might require some additional planning and configuration. The guides in this section describe some best practices for generating useful {{ml}} results and insights from your data.

* [Generating alerts for {{anomaly-jobs}}](ml-configuring-alerts.md)
* [Aggregating data for faster performance](ml-configuring-aggregation.md)
* [Using runtime fields in {{dfeeds}}](ml-configuring-transform.md)
* [Customizing detectors with custom rules](ml-configuring-detector-custom-rules.md)
* [Detecting anomalous categories of data](ml-configuring-categories.md)
* [Performing population analysis](ml-configuring-populations.md)
* [Reverting to a model snapshot](ml-reverting-model-snapshot.md)
* [Detecting anomalous locations in geographic data](geographic-anomalies.md)
* [Mapping anomalies by location](mapping-anomalies.md)
* [Adding custom URLs to machine learning results](ml-configuring-url.md)
* [{{anomaly-jobs-cap}} from visualizations](ml-jobs-from-lens.md)
* [Exporting and importing {{ml}} jobs](../setting-up-machine-learning.md#move-jobs)

## {{anomaly-detect-cap}} examples in blog posts [anomaly-examples-blog-posts]

The blog posts listed below show how to get the most out of Elastic {{ml}} {{anomaly-detect}}.

* [Sizing for {{ml}} with {{es}}](https://www.elastic.co/blog/sizing-machine-learning-with-elasticsearch)
* [Filtering input data to refine {{ml-jobs}}](https://www.elastic.co/blog/filtering-input-data-to-refine-machine-learning-jobs)
* [Temporal vs. population analysis in Elastic {{ml}}](https://www.elastic.co/blog/temporal-vs-population-analysis-in-elastic-machine-learning)
* [Using {{es}} and {{ml}} for IT Operations](https://www.elastic.co/blog/using-elasticsearch-and-machine-learning-for-it-operations)
* [Using {{ml}} and {{es}} for security analytics](https://www.elastic.co/blog/using-machine-learning-and-elasticsearch-for-security-analytics-deep-dive)
* [User annotations for Elastic {{ml}}](https://www.elastic.co/blog/augmenting-results-with-user-annotations-for-elastic-machine-learning)
* [Custom {{es}} aggregations for {{ml-jobs}}](https://www.elastic.co/blog/custom-elasticsearch-aggregations-for-machine-learning-jobs)
* [Analysing Linux auditd anomalies with Auditbeat and {{ml}}](https://www.elastic.co/blog/analysing-linux-auditd-anomalies-with-auditbeat-and-elastic-stack-machine-learning)
* [How to optimize {{es}} {{ml}} job configurations using job validation](https://www.elastic.co/blog/how-to-optimize-elasticsearch-machine-learning-job-configurations-using-job-validation)
* [Interpretability in {{ml}}: Identifying anomalies, influencers, and root causes](https://www.elastic.co/blog/interpretability-in-ml-identifying-anomalies-influencers-root-causes)

There are also some examples in the {{ml}} folder in the [examples repository](https://github.com/elastic/examples).
