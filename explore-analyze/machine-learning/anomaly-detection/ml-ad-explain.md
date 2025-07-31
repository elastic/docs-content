---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-explain.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Anomaly score explanation [ml-ad-explain]

Every anomaly has an anomaly score assigned to it. That score indicates how anomalous the data point is, which makes it possible to define its severity compared to other anomalies. This page gives you a high-level explanation of the critical factors considered for calculating anomaly scores, how the scores are calculated, and how renormalization works.

## Anomaly score impact factors [score-impact-factors]

{{anomaly-jobs-cap}} split the time series data into time buckets. The data within a bucket is aggregated using functions. Anomaly detection is happening on the bucket values. Three factors can affect the initial anomaly score of a record:

* single bucket impact,
* multi-bucket impact,
* anomaly characteristics impact.

### Single bucket impact [single-bucket-impact]

The probability of the actual value in the bucket is calculated first. This probability depends on how many similar values were seen in the past. It often relates to the difference between actual and typical values. The typical value is the median value of the probability distribution for the bucket. This probability leads to the single bucket impact. It usually dominates the initial anomaly score of a short spike or dip.

### Multi-bucket impact [multi-bucket-impact]

The probabilities of the values in the current bucket and the preceding 11 buckets contribute to the multi-bucket impact. The accumulated differences between the actual and typical values result in the multi-bucket impact on the initial anomaly score of the current bucket. High multi-bucket impact indicates unusual behavior in the interval preceding the current bucket, even if the value of this bucket may be within the 95% confidence interval.

Different signs mark the anomalies with high multi-bucket impact to highlight the distinction. A cross sign "+" represents these anomalies in {{kib}}, instead of a circle.

### Anomaly characteristics impact [anomaly-characteristics-impact]

The impact of the anomaly characteristics considers the different features of the anomaly, such as its length and size. The total duration of the anomaly is considered, and not a fixed interval as in the case of the multi-bucket impact calculation. The length might be only one bucket or thirty (or more) buckets. Comparing the length and size of the anomaly to the historical averages makes it possible to adapt to your domain and the patterns in data. The default behavior of the algorithm is to score longer anomalies higher than short-lived spikes. In practice, short anomalies often turn out to be errors in data, while long anomalies are something you might need to react to.

Combining multi-bucket impact and anomaly characteristics impact leads to more reliable detection of abnormal behavior over various domains.

## Record score reduction (renormalization) [record-score-reduction]

Anomaly scores are in the range of 0 and 100. The values close to 100 signify the biggest anomalies the job has seen to date. For this reason, when an anomaly bigger than any other before is detected, the scores of previous anomalies need to be reduced.

The process when the anomaly detection algorithm adjusts the anomaly scores of past records when new data comes in is called *renormalization*. The `renormalization_window_days` configuration parameter specifies the time interval for this adjustment. The **Single Metric Viewer** in Kibana highlights the renormalization change.

:::{image} /explore-analyze/images/machine-learning-renormalization-score-reduction.jpg
:alt: Example of a record score reduction in {{kib}}
:screenshot:
:::

## Other factors for score reduction [other-factors]

Two more factors may lead to a reduction of the initial score: a high variance interval and an incomplete bucket.

{{anomaly-detect-cap}} is less reliable if the current bucket is part of a seasonal pattern with high variability in its data. For example, you may have server maintenance jobs running every night at midnight. These jobs can lead to high variability in the latency of request processing. The job is also more reliable if the current bucket has received a similar number of observations as historically expected.

Real-world anomalies often show the impacts of several factors. The **Anomaly explanation** section in the Single Metric Viewer can help you interpret an anomaly in its context.

:::{image} /explore-analyze/images/machine-learning-detailed-single-metric.png
:alt: Detailed view of the Single Metric Viewer in {{kib}}
:screenshot:
:::

You can also find this information in the `anomaly_score_explanation` field of the [get record API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-get-records).
