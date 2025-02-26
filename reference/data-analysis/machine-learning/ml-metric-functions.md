---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-metric-functions.html
---

# Metric functions [ml-metric-functions]

The metric functions include functions such as mean, min and max. These values are calculated for each bucket. Field values that cannot be converted to double precision floating point numbers are ignored.

The {{ml-features}} include the following metric functions:

* [`min`](ml-metric-functions.md#ml-metric-min)
* [`max`](ml-metric-functions.md#ml-metric-max)
* [`median`, `high_median`, `low_median`](ml-metric-functions.md#ml-metric-median)
* [`mean`, `high_mean`, `low_mean`](ml-metric-functions.md#ml-metric-mean)
* [`metric`](ml-metric-functions.md#ml-metric-metric)
* [`varp`, `high_varp`, `low_varp`](ml-metric-functions.md#ml-metric-varp)

::::{note}
You cannot add rules with conditions to detectors that use the `metric` function.
::::



## Min [ml-metric-min]

The `min` function detects anomalies in the arithmetic minimum of a value. The minimum value is calculated for each bucket.

High- and low-sided functions are not applicable.

This function supports the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "min",
  "field_name" : "amt",
  "by_field_name" : "product"
}
```

If you use this `min` function in a detector in your {{anomaly-job}}, it detects where the smallest transaction is lower than previously observed. You can use this function to detect items for sale at unintentionally low prices due to data entry mistakes. It models the minimum amount for each product over time.


## Max [ml-metric-max]

The `max` function detects anomalies in the arithmetic maximum of a value. The maximum value is calculated for each bucket.

High- and low-sided functions are not applicable.

This function supports the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "max",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `max` function in a detector in your {{anomaly-job}}, it detects where the longest `responsetime` is longer than previously observed. You can use this function to detect applications that have `responsetime` values that are unusually lengthy. It models the maximum `responsetime` for each application over time and detects when the longest `responsetime` is unusually long compared to previous applications.

```js
{
  "function" : "max",
  "field_name" : "responsetime",
  "by_field_name" : "application"
},
{
  "function" : "high_mean",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

The analysis in the previous example can be performed alongside `high_mean` functions by application. By combining detectors and using the same influencer this job can detect both unusually long individual response times and average response times for each bucket.


## Median, high_median, low_median [ml-metric-median]

The `median` function detects anomalies in the statistical median of a value. The median value is calculated for each bucket.

If you want to monitor unusually high median values, use the `high_median` function.

If you are just interested in unusually low median values, use the `low_median` function.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "median",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `median` function in a detector in your {{anomaly-job}}, it models the median `responsetime` for each application over time. It detects when the median `responsetime` is unusual compared to previous `responsetime` values.


## Mean, high_mean, low_mean [ml-metric-mean]

The `mean` function detects anomalies in the arithmetic mean of a value. The mean value is calculated for each bucket.

If you want to monitor unusually high average values, use the `high_mean` function.

If you are just interested in unusually low average values, use the `low_mean` function.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "mean",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `mean` function in a detector in your {{anomaly-job}}, it models the mean `responsetime` for each application over time. It detects when the mean `responsetime` is unusual compared to previous `responsetime` values.

```js
{
  "function" : "high_mean",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `high_mean` function in a detector in your {{anomaly-job}}, it models the mean `responsetime` for each application over time. It detects when the mean `responsetime` is unusually high compared to previous `responsetime` values.

```js
{
  "function" : "low_mean",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `low_mean` function in a detector in your {{anomaly-job}}, it models the mean `responsetime` for each application over time. It detects when the mean `responsetime` is unusually low compared to previous `responsetime` values.


## Metric [ml-metric-metric]

The `metric` function combines `min`, `max`, and `mean` functions. You can use it as a shorthand for a combined analysis. If you do not specify a function in a detector, this is the default function.

High- and low-sided functions are not applicable. You cannot use this function when a `summary_count_field_name` is specified.

This function supports the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "metric",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `metric` function in a detector in your {{anomaly-job}}, it models the mean, min, and max `responsetime` for each application over time. It detects when the mean, min, or max `responsetime` is unusual compared to previous `responsetime` values.


## Varp, high_varp, low_varp [ml-metric-varp]

The `varp` function detects anomalies in the variance of a value which is a measure of the variability and spread in the data.

If you want to monitor unusually high variance, use the `high_varp` function.

If you are just interested in unusually low variance, use the `low_varp` function.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "varp",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `varp` function in a detector in your {{anomaly-job}}, it models the variance in values of `responsetime` for each application over time. It detects when the variance in `responsetime` is unusual compared to past application behavior.

```js
{
  "function" : "high_varp",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `high_varp` function in a detector in your {{anomaly-job}}, it models the variance in values of `responsetime` for each application over time. It detects when the variance in `responsetime` is unusual compared to past application behavior.

```js
{
  "function" : "low_varp",
  "field_name" : "responsetime",
  "by_field_name" : "application"
}
```

If you use this `low_varp` function in a detector in your {{anomaly-job}}, it models the variance in values of `responsetime` for each application over time. It detects when the variance in `responsetime` is unusual compared to past application behavior.

