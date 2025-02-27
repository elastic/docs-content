---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-sum-functions.html
---

# Sum functions [ml-sum-functions]

The sum functions detect anomalies when the sum of a field in a bucket is anomalous.

If you want to monitor unusually high totals, use high-sided functions.

If want to look at drops in totals, use low-sided functions.

If your data is sparse, use `non_null_sum` functions. Buckets without values are ignored; buckets with a zero value are analyzed.

The {{ml-features}} include the following sum functions:

* [`sum`, `high_sum`, `low_sum`](ml-sum-functions.md#ml-sum)
* [`non_null_sum`, `high_non_null_sum`, `low_non_null_sum`](ml-sum-functions.md#ml-nonnull-sum)


## Sum, high_sum, low_sum [ml-sum]

The `sum` function detects anomalies where the sum of a field in a bucket is anomalous.

If you want to monitor unusually high sum values, use the `high_sum` function.

If you want to monitor unusually low sum values, use the `low_sum` function.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `over_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

```js
{
  "function" : "sum",
  "field_name" : "expenses",
  "by_field_name" : "costcenter",
  "over_field_name" : "employee"
}
```

If you use this `sum` function in a detector in your {{anomaly-job}}, it models total expenses per employees for each cost center. For each time bucket, it detects when an employee’s expenses are unusual for a cost center compared to other employees.

```js
{
  "function" : "high_sum",
  "field_name" : "cs_bytes",
  "over_field_name" : "cs_host"
}
```

If you use this `high_sum` function in a detector in your {{anomaly-job}}, it models total `cs_bytes`. It detects `cs_hosts` that transfer unusually high volumes compared to other `cs_hosts`. This example looks for volumes of data transferred from a client to a server on the internet that are unusual compared to other clients. This scenario could be useful to detect data exfiltration or to find users that are abusing internet privileges.


## Non_null_sum, high_non_null_sum, low_non_null_sum [ml-nonnull-sum]

The `non_null_sum` function is useful if your data is sparse. Buckets without values are ignored and buckets with a zero value are analyzed.

If you want to monitor unusually high totals, use the `high_non_null_sum` function.

If you want to look at drops in totals, use the `low_non_null_sum` function.

These functions support the following properties:

* `field_name` (required)
* `by_field_name` (optional)
* `partition_field_name` (optional)

For more information about those properties, see the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

::::{note}
Population analysis (that is to say, use of the `over_field_name` property) is not applicable for this function.
::::


```js
{
  "function" : "high_non_null_sum",
  "field_name" : "amount_approved",
  "by_field_name" : "employee"
}
```

If you use this `high_non_null_sum` function in a detector in your {{anomaly-job}}, it models the total `amount_approved` for each employee. It ignores any buckets where the amount is null. It detects employees who approve unusually high amounts compared to their past behavior.

