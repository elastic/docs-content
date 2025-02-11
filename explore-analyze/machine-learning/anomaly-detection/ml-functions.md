---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-functions.html
---

# Function reference [ml-functions]

The {{ml-features}} include analysis functions that provide a wide variety of flexible ways to analyze data for anomalies.

When you create {{anomaly-jobs}}, you specify one or more detectors, which define the type of analysis that needs to be done. If you are creating your job by using {{ml}} APIs, you specify the functions in detector configuration objects. If you are creating your job in {{kib}}, you specify the functions differently depending on whether you are creating single metric, multi-metric, or advanced jobs.

Most functions detect anomalies in both low and high values. In statistical terminology, they apply a two-sided test. Some functions offer low and high variations (for example, `count`, `low_count`, and `high_count`). These variations apply one-sided tests, detecting anomalies only when the values are low or high, depending one which alternative is used.

You can specify a `summary_count_field_name` with any function except `metric`. When you use `summary_count_field_name`, the {{ml}} features expect the input data to be pre-aggregated. The value of the `summary_count_field_name` field must contain the count of raw events that were summarized. In {{kib}}, use the **summary_count_field_name** in advanced {{anomaly-jobs}}. Analyzing aggregated input data provides a significant boost in performance. For more information, see [Aggregating data for faster performance](ml-configuring-aggregation.md).

If your data is sparse, there may be gaps in the data which means you might have empty buckets. You might want to treat these as anomalies or you might want these gaps to be ignored. Your decision depends on your use case and what is important to you. It also depends on which functions you use. The `sum` and `count` functions are strongly affected by empty buckets. For this reason, there are `non_null_sum` and `non_zero_count` functions, which are tolerant to sparse data. These functions effectively ignore empty buckets.

* [Count functions](https://www.elastic.co/guide/en/machine-learning/current/ml-count-functions.html)
* [Geographic functions](https://www.elastic.co/guide/en/machine-learning/current/ml-geo-functions.html)
* [Information content functions](https://www.elastic.co/guide/en/machine-learning/current/ml-info-functions.html)
* [Metric functions](https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html)
* [Rare functions](https://www.elastic.co/guide/en/machine-learning/current/ml-rare-functions.html)
* [Sum functions](https://www.elastic.co/guide/en/machine-learning/current/ml-sum-functions.html)
* [Time functions](https://www.elastic.co/guide/en/machine-learning/current/ml-time-functions.html)
