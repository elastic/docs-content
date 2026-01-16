---
navigation_title: Troubleshooting and FAQ
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-ad-troubleshooting.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Troubleshooting and FAQ [ml-ad-troubleshooting]

Use the information in this section to troubleshoot common problems and find answers for frequently asked questions.

## How to restart failed {{anomaly-jobs}} [ml-ad-restart-failed-jobs]

If an {{anomaly-job}} fails, try to restart the job by following the procedure described below. If the restarted job runs as expected, then the problem that caused the job to fail was transient and no further investigation is needed. If the job quickly fails after the restart, then the problem is persistent and needs further investigation. In this case, find out which node the failed job was running on by checking the job stats on the **Job management** pane in {{kib}}. Then get the logs for that node and look for exceptions and errors where the ID of the {{anomaly-job}} is in the message to have a better understanding of the issue.

If an {{anomaly-job}} has failed, do the following to recover from `failed` state:

1. *Force* stop the corresponding {{dfeed}} by using the [Stop {{dfeed}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-stop-datafeed) with the `force` parameter being `true`. For example, the following request force stops the `my_datafeed` {{dfeed}}.
   ```console
   POST _ml/datafeeds/my_datafeed/_stop
    {
      "force": "true"
    }
   ```

2. *Force* close the {{anomaly-job}} by using the [Close {{anomaly-job}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-close-job) with the `force` parameter being `true`. For example, the following request force closes the `my_job` {{anomaly-job}}:
   ```console
   POST _ml/anomaly_detectors/my_job/_close?force=true
   ```

3. Restart the {{anomaly-job}} on the **Job management** pane in {{kib}}.

## What {{ml}} methods are used for {{anomaly-detect}}? [faq-methods]

For detailed information, refer to the paper [Anomaly Detection in Application Performance Monitoring Data](https://www.ijmlc.org/papers/398-LC018.pdf) by Thomas Veasey and Stephen Dodson, as well as our webinars on [The Math behind Elastic Machine Learning](https://www.elastic.co/elasticon/conf/2018/sf/the-math-behind-elastic-machine-learning) and [Machine Learning and Statistical Methods for Time Series Analysis](https://www.elastic.co/elasticon/conf/2017/sf/machine-learning-and-statistical-methods-for-time-series-analysis).

Further papers cited in the C++ code:

* [Modern hierarchical, agglomerative clustering algorithms](http://arxiv.org/pdf/1109.2378.pdf)
* [An Efficient k-Means Clustering Algorithm: Analysis and Implementation](https://www.cs.umd.edu/~mount/Projects/KMeans/pami02.pdf)
* [Large-Scale Bayesian Logistic Regression for Text Categorization](http://www.stat.columbia.edu/~madigan/PAPERS/techno.pdf)
* [X-means: Extending K-means with Efficient Estimation of the Number of Clusters](https://www.cs.cmu.edu/~dpelleg/download/xmeans.pdf)

## What are the input features used by the model? [faq-features]

All input features are specified by the user, for example, using [diverse statistical functions](/explore-analyze/machine-learning/anomaly-detection/ml-functions.md) like count or mean over the data of interest.

## Does the data used by the model only include customers' data? [faq-data]

Yes. Only the data specified in the {{anomaly-job}} configuration are used for detection.

## What does the model output score represent? How is it generated and calibrated? [faq-output-score]

The ensemble model generates a probability value, which is then mapped to an anomaly severity score between 0 and 100. The lower the probability of observed data, the higher the severity score. Refer to this [advanced concept doc](ml-ad-explain.md) for details. Calibration (also called as normalization) happens on two levels:

1. Within the same metric/partition, the scores are re-normalized “back in time” within the window specified by the `renormalization_window_days` parameter. This is the reason, for example, that both `record_score` and `initial_record_score` exist.
2. Over multiple partitions, scores are renormalized as described in [this blog post](https://www.elastic.co/blog/changes-to-elastic-machine-learning-anomaly-scoring-in-6-5).

## Is the model static or updated periodically? [faq-model-update]

It’s an online model and updated continuously. Old parts of the model are pruned out based on the parameter `model_prune_window` (usually 30 days).

## Is the performance of the model monitored? [faq-model-performance]

There is a set of benchmarks to monitor the performance of the {{anomaly-detect}} algorithms and to ensure no regression occurs as the methods are continuously developed and refined. They are called "data scenarios" and consist of 3 things:

* a dataset (stored as an {{es}} snapshot),
* a {{ml}} config ({{anomaly-detect}}, dfanalysis, transform, or {{infer}}),
* an arbitrary set of static assertions (bucket counts, anomaly scores, accuracy value, and so on).

Performance metrics are collected from each and every scenario run and they are persisted in an Elastic Cloud cluster. This information is then used to track the performance over time, across the different builds, mainly to detect any regressions in the performance (both result quality and compute time).

On the customer side, the situation is different. There is no conventional way to monitor the model performance as it’s unsupervised. Usually, operationalization of the model output include one or several of the following steps:

* Creating alerts for influencers, buckets, or records based on a certain anomaly score.
* Use the forecasting feature to predict the development of the metric of interest in the future.
* Use one or a combination of multiple {{anomaly-jobs}} to identify the significant anomaly influencers.

## How to measure the accuracy of the unsupervised {{ml}} model? [faq-model-accuracy]

For each record in a given time series, anomaly detection models provide an anomaly severity score, 95% confidence intervals, and an actual value. This data is stored in an index and can be retrieved using the Get Records API. With this information, you can use standard measures to assess prediction accuracy, interval calibration, and so on. Elasticsearch aggregations can be used to compute these statistics.

The purpose of {{anomaly-detect}} is to achieve the best ranking of periods where an anomaly happened. A practical way to evaluate this is to keep track of real incidents and see how well they correlate with the predictions of {{anomaly-detect}}.

## Can the {{anomaly-detect}} model experience model drift? [faq-model-drift]

Elasticsearch’s {{anomaly-detect}} model continuously learns and adapts to changes in the time series. These changes can take the form of slow drifts as well as sudden jumps. Therefore, we take great care to manage the adaptation to changing data characteristics. There is always a fine trade-off between fitting anomalous periods (over-fitting) and not learning new normal behavior. The following are the main approaches Elastic uses to manage this trade-off:

* Learning the optimal decay rate based on measuring the bias in the forecast and the moments of the error distribution and error distribution moments.
* Allowing continuous small drifts in periodic patterns. This is achieved by continuously minimizing the mean prediction error over the last iteration with respect to a small bounded time shift.
* If the predictions are significantly wrong over a long period of time, the algorithm tests whether the time series has undergone a sudden change. Hypothesis Testing is used to test for different types of changes, such as scaling of values, shifting of values, and large time shifts in periodic patterns such as daylight saving time.
* Running continuous hypothesis tests on time windows of various lengths to test for significant evidence of new or changed periodic patterns, and update the model if the null hypothesis of unchanged features is rejected.
* Accumulating error statistics on calendar days and continuously test whether predictive calendar features need to be added or removed from the model.

## What is the minimum amount of data for an {{anomaly-job}}? [faq-minimum-data]

Elastic {{ml}} needs a minimum amount of data to be able to build an effective model for {{anomaly-detect}}.

* For sampled metrics such as `mean`, `min`, `max`, and `median`, the minimum data amount is either eight non-empty bucket spans or two hours, whichever is greater.
* For all other non-zero/null metrics and count-based quantities, it’s four non-empty bucket spans or two hours, whichever is greater.
* For the `count` and `sum` functions, empty buckets matter and therefore it is the same as sampled metrics - eight buckets or two hours.
* For the `rare` function, it’s typically around 20 bucket spans. It can be faster for population models, but it depends on the number of people that interact per bucket.

Rules of thumb:

* more than three weeks for periodic data or a few hundred buckets for non-periodic data
* at least as much data as you want to forecast

## Are there any checks or processes to ensure data integrity? [faq-data-integrity]

The Elastic {{ml}} algorithms are programmed to work with missing and noisy data and use denoising and data reputation techniques based on the learned statistical properties.
